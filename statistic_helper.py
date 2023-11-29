class StatisticHelper(object):
    # 对githubhelper中的信息进行统计
    def __init__(self, date=(0,0,0)):
        super().__init__()
        self.year = date[0]
        self.month = date[1]
        self.day = date[2]
        self.pr_num = 0
        self.issue_num = 0

    def get_total_pr_number(self, g_data):
        # NOTE: 当前只支持g_data包含Paddle仓库下的pr提取结果
        pr_number = 0
        for key in g_data.keys():
            pr_number = len(g_data[key])
        self.pr_num = pr_number
        return self.pr_num