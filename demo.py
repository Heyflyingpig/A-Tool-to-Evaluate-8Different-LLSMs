import json
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
import re


# 保留字母函数
def keep_only_letters(text):
    return re.sub(r'[^A-D]', '', text)  # 设置选择题的模糊匹配，保留ABCD


# 创建一个函数，加载不同的回答数据
def load_answers(json_file):
    summary_answers = []
    with open(json_file, 'r', encoding='utf-8') as f:
        answers_example = json.load(f)  # 加载大模型回答数据
        for answers_item in answers_example:
            A_answers = answers_item["answer"]["result"]
            ID = answers_item["id"]
            summary_answers.append({
                "id": ID,
                "answers": A_answers,
            })
    return summary_answers


# 提取问题的数据
summary_question = []
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


# 通过函数加载不同的回答数据
summary_answers = load_answers('baidu_only_answers_example.json')

total_len = len(summary_answers)

print(summary_question)
print(summary_answers)


# 数据匹配
matching_results = []
Com_data = []  # 综合题数据库
selection_score = 0  # 分数区分
gap_score = 0
com_score = 0
selection_len = 0  # 一共有多少道选择题
gap_len = 0  # 一共有多少道填空题
com_len = 0  # 一共有多少道问答题

# 构建难易度库
difficulty_scores = {'ez': {'correct': 0, 'total': 0},
                     'av': {'correct': 0, 'total': 0},
                     'me': {'correct': 0, 'total': 0},
                     'ha': {'correct': 0, 'total': 0}}


for question in summary_question:
    difficulty = question["Difficulty"]
    # 选择题
    if "Selection_answers" in question:
        difficulty_scores[difficulty]['total'] += 1
        selection_len += 1
        question_id = question["id"]
        correct_answer = keep_only_letters(question["Selection_answers"].strip())  # 去除前后空格

        for answer in summary_answers:
            if answer['id'] == question_id:  # 匹配 ID
                model_answer = keep_only_letters(answer['answers'].strip())  # 去除前后空格
                # 使用 token_sort_ratio 进行模糊匹配
                similarity_score = fuzz.token_sort_ratio(correct_answer, model_answer)
                if similarity_score > 67:  # 进行模糊匹配,如果ai进行多选，那么也可以判断出来
                    selection_score += 1
                    difficulty_scores[difficulty]['correct'] += 1
                    matching_results.append({
                        'question_id': question_id,
                        'model_answer': model_answer,
                        'correct_answer': correct_answer,
                        'similarity_score': similarity_score
                    })
    # 如果是填空题
    elif "answers" in question:
        gap_len += 1
        question_id = question["id"]
        correct_answer = question["answers"].strip()  # 去除前后空格
        difficulty_scores[difficulty]['total'] += 1
        for answer in summary_answers:
            if answer['id'] == question_id:  # 匹配 ID
                model_answer = answer['answers'].strip()  # 去除前后空格
                # 使用 token_sort_ratio 进行模糊匹配
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
    # 如果是综合题
    elif "Com_answers" in question:
        com_len += 1
        question_id = question["id"]
        correct_answer = question["Com_answers"].strip()  # 去除前后空格
        difficulty_scores[difficulty]['total'] += 1  # 难度库总值加一
        for answer in summary_answers:
            if answer['id'] == question_id:  # 匹配 ID
                model_answer = answer['answers']  # 去除前后空格
                Com_data.append({
                    'question_id': question_id,
                    'model_answer': model_answer,
                    'correct_answer': correct_answer,
                })

score = gap_score + selection_score
selection_correct_rate = selection_score / selection_len
gap_correct_rate = gap_score / gap_len
com_correct_rate = 0.25

ez_correct_rate = difficulty_scores["ez"]["correct"] / difficulty_scores["ez"]["total"]
av_correct_rate = difficulty_scores["av"]["correct"] / difficulty_scores["av"]["total"]
me_correct_rate = difficulty_scores["me"]["correct"] / difficulty_scores["me"]["total"]
ha_correct_rate = difficulty_scores["ha"]["correct"] / difficulty_scores["ha"]["total"]
#  构建正确率矩阵

type_correct_rate = np.array(
    [selection_correct_rate, gap_correct_rate, com_correct_rate]
)
dif_correct_rate = np.array(
    [ez_correct_rate, av_correct_rate, me_correct_rate, ha_correct_rate]
)

print("匹配成功的数量:", score)
print("匹配结果:", matching_results)
print(f"选择题正确率: ", selection_correct_rate, "填空题正确率： ", gap_correct_rate, "综合题正确率： ", com_correct_rate)
print(Com_data)
print(difficulty_scores)

# 不同题型的正确率
Differenttype_rate_pd = pd.DataFrame(type_correct_rate, ["选择题正确率", "填空题正确率", "综合题正确率"], ["百度"])

# 不同难度的正确率
Differentdiff_rate_pd = pd.DataFrame(dif_correct_rate, ["简单题正确率", "中上题正确率", "中下题正确率", "难题正确率"], ["百度"])

print(Differenttype_rate_pd, "\n", Differentdiff_rate_pd)