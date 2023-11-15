from datetime import datetime
from configure import *
from loguru import logger

import github_helper


def log_init():
    # TODO(gouzil): 改个前缀
    logger.add(
        "./logs/PaddleDailyNews.log",
        rotation="10MB",
        encoding="utf-8",
        enqueue=True,
        retention="10d",
        level="DEBUG"
        )

log_init()
g = github_helper.GithubHelper("GITHUB_TOKEN")
print(g.get_user_name())
g.RefreshData("paddle",datetime(2023,11,1))
g.GetRepoList()

