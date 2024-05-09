import json

import httpx
from aiofiles import open as async_open
from database import add_info, put_info, get_info, delete_info, get_info_dialogs, create_dialog
from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    dialogId: int
    message: str
    date: str


class UpdateMessage(BaseModel):
    dialogId: int
    messageId: int
    message: str


API_URL = "https://api-inference.huggingface.co" \
          "/models/deepset/roberta-base-squad2"
headers = {"Authorization": "Bearer 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"}


async def post_history_message(info):

    async with async_open('context.txt', 'r') as file:
        content = await file.read()

    payload = {
        "inputs": {
            "question": info.message,
            "context": content
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_URL, headers=headers, json=payload, timeout=None
        )

    response = Message(
        dialogId=info.dialogId,
        message=response.json()["answer"],
        date=await getDate()
    )

    await add_info(info, True)
    await add_info(response, False)

    return response.json()


async def get_history_dialogs():
    return await get_info_dialogs()


async def getDate():
    current_time = datetime.now()
    result_date = current_time.strftime('%a %b %d %Y %H:%M:%S GMT%z')

    return result_date


async def put_history_message(info):
    await put_info(info)

    return json.dumps({"response": "success put"})


async def get_history_message(dialogId: int):
    history = await get_info(dialogId)

    if history:
        return [
            {
                "dialogId": row[0],
                "message": row[1],
                "date": row[2],
                "state": row[3],
                "messageId": row[4]
            } for row in history
        ]
    else:
        return []


async def delete_history_message(dialogId):
    await delete_info(dialogId)

    return json.dumps({"response": "success deleted"})


async def create_new_dialog():
    await create_dialog()
