from datetime import datetime
from configure import *
from loguru import logger

from github_helper import CacheMode, GithubHelper


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
g = GithubHelper(GITHUB_TOKEN)
print(g.get_user_name())
g.RefreshData([CacheMode.PR, CacheMode.ISSUES], datetime(2023, 11, 18), ["paddle"])
g.GetRepoList()
