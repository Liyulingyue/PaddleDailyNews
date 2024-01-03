from llm import LLM_base


def get_llm_json_answer(model: LLM_base, prompt: str):
    result = model.get_llm_answer(prompt)
    json_dict = model.extract_json_from_llm_answer(result)
    return json_dict


def get_score_of_a_change(model: LLM_base, raw_str: str):
    sum_score = 0
    sum_comment = ""
    sum_introduction = ""
    count = 0
    changed_codes: str = raw_str.replace(" ", "")
    res_js = """
    {
    "得分":float
    "评分理由":str
    "修改内容简单介绍":str
    }
    """
    prompt = """
    你是百度公司的员工，你之前是程序员，现在是产品经理，你对于代码和产品都非常了解，你将根据github的代码diff信息给代码进行打分以评价这份代码的重要程度。
    你对代码的评价和这段代码的修改难度和重要程度等等因素都有关系。你需要非常具有发散性思维来考虑并给出具体的得分数值。有些代码变动非常困难并重要，有些则非常简单。
    请以Json形式给出回复，Json返回的内容格式为：
    {res_js}
    得分的取值介于0到10。
    代码中以`+`开头的行是这次改动增加的行，`-`开头的行是这次改动删除的行，其他符号开头的代码仅用于提供上下文信息。你需要进行评价的代码是：{codes}
    """

    # 有上限模式和无上限模式, 无上限模式不需要循环, 也不需要计算平均数
    match model.gap_length:
        case -1:
            result = get_llm_json_answer(model, prompt.format(res_js=res_js, codes=changed_codes))
            sum_score = result["得分"]
            sum_comment = result["评分理由"]
            sum_introduction = result["修改内容简单介绍"]
        case _:
            cut_str = [changed_codes[i : i + model.gap_length] for i in range(0, len(changed_codes), model.gap_length)]
            for codes in cut_str:
                try:
                    result = get_llm_json_answer(model, prompt.format(res_js=res_js, codes=codes))
                    sum_score += result["得分"]
                    sum_comment += result["评分理由"]
                    sum_introduction += result["修改内容简单介绍"]
                    count += 1
                except Exception:
                    count += 0
            sum_score: float = sum_score / count
    return sum_score, sum_comment, sum_introduction


def get_score_of_a_issue(model: LLM_base, raw_str: str) -> tuple[float, str, str]:
    sum_score = 0
    sum_comment: str = ""
    sum_introduction: str = ""
    count = 0
    changed_codes = raw_str.replace(" ", "")
    res_js = """
    {
    "得分":float
    "评分理由":str
    "修改内容简单介绍":str
    }
    """
    prompt = """
    你是百度公司的员工，你之前是程序员，现在是产品经理，你对于代码和产品都非常了解，你将根据issue信息进行打分以评价这个issue的重要程度。
    你对issue的评价和这个issue的技术难度等因素都有关系。你需要非常具有发散性思维来考虑并给出具体的得分数值。有些issue非常困难并重要，有些则非常不重要。
    issue的信息是{codes}
    请以Json形式给出回复，Json返回的内容格式为：
    {res_js}
    得分的取值介于0到10。
    """
    match model.gap_length:
        case -1:
            result = get_llm_json_answer(model, prompt.format(res_js=res_js, codes=changed_codes))
            sum_score = result["得分"]
            sum_comment = result["评分理由"]
            sum_introduction = result["修改内容简单介绍"]
        case _:
            cut_str = [changed_codes[i : i + model.gap_length] for i in range(0, len(changed_codes), model.gap_length)]
            for codes in cut_str:
                try:
                    result = get_llm_json_answer(model, prompt.format(res_js=res_js, codes=codes))
                    sum_score += result["得分"]
                    sum_comment += result["评分理由"]
                    sum_introduction += result["修改内容简单介绍"]
                    count += 1
                except Exception:
                    count += 0
            sum_score: float = sum_score / count
    return sum_score, sum_comment, sum_introduction


def get_summary_of_a_change(model: LLM_base, raw_str: str) -> str:
    sum_introduction: str = ""
    changed_codes: str = raw_str.replace(" ", "")
    res_js = """
    "介绍":str
    """
    prompt = """
    你是百度公司的员工，你之前是程序员，现在是产品经理，你对于代码和产品都非常了解，现在有很多段代码改动的介绍文本，你需要结合上下文信息，生成一份完整的代码改动介绍文本。
    请以Json形式给出回复，Json返回的内容格式为：
    {res_js}
    代码改动的介绍文本是：{codes}
    """
    match model.gap_length:
        case -1:
            result = get_llm_json_answer(model, prompt.format(res_js=res_js, codes=changed_codes))
            sum_introduction = result["介绍"]
        case _:
            cut_str = [changed_codes[i : i + model.gap_length] for i in range(0, len(changed_codes), model.gap_length)]
            for codes in cut_str:
                try:
                    result = get_llm_json_answer(model, prompt.format(res_js=res_js, codes=codes))
                    sum_introduction += result["介绍"]
                except Exception:
                    pass
    return sum_introduction
