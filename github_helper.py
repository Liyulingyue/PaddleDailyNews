from datetime import datetime, timezone
from typing import TYPE_CHECKING

from github import Auth, Github
from github.PullRequest import PullRequest
from loguru import logger

if TYPE_CHECKING:
    from github.Organization import Organization
    from github.PaginatedList import PaginatedList
    from github.Repository import Repository


# 暂不支持多线程(没有读写锁)
class GithubHelper(object):
    def __init__(self, token: str, org: str = "paddlepaddle") -> None:
        self.g = Github(auth=Auth.Token(token), per_page=100)
        self.data_ccashe: dict[str, list[PullRequest] | None] = {}
        # 请不要修改 org, 如果需要修改请重新创建一个 GithubHelper
        self.__org:Organization = self.g.get_organization(org)

    # for debug
    def get_user_name(self) -> str:
        """
        返回登录的用户 id
        """
        return self.g.get_user().login

    # for debug
    def get_org_name(self) -> str:
        return self.__org.login

    def get_ccashe(self) -> dict[str, list[PullRequest] | None]:
        """
        获取已缓存的数据
        """
        return self.data_ccashe

    def RefreshData(
            self,
            repo_name: str,
            start_time: datetime,
            end_time: datetime=datetime.now(),
            base:str="develop",
            write_cache:bool = True
            ) -> list[PullRequest]:
        """
        repo_name: 仓库名称
        start_time: 最早的创建时间
        end_time: 最晚的创建时间
        base: 合入的分支
        """
        # TODO(gouzil): move time utils
        def convert_time_zone(t: datetime) -> datetime:
            match t.tzinfo:
                case None:
                    t = t.replace(tzinfo=timezone.utc)
                case _:
                    ...
            return t
        logger.info(f"requast repo: {self.__org.login}/{repo_name} branch: {base} start")
        # 转换时区
        start_time = convert_time_zone(start_time)
        end_time = convert_time_zone(end_time)
        logger.info(f"request start time: {start_time}, end time: {end_time}")

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

        # 写入缓存
        if write_cache:
            self.data_ccashe[repo_name] = res_list

        logger.info(f"request repo: {self.__org.login}/{repo_name} branch: {base} end")
        logger.debug(f"request len: {len(res_list)}")
        return res_list

    def GetRepoList(self, write_cache:bool = True) -> list[str]:
        """
        获取当前组织下所有的仓库
        """
        logger.info(f"start get org repos: {self.__org.login}")
        # NOTE: 为什么不用all, 防止一些研发大哥把 private 的项目公开出来
        repos: PaginatedList[Repository] = self.__org.get_repos(type="public")
        res: list[str] = []
        for i in repos:
            res.append(i.name)
            if write_cache and i.name not in self.data_ccashe.keys():
                logger.debug(f"write cache {self.__org.login}: {i.name}")
                self.data_ccashe[i.name] = None

        logger.info(f"end get org repos: {self.__org.login}")
        return res

    def PreprocessInformation(self):
        pass
