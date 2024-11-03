import os
import qianfan
import re

# 定义文件路径
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

# 多轮对话
resp = chat_comp.do(model="ERNIE-Speed-128K", messages=[{
    "role": "user",
    "content": "如下有一道题目，请一题多解该题目，每个解之间请用换行符分开：\n已知集合M={x|-4<x<2}，N={x|x^2-x-6< 0}，则M∩N = () A．{x|-4<x<3}	B．{x|-4<x< 2}	C．{x|-2<x<2}	D．{x|2<x<3} "
},
])
answer = resp["body"]
print(answer)

# [\s\S]*?：匹配任意字符（\s匹配空白字符，\S匹配非空白字符，放在一起就是匹配所有字符）*代表零次或多次，但尽可能少地匹配（非贪婪模式，由*?实现）。
# (?=\n\n解法|$)？=是正向前瞻断言，用于表现为直到\n\n解法或着字符串的末尾为止，
# 其中re.dotall用于匹配所有字符，用于转行，也可以匹配
pattern = re.compile(r'(解法[一二三四五六七八九十]+：.*?)(?=\n\n解法|$)', re.DOTALL)

# 查找所有匹配项
matches = pattern.findall(answer["result"])
# 由于正则表达式可能捕获到额外的换行符或空格，我们需要清理这些字符
cleaned_matches = [match.strip() for match in matches]
# 存储解法的列表
solutions = cleaned_matches
# 计算解法的数量
num_solutions = len(solutions)
print(num_solutions)
print(solutions)


