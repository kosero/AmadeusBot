import json
from characterai import aiocai
from src.cmd.webhook import send_webhook_message
from src.utils import chg_json_var

###################
#    VARiABLES    #
###################
with open('config/config.json', 'r') as file:
    config = json.load(file)

CAI_CHAT_ID = config["CAI_CHAT_ID"]
CAI_TOKEN = config["CAI_TOKEN"]

cai_client = aiocai.Client(CAI_TOKEN)
char = "NbOISAxpDy88mPv7YB-PfHFwNzVcZv0GDA2OlcWgeZY"

async def create_new_chat(char):
    me = await cai_client.get_me()

    async with await cai_client.connect() as chat:
        new, answer = await chat.new_chat(char, me.id)
        print(f'[info]. Chat ID: {new.chat_id}')
        return new.chat_id

async def send_cai(text, char, chat_id):
    async with await cai_client.connect() as chat:
        message = await chat.send_message(char, chat_id, text)
        return message.text

async def kurisu_ch(message):
    if message.content.startswith("!RESET"):
        chat_id = await create_new_chat(char)
        chg_json_var("config/config.json", "CAI_CHAT_ID", chat_id)
        global CAI_CHAT_ID
        CAI_CHAT_ID = chat_id
        await message.reply("[ok]")
        return
    else:
        await message.channel.typing()
        message_makise = await send_cai(message.content, char, CAI_CHAT_ID)
        await send_webhook_message("custom", message.channel, message_makise, custom_avatar="https://i.pinimg.com/736x/86/60/53/86605345b8bc58bfb34151e9e0229196.jpg", custom_name="Makise Kurisu")

