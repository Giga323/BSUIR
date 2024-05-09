from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from qa_model import post_history_message, put_history_message, get_history_message,\
    delete_history_message, UpdateMessage , Message, get_history_dialogs, create_new_dialog
from uvicorn import run


app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/answer")
async def post_message(info: Message):
    return await post_history_message(info)


@app.post("/createDialog")
async def create_dialog():
    return await create_new_dialog()


@app.get("/getDialogs")
async def get_dialogs():
    return await get_history_dialogs()


@app.put("/history/put")
async def put_message(info: UpdateMessage):
    return await put_history_message(info)


@app.get("/history/get/{dialogId:int}")
async def get_dialog(dialogId: int):
    return await get_history_message(dialogId)


@app.delete("/history/delete/{dialogId:int}")
async def delete_dialog(dialogId: int):
    return await delete_history_message(dialogId)


if __name__ == '__main__':
    run(app, host="0.0.0.0", port=5000)

