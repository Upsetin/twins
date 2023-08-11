import aiohttp
import asyncio
import json

async def get_answer_async(prompt: str='请用python写一个冒泡排序', model: str='gpt-3.5-turbo'):
    url = "http://api.openai.com/v1/engines/{}/completions".format(model)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 60
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as resp:
            response_data = await resp.text()
            print(response_data)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_answer_async())
