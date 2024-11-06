import requests
import json
import time
import re
import os
import sys



# 读取凭证文件
credentials_file_path = '../aliyun_secret.txt'
credentials = {}
with open(credentials_file_path, 'r') as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, value = line.split('=', 1)
        credentials[key] = value

API_KEY = credentials.get('ALIYUN_API_KEY')
print("1",API_KEY)


url = "https://api.siliconflow.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def aliyun1(input_json_path, output_json_path):
    results = []
    
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        questions = data["math_question"]

    for question_item in questions:
        description_list = question_item["Description"]
        ID = question_item.get("id")

        for item in description_list:
            prompt = "如下是完整的题目，如果是选择题和填空题，请只给出答案 \n" + item['Qu'] + "如上是完整的题目，请只给出答案，不需要分析 \n"

            print(f"\n提问: {prompt}")
            start_time = time.time()

            payload = {
                "messages": [{"role": "user", "content": prompt}],
                "model": "Qwen/Qwen2.5-7B-Instruct"
            }

            response = requests.request("POST", url, json=payload, headers=headers)   
            response_json = json.loads(response.text)  # 解析JSON响应
            answer = response_json['choices'][0]['message']['content']  # 获取content内容
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

def aliyun2(input_json_path, output_json_path):
    results = []

    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        questions = data.get("math_question", [])

    for question_item in questions:
        description_list = question_item.get("Description", [])
        ID = question_item.get("id")

        for item in description_list:
            prompt = "如下有一道题目，请一题多解该题目，每个解之间请用换行符分开,并在开头注明解法几：\n" + item['Qu']

            print(f"\n提问: {prompt}")
            start_time = time.time()

            payload = {
                "messages": [{"role": "user", "content": prompt}],
                "model": "Qwen/Qwen2.5-7B-Instruct"
            }

            response = requests.request("POST", url, json=payload, headers=headers)   
            response_json = json.loads(response.text)  # 解析JSON响应
            answer = response_json['choices'][0]['message']['content']  # 获取content内容
            end_time = time.time()           
            response_time = end_time - start_time

            # 修改正则表达式以匹配更多格式的解法标记
            pattern = re.compile(r'([#\s]*解法[一二三四五六七八九十]+[：:]\s*.*?)(?=\n\n[#\s]*解法|$)', re.DOTALL)
            matches = pattern.findall(answer)
            cleaned_matches = [match.strip() for match in matches]
            solutions = cleaned_matches
            num_solutions = len(solutions)

            results.append({
                "question": prompt,
                "answer": solutions,
                "response": answer,
                "response_time": response_time,
                "id": ID,
                "num": num_solutions
            })

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

# 主程序执行
if __name__ == "__main__":
    input_path = 'question_example.json'
    output_path = 'aliyun_only_answers_example.json'
    output_path_2 = "aliyun_different_answers_example.json"
    
    aliyun1(input_path, output_path)
    aliyun2(input_path, output_path_2)