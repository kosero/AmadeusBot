import discord

async def kick_user(message, args):
    if not message.author.guild_permissions.kick_members:
        await message.reply("[warn]: No permission")
        return

    if len(args) < 2:
        await message.reply("[warn]: `!kick @user/id`")
        return

    member = None
    if message.mentions:
        member = message.mentions[0]
    else:
        try:
            user_id = int(args[1])
            member = message.guild.get_member(user_id)
        except ValueError:
            await message.reply("[warn]: user id is wrong")
            return

    if not member:
        await message.reply("[warn]: user not found")
        return

    if member == message.author:
        await message.reply("[warn]: you can't kick yourself")
        return
        
    if message.guild.owner_id == member.id:
        await message.reply("[warn]: you can't kick the guild owner")
        return

    if message.author.top_role <= member.top_role:
        await message.reply("[warn]: your permission is not enough to kick this user")
        return
    try:
        await member.kick(reason=f"kicked by {message.author}")
        await message.reply(f"[info]: {member.mention} kicked by {member.author}")
        return
    except discord.Forbidden:
        await message.reply("[warn]: I don't have permission to kick this user")
        return
    except discord.HTTPException as e:
        await message.reply(f"[error]: {e}")
        return

