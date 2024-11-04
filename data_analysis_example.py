import json
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
import re
import matplotlib.pyplot as plt
import qianfan
import os

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为SimHei
plt.rcParams['axes.unicode_minus'] = False    # 解决负号无法显示的问题

# 设置pd输出正确
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 调用千帆大模型，进行综合题的判断
credentials_file_path = '../baidu_secret.txt'

# 初始化字典来存储密钥
credentials = {}

# 读取文件并解析密钥
with open(credentials_file_path, 'r') as file:
    for line in file:
        # 去除换行符和空格
        line = line.strip()
        # 检查是否为空行或注释行（以#开头）
        if not line or line.startswith('#'):
            continue
            # 分割键和值
        key, value = line.split('=', 1)
        # 存储到字典中
        credentials[key] = value

    # 访问密钥
os.environ["QIANFAN_ACCESS_KEY"] = credentials.get('QIANFAN_ACCESS_KEY')
os.environ["QIANFAN_SECRET_KEY"] = credentials.get('QIANFAN_SECRET_KEY')
chat_comp = qianfan.ChatCompletion()

# 保留字母函数
def keep_only_letters(text):
    return re.sub(r'[^A-D]', '', text)  # 设置选择题的模糊匹配，保留ABCD


# 创建一个可以分析不同大模型的函数文件

def different_respond(json_file):
    summary_answers = []  # 提取大数据回答的数据

    with open(json_file, 'r', encoding='utf-8') as f:
        answers_example = json.load(f)
        for answers_item in answers_example:  # 不同模型输出的结果不同，判断模型在第一层还是第二层输出答案，来把答案遍历下来
            if isinstance(answers_item['answer'], dict):
                A_answers = answers_item["answer"]["result"]
                ID = answers_item["id"]
                Response_time = answers_item["response_time"]
                summary_answers.append({
                    "id": ID,
                    "answers": A_answers,
                    "response_time": Response_time,
                })
            elif isinstance(answers_item["answer"], str):
                A_answers = answers_item["answer"]
                ID = answers_item["id"]
                Response_time = answers_item["response_time"]
                summary_answers.append({
                    "id": ID,
                    "answers": A_answers,
                    "response_time": Response_time,
                })
            elif isinstance(answers_item["answer"], list):  # 如果为列表。即必须保证输入的文件，在一题多解的文件里面，这个路劲下必须是列表
                A_answers = answers_item["answer"]
                if isinstance(answers_item["response"],str):
                    B_answers = answers_item["response"]
                else:
                    B_answers = answers_item["response"]["result"]
                ID = answers_item["id"]
                Response_time = answers_item["response_time"]
                respond_num = answers_item["num"]
                summary_answers.append({
                     "id": ID,
                     "answers": A_answers,
                     "response_time": Response_time,
                     "answers_2": B_answers,
                     "tag": "Different",
                     "num": respond_num
                    })
        return summary_answers


# 创建判断正确率主函数
def calculate_accuracy(answers_json):
    total_summary = []
    summary_question = []  # 提取问题的数据

    summary_answers = different_respond(answers_json)  # 调用大模型回答函数
    # 需要注意的是，summary_answers 是通过调用 different_respond 函数得到的，它会为传入的每个 JSON 文件提取答案。

    with open('question_example.json', 'r', encoding='utf-8') as f:
        question_example = json.load(f)  # 加载问题的数据库

    questions = question_example["math_question"]
    for question_item in questions:

        answers = question_item['An']
        Id = question_item['id']
        Type = question_item["type"]
        Difficulty = question_item["difficulty"]

        if Type == "comprehensive":  # 如果是综合题
            summary_question.append({
                "id": Id,
                "Com_answers": answers,
                "Type": Type,
                "Difficulty": Difficulty
            })
        elif Type == "gap":  # 如果是填空题
            summary_question.append({
                "id": Id,
                "answers": answers,  # 填空题
                "Type": Type,
                "Difficulty": Difficulty
            })
        else:
            summary_question.append({
                "id": Id,
                "Selection_answers": answers,  # 选择
                "Type": Type,
                "Difficulty": Difficulty
            })
    total_summary = [summary_question, summary_answers]
    print(summary_question)
    print(summary_answers)


    # 数据匹配
    matching_results = []  # 匹配数据库
    Com_data = []  # 综合题数据库
    comsequence_score = []  # 不同解得分
    selection_score = 0  # 分数区分
    gap_score = 0
    com_score = 0
    selection_len = 0  # 一共有多少道选择题
    gap_len = 0  # 一共有多少道填空题
    com_len = 0  # 一共有多少道问答题

    dif_len = 0
    dif_score = 0


    # 构建难易度库
    difficulty_scores = {'ez': {'correct': 0, 'total': 0},
                         'av': {'correct': 0, 'total': 0},
                         'me': {'correct': 0, 'total': 0},
                         'ha': {'correct': 0, 'total': 0}}

