from datetime import datetime, timedelta

from configure import *  # noqa: F403
from github_helper import CacheMode, GithubHelper
from layout_helper import LayoutHelper
from statistic_helper import StatisticHelper
from utils import llm_init, log_init

Year = 2023
Month = 12
Day = 15
ORGANIZATION = "PaddlePaddle"
REPO_NAME = "paddle"


log_init()
model = llm_init()
g_helper = GithubHelper(GITHUB_TOKEN, org=ORGANIZATION)  # noqa: F405
print(g_helper.get_user_name())
g_helper.RefreshData(
    [CacheMode.PR, CacheMode.ISSUES],
    start_time=datetime(Year, Month, Day),
    end_time=datetime(Year, Month, Day) + timedelta(days=1),
    repo_names=[REPO_NAME],
)

s_helper = StatisticHelper(model, date=(Year, Month, Day))
s_helper.refresh_number(g_helper)
s_helper.get_score_of_pr(g_helper)
s_helper.get_score_of_issue(g_helper)
s_helper.get_rank_of_contributors(g_helper)
s_helper.get_rank_of_issuers(g_helper)

l_helper = LayoutHelper(model=model, repo_name=REPO_NAME)
l_helper.generate_layout(s_helper)
l_helper.Export2MarkdownFile()
