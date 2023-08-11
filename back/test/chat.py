import openai

openai.api_key = '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'

# 初始化对话历史
dialogue_history = []


# 发送对话请求
def send_dialogue_request(message):
    global dialogue_history

    # 将对话历史和新的用户消息合并为一个字符串
    user_message = 'USER: ' + message
    # dialogue_history.append(user_message)

    # 将对话历史作为输入文本
    # input_text = '\n'.join(dialogue_history)


    # print([input_text])
    # 发送对话请求
    response = openai.Completion.create(
        engine="text-davinci-003",  # 使用 gpt-3.5-turbo 模型
        prompt=user_message,
        max_tokens=500
    )

    print(response)


    # 提取模型生成的回复
    reply = response.choices[0].text.strip()

    # 将模型回复添加到对话历史中
    dialogue_history.append('AI: ' + reply)

    return reply


# 与模型进行对话
while True:
    user_input = input('User: ')
    if user_input.lower() == 'exit':
        break
    response = send_dialogue_request(user_input)
    print('AI:', response)