# 创建函数来判断后续的操作
    def check_condition(total_summary):
        for respond in total_summary[1]:
            if "tag" not in respond:
                return True  # 找到符合条件的项
        return False  # 没有符合条件的项

    # 使用布尔标志来控制后续逻辑
    condition_met = check_condition(total_summary)
# 首先进行判断，看看是否是多回答的那份回答

    if condition_met:
        for question in total_summary[0]:
            difficulty = question["Difficulty"]
            # 选择题
            if "Selection_answers" in question:
                difficulty_scores[difficulty]['total'] += 1
                selection_len += 1
                question_id = question["id"]
                correct_answer = keep_only_letters(question["Selection_answers"].strip())  # 去除前后空格

                for answer in summary_answers:
                    if answer['id'] == question_id:  # 匹配 ID
                        model_answer_clear = answer['answers'].strip()  # 先只去除空格，不要立即过滤字母
                        if "【答案】" in model_answer_clear:
                            # 分割并获取答案部分，然后去除换行符并保留字母
                            model_answer = keep_only_letters(model_answer_clear.split("【答案】")[1].strip())
                        else:
                            model_answer = keep_only_letters(model_answer_clear)
                        # 现在 model_answer 应该只包含答案字母（如"C"）
                        similarity_score = fuzz.token_sort_ratio(correct_answer, model_answer)
                        if similarity_score > 50:  # 进行模糊匹配,如果ai进行多选，那么也可以判断出来
                            selection_score += 1
                            difficulty_scores[difficulty]['correct'] += 1
                            matching_results.append({
                                'question_id': question_id,
                                'model_answer': model_answer,
                                'correct_answer': correct_answer,
                                'similarity_score': similarity_score
                            })
                        else:
                            print("\n答案错误",model_answer,correct_answer)
            # 如果是填空题
            elif "answers" in question:
                gap_len += 1
                question_id = question["id"]
                correct_answer = question["answers"].strip()  # 去除前后空格
                difficulty_scores[difficulty]['total'] += 1
                for answer in summary_answers:
                    if answer['id'] == question_id:  # 匹配 ID
                        model_answer_clear = answer['answers'].strip()  # 先只去除空格，不要立即过滤字母
                        if "【答案】" in model_answer_clear:
                            # 分割并获取答案部分，然后去除换行符并保留字母
                            model_answer = model_answer_clear.split("【答案】")[1].strip()
                        else:
                            model_answer = model_answer_clear
                        # 现在 model_answer 应该只包含答案字母（如"C"）
                        
                        similarity_score = fuzz.token_sort_ratio(correct_answer, model_answer)
                        if similarity_score > 50:
                            difficulty_scores[difficulty]['correct'] += 1
                            gap_score += 1
                            matching_results.append({
                                'question_id': question_id,
                                'model_answer': model_answer,
                                'correct_answer': correct_answer,
                                'similarity_score': similarity_score   # 近似度
                            })
                        else:
                            print("\n答案错误",model_answer,correct_answer)
            # 如果是综合题
            elif "Com_answers" in question:
                com_len += 1
                question_id = question["id"]
                correct_answer = question["Com_answers"].strip()  # 去除前后空格
                difficulty_scores[difficulty]['total'] += 1  # 难度库总值加一
                for answer in summary_answers:
                    if answer['id'] == question_id:  # 匹配 ID
                        model_answer = answer['answers'].strip()  # 去除前后空格
                        Com_data.append({
                            'question_id': question_id,
                            'model_answer': model_answer,
                            'correct_answer': correct_answer,
                        })
                        answer_model = Com_data[-1]["model_answer"]
                        answer_correct = Com_data[-1]["correct_answer"]
                        print("Sending request to model...")

                        resp = chat_comp.do(model="ERNIE-Speed-128K", messages=[{
                            "role": "user",
                            "content": "以下是某一道数学题的答案，前一份是正确答案，后一份是给出的回答，请遵循以下标准："
                                       "比较答案和回答：如果表示答案和回答的内容基本一致，大多数重要步骤和结果都正确输出‘麦’，"
                                       "如果表示答案和回答在某些重要步骤或结果上存在明显的不同或错误请输出‘肯’，"
                                       "如果无法判断正确错误请输出‘劳’"
                                       "请注意，我只希望在你的回答中出现‘麦’，‘肯’，‘劳’这三个字符之一，而不要出现其他分析 \n" + answer_correct + "\n " + answer_model

                        }])
                        print("Received response from model.")
                        answer = resp["body"]
                        # print(answer)
                        if "麦" in answer["result"]:
                            com_score += 1
                            difficulty_scores[difficulty]['correct'] += 1
