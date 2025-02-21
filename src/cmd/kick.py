import discord
from discord.ext import commands
from discord import app_commands


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        if not ctx.author.guild_permissions.kick_members:
            await ctx.reply("[warn]: No permission", delete_after=5)
            return

        if member == ctx.author:
            await ctx.reply("[warn]: You can't kick yourself", delete_after=5)
            return

        if ctx.guild.owner_id == member.id:
            await ctx.reply("[warn]: You can't kick the guild owner", delete_after=5)
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.reply(
                "[warn]: Your permission is not enough to kick this user",
                delete_after=5,
            )
            return

        try:
            await member.kick(reason=reason)
            await ctx.reply(
                f"[info]: {member.mention} has been kicked by {ctx.author}, reason: {reason if reason else 'No reason provided'}"
            )
        except discord.Forbidden:
            await ctx.reply(
                "[warn]: I don't have permission to kick this user", delete_after=5
            )
        except discord.HTTPException as e:
            await ctx.reply(f"[error]: {e}", delete_after=5)


class SlashKick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a member.")
    @app_commands.describe(member="The member to kick", reason="Reason for kicking")
    async def slash_kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None,
    ):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message(
                "[warn]: No permission", ephemeral=True
            )
            return

        if member == interaction.user:
            await interaction.response.send_message(
                "[warn]: You can't kick yourself", ephemeral=True
            )
            return

        if interaction.guild.owner_id == member.id:
            await interaction.response.send_message(
                "[warn]: You can't kick the guild owner", ephemeral=True
            )
            return

        if interaction.user.top_role <= member.top_role:
            await interaction.response.send_message(
                "[warn]: Your permission is not enough to kick this user",
                ephemeral=True,
            )
            return

        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(
                f"[info]: {member.mention} has been kicked by {interaction.user}, reason: {reason if reason else 'No reason provided'}"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "[warn]: I don't have permission to kick this user", ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(f"[error]: {e}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Kick(bot))
    await bot.add_cog(SlashKick(bot))
