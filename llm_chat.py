import erniebot
import json
from configure import ERNIE_TOKEN

def get_llm_answer(prompt):
    erniebot.api_type = 'aistudio'
    erniebot.access_token = ERNIE_TOKEN
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=[{'role': 'user', 'content': prompt}],
        top_p=0,
        temperature = 0.1,
    )
    result = response.get_result()
    return result

def extract_json_from_llm_answer(result):
    s_id = result.index('```json')
    e_id = result.index('```', s_id+7)
    json_str = result[s_id+7:e_id]
    json_dict = json.loads(json_str)
    return json_dict

def get_llm_json_answer(prompt):
    result = get_llm_answer(prompt)
    json_dict = extract_json_from_llm_answer(result)
    return json_dict
