from datetime import datetime, timezone
from enum import Flag, auto
from typing import TYPE_CHECKING

from github import Auth, Github
from github.Issue import Issue
from github.PullRequest import PullRequest
from loguru import logger

if TYPE_CHECKING:
    from github.Organization import Organization
    from github.PaginatedList import PaginatedList
    from github.Repository import Repository


# TODO(gouzil): move time utils
def convert_time_zone(t: datetime) -> datetime:
    match t.tzinfo:
        case None:
            t = t.replace(tzinfo=timezone.utc)
        case _:
            ...
    return t


class CacheMode(Flag):
    PR = auto()
    ISSUES = auto()

    def lower_case_name(self):
        return self.name.lower()


class GithubCacheData:
    def __init__(
        self,
        key: CacheMode | None = None,
        data: list[PullRequest] | list[Issue] | None = None,
        update_time: datetime = datetime.now(),
    ):
        self.key: CacheMode | None = key
        self.data: list[PullRequest] | list[Issue] | None = data
        self.update_time: datetime | None = update_time

    def set(self, key: CacheMode, data: list[PullRequest] | list[Issue], update_time: datetime = datetime.now()):
        # pr | issues
        self.key = key
        # 请求列表
        self.data = data
        self.update_time = update_time

    def set_key(self, key: CacheMode):
        assert isinstance(self.key, CacheMode)
        self.key = key

    def get_key(self) -> str:
        assert isinstance(self.key, str)
        return self.key

    def set_data(self, data: list[PullRequest] | list[Issue]):
        assert isinstance(self.data, list)
        self.data = data

    def get_data(self) -> list[PullRequest] | list[Issue]:
        assert isinstance(self.data, list)
        return self.data

    def set_update_time(self, update_time: datetime = datetime.now()):
        assert isinstance(self.key, str)
        self.update_time = update_time

    def get_update_time(self) -> datetime:
        assert isinstance(self.update_time, datetime)
        return self.update_time


# 暂不支持多线程(没有读写锁)
class GithubHelper:
    def __init__(self, token: str, org: str = "paddlepaddle") -> None:
        self.g = Github(auth=Auth.Token(token), per_page=100)
        # 存储层级: 仓库 -> (pr|issues) -> list[PullRequest]
        self.data_ccashe: dict[str, list[GithubCacheData]] = {}
        # 请不要修改 org, 如果需要修改请重新创建一个 GithubHelper
        self.__org: Organization = self.g.get_organization(org)

    # for debug
    def get_user_name(self) -> str:
        """
        返回登录的用户 id
        """
        return self.g.get_user().login

    # for debug
    def get_org_name(self) -> str:
        """
        获取组织名称
        """
        return self.__org.login

    def GetRepoList(self, write_cache: bool = True) -> list[str]:
        """
        获取当前组织下所有的仓库
        """
        logger.info(f"start get org repos: {self.__org.login}")
        # 为什么不用all, 防止一些研发大哥把 private 的项目公开出来
        repos: PaginatedList[Repository] = self.__org.get_repos(type="public")
        res: list[str] = []
        for i in repos:
            res.append(i.name)
            if write_cache and i.name not in self.data_ccashe.keys():
                logger.debug(f"write cache {self.__org.login}: {i.name}")
                self.data_ccashe[i.name] = []

        logger.info(f"end get org repos: {self.__org.login}")
        return res

    def get_ccashe(self) -> dict[str, list[GithubCacheData]]:
        """
        获取已缓存的数据
        """
        return self.data_ccashe

    def set_cache(self, key: str, data: GithubCacheData):
        """
        所有的缓存都应该调用这个方法
        """
        # TODO(gouzil): 加个锁
        if key in self.data_ccashe.keys():
            for cache_data in self.data_ccashe[key]:
                if data.key == cache_data.key:
                    self.data_ccashe[key].remove(cache_data)
                    break
        else:
            self.data_ccashe[key] = []
        self.data_ccashe[key].append(data)

    def RefreshData(
        self,
        modes: list[CacheMode],
        start_time: datetime,
        repo_names: list[str] | None = None,
        end_time: datetime = datetime.now(),
        base: str = "develop",
    ):
        if repo_names is None:
            repo_names_list: list[str] = self.GetRepoList()
        else:
            repo_names_list = repo_names

        for mode in modes:
            match mode:
                case CacheMode.PR:
                    for repo_name in repo_names_list:
                        self.set_cache(
                            repo_name,
                            GithubCacheData(
                                key=CacheMode.PR,
                                data=self.RefreshPrData(
                                    repo_name=repo_name,
                                    start_time=start_time,
                                    end_time=end_time,
                                    base=base,
                                ),
                            ),
                        )
                case CacheMode.ISSUES:
                    for repo_name in repo_names_list:
                        self.set_cache(
                            repo_name,
                            GithubCacheData(
                                CacheMode.PR,
                                self.RefreshIssuesData(
                                    repo_name=repo_name,
                                    start_time=start_time,
                                    end_time=end_time,
                                ),
                            ),
                        )

    def RefreshPrData(
        self,
        repo_name: str,
        start_time: datetime,
        end_time: datetime = datetime.now(),
        base: str = "develop",
    ) -> list[PullRequest]:
        """
        获取仓库下指定时间段内的pr

        repo_name: 仓库名称
        start_time: 最早的创建时间
        end_time: 最晚的创建时间
        base: 合入的分支
        """

        logger.info(f"requast pr list: {self.__org.login}/{repo_name} branch: {base} start")
        # 转换时区
        start_time = convert_time_zone(start_time)
        end_time = convert_time_zone(end_time)
        logger.info(f"request pr list start time: {start_time}, end time: {end_time}")

        repo: Repository = self.g.get_repo(f"{self.__org.login}/{repo_name}")
        res_list: list[PullRequest] = []
        pulls: PaginatedList[PullRequest] = repo.get_pulls(state="all", base=base)
        for i in pulls:
            logger.debug(f"request pr number: {i.number}, pr create time: {i.created_at}, pr status: {i.state}")
            if not i.created_at < end_time or not i.created_at > start_time:
                logger.debug(f"end request pr number: {i.number}")
                break
            # 不在这里做细分筛选，只进行数据收集
            res_list.append(i)

        logger.info(f"requast pr list {self.__org.login}/{repo_name} branch: {base} end")
        logger.debug(f"requast pr list len: {len(res_list)}")
        return res_list

    def RefreshIssuesData(
        self, repo_name: str, start_time: datetime, end_time: datetime = datetime.now()
    ) -> list[Issue]:
        """
        获取仓库下指定时间段内的 issues

        repo_name: 仓库名称
        start_time: 最早的创建时间
        end_time: 最晚的创建时间
        """
        logger.info(f"requast issues list: {self.__org.login}/{repo_name} start")
        # 转换时区
        start_time = convert_time_zone(start_time)
        end_time = convert_time_zone(end_time)
        logger.info(f"request issues list start time: {start_time}, end time: {end_time}")

        repo: Repository = self.g.get_repo(f"{self.__org.login}/{repo_name}")
        res_list: list[Issue] = []
        issues: PaginatedList[Issue] = repo.get_issues(state="all")
        for i in issues:
            logger.debug(f"request issue number: {i.number}, create time: {i.created_at}, status: {i.state}")
            if not i.created_at < end_time or not i.created_at > start_time:
                logger.debug(f"end request issue number: {i.number}")
                break
            # 不在这里做细分筛选，只进行数据收集
            res_list.append(i)

        logger.info(f"requast issues list {self.__org.login}/{repo_name} end")
        logger.debug(f"requast issues list len: {len(res_list)}")
        return res_list
