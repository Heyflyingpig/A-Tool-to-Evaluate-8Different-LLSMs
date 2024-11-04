doubao = "【答案】\nC"
if "【答案】" in doubao:
    doubao_clear = doubao.strip().split("【答案】")[1].strip()
    print(doubao_clear)
else:
    doubao_clear = doubao.strip()
    print("1")