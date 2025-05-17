import discord
from discord.ext import commands
from discord import app_commands


class MessagePurge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _purge_messages(self, channel: discord.TextChannel, count: int):
        return await channel.purge(limit=count + 1)

    def _has_permission(self, perms: discord.Permissions) -> bool:
        return perms.manage_messages

    @commands.command()
    async def purge(self, ctx: commands.Context, count: int = 0):
        if not self._has_permission(ctx.channel.permissions_for(ctx.author)):
            await ctx.reply("[warn]: No permission", delete_after=5)
            return

        if not 1 <= count <= 100:
            await ctx.reply("[warn]: `!purge 1-100`", delete_after=5)
            return

        deleted = await self._purge_messages(ctx.channel, count)
        await ctx.reply(f"[info]: {len(deleted)} messages deleted", delete_after=5)

    @app_commands.command(
        name="purge", description="Delete a certain number of messages."
    )
    @app_commands.describe(count="The number of messages to delete (1-100).")
    async def slash_purge(self, interaction: discord.Interaction, count: int = 0):
        if not self._has_permission(
            interaction.channel.permissions_for(interaction.user)
        ):
            await interaction.response.send_message(
                "[warn]: No permission", ephemeral=True
            )
            return

        if not 1 <= count <= 100:
            await interaction.response.send_message(
                "[warn]: `/purge 1-100`", ephemeral=True
            )
            return

        deleted = await self._purge_messages(interaction.channel, count)
        await interaction.response.send_message(
            f"[info]: {len(deleted)} messages deleted", ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(MessagePurge(bot))