# 是多回答的那份回答
    else:

        for question in total_summary[0]:
            difficulty = question["Difficulty"]  # 设置难度
            dif_len += 1
            question_id = question["id"]
            # 对question进行处理，无论是哪个键都可以储存下来
            correct_answer = (
                    question.get("Com_answers", None) or
                    question.get("Selection_answers", None) or
                    question.get("answers", None)
            ).strip()

            difficulty_scores[difficulty]['total'] += 1  # 难度库总值加一
            for answer in summary_answers:
                if answer['id'] == question_id:  # 匹配 ID
                    model_answer = answer["answers_2"].strip()  # 去除前后空格
                    Com_data.append({
                        'question_id': question_id,
                        'model_answer': model_answer,
                        'correct_answer': correct_answer,
                    })
                    answer_model = Com_data[-1]["model_answer"]
                    answer_correct = Com_data[-1]["correct_answer"]
                    print("\n多解模型加载...")
                    resp = chat_comp.do(model="ERNIE-Speed-128K", messages=[{
                        "role": "user",
                        "content": "以下是某一道数学题的答案，前一份是正确答案，后一份是给出的多解回答，请严格遵循以下标准："
                                   "1. 必须每个解法都完全正确才输出'麦'"
                                   "2. 如果任何一个解法有错误或重要步骤缺失输出'肯'"
                                   "3. 如果无法判断输出'劳'"
                                   "请注意，我只希望看到'麦'，'肯'，'劳'这三个字符之一\n" + correct_answer + "\n " + answer_model
                    }])
                    print("多解模型结束加载")
                    answer = resp["body"]
                    print(answer)
                    if "麦" in answer["result"]:
                        dif_score += 1
                        difficulty_scores[difficulty]['correct'] += 1
                    print("\n复杂性评估...")

                    resp = chat_comp.do(model="ERNIE-Speed-128K", messages=[{
                        "role": "user",
                        "content": "以下是某一道数学题的多解答案，请遵循以下标准："
                                   "请综合回答的复杂性（评估每个解法的复杂性，检查模型是否能够给出简单和复杂的解决方案）"
                                   "和不同性（对查看不同解法之间的差异，分析是否采用了不同的思路。）综合得出一个得分（0-100分）\n" + answer_correct + "\n " + answer_model

                    }])

                    print("评估结束")
                    answer = resp["body"]

                    score_pattern = re.compile(r'(\d+)分')
                    match = score_pattern.search(answer["result"])

                    # 查找匹配的分数
                    if match is not None:
                        complex_score = int(match.group(1)) / 100
                        comsequence_score.append(complex_score)
                    else:
                        comsequence_score.append(int(40))
    score = gap_score + selection_score + com_score  # 应该加上com_score
    selection_correct_rate = selection_score / selection_len if selection_len > 0 else 0
    gap_correct_rate = gap_score / gap_len if gap_len > 0 else 0
    com_correct_rate = com_score / com_len if com_len > 0 else 0
    dif_correct_rate = dif_score / dif_len if dif_len > 0 else 0

    return [difficulty_scores,  # 返回难易度列表
            {
                "score": score,
                "selection_correct_rate": selection_correct_rate,
                "gap_correct_rate": gap_correct_rate,
                "matching_results": matching_results,
                "com_correct_rate": com_correct_rate
            }, summary_question,
            {
                "different_correct": dif_correct_rate,  # 一题多解的正确率
                "different_complex": comsequence_score  # 一题多解的复杂性
            }]

