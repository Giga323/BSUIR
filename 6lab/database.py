import json

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="lab6EYAZIS",
    user="postgres",
    password="postgres1"
)


async def get_info_dialogs():
    cursor = conn.cursor()

    cursor.execute(
        "select * from dialogs"
    )
    indexes = cursor.fetchall()
    cursor.close()

    return [{"dialogId": index[0]} for index in indexes]


async def add_info(info, state):
    cursor = conn.cursor()
    dialogId = info.dialogId
    message = info.message
    date = info.date

    cursor.execute(
        "INSERT INTO history (dialogId, message, date, state)" +
        "VALUES (%s, %s, %s, %s)",
        (dialogId, message, date, state)
    )

    conn.commit()
    cursor.close()


async def put_info(info):
    cursor = conn.cursor()

    dialogId = info.dialogId
    messageId = info.messageId
    message = info.message

    cursor.execute(
        "UPDATE history SET message = (%s) WHERE dialogId = (%s) AND messageId = (%s)",
        (message, dialogId, messageId)
    )

    conn.commit()
    cursor.close()


async def get_info(dialogId):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM history WHERE history.dialogId = (%s)",
        (dialogId,)
    )
    info = cursor.fetchall()

    conn.commit()
    cursor.close()

    if len(info) == 0:
        info = []

    return info


async def delete_info(dialogId):
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM history WHERE history.dialogId = (%s)",
        (dialogId,)
    )

    conn.commit()
    cursor.close()


async def create_dialog():
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO dialogs DEFAULT VALUES RETURNING dialogId;"
    )

    conn.commit()
    cursor.close()
