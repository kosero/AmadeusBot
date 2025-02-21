import json
from characterai import aiocai

###################
#    VARiABLES    #
###################
with open("config/config.json", "r") as file:
    config = json.load(file)

CAI_TOKEN = config["CAI_TOKEN"]

cai_client = aiocai.Client(CAI_TOKEN)


async def create_new_chat(char):
    me = await cai_client.get_me()

    async with await cai_client.connect() as chat:
        new, answer = await chat.new_chat(char, me.id)
        print(f"[info]. Chat ID: {new.chat_id}")
        return new.chat_id


async def send_cai(text, char, chat_id):
    async with await cai_client.connect() as chat:
        message = await chat.send_message(char, chat_id, text)
        return message.text
