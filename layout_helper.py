from statistic_helper import *  # noqa: F403


class LayoutHelper(object):
    def __init__(self):
        super().__init__()
        self.MarkDown_str = ""

    def generate_layout(self, s: StatisticHelper):  # noqa: F405
        self.MarkDown_str = f"""
# 飞桨日报
{s.year}年{s.month}月{s.day}日 PR:{s.pr_num}条 ISSUE:{s.issue_num}条

---

## 概述
*简述：概述当天PaddlePaddle社区的活跃情况，提及PR和ISSUE的总数，并突出一些重要或热点的内容。*

---

## PR聚焦
*数据分析：对当日PR的统计数据进行分析，如提交者的地域分布、PR涉及的模块分布等。*

1. **[PR#XXXX](https://github.com/PaddlePaddle/Paddle/pull/XXXX)**
    - 内容介绍：*详细描述：对此次PR的核心内容进行简要描述，如功能增加、性能提升或BUG修复等。*
2. **[PR#XXXX](https://github.com/PaddlePaddle/Paddle/pull/XXXX)**
    - 内容介绍: *详细描述：针对此PR的创新点、重要性或影响范围进行描述。*

---

## ISSUE追踪
*数据分析：对当日ISSUE的统计，如问题类型分布、解决问题所消耗的时间等。*

1. **[ISSUE#XXXX](https://github.com/PaddlePaddle/Paddle/issues/XXXX)**
    - 内容介绍: *详细描述：描述此ISSUE的主要问题、影响范围及当前状态。*
2. **[ISSUE#XXXX](https://github.com/PaddlePaddle/Paddle/issues/XXXX)**
    - 内容介绍: *详细描述：对另一热点ISSUE进行简要介绍，引发读者关注。*

---

## 贡献者荣誉榜

### PR
1. *贡献者名称：对此贡献者的贡献内容进行简要描述，并链接到其个人主页。*
2. *贡献者名称：简要描述其贡献内容。*
3. *贡献者名称：简要描述其贡献内容。*

### Reviewer
1. *贡献者名称：对此贡献者的贡献内容进行简要描述，并链接到其个人主页。*
2. *贡献者名称：简要描述其贡献内容。*
3. *贡献者名称：简要描述其贡献内容。*

### 讨论
1. *贡献者名称：对此贡献者的贡献内容进行简要描述，并链接到其个人主页。*
2. *贡献者名称：简要描述其贡献内容。*
3. *贡献者名称：简要描述其贡献内容。*

---

感谢各位开发者对PaddlePaddle的持续关注和贡献，让我们一起推动深度学习技术的发展和应用。期待明天更多的精彩！
        """

    def Export2MarkdownFile(self, path="DailyReport.md"):
        with open(path, "w", encoding="utf8") as f:
            f.write(self.MarkDown_str)
