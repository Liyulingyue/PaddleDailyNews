import gc
import json
import time
from typing import Any

import torch
from loguru import logger
from transformers import AutoModel, AutoTokenizer

from ..base import LLM_base


class ChatGLM3(LLM_base):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.tokenizer = None
        self.load_model()
        # 字符串上限
        self.set_gap_length()

    def set_gap_length(self) -> None:
        """
        设置字符串上限
        """
        match self.model_name:
            case "ZhipuAI/chatglm3-6b":
                self.gap_length = 8192
            case "ZhipuAI/chatglm3-6b-32k":
                self.gap_length = 32768
            case _:
                pass

    def load_model(self) -> None:
        """
        加载模型
        """
        logger.info("load model.......")
        model_path = f"model/{self.model_name}"
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True, device_map="auto").eval()
        logger.info(f"load model {self.get_device()} success")

    def get_llm_answer(self, prompt: str) -> str:
        """
        生成结果
        """
        logger.info("get_llm_answer start")
        logger.debug(f"get_llm_answer len: {len(prompt)}")
        start_time = time.time()
        response, _ = self.model.chat(
            self.tokenizer,
            prompt,
            history=[],
        )
        assert isinstance(response, str)

        # self.clean_mem()

        logger.info(f"get_llm_answer end, Generation time: {time.time()-start_time}")
        return response

    def extract_json_from_llm_answer(self, result: str) -> dict[str, Any]:
        """
        提取json格式
        """
        s_id = result.find("{")
        e_id = result.rfind("}")
        json_str = result[s_id : e_id + 1]
        json_dict = json.loads(json_str)
        return json_dict

    def get_device(self) -> str:
        """
        获取设备
        """
        if torch.backends.mps.is_built():
            return "mps"
        elif torch.backends.cuda.is_built():
            return "cuda"

        return "cpu"

    def clean_mem(self):
        """
        清理内存
        """
        gc.collect()
        match self.get_device():
            case "mps":
                torch.mps.empty_cache()
            case "cuda":
                torch.cuda.empty_cache()
            case _:
                pass
