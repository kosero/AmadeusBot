import discord
from discord.ext import commands
from discord import app_commands


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        if not ctx.author.guild_permissions.ban_members:
            await ctx.reply("[warn]: No permission", delete_after=5)
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.reply(
                "[warn]: Your permission is not enough to ban this user", delete_after=5
            )
            return

        try:
            await member.ban(reason=reason)
            await ctx.reply(
                f"[info]: {member.mention} has been banned by {ctx.author}, reason: {reason if reason else 'No reason provided'}"
            )
        except discord.Forbidden:
            await ctx.reply(
                "[warn]: I don't have permission to ban this user", delete_after=5
            )
        except discord.HTTPException as e:
            await ctx.reply(f"[error]: {e}", delete_after=5)


class SlashBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Ban a member.")
    @app_commands.describe(member="The member to ban", reason="Reason for banning")
    async def slash_ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None,
    ):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(
                "[warn]: No permission", ephemeral=True
            )
            return

        if interaction.user.top_role <= member.top_role:
            await interaction.response.send_message(
                "[warn]: Your permission is not enough to ban this user", ephemeral=True
            )
            return

        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(
                f"[info]: {member.mention} has been banned by {interaction.user}, reason: {reason if reason else 'No reason provided'}"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "[warn]: I don't have permission to ban this user", ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(f"[error]: {e}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Ban(bot))
    await bot.add_cog(SlashBan(bot))
