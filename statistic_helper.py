class StatisticHelper(object):
    # 对githubhelper中
    def __init__(self):
        pass

    def get_total_pr_number(self, g_data):
        # NOTE: 当前只支持g_data包含Paddle仓库下的pr提取结果
        pr_number = 0
        for key in g_data.keys():
            pr_number = len(g_data[key])
        return pr_number