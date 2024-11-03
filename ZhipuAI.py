from zhipuai import ZhipuAI
import json
import time
client = ZhipuAI(api_key="")  # API Key49520ba1c63a183b4c6333b4b4d523fe.9C6LVcy8IPz80pyf
results = []
# 读取 JSON 文件
A = "请一题多解该题：\n"  # 对于无法一题多解的情况
B = "你是一个准备高考的优秀高中生，掌握了很多高中知识，在考场上你遇到了如下这道题： \n "  # 模拟情景，不同的prompt
C = "你是一个数学家，你掌握了很多知识与公式定理，你将解决如下这道题: \n"
D = ""

with open('question_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    questions = data["math_question"]

for question_item in questions:
    description_list = question_item["Description"]
    for item in description_list:
            prompt = item['Qu']
            picture = item.get('picture')
            print(f"\n提问: {prompt}")

            start_time = time.time()
            response = client.chat.completions.create(
                model="glm-4",  # 模型名称
                messages=[
                    {"role": "user", "content": prompt}
                ],

            )

    answer = response.choices[0].message.content  # 只获取回答
    end_time = time.time()
    print("\nZhipuAI:", answer)

    response_time = end_time - start_time
    print(f"获取答案时间: {response_time:.2f} 秒")

    results.append({
        "question": prompt,
        "answer": answer,
        "response_time": response_time,  # 保存获取答案的时间
    })  # 保存答案

# 将结果保存为 JSON 文件
with open('answers.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)