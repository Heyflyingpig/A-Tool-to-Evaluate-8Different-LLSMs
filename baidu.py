import os
import qianfan
import json
import time
import re
# 通过环境变量初始化认证信息
# 方式一：【推荐】使用安全认证AK/SK
# 替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk，如何获取请查看https://cloud.baidu.com/doc/Reference/s/9jwvz2egb
credentials_file_path = '../secret.txt'

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

# 读取 JSON 文件
A = "请一题多解该题：\n"  # 对于无法一题多解的情况
B = "你是一个准备高考的优秀高中生，掌握了很多高中知识，在考场上你遇到了如下这道题： \n "  # 模拟情景，不同的prompt
C = "你是一个数学家，你掌握了很多知识与公式定理，你将解决如下这道题: \n"
D = ""


def baidu1(input_json_path, output_json_path):
    results = []

    # 读取输入JSON文件
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        questions = data["math_question"]

        # 遍历问题列表
    for question_item in questions:
        description_list = question_item["Description"]
        ID = question_item.get("id")

        for item in description_list:
            prompt = "如下是完整的题目，如果是选择题和填空题，请只给出答案 \n" + item['Qu'] + "如上是完整的题目，请只给出答案，不需要分析 \n"

            picture = item.get('picture')
            print(f"\n提问: {prompt}")

            start_time = time.time()

            # 与模型交互获取答案
            resp = chat_comp.do(model="ERNIE-Speed-128K", messages=[{
                "role": "user",
                "content": prompt
            }])
            print("Received response from model.")
            end_time = time.time()
            answer = resp.get("body", "")
            print(answer)
            response_time = end_time - start_time
            print(f"获取答案时间: {response_time:.2f} 秒")

            # 保存答案及相关信息
            results.append({
                "question": prompt,
                "answer": answer,
                "response_time": response_time,
                "id": ID
            })

            # 将结果保存到输出JSON文件
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    # 调用函数
def baidu2(input_json_path, output_json_path):
    results = []
    results_2 = []

    # 读取输入JSON文件
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        questions = data.get("math_question", [])

        # 遍历问题列表
    for question_item in questions:
        description_list = question_item.get("Description", [])
        ID = question_item.get("id")

        for item in description_list:
            prompt = "如下有一道题目，请一题多解该题目，每个解之间请用换行符分开：\n" + item['Qu']

            picture = item.get('picture')
            print(f"\n提问: {prompt}")

            start_time = time.time()

            # 与模型交互获取答案
            resp = chat_comp.do(model="ERNIE-Speed-128K", messages=[{
                "role": "user",
                "content": prompt
            }])

            end_time = time.time()
            answer = resp["body"]

            response_time = end_time - start_time
            print(f"获取答案时间: {response_time:.2f} 秒")
            pattern = re.compile(r'(解法[一二三四五六七八九十]+：.*?)(?=\n\n解法|$)', re.DOTALL)

            # 查找所有匹配项,并分为列表的各个部分
            matches = pattern.findall(answer["result"])
            # 由于正则表达式可能捕获到额外的换行符或空格，我们需要清理这些字符
            cleaned_matches = [match.strip() for match in matches]
            # 存储解法的列表
            solutions = cleaned_matches
            # 计算解法的数量
            num_solutions = len(solutions)
            print(num_solutions)

            # 保存答案及相关信息
            results.append({
                "question": prompt,
                "answer": solutions,  # 返回的值是列表
                "response": answer,  # 原始回答
                "response_time": response_time,
                "id": ID,
                "num": num_solutions
            })

            # 将结果保存到输出JSON文件
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

input_path = 'question_example.json'
output_path = 'baidu_only_answers_example.json'
baidu1(input_path, output_path)
output_path_2 = "baidu_different_answers_example.json"
baidu2(input_path, output_path_2)

