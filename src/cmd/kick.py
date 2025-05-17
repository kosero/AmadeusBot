import discord
from discord.ext import commands
from discord import app_commands


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _has_permission(self, user):
        return user.guild_permissions.kick_members

    async def _can_kick(self, actor, member, guild):
        if member == actor:
            return False, "[warn]: You can't kick yourself"
        if member.id == guild.owner_id:
            return False, "[warn]: You can't kick the guild owner"
        if actor.top_role <= member.top_role:
            return False, "[warn]: Your permission is not enough to kick this user"
        return True, None

    async def _kick_member(self, actor, member, reason, guild):
        can_kick, error_message = await self._can_kick(actor, member, guild)
        if not can_kick:
            return False, error_message

        try:
            await member.kick(reason=reason)
            return (
                True,
                f"[info]: {member.mention} has been kicked by {actor}, reason: {reason or 'No reason provided'}",
            )
        except discord.Forbidden:
            return False, "[warn]: I don't have permission to kick this user"
        except discord.HTTPException as e:
            return False, f"[error]: {e}"

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        if not await self._has_permission(ctx.author):
            await ctx.reply("[warn]: No permission", delete_after=5)
            return

        success, message = await self._kick_member(
            ctx.author, member, reason, ctx.guild
        )
        await ctx.reply(message, delete_after=5 if not success else None)

    @app_commands.command(name="kick", description="Kick a member.")
    @app_commands.describe(member="The member to kick", reason="Reason for kicking")
    async def slash_kick(
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

        success, message = await self._kick_member(
            interaction.user, member, reason, interaction.guild
        )
        await interaction.response.send_message(message, ephemeral=not success)


async def setup(bot):
    await bot.add_cog(Kick(bot))
