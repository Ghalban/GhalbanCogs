import discord
from redbot.core import commands

class AniMod(commands.Cog):
    """Commands for A&I Server"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    @commands.has_role(878240352857886731)
    async def verify(self, ctx: commands.Context, member: discord.Member):

        """Assigns `@Initiate` role to new member and welcomes them too!"""
        
        import random
        greeting = (
            f"{member.mention} just joined the server!",
            f"I've been expecting you, {member.mention}.",
            f"I know why you're here {member.mention}.",
            f"Look! It's {member.mention}. Hello {member.mention}!\n(^v^)/",
            f"Alright, {member.mention} you're in!",
            f"{member.mention} has completed verification! Nice.",
            f"So, are we just going to sit down and pretend that {member.mention} hasn't joined us?",
            f"{member.mention} is at least 20% cooler now that they're here.",
            f"Welcome, {member.mention}! Please take a moment to look around the server.",
            f"Guys, say hello to my new friend {member.mention}!"
        )

        initiate = ctx.guild.get_role(487854898692489227)

        if initiate in member.roles:
            return await ctx.send(f"{member.mention} is already verified.")

        await member.add_roles(initiate)
        await ctx.tick()
        return await ctx.guild.get_channel(684822519865147403).send(random.choice(greeting))

    @commands.command(pass_context=True)
    @commands.has_role(878240352857886731)
    async def grad(self, ctx: commands.Context, member: discord.Member):
        """Assigns `@Alumni` and `@Master` roles to grads!"""
        alumni = ctx.guild.get_role(657056079926001686)
        master = ctx.guild.get_role(546873124944216075)
        await member.add_roles(alumni, master)
        await ctx.tick()
        return await ctx.guild.get_channel(749397281924448326).send(f"{member.mention} is an `@Alumni`! Congrats!")
