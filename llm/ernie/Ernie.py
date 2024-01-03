import json
from typing import Any

import erniebot

from ..base import LLM_base


class Ernie(LLM_base):
    def __init__(self, model_name: str, token: str):
        super().__init__(model_name)
        # 字符串长度上限
        self.gap_length = 1902
        erniebot.api_type = "aistudio"
        erniebot.access_token = token

    def load_model(self):
        pass

    def get_llm_answer(self, prompt: str) -> str:
        response = erniebot.ChatCompletion.create(
            model="ernie-bot",
            messages=[{"role": "user", "content": prompt}],
            top_p=0.1,
            temperature=0.1,
            penalty_score=1.0,
        )
        result = response.get_result()
        assert isinstance(result, str)
        return result

    def extract_json_from_llm_answer(self, result: str) -> dict[str, Any]:
        s_id = result.index("```json")
        e_id = result.index("```", s_id + 7)
        json_str = result[s_id + 7 : e_id]
        json_dict = json.loads(json_str)
        return json_dict
