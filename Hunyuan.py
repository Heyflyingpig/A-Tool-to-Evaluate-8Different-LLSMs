import json
import types
import os
import time
import re
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models


cred = credential.Credential(
    os.environ.get("TENCENTCLOUD_SECRET_ID"),
    os.environ.get("TENCENTCLOUD_SECRET_KEY")
)
# 读取 JSON 文件
A = "请一题多解该题：\n"  # 对于无法一题多解的情况
B = "你是一个准备高考的优秀高中生，掌握了很多高中知识，在考场上你遇到了如下这道题： \n "  # 模拟情景，不同的prompt
C = "你是一个数学家，你掌握了很多知识与公式定理，你将解决如下这道题: \n"
D = ""
def hunyuan1(input_json,output_json):
    results = []


    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        questions = data["math_question"]
    for question_item in questions:
        description_list = question_item["Description"]
        ID = question_item["id"]
        for item in description_list:
                prompt = item['Qu'] + "\n 如上是完整的题目，请只给出答案，不需要分析 \n"

                picture = item.get('picture')
                print(f"\n提问: {prompt}")

                start_time = time.time()

                # 指定特定模型
                try:
                    # 实例化一个http选项，可选的，没有特殊需求可以跳过
                    httpProfile = HttpProfile()
                    httpProfile.endpoint = "hunyuan.tencentcloudapi.com"

                    # 实例化一个client选项，可选的，没有特殊需求可以跳过
                    clientProfile = ClientProfile()
                    clientProfile.httpProfile = httpProfile
                    # 实例化要请求产品的client对象,clientProfile是可选的
                    client = hunyuan_client.HunyuanClient(cred, "", clientProfile)

                    # 实例化一个请求对象,每个接口都会对应一个request对象
                    req = models.ChatCompletionsRequest()
                    params = {
                        "Model": "hunyuan-lite",
                        "Messages": [
                            {
                                "Role": "user",
                                "Content": prompt
                            }
                        ]
                    }
                    req.from_json_string(json.dumps(params))

                    # 返回的resp是一个ChatCompletionsResponse的实例，与请求对象对应
                    resp = client.ChatCompletions(req)# 输出json格式的字符串回包
                    resp_json_str = resp.to_json_string()  #
                    print(resp)
                except TencentCloudSDKException as err:
                    print(err)
        end_time = time.time()
        response_time = end_time - start_time
        print(f"获取答案时间: {response_time:.2f} 秒")  # f-string ，：代表的是格式化指令的开始，2f代表用两位小数表达，而不用科学计数法

        # 将JSON字符串解析为Python字典
        response_dict = json.loads(resp_json_str)
        # 提取Choices数组中的第一个对象
        choice = response_dict.get('Choices', [])[0]
        # 提取Message对象
        message = choice.get('Message', {})
        # 获取Content字段的值
        answer = message.get('Content')

        results.append({
                "question": prompt,
                "answer": answer,
                "response_time": response_time,  # 保存获取答案的时间
                "id": ID
            })  # 保存答案

        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)


def hunyuan2(input_json, output_json):
    results = []

    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        questions = data["math_question"]
    for question_item in questions:
        description_list = question_item["Description"]
        ID = question_item["id"]
        for item in description_list:
            prompt = "如下有一道题目，请一题多解该题目，每个解之间请用换行符分开：\n" + item['Qu']

            picture = item.get('picture')
            print(f"\n提问: {prompt}")

            start_time = time.time()

            # 指定特定模型
            try:
                # 实例化一个http选项，可选的，没有特殊需求可以跳过
                httpProfile = HttpProfile()
                httpProfile.endpoint = "hunyuan.tencentcloudapi.com"

                # 实例化一个client选项，可选的，没有特殊需求可以跳过
                clientProfile = ClientProfile()
                clientProfile.httpProfile = httpProfile
                # 实例化要请求产品的client对象,clientProfile是可选的
                client = hunyuan_client.HunyuanClient(cred, "", clientProfile)

                # 实例化一个请求对象,每个接口都会对应一个request对象
                req = models.ChatCompletionsRequest()
                params = {
                    "Model": "hunyuan-lite",
                    "Messages": [
                        {
                            "Role": "user",
                            "Content": prompt
                        }
                    ]
                }
                req.from_json_string(json.dumps(params))

                # 返回的resp是一个ChatCompletionsResponse的实例，与请求对象对应
                resp = client.ChatCompletions(req)  # 输出json格式的字符串回包
                resp_json_str = resp.to_json_string()  #
                print(resp)
            except TencentCloudSDKException as err:
                print(err)
        end_time = time.time()
        response_time = end_time - start_time

        print(f"获取答案时间: {response_time:.2f} 秒")  # f-string ，：代表的是格式化指令的开始，2f代表用两位小数表达，而不用科学计数法

        # 将JSON字符串解析为Python字典
        response_dict = json.loads(resp_json_str)
        # 提取Choices数组中的第一个对象
        choice = response_dict.get('Choices', [])[0]
        # 提取Message对象
        message = choice.get('Message', {})
        # 获取Content字段的值
        answer = message.get('Content')
        pattern = re.compile(r'(解法[一二三四五六七八九十]+：.*?)(?=\n\n解法|$)', re.DOTALL)

        # 查找所有匹配项,并分为列表的各个部分
        matches = pattern.findall(answer)
        # 由于正则表达式可能捕获到额外的换行符或空格，我们需要清理这些字符
        cleaned_matches = [match.strip() for match in matches]
        # 存储解法的列表
        solutions = cleaned_matches
        # 计算解法的数量
        num_solutions = len(solutions)
        print(num_solutions)
        results.append({
            "question": prompt,
            "answer": solutions,  # 返回的值是列表
            "response": answer,  # 原始回答
            "response_time": response_time,
            "id": ID,
            "num": num_solutions
        })

        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

input = 'question_example.json'
output_1 = 'hunyuan_only_answers_example.json'
output_2 = "hunyuan_different_answers_example.json"
hunyuan1(input, output_1)
hunyuan2(input, output_2)
