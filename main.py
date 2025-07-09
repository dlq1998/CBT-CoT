import json
from openai import OpenAI
from swarm import Swarm

from CBT_Multi_Agent import (
    # Generation_agent
    Automatic_Thought_Extraction_agent,
    Automatic_Thought_Evaluation_agent,
    CoT_infer_agent,
    Supportive_Response_agent,
    transfer_to_Automatic_Thought_Evaluation_agent,
    transfer_to_CoT_infer_agent,
    transfer_to_Supportive_Response_agent
)

# 加载 OpenAI API 客户端
# aoai_client = OpenAI(api_key="sk-9815b5d0e9a94225855c15cc94c0b0d9",
#                      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
aoai_client = OpenAI(api_key="sk-c684d8d17de243419ab3152d99ff7b61",
                     base_url="https://api.deepseek.com")
# aoai_client = OpenAI(api_key="sk-A9CtQlI6PzZSxoEffAjlEjBASqwzI5fZFxP0gjErwnJ2IE7f",
#                       base_url="https://api.zhiyungpt.com/v1")
# gpt-3.5-turbo
five_o_client = Swarm(aoai_client)

# 读取问题描述数据
with open('data_again/again/unmatched_20000_output.json', 'r', encoding='utf-8') as file:
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
    response = five_o_client.run(agent=Automatic_Thought_Extraction_agent, messages=history_messages, debug=True)
    res = response.messages[-1]["content"]
    history_messages.append({'role': 'assistant', 'content': res})
    print(f'治疗师: {res}')

    # 添加结果
    result_data.append({
        'question': question,
        'description': problem_des,
        'therapist_response': res
    })

    # 每处理 10 条数据就保存一次
    if idx % 5 == 0:
        output_file = 'data_again/A_2/matched_20000_2.json'
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

# 处理最后不足 10 条的数据
if result_data:
    output_file = 'data_again/A_2/matched_20000_2.json'
    try:
        with open(output_file, 'r', encoding='utf-8') as outfile:
            existing_data = json.load(outfile)
    except FileNotFoundError:
        existing_data = []
    combined_data = existing_data + result_data
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(combined_data, outfile, ensure_ascii=False, indent=4)
    print(f"✅ 所有 {len(data)} 条数据已成功保存到文件！")
