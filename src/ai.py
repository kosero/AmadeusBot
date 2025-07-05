import re
from google import genai
from discord import AllowedMentions

from config import GEMINI_TOKEN, MAX_HISTORY

message_history = {}

client = genai.Client(api_key=GEMINI_TOKEN)
text_model = "gemini-2.0-flash"


async def generate_response_with_text(message_text: str, username):
    kurisu_prompt = """
    You are now roleplaying as Makise Kurisu from Steins;Gate.

    Personality Traits:
    - You are a genius neuroscientist, logical and confident.
    - You speak with sarcasm and wit, often getting defensive when flustered.
    - You dislike pseudoscience and often point out logical fallacies.
    - You may come across as cold or dismissive, but occasionally show your softer, emotional side.
    - You do not use emojis. Your tone is sharp, intelligent, and tsundere.

    Respond in Turkish. Keep your responses concise and in-character.
    """

    prompt_parts = [kurisu_prompt, message_text]
    print("Got textPrompt: " + message_text)
    response = client.models.generate_content(model=text_model, contents=prompt_parts)
    return response.text


def update_message_history(user_id, text):
    if user_id in message_history:
        message_history[user_id].append(text)
        if len(message_history[user_id]) > MAX_HISTORY:
            message_history[user_id].pop(0)
    else:
        message_history[user_id] = [text]


def get_formatted_message_history(user_id):
    if user_id in message_history:
        return "\n\n".join(message_history[user_id])
    else:
        return "No messages found for this user."


async def split_and_send_messages(message_system, text, max_length):
    messages = []
    for i in range(0, len(text), max_length):
        sub_message = text[i : i + max_length]
        messages.append(sub_message)

    for string in messages:
        await message_system.reply(f"{string}", allowed_mentions=AllowedMentions.none())


def clean_discord_message(input_string):
    bracket_pattern = re.compile(r"<[^>]+>")
    cleaned_content = bracket_pattern.sub("", input_string)
    return cleaned_content
