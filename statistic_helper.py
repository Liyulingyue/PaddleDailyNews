from github_helper import GithubHelper, CacheMode

class StatisticHelper(object):
    # 对githubhelper中的信息进行统计
    def __init__(self, date=(0,0,0)):
        super().__init__()
        self.year = date[0]
        self.month = date[1]
        self.day = date[2]
        self.pr_num = 0
        self.issue_num = 0

    def refresh_number(self, g_helper: GithubHelper):
        g_helper.get_ccashe()
        cache_pr = g_helper.get_ccashe("paddle")
        cache_issue = g_helper.get_ccashe("paddle", CacheMode.ISSUES)
        self.pr_num = len(cache_pr)
        self.issue_num = len(cache_issue)
