from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
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
        content='你好呀'
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages])
print(a.generations[0][0].text)
