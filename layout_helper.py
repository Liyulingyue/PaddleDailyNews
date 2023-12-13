from statistic_helper import *  # noqa: F403
from llm_chat import *

class LayoutHelper(object):
    def __init__(self):
        super().__init__()
        self.MarkDown_str = ""

    def generate_layout(self, s_helper: StatisticHelper):  # noqa: F405
        self.MarkDown_str = ""
        self.MarkDown_str += self.generate_layout_header(s_helper)
        # self.MarkDown_str += self.generate_layout_summary(s_helper)
        self.MarkDown_str += self.generate_layout_PR_infor(s_helper)
        self.MarkDown_str += self.generate_layout_Issue_infor(s_helper)
        self.MarkDown_str += self.generate_layout_pr_ranks(s_helper)
        self.MarkDown_str += self.generate_layout_issue_ranks(s_helper)
        self.MarkDown_str += self.generate_layout_ender(s_helper)

    def Export2MarkdownFile(self, path="DailyReport.md"):
        with open(path, "w", encoding="utf8") as f:
            f.write(self.MarkDown_str)

    def generate_layout_header(self, s_helper: StatisticHelper):
        Markdown_str = f"""
# 飞桨日报
{s_helper.year}年{s_helper.month}月{s_helper.day}日 PR:{s_helper.pr_num}条 ISSUE:{s_helper.issue_num}条

---

        """
        return Markdown_str

    def generate_layout_summary(self, s_helper: StatisticHelper):
        Markdown_str = f"""
## 概述
*简述：概述当天PaddlePaddle社区的活跃情况，提及PR和ISSUE的总数，并突出一些重要或热点的内容。*

---

        """
        return Markdown_str

    def generate_layout_PR_infor(self, s_helper: StatisticHelper):
        score_threshold = 0 if len(s_helper.pr_list)<3 else max(0, s_helper.pr_list[2]["score"])
        Markdown_str = ""
        if 0:
            Markdown_str += f"""
## PR聚焦
*数据分析：对当日PR的统计数据进行分析，如提交者的地域分布、PR涉及的模块分布等。*
        
            """
        else:
            Markdown_str += f"""
## PR聚焦

            """
        for pr_infor in s_helper.pr_list:
            if pr_infor["score"]>=score_threshold:
                Markdown_str += f"""
1. **[#{pr_infor['id']}](https://github.com/PaddlePaddle/Paddle/pull/{pr_infor['id']})**
    - 内容介绍：{get_summary_of_a_change(pr_infor["introduction"])}
    - 量化评分：{pr_infor["score"]}
                """

        Markdown_str += f"""

---

        """
        return Markdown_str

    def generate_layout_Issue_infor(self, s_helper: StatisticHelper):
        score_threshold = 0 if len(s_helper.issue_list)<3 else max(0, s_helper.issue_list[2]["score"])
        Markdown_str = ""
        if 0:
            Markdown_str += f"""
    ## ISSUE追踪
    *数据分析：对当日ISSUE的统计，如问题类型分布、解决问题所消耗的时间等。*
    
            """
        else:
            Markdown_str += f"""
## ISSUE追踪

        """
        for issue_infor in s_helper.issue_list:
            if issue_infor["score"] >= score_threshold:
                Markdown_str += f"""
1. **[#{issue_infor['id']}](https://github.com/PaddlePaddle/Paddle/issues/{issue_infor['id']})**
    - 内容介绍：{issue_infor["comments"]}
    - 量化评分：{issue_infor["score"]}
                        """

        Markdown_str += f"""

---

                """
        return Markdown_str

    def generate_layout_pr_ranks(self, s_helper: StatisticHelper):
        Markdown_str = ""
        Markdown_str += f"""
## 贡献者荣誉榜

### PR
        """
        for infor in s_helper.pr_rank_list:
            Markdown_str += f"""
1. {infor["user"]}：提交PR{infor["times"]}次
            """
        return Markdown_str

    def generate_layout_issue_ranks(self, s_helper: StatisticHelper):
        Markdown_str = ""
        Markdown_str += f"""

### ISSUE
        """
        for infor in s_helper.issue_rank_list:
            Markdown_str += f"""
1. {infor["user"]}：提交ISSUE{infor["times"]}次
            """
        Markdown_str += f"""

---

        """
        return Markdown_str

    def generate_layout_ender(self, s_helper: StatisticHelper):
        MarkDown_str = f"""

感谢各位开发者对PaddlePaddle的持续关注和贡献，让我们一起推动深度学习技术的发展和应用。期待明天更多的精彩！
        """
        return MarkDown_str
