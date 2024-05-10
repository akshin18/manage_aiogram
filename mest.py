import asyncio
from pyrogram import Client

api_id = 27283285
api_hash = "ea73d6f98e659d572f7fe7aa02c13d66"


async def main():
    async with Client("my_account", api_id, api_hash) as app:
        async for i in app.get_dialogs():
            chat_id = i.chat.id
            look_for = -1002109637757
            data = []
            if chat_id == look_for:
                # a = await app.get_chat(chat_id)
                async for topic in app.get_forum_topics(chat_id):
                    data.append([topic.name,topic.message_thread_id,look_for])
                print(data)


asyncio.run(main())
