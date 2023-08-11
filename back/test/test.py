import asyncio
import time

import httpx
import openai
import redis
from loguru import logger

openai.api_key = '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'  # 替换为你的 OpenAI API 密钥
openai.api_base = 'http://bitorgin.cn/v1'


async def ask_question(question: str):

    response = await openai.ChatCompletion.acreate(
        # engine="text-davinci-003",  # 使用 gpt-3.5-turbo 模型
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
            # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            # {"role": "user", "content": "Where was it played?"}
        ],
        max_tokens=300
    )

    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=messages,
    #     max_tokens=300,
    #     n=1,
    #     stop=None,
    #     temperature=0.7,
    # )

    print(response)

    return response["choices"][0]["message"]['content']


if __name__ == '__main__':
    start_time = time.time()
    r = asyncio.run(ask_question("网易为什么这么赚钱"))

    print(r)
    print(f'cost time: {round(time.time() - start_time, 2)}')

