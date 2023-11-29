from datetime import datetime

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


log_init()
g = GithubHelper(GITHUB_TOKEN)  # noqa: F405
print(g.get_user_name())
g.RefreshData([CacheMode.PR, CacheMode.ISSUES], datetime(2023, 11, 18), ["paddle"])
g.GetRepoList()

s_helper = StatisticHelper()
l_helper = LayoutHelper()
l_helper.generate_layout(s_helper)
l_helper.Export2MarkdownFile()
