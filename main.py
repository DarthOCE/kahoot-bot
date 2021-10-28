import asyncio
import os
import datetime, time
from itertools import cycle


import discord
from discord.ext import commands
from discord_components import *
from kahoot import client as account


token = ""
client = commands.Bot(command_prefix='k!')
client.remove_command('help')


bots = []

promobuttons = [
	[
		Button(
			style=ButtonStyle.URL,
			label="See my GitHub!",
			url="https://github.com/T3ARED"
		),

		Button(
			style=ButtonStyle.URL,
			label="Join the support server!",
			url="https://kahootbotter.live/discord/"
		),
        
        Button(
			style=ButtonStyle.URL,
			label="Vote on top.gg!",
			url="https://top.gg/bot/894342726210945054/vote"
        )
	],
]

invitebutton = [
    [
        Button(
		style=ButtonStyle.URL,
		label="Invite to your server!",
		url="https://discord.com/api/oauth2/authorize?client_id=894342726210945054&permissions=532576300096&scope=bot"
        ),
        
        Button(
			style=ButtonStyle.URL,
			label="Join the support server!",
			url="https://kahootbotter.live/discord/"
		),

    ]
]

votebutton = [
    [
        Button(
			style=ButtonStyle.URL,
			label="Vote on top.gg!",
			url="https://top.gg/bot/894342726210945054"
        )
    ]
]


@client.event
async def on_ready():
    global startTime
    startTime = time.time()
    servers = len(client.guilds)
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1

        statuses = [f'k!help | {members} users', f'k!help | {servers} servers']

        displaying = cycle(statuses)

        running = True

        print("================================================")
        print('Connected to bot: {}'.format(client.user.name))
        print('Bot ID: {}'.format(client.user.id))
        print("================================================")

        while running:
            current_status = next(displaying)
            await client.change_presence(status=discord.Status.online,
                                         activity=discord.Activity(name=current_status, type=3))
            await asyncio.sleep(20)
        


@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="https://kahootbotter.live",
        colour=discord.Colour.purple()
    )
    embed.set_footer(text=f"KahootBotter.live#6221")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/894342726210945054/f4075ae8075d339297c1b24e44752c26.png?size=256")
    embed.add_field(name="help", value="● Displays all bot commands.", inline=False)
    embed.add_field(name="ping", value="● Displays bot latancy and uptime.", inline=True)
    embed.add_field(name="invite", value="● Invite the bot too your server!.", inline=True)
    embed.add_field(name="flood / bot <pin> <name> <n>",
    value="● Kahoot Pin <pin>.\n⠀⠀<name> Name the bots. \n⠀⠀<n> How many bots you want to send.\n⠀⠀(Ex: k!flood 1234567 Botted 1000)", inline=False)
    embed.add_field(name="leave", value="● Disconnects the bots from the kahoot", inline=False)

    await ctx.send(embed=embed, components=promobuttons)


@client.command()
async def invite(ctx):
    embed = discord.Embed(
        title="https://kahootbotter.live",
        colour=discord.Colour.purple()
    )
    embed.set_footer(text=f"KahootBotter.live#6221")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/894342726210945054/f4075ae8075d339297c1b24e44752c26.png?size=256")
    embed.add_field(name="Bot Invite",
                    value="You can add the bot [here](https://discord.com/api/oauth2/authorize?client_id=894342726210945054&permissions=532576300096&scope=bot)", inline=True)
    embed.add_field(name="FAQ", value="For more info on how to use the bot you can click read the [FAQ](https://kahootbotter.live/faq/)", inline=True)
                    
                    
    await ctx.send(embed=embed, components=invitebutton)
    
    


@client.command()
async def ping(ctx):
    await ctx.send(f" My latency is {round(client.latency * 1000)}ms and i have been online for {str(datetime.timedelta(seconds=int(round(time.time()-startTime))))}")



@client.command(aliases=["bot"])
async def flood(ctx, pin, name, n):
    await ctx.send(f"Sending {n} bots too {pin}...\n Sender:{ctx.message.author.mention}")

    n = int(n)
    index = 0
    while (index != n):
        bot = account()
        bot.join(pin, f"{name}{index + 1}")
        bots.append(bot)
        index += 1

    await ctx.send("Bots sent successfully")
    await ctx.message.add_reaction("✅")


@client.command()
async def leave(ctx):
    await ctx.message.add_reaction("👋")
    await ctx.send("Disconnect the bots...")

    for bot in bots:
        bot.leave()

    bots.clear()


    



client.run(token)
