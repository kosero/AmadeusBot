import discord
from discord.ext import commands
from discord import app_commands


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _has_permission(self, user):
        return user.guild_permissions.ban_members

    async def _can_ban(self, actor, target):
        return actor.top_role > target.top_role

    async def _ban_member(self, guild_actor, member, reason):
        try:
            await member.ban(reason=reason)
            return (
                True,
                f"[info]: {member.mention} has been banned by {guild_actor}, reason: {reason or 'No reason provided'}",
            )
        except discord.Forbidden:
            return False, "[warn]: I don't have permission to ban this user"
        except discord.HTTPException as e:
            return False, f"[error]: {e}"

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        if not await self._has_permission(ctx.author):
            await ctx.reply("[warn]: No permission", delete_after=5)
            return

        if not await self._can_ban(ctx.author, member):
            await ctx.reply(
                "[warn]: Your permission is not enough to ban this user", delete_after=5
            )
            return

        success, message = await self._ban_member(ctx.author, member, reason)
        await ctx.reply(message, delete_after=5 if not success else None)

    @app_commands.command(name="ban", description="Ban a member.")
    @app_commands.describe(member="The member to ban", reason="Reason for banning")
    async def slash_ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None,
    ):
        if not await self._has_permission(interaction.user):
            await interaction.response.send_message(
                "[warn]: No permission", ephemeral=True
            )
            return

        if not await self._can_ban(interaction.user, member):
            await interaction.response.send_message(
                "[warn]: Your permission is not enough to ban this user", ephemeral=True
            )
            return

        success, message = await self._ban_member(interaction.user, member, reason)
        await interaction.response.send_message(message, ephemeral=not success)


async def setup(bot):
    await bot.add_cog(Ban(bot))
