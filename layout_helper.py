from statistic_helper import *

class LayoutHelper(object):
    def __init__(self):
        super(self).__init__()

    def generate_layout(self, s:StatisticHelper):
        MarkDown_str = f"""
# 飞桨日报
{s.year}年{s.month}月{s.day}日 PR:{s.pr_num}条 ISSUE:{s.issue_num}条
---

## 概述
*简述：概述当天PaddlePaddle社区的活跃情况，提及PR和ISSUE的总数，并突出一些重要或热点的内容。*
---


**PR聚焦**

*标题：重要PR一览*

1. **[PR#XXXX](https://github.com/PaddlePaddle/Paddle/pull/XXXX)**：*详细描述：对此次PR的核心内容进行简要描述，如功能增加、性能提升或BUG修复等。*
2. **[PR#XXXX](https://github.com/PaddlePaddle/Paddle/pull/XXXX)**：*详细描述：针对此PR的创新点、重要性或影响范围进行描述。*

*数据分析：对当日PR的统计数据进行分析，如提交者的地域分布、PR涉及的模块分布等。*

---

**ISSUE追踪**

*标题：热点ISSUE速览*

1. **[ISSUE#XXXX](https://github.com/PaddlePaddle/Paddle/issues/XXXX)**：*详细描述：描述此ISSUE的主要问题、影响范围及当前状态。*
2. **[ISSUE#XXXX](https://github.com/PaddlePaddle/Paddle/issues/XXXX)**：*详细描述：对另一热点ISSUE进行简要介绍，引发读者关注。*

*数据分析：对当日ISSUE的统计，如问题类型分布、解决问题所消耗的时间等。*

---

**社区之声**

*标题：精彩讨论与热门话题*

* 描述：介绍社区中的热门讨论和话题，可以是对某个功能的讨论、使用心得分享、学习教程等。引发读者的参与和讨论。

---

**贡献者荣誉榜**

*标题：当日贡献者TOP3*

1. *贡献者名称：对此贡献者的贡献内容进行简要描述，并链接到其个人主页。*
2. *贡献者名称：简要描述其贡献内容。*
3. *贡献者名称：简要描述其贡献内容。*

---

**尾版寄语**

感谢各位开发者对PaddlePaddle的持续关注和贡献，让我们一起推动深度学习技术的发展和应用。期待明天更多的精彩！
        """