import torch


class LLM_base:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None

    def load_model(self) -> None:
        raise NotImplementedError("Error LLM should implement load_model")

    def get_llm_answer(self, prompt: str) -> str:
        raise NotImplementedError("Error LLM should implement get_llm_answer")

    def get_device(self) -> str:
        if torch.backends.mps.is_built():
            return "mps"
        elif torch.backends.cuda.is_built():
            return "cuda"

        return "cpu"

    def extract_json_from_llm_answer(self, result: str):
        raise NotImplementedError("Error LLM should implement extract_json_from_llm_answer")
