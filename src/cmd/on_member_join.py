import discord
from discord.ext import commands
from src.cfg.config import GOS_GUILD, GOS_REGISTER_CH, LUM_GUILD, GATE_KEEPER


def welcome_message(member):
    welcome = (
        f"Hos geldin {member}, sunucuya katilman icin bizle biraz sohbet etmelisin.\n"
        "Sunucu herhangi bir kisitlama yoktur ama rahatsizlik vermeyin, gercek hayatta tanimadiginiz insanlara yapilmayacak seyleri burada yapmayi denemeyin kisaca insan olun.\n"
        f"<@&{GATE_KEEPER}> seninle ozenle ilgilenecektir."
    )
    return welcome


class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        steinsgate_guild = self.bot.get_guild(GOS_GUILD)
        lum_guild = self.bot.get_guild(LUM_GUILD)

        if steinsgate_guild:
            if steinsgate_guild.get_member(member.id):
                role = discord.utils.get(member.guild.roles, id=GOS_GUILD)
                await member.add_roles(role)

                register_ch = self.bot.get_channel(GOS_REGISTER_CH)
                if register_ch:
                    await register_ch.send(member.mention, delete_after=5)
                print(f"[info]: {member.name} joins GOS guild")
                return

        if lum_guild:
            if lum_guild.get_member(member.id):
                guild = member.guild
                gate_keeper = guild.get_role(GATE_KEEPER)
                wait_category = discord.utils.get(guild.categories, name="BEKLE!")

                if not wait_category:
                    channel = member.guild.system_channel
                    await channel.send("[error]: category not found")
                    return

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    member: discord.PermissionOverwrite(
                        view_channel=True, send_messages=True
                    ),
                    gate_keeper: discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        embed_links=True,
                        attach_files=True,
                        add_reactions=True,
                    ),
                }
                try:
                    member_ch = await wait_category.create_text_channel(
                        name=member.name, overwrites=overwrites
                    )
                    await member_ch.send(welcome_message(member.mention))
                    embed = discord.Embed(
                        title=f"[user]: {member.mention}!",
                        color=discord.Color.blue(),
                    )
                    embed.set_thumbnail(
                        url=(
                            member.avatar.url
                            if member.avatar
                            else member.default_avatar.url
                        )
                    )
                    embed.add_field(
                        name="Hesap Oluşturulma Tarihi",
                        value=member.created_at.strftime("%d %B %Y"),
                        inline=True,
                    )
                    await member_ch.send(embed=embed)
                    print(f"[info]: {member.name} joins lum guild")
                except discord.Forbidden:
                    print("[error]: No permission")
                except discord.HTTPException as e:
                    print(f"[error]: {e}")
                return


async def setup(bot):
    await bot.add_cog(MemberJoin(bot))
