import discord

async def message_purge(message, args):
    if message.channel.permissions_for(message.author).manage_messages:
        args = message.content.split()
        count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 0
        if count < 1 or count > 100:
            await message.reply("[warn]: `!purge 1-100`", delete_after=5)
            return
        deleted = await message.channel.purge(limit=count + 1)
        await message.channel.send(f"[info]: {len(deleted)} messages deleted", delete_after=5)
    else:
        await message.reply("[warn]: No permission", delete_after=5)
        return

