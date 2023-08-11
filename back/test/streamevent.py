import asyncio
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from chat import get_answer
import time

app = FastAPI()


@app.get("/api/chat/{prompt}")
async def get_chat(request: Request, prompt: str = None):
    print('prompt:', prompt)
    accept = request.headers.get("Accept")
    user_agent = request.headers.get("User-Agent")

    # 处理请求...

    return StreamingResponse(get_answer(prompt), media_type="text/event-stream")


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8000)

