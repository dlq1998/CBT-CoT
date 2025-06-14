import json
from openai import OpenAI
from swarm import Swarm
from CBT_Multi_Agent import (
    Three_Column_agent,
)

# 加载 OpenAI API 客户端
aoai_client = OpenAI(api_key="sk-b5cfe6e7699648bfa87eb0e17f96df10",
                     base_url="https://api.deepseek.com")
five_o_client = Swarm(aoai_client)

# 读取问题描述数据
with open('prompt/sampled_180.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 存储所有结果的列表
result_data = []

# 循环处理每个问题和描述
for idx, item in enumerate(data, 1):
    problem_des = item['description']
    question = item['question']

    print(f"\n第{idx}条")
    print(f"问题: {question}")
    print(f"描述: {problem_des}")

    # 初始化对话历史
    history_messages = []

    # 构造用户的初始发言
    initial_statement = f"问题: [{question}]，描述: [{problem_des}]"
    history_messages.append({'role': 'user', 'content': initial_statement})
    print(f'用户: {initial_statement}')

    # 由 inspector_agent 处理
    response = five_o_client.run(agent=Three_Column_agent, messages=history_messages, debug=True)
    res = response.messages[-1]["content"]
    history_messages.append({'role': 'assistant', 'content': res})
    print(f'治疗师: {res}')

    # 添加结果
    result_data.append({
        'question': question,
        'description': problem_des,
        'therapist_response': res
    })

    # 每处理 5 条数据就保存一次
    if idx % 5 == 0:
        output_file = 'data/A/sampled_180.json'
        try:
            # 尝试读取现有文件内容
            with open(output_file, 'r', encoding='utf-8') as outfile:
                existing_data = json.load(outfile)
        except FileNotFoundError:
            # 如果文件不存在，初始化为空列表
            existing_data = []
        # 合并现有数据和新结果
        combined_data = existing_data + result_data
        # 将合并后的数据写回文件
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(combined_data, outfile, ensure_ascii=False, indent=4)
        print(f"✅ 前 {idx} 条数据已成功保存到文件！")
        # 清空结果列表，为下一批 10 条数据做准备
        result_data = []

# 处理最后不足 5 条的数据
if result_data:
    output_file = 'data/A/sampled_180.json'
    try:
        with open(output_file, 'r', encoding='utf-8') as outfile:
            existing_data = json.load(outfile)
    except FileNotFoundError:
        existing_data = []
    combined_data = existing_data + result_data
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(combined_data, outfile, ensure_ascii=False, indent=4)
    print(f"✅ 所有 {len(data)} 条数据已成功保存到文件！")
