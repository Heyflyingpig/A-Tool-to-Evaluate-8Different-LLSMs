from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import json
import time
import re
#星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看

credentials_file_path = '../doubao_secret.txt'
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
SPARKAI_APP_ID = credentials.get('APPID')
SPARKAI_API_SECRET = credentials.get('APISecret')
SPARKAI_API_KEY = credentials.get('APIKey')
SPARKAI_DOMAIN = 'lite'


def doubao_1(input_json_path, output_json_path):
    results = []

    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        questions = data["math_question"]

        # 遍历问题列表
    for question_item in questions:
        description_list = question_item["Description"]
        ID = question_item.get("id")

        for item in description_list:
            prompt = "如下是完整的题目，如果是选择题和填空题，请只给出答案 \n" + item['Qu']+"\n如上是完整的题目，如果是选择题和填空题，请只给出答案，不需要分析"

            picture = item.get('picture')
            print(f"\n提问: {prompt}")

            start_time = time.time()

            if __name__ == '__main__':
                spark = ChatSparkLLM(
                    spark_api_url=SPARKAI_URL,
                    spark_app_id=SPARKAI_APP_ID,
                    spark_api_key=SPARKAI_API_KEY,
                    spark_api_secret=SPARKAI_API_SECRET,
                    spark_llm_domain=SPARKAI_DOMAIN,
                    streaming=False,
                )
                messages = [ChatMessage(
                    role="user",
                    content=prompt
                )]
                handler = ChunkPrintHandler()
                a = spark.generate([messages])
                answers = a.generations[0][0].text
            print(answers)
            end_time = time.time()
            response_time = end_time - start_time
            print(f"获取答案时间: {response_time:.2f} 秒")

            # 保存答案及相关信息
            results.append({
                "question": prompt,
                "answer": answers,
                "response_time": response_time,
                "id": ID
            })

            # 将结果保存到输出JSON文件
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


def doubao_2(input_json_path, output_json_path):
    results = []

    # 读取输入JSON文件
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        questions = data.get("math_question", [])

        # 遍历问题列表
    for question_item in questions:
        description_list = question_item.get("Description", [])
        ID = question_item.get("id")

        for item in description_list:
            prompt = "如下有一道题目，请一题多解该题目，每个解之间请用换行符分开,并在开头注明解法几：\n" + item['Qu'] + "如上有一道题目，请一题多解该题目，每个解之间请用换行符分开,并在开头注明解法几：\n"

            picture = item.get('picture')
            print(f"\n提问: {prompt}")

            start_time = time.time()

            # 与模型交互获取答案
            if __name__ == '__main__':
                spark = ChatSparkLLM(
                    spark_api_url=SPARKAI_URL,
                    spark_app_id=SPARKAI_APP_ID,
                    spark_api_key=SPARKAI_API_KEY,
                    spark_api_secret=SPARKAI_API_SECRET,
                    spark_llm_domain=SPARKAI_DOMAIN,
                    streaming=False,
                )
                messages = [ChatMessage(
                    role="user",
                    content=prompt
                )]
                handler = ChunkPrintHandler()
                a = spark.generate([messages])
                answers = a.generations[0][0].text

            end_time = time.time()

            response_time = end_time - start_time
            print(f"获取答案时间: {response_time:.2f} 秒")
            pattern = re.compile(r'(解法[123456789一二三四五六七八九十]+：.*?)(?=\n\n解法|$)', re.DOTALL)

            # 查找所有匹配项,并分为列表的各个部分
            matches = pattern.findall(answers)
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
                "response": answers,  # 原始回答
                "response_time": response_time,
                "id": ID,
                "num": num_solutions
            })

            # 将结果保存到输出JSON文件
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


input_path = 'question_example.json'
output_path = 'Doubao_only_answers_example.json'
#doubao_1(input_path, output_path)
output_path_2 = "Doubao_different_answers_example.json"
doubao_2(input_path, output_path_2)
