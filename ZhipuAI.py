from zhipuai import ZhipuAI
import json
import time
import re

credentials_file_path = '../zhipu_secret.txt'

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

# 初始化客户端
client = ZhipuAI(api_key=credentials.get('zhipu_API'))  # 需要填入你的 API Key

# 定义提示语
A = "请一题多解该题：\n"
B = "你是一个准备高考的优秀高中生，掌握了很多高中知识，在考场上你遇到了如下这道题： \n "
C = "你是一个数学家，你掌握了很多知识与公式定理，你将解决如下这道题: \n"
D = ""

def zhipu1(input_json_path, output_json_path):
    results = []
    
    # 读取输入JSON文件
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        questions = data["math_question"]

    for question_item in questions:
        description_list = question_item["Description"]
        ID = question_item.get("id")

        for item in description_list:
            prompt = "如下是完整的题目，如果是选择题和填空题，请只给出答案 \n" + item['Qu'] + "如上是完整的题目，请只给出答案，不需要分析 \n"
            
            picture = item.get('picture')
            print(f"\n提问: {prompt}")

            start_time = time.time()
            response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[{"role": "user", "content": prompt}]
            )
            
            answer = response.choices[0].message.content
            end_time = time.time()
            response_time = end_time - start_time
            print(f"获取答案时间: {response_time:.2f} 秒")

            results.append({
                "question": prompt,
                "answer": answer,
                "response_time": response_time,
                "id": ID
            })

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def zhipu2(input_json_path, output_json_path):
    results = []
    
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        questions = data.get("math_question", [])

    for question_item in questions:
        description_list = question_item.get("Description", [])
        ID = question_item.get("id")

        for item in description_list:
            prompt = "如下有一道题目，请一题多解该题目，每个解之间请用换行符分开,并在开头注明解法几：\n"+ item['Qu']
            
            picture = item.get('picture')
            print(f"\n提问: {prompt}")

            start_time = time.time()
            response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[{"role": "user", "content": prompt}]
            )
            
            answer = response.choices[0].message.content
            end_time = time.time()
            response_time = end_time - start_time
            
            # 使用相同的正则表达式解析多个解法
            pattern = re.compile(r'(解法[一二三四五六七八九十]+：.*?)(?=\n\n解法|$)', re.DOTALL)
            matches = pattern.findall(answer)
            cleaned_matches = [match.strip() for match in matches]
            num_solutions = len(cleaned_matches)

            results.append({
                "question": prompt,
                "answer": cleaned_matches,
                "response": answer,
                "response_time": response_time,
                "id": ID,
                "num": num_solutions
            })

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

# 调用函数
input_path = 'question_example.json'
output_path = 'zhipu_only_answers_example.json'
output_path_2 = "zhipu_different_answers_example.json"

zhipu1(input_path, output_path)
zhipu2(input_path, output_path_2)