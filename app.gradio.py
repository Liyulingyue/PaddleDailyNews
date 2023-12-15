import gradio as gr

from datetime import datetime, timedelta
from utils import log_init
import erniebot

from github_helper import CacheMode, GithubHelper
from statistic_helper import StatisticHelper
from layout_helper import LayoutHelper


def fn_get_markdown_str(GITHUB_TOKEN,
                        ERNIE_TOKEN,
                        Year=2023,
                        Month=12,
                        Day=14,
                        ORGANIZATION = "PaddlePaddle",
                        REPO_NAME = "paddle"):
    log_init()
    erniebot.api_type = 'aistudio'
    erniebot.access_token = ERNIE_TOKEN

    g_helper = GithubHelper(GITHUB_TOKEN, org=ORGANIZATION)  # noqa: F405
    print(g_helper.get_user_name())
    g_helper.RefreshData([CacheMode.PR, CacheMode.ISSUES],
                        start_time=datetime(Year, Month, Day),
                        end_time=datetime(Year, Month, Day)+timedelta(days=1),
                        repo_names = [REPO_NAME])

    s_helper = StatisticHelper(date=(Year,Month,Day))
    s_helper.refresh_number(g_helper)
    s_helper.get_score_of_pr(g_helper)
    s_helper.get_score_of_issue(g_helper)
    s_helper.get_rank_of_contributors(g_helper)
    s_helper.get_rank_of_issuers(g_helper)

    l_helper = LayoutHelper(repo_name=REPO_NAME)
    l_helper.generate_layout(s_helper)
    markdown_str = l_helper.GetMarkdownStr()
    return gr.update(value=markdown_str)



with gr.Blocks() as demo:
    gr.Markdown("""
    # 基于文心一言的Github仓库日报生成器

    输入你想要生成日报的时间、你的AIStudio Token以及Github Token，为你生成一个当前仓库的日报。

    **特别说明：请勿尝试，目前无法确认AISTUDIO是否会导致串Token的问题，该方案巨烧Token，想查看效果可以查看源项目，包含样例和源代码仓库。**
    
    """)
    GITHUB_TOKEN = gr.Text(label="Github Token")
    ERNIE_TOKEN = gr.Text(label="AiStudio Token")
    Y = gr.Number(label="年份",value=2023)
    M = gr.Number(label="月份",value=12)
    D = gr.Number(label="日",value=14)
    Org = gr.Text(label="用户名称",value="PaddlePaddle")
    Rep = gr.Text(label="仓库名称",value="paddle")
    btn = gr.Button(value="生成")
    Result = gr.Markdown(label="生成结果样例",value=f"""
# 当前是生成样例

# 飞桨日报
2023年12月14日 PR:24条 ISSUE:2条

---

        
## PR聚焦

            
1. **[#60024](https://github.com/PaddlePaddle/Paddle/pull/60024)**
    - 内容介绍：这段代码主要对DenseTensor类的赋值操作符和构造函数进行了修改，移除了对#ifdefPADDLE_WITH_DNNL的条件编译，这意味着不再使用DNNL后向传递。修改涉及到对象的深拷贝和移动语义，是代码中较为核心的部分。同时，代码中增加了一些函数和变量，移除了一些注释，使代码变得更加简洁和清晰。新增的函数set_mem_desc用于设置存储属性，涉及到DenseTensor类存储属性的修改，需要考虑到代码的稳定性和正确性。此外，代码将CopyStorageProperties(src.storage_properties_)的结果使用std::move转移所有权给properties_，避免了不必要的拷贝操作，提高了代码效率。同时删除了与DNNl相关的mem_desc_赋值，可能是由于不再需要这个变量或者这个变量的值已经被其他方式处理过了。
    - 量化评分：7.125
                
1. **[#60023](https://github.com/PaddlePaddle/Paddle/pull/60023)**
    - 内容介绍：这段代码主要负责对输入的days和hours进行校验，确保其中不含有特定的特殊字符，并将split_interval和split_per_pass转换为整数。
    - 量化评分：7.0
                
1. **[#60022](https://github.com/PaddlePaddle/Paddle/pull/60022)**
    - 内容介绍：这段代码主要涉及插入操作，对原有的函数进行了较大的改动，增加了代码的复杂性和执行难度。修改内容包括对函数参数的调整以及插入操作的修改，体现了代码的重要性和修改难度。这段代码主要修改了insert_allgather_op函数，增加了sync参数，并相应地在函数内部对sync进行了处理。同时，对insert_op的调用也根据sync的值进行了选择。这种修改可以更好地适应不同的使用场景，提高代码的灵活性和可维护性。这段代码主要是对函数`defis_grad`的参数和某些变量进行了修改，包括添加了新的参数`sync`，并对一些变量进行了赋值操作。这些修改都相对简单，没有涉及到复杂的逻辑或算法。由于修改的代码较少，所以整体评价为7分。在函数调用中添加了一个名为sync的参数，该参数可能用于同步操作。原有逻辑未发生变化。
    - 量化评分：6.583333333333333
                

---

        
## ISSUE追踪

        
1. **[#59998](https://github.com/PaddlePaddle/Paddle/issues/59998)**
    - 内容介绍：该问题涉及到C++代码的性能优化，这是一个非常重要的问题。由于C++代码的性能对于实际应用来说非常重要，因此这个问题需要得到重视。同时，这个问题也涉及到代码优化和性能测试，需要一定的技术能力和经验来解决。因此，我会给这个问题的得分为8分。
    - 量化评分：8.0
                        
1. **[#60013](https://github.com/PaddlePaddle/Paddle/issues/60013)**
    - 内容介绍：该issue涉及到飞桨编译过程中的优化，对于提高开发效率和减少编译体积有重要意义。同时，该issue也涉及到多个代码库的修改，需要一定的技术难度和细心程度。因此，该issue的得分较高。没有具体的代码或产品信息，无法进行评估。
    - 量化评分：4.0
                        

---

                
## 贡献者荣誉榜

### PR
        
1. Galaxy1458：提交PR2次
            
1. pangengzheng：提交PR1次
            
1. zyfncg：提交PR1次
            
1. NeroLoh：提交PR1次
            
1. wanghuancoder：提交PR1次
            
1. danleifeng：提交PR1次
            
1. AndSonder：提交PR1次
            
1. tianhaodongbd：提交PR1次
            
1. SylarTiaNII：提交PR1次
            
1. cyber-pioneer：提交PR1次
            
1. zhaoyinglia：提交PR1次
            
1. winter-wang：提交PR1次
            
1. lyuwenyu：提交PR1次
            
1. DrRyanHuang：提交PR1次
            
1. MarioLulab：提交PR1次
            
1. zxcd：提交PR1次
            
1. zhangbo9674：提交PR1次
            
1. 0x45f：提交PR1次
            
1. FlyingQianMM：提交PR1次
            
1. chalsliu：提交PR1次
            
1. pkuzyc：提交PR1次
            
1. gouzil：提交PR1次
            
1. xiaoguoguo626807：提交PR1次
            

### ISSUE
        
1. risemeup1：提交ISSUE1次
            
1. xiefuwei390：提交ISSUE1次
            

---

        

感谢各位开发者对PaddlePaddle的持续关注和贡献，让我们一起推动深度学习技术的发展和应用。期待明天更多的精彩！
    
    
    """)

    btn.click(fn=fn_get_markdown_str, inputs=[GITHUB_TOKEN,ERNIE_TOKEN,Y,M,D,Org,Rep], outputs=Result)
    



demo.launch()