# 创建判断时间的主函数
def compare_json_time(answer_json):
    time = {}
    different_time_list = different_respond(answer_json)  # 调用简化后的遍历出来的列表
    for answer in different_time_list:
        question_id = answer["id"]  # 获取问题 ID
        response_time = answer["response_time"]  # 获取响应时间
        # 将时间信息存入字典
        time[question_id] = response_time
    return time  # 返回字典


# 可视化单解 JSON 文件的正确率
def compare_json_accuracy(answers_json):
    print("continue compare_json_accuracy")
    results = {}
    for answers_file in answers_json:  # 遍历每个 JSON 文件
            accuracy_result = calculate_accuracy(answers_file)
            results[answers_file] = accuracy_result

    # 将结果转换为 DataFrame 以便更好地展示
    accuracy_df = pd.DataFrame({
        "文件名": list(results.keys()),
        "匹配成功的数量": [res[1]['score'] for res in results.values()],  # res：在每次迭代中，res 将依次引用 results.values() 返回的每个字典。
        "选择题正确率": [res[1]['selection_correct_rate'] for res in results.values()],  # 也就是说，res先在value中遍历一边，然后字典中选择第二个列表
        "填空题正确率": [res[1]['gap_correct_rate'] for res in results.values()],
        "综合题正确率": [res[1]['com_correct_rate'] for res in results.values()],

    })
    for difficulty in ['ez', 'av', 'me', 'ha']:
        accuracy_df[f"{difficulty}正确率"] = [
            (res[0][difficulty]['correct'] / res[0][difficulty][
                'total'] * 100)
            if res[0][difficulty]['total'] > 0 else 0
            for res in results.values()
        ]

    return accuracy_df


# 可视化单解json文件的时间
def compare_time(answers_json):
    # 储存简化后的大数据保存的答案结果
    question_data = {}
    answers_data = {}
    time_results = pd.DataFrame()  # 建立一个用于储存循环的pd

    for answers_file in answers_json:
        question_data[answers_file] = compare_json_time(answers_file) # 返回时间函数的值
        answers_data[answers_file] = calculate_accuracy(answers_file)[2]  # 返回主函数的 summar_qustion
        for question in answers_data[answers_file]:  # 这里假设 question 是一个字典
            question_id = question.get("id")
            question_type = question.get("Type")
            difficulty = question.get("Difficulty")

            if question_id is not None:
                if answers_file in question_data and question_id in question_data[answers_file]:  # 检查id是否一致
                    response_time = question_data[answers_file].get(question_id)
                else:
                    print("No response time")  # 当没有找到对应的响应时间

                # 根据不同题型进行分类汇总响应时间
                time_results_1 = pd.DataFrame({
                    '模型': [answers_file],
                    '题号': [question_id],
                    '题型': [question_type],
                    '难度': [difficulty],
                    '响应时间': [response_time]
                })
                time_results = pd.concat([time_results, time_results_1], ignore_index=True)  # 拼接
    # 所有的情况
    avg_time_results = time_results.groupby(['模型', '题型', '难度'])['响应时间'].mean().reset_index()  # groupby(['模型', '题型', '难度'])：groupby 函数按照指定的列对 DataFrame 进行分组。
    # 根据题型分类，如果需要更改输出，则把难度改为题型即可
    avg_time_results = time_results.groupby(['模型', '难度'])['响应时间'].mean().reset_index()
    #
    return avg_time_results


