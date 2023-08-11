import datetime
import json
import time

import openai
from pydantic import BaseModel

from db import MongoClient
from db import mongo_client, redis_client

openai.api_key = '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'


class chat_content(BaseModel):
    content: str
    chat_id: None | str


async def get_answer(item: chat_content, all_question: list, by_user: str = 'test_user',
                     model: str = 'gpt-3.5-turbo', is_new_chat: bool = False, db=None):
    start_time = time.time()

    # send a ChatCompletion request to count to 100
    response = openai.ChatCompletion.create(
        model=model,
        messages=all_question,
        temperature=0.8,
        stream=True  # again, we set stream=True
    )

    # print(response)

    # create variables to collect the stream of chunks
    collected_chunks = []
    collected_messages = []
    # iterate through the stream of events


    try:
        for chunk in response:
            # print("chunk:", chunk)
            chunk_time = time.time() - start_time  # calculate the time delay of the chunk
            collected_chunks.append(chunk)  # save the event response
            chunk_message = chunk['choices'][0]['delta']  # extract the message
            collected_messages.append(chunk_message)  # save the message
            answer_str = chunk_message.get('content', '')
            # answer_resp = {'msg': answer_str}
            yield f'{answer_str}'

        # print the time delay and text received
        print(f"Full response received {chunk_time:.2f} seconds after request")
        full_reply_content = ''.join([m.get('content', '') for m in collected_messages])

        print(f'cost time: {type(chunk_time)}| {chunk_time}')

        # 将回答存入对话数据库
        mongo_client['tpcosmo']['chat_log'].insert_one(
            {
                'chat_id': item.chat_id,
                'user_content': item.content,
                'got_content': full_reply_content,
                'create_time': str(datetime.datetime.now()),
                'gpt_type': model,
                'by_user': by_user,
                'total_cost_time': chunk_time,
                'total_tokens': 937.5
            }
        )
        # 插入chat_id
        if is_new_chat:
            # 存入数据库
            MongoClient(collection_name='chat_id').insert_data(
                db
            )

        # 更新token消耗
        filter = {
            'openid': by_user
        }
        # 固定一个问题500
        update_data = {"$inc": {"token": -937.5}}

        MongoClient(collection_name='user_base_info').update_data(
            filter, update_data, update_many=True, costumed=True, upsert=False
        )
        # print(f"Full conversation received: {full_reply_content}")
        redis_client.hset('chat:lock_one_time', by_user, json.dumps({'t': int(time.time()), 'is_ok': 1}))
        yield ''

    except:
        # 更新redis
        redis_client.hset('chat:lock_one_time', by_user, json.dumps({'t': int(time.time()), 'is_ok': 1}))
        # print('erro!')
        yield '\n\n<p style="color: darkred;font-weight: bold;">当前服务器繁忙,请重试...</p>'

        # print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")  # print the delay and text
