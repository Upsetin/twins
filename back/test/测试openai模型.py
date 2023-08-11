import time

import openai

openai.api_key = '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'

import openai

start_time = time.time()


# 写作
response = openai.Completion.create(
  model="text-davinci-003",
  prompt="帮我用python写一个贪吃蛇游戏",
  max_tokens=300
)


print(response)
generated_text = response.choices[0].text
print(generated_text)

print(f'cost time: {time.time() - start_time}s')

