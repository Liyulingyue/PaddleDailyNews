from datetime import datetime

from loguru import logger

import github_help


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
g = github_help.GithubHelper("****")
print(g.get_user_name())
g.RefreshData("paddle",datetime(2023,11,1))
g.GetRepoList()

