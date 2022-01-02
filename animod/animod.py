import discord
from redbot.core import commands

class AniMod(commands.Cog):
    """Commands for A&I Server"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role(878240352857886731)
    async def verify(self, ctx: commands.Context, member: discord.Member):
        """Assigns `@Initiate` role to new member"""
        import random
        greeting = (
            f"{member.mention} just joined the server!",
            f"I've been expecting you, {member.mention}.",
            f"I know why you're here {member.mention}.",
            f"Guys, we have fresh blood! Welcome {member.mention}!",
            f"Alright, {member.mention} youre in!",
            f"{member.mention} has completed verification! Nice.",
            f"So, are we just going to sit down and pretend that {member.mention} hasn't joined us?",
            f"{member.mention} is at least 20% cooler now that they're here.",
            f"Welcome, {member.mention}! Please take a look around.",
            f"Guys, say hello to my new friend {member.mention}!"
        )
        role = ctx.guild.get_role(487854898692489227)
        if role in member.roles:
            return await ctx.send(f"{member.mention} is already verified!")
        await member.add_roles(role)
        await ctx.tick()
        return await ctx.guild.get_channel(684822519865147403).send(random.choice(greeting))

    @commands.command(pass_context=True)
    @commands.has_role(878240352857886731)
    async def grad(self, ctx: commands.Context, member: discord.Member):
        """Assigns `@Alumnli` and `@Master` roles to grads!"""
        alumn  = ctx.guild.get_role(657056079926001686)
        master = ctx.guild.get_role(546873124944216075)
        await member.add_roles(alumn, master)
        await ctx.tick()
        return await ctx.guild.get_channel(749397281924448326).send(f"{member.mention} is an alumn now! Congrats!")
  