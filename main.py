from datetime import datetime, timedelta

from loguru import logger

from configure import *  # noqa: F403
from github_helper import CacheMode, GithubHelper
from layout_helper import LayoutHelper
from statistic_helper import StatisticHelper


def log_init():
    # TODO(gouzil): 改个前缀
    logger.add(
        "./logs/PaddleDailyNews.log",
        rotation="10MB",
        encoding="utf-8",
        enqueue=True,
        retention="10d",
        level="DEBUG",
    )

Year = 2023
Month = 11
Day = 28

log_init()
g_helper = GithubHelper(GITHUB_TOKEN)  # noqa: F405
print(g_helper.get_user_name())
g_helper.RefreshData([CacheMode.PR, CacheMode.ISSUES],
                     start_time=datetime(Year, Month, Day),
                     end_time=datetime(Year, Month, Day)+timedelta(days=1),
                     repo_names = ["paddle"])
g_helper.GetRepoList()
g_helper.get_ccashe()
cache_pr = g_helper.get_ccashe("paddle")
cache_issue = g_helper.get_ccashe("paddle", CacheMode.ISSUES)

s_helper = StatisticHelper(date=(Year,Month,Day))
s_helper.refresh_number(g_helper)
s_helper.get_score_of_pr(g_helper)

l_helper = LayoutHelper()
l_helper.generate_layout(s_helper)
l_helper.Export2MarkdownFile()
