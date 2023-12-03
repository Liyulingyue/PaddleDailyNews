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
