from loguru import logger

from configure import LLM
from llm import ChatGLM3, Ernie, LLM_base


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


# modelscope 模型下载
def modelscope_download(model_name: str, version: str):
    from modelscope import snapshot_download

    logger.info(f"start download: {model_name} model")
    snapshot_download(model_id=model_name, cache_dir="model/", revision=version)
    logger.info(f"download {model_name} model success")


def llm_init() -> LLM_base:
    match LLM:
        case "ZhipuAI/chatglm3-6b":
            modelscope_download(LLM, "v1.0.2")
            return ChatGLM3(LLM)
        case "ZhipuAI/chatglm3-6b-32k":
            modelscope_download(LLM, "v1.0.1")
            return ChatGLM3(LLM)
        case "":
            raise RuntimeError("Please fill in LLM in the configuration file")
        case "ernie" | _:
            return Ernie("")