# 表格化多解json文件的时间
def different_respond_time(dif_ans):
    results = {}

    for fid_answers in dif_ans:
        results[fid_answers] = different_respond(fid_answers)

    total_response_times = []
    for result in results:
        times_list = results[result]
        respond_time = 0  # 每个文件的响应时间从0开始
        for i in range(len(times_list)):
            respond_time += times_list[i]["response_time"]
        total_response_times.append(respond_time)

        # 创建DataFrame
    accuracy_df = pd.DataFrame({
        "文件名": list(results.keys()),
        "耗费时间": total_response_times
    })
    print(accuracy_df)
    return accuracy_df


# 可视化多种多解json的得分
def different_respond_vision(dif_ans):
    results = {
        "文件名": [],
        "正确率": [],
        "复杂度": []
    }
    for dif_an in dif_ans:
        different_res = calculate_accuracy(dif_an)[3]
        dif_cor = different_res["different_correct"]  # 正确率
        dif_cpl = different_res["different_complex"]  # 复杂度
        results["文件名"].append(dif_an)  # 假设 dif_an 是文件名
        results["正确率"].append(dif_cor)
        avg_complexity = sum(dif_cpl) / len(dif_cpl) if dif_cpl else 0
        results["复杂度"].append(avg_complexity)
    df_results = pd.DataFrame(results)

    # 将文件名设置为索引
    df_results.set_index("文件名", inplace=True)
    print(df_results)
    return df_results

# 画图多解正确率和复杂度
def plot_different_respond(df_results):

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 绘制正确率的柱状图
    ax1.bar(df_results.index, df_results["正确率"], color='b', alpha=0.6, label='正确率')
    ax1.set_xlabel('文件名')
    ax1.set_ylabel('正确率', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # 创建第二个坐标轴来绘制复杂度
    ax2 = ax1.twinx()
    ax2.plot(df_results.index, df_results["复杂度"], color='r', marker='o', label='复杂度')
    ax2.set_ylabel('平均复杂度', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # 添加图例
    fig.tight_layout()
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.title('不同文件的正确率和复杂度')
    plt.xticks(rotation=45)  # 旋转横坐标标签
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()


# 可视化多解解法数量
def num_different(num_ans):
    for df_result in num_ans:
        df_summary = pd.DataFrame(different_respond(df_result))
        df_summary.set_index("id", inplace=True)
        print(f"{df_summary}")


answers_json = ["baidu_only_answers_example.json", "Hunyuan_only_answers_example.json", "Doubao_only_Answers_example.json"]  # 多个json
respond_json = ["baidu_different_answers_example.json","hunyuan_different_answers_example.json", "Doubao_different_answers_example.json"]
questions_json = 'question_example.json'
comparison_results = compare_json_accuracy(answers_json)  # 正确率比较
time_comparison_results = compare_time(answers_json)  # 时间比较

dif_time_comparison = different_respond_time(respond_json)  # 时间比较
# 画图
df_results = different_respond_vision(respond_json)  # 正确率比较
plot_different_respond(df_results)

num_different(respond_json)  # 数量列表

# 单解数据和画图
def draw(time_comparison_results,comparison_results):

    #  画图
    time_comparison_results['模型'] = time_comparison_results['模型'].str.replace('_only_answers_example.json', '')  # 替换掉
    pivot_table = time_comparison_results.pivot(index='难度', columns='模型', values='响应时间')
    pivot_table.plot(kind='bar', figsize=(10, 6), width=0.7)
    plt.xlabel('难度')
    plt.ylabel('平均响应时间 (秒)')
    plt.title('不同题型下各模型的平均响应时间')
    plt.xticks(rotation=0)  # 横坐标标签保持水平
    plt.legend(title='模型')

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()

    print(comparison_results.to_string(index=False, justify='center', col_space=5))  # 防止标签折叠
    print(time_comparison_results)


draw(time_comparison_results, comparison_results)











