from github_helper import GithubHelper, CacheMode
import requests
from llm_chat import *
import traceback

class StatisticHelper(object):
    # 对githubhelper中的信息进行统计
    def __init__(self, date=(0,0,0)):
        super().__init__()
        self.year = date[0]
        self.month = date[1]
        self.day = date[2]
        self.pr_num = 0
        self.issue_num = 0
        self.pr_list = []
        self.issue_list = []
        self.pr_rank_list = []
        self.issue_rank_list = []

    def refresh_number(self, g_helper: GithubHelper):
        g_helper.get_ccashe()
        cache_pr = g_helper.get_ccashe("paddle")
        cache_issue = g_helper.get_ccashe("paddle", CacheMode.ISSUES)
        self.pr_num = len(cache_pr)
        self.issue_num = len(cache_issue)

    def get_score_of_pr(self, g_helper: GithubHelper):
        g_helper.get_ccashe()
        cache_pr = g_helper.get_ccashe("paddle")
        self.pr_list = []
        for pr in cache_pr:
            print(f"make score in {pr.number}, total pr number is {len(cache_pr)}")
            title = pr.title
            id = pr.number
            user = pr.user
            diff_url = pr.diff_url
            try:
                r = requests.get(diff_url)
                score, comments, introduction = get_score_of_a_change(r.text)
            except:
                score = -1
                comments = ""
                introduction = ""
                print(traceback.format_exc())
            self.pr_list.append({"title": title, "id": id, "user": user, "score": score, "comments": comments, "introduction":introduction})

        self.pr_list.sort(key=lambda x: x['score'], reverse=True)

    def get_score_of_issue(self, g_helper: GithubHelper):
        g_helper.get_ccashe()
        cache_issue = g_helper.get_ccashe("paddle", CacheMode.ISSUES)
        self.issue_list = []
        for issue in cache_issue:
            print(f"make score in {issue.number}, total issue number is {len(cache_issue)}")
            title = issue.title
            id = issue.number
            user = issue.user
            content = issue.body
            try:
                score, comments, introduction = get_score_of_a_issue(content)
            except:
                score = -1
                comments = ""
                introduction = ""
                print(traceback.format_exc())
            self.issue_list.append({"title": title, "id": id, "user": user, "score": score, "comments": comments, "introduction":introduction})

        self.issue_list.sort(key=lambda x: x['score'], reverse=True)

    def get_rank_of_contributors(self, g_helper: GithubHelper):
        g_helper.get_ccashe()
        cache_pr = g_helper.get_ccashe("paddle")
        tmp_dict = {}
        self.pr_rank_list = []
        for pr in cache_pr:
            if pr.user.login in tmp_dict:
                tmp_dict[pr.user.login] += 1
            else:
                tmp_dict[pr.user.login] = 1
        for user in tmp_dict:
            self.pr_rank_list.append({"user": user, "times": tmp_dict[user]})

        self.pr_rank_list.sort(key=lambda x: x['times'], reverse=True)


    def get_rank_of_issuers(self, g_helper: GithubHelper):
        g_helper.get_ccashe()
        cache_issue = g_helper.get_ccashe("paddle", CacheMode.ISSUES)
        tmp_dict = {}
        self.issue_rank_list = []
        for issue in cache_issue:
            if issue.user.login in tmp_dict:
                tmp_dict[issue.user.login] += 1
            else:
                tmp_dict[issue.user.login] = 1
        for user in tmp_dict:
            self.issue_rank_list.append({"user": user, "times": tmp_dict[user]})

        self.issue_rank_list.sort(key=lambda x: x['times'], reverse=True)