import discord

async def ban_user(message, args):
    if not message.author.guild_permissions.ban_members:
        await message.reply("[warn]: No permission", delete_after=5)
        return

    args = message.content.split()
    if len(args) < 2:
        await message.reply("[warn]: `!ban @user/id [reason]`", delete_after=5)
        return

    user_mention = message.mentions[0] if message.mentions else None
    user_id = args[1] if not user_mention else None
    reason = " ".join(args[2:]) if len(args) > 2 else ""
    user = None

    try:
        if user_mention:
            user = user_mention
        elif user_id and user_id.isdigit():
            user = user_id
        else:
            await message.reply("[warn]: not found user_id", delete_after=5)
            return

        if isinstance(user, discord.Member):
            if message.author.top_role <= user.top_role:
                await message.reply("[warn]: your permission is not enough to ban this user", delete_after=5)
                return

        await message.guild.ban(user, reason=reason)
        await message.reply(f"[info]: {user.mention} kicked by {message.author}, {reason}")

    except discord.Forbidden:
        await message.reply("[warn]: I don't have permission to kick this user", delete_after=5)
    except discord.HTTPException as e:
        await message.reply(f"[error]: {e}", delete_after=5)

