from typing import Any


class LLM_base:
    def __init__(self, model_name: str, token: str = ""):
        self.model_name = model_name
        self.model = None
        # 字符串上限: -1 代表不限制
        self.gap_length: int = -1

    def load_model(self) -> None:
        raise NotImplementedError("Error LLM should implement load_model")

    def get_llm_answer(self, prompt: str) -> str:
        raise NotImplementedError("Error LLM should implement get_llm_answer")

    def extract_json_from_llm_answer(self, result: str) -> dict[str, Any]:
        raise NotImplementedError("Error LLM should implement extract_json_from_llm_answer")
