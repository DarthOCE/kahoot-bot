import asyncio
import datetime, time
import json
from itertools import cycle


import discord
from discord.ext import commands
from discord_components import *
from discord_slash import SlashCommand
from kahoot import client as account


config = json.load(open('config.json', 'r'))
token = config["token"]
prefix = config["prefix"]
client = commands.Bot(command_prefix=prefix)
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True)


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
		url="https://discord.com/api/oauth2/authorize?client_id=894342726210945054&permissions=397284502592&scope=bot%20applications.commands"
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

invitebutton1 = [
    [
        Button(
			style=ButtonStyle.URL,
			label="Join the Support Server!!",
			url="https://discord.gg/Wb4j2zJkC5"
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

        statuses = [f'/help | {servers} servers', f'/help | {servers} servers']

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
        




@slash.slash(description="Displays all bot commands")
async def help(ctx):
    embed = discord.Embed(
        title="https://kahootbotter.live",
        colour=discord.Colour.purple()
    )
    embed.set_footer(text=f"Requested by {ctx.author}")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/894342726210945054/f4075ae8075d339297c1b24e44752c26.png?size=256")
    embed.add_field(name="help", value="● Displays all bot commands.", inline=False)
    embed.add_field(name="ping", value="● Displays bot latancy and uptime.", inline=True)
    embed.add_field(name="invite", value="● Invite the bot too your server!.", inline=True)
    embed.add_field(name="flood / bot <pin> <name> <n>",
    value="● Kahoot Pin <pin>.\n⠀⠀<name> Name the bots. \n⠀⠀<n> How many bots you want to send.\n⠀⠀(Ex: k!flood 1234567 Botted 1000)", inline=False)
    embed.add_field(name="leave", value="● Disconnects the bots from the kahoot", inline=False)
    await ctx.send(embed=embed)


@slash.slash(description="Get the bost latency and uptime")
async def ping(ctx):
    embed = discord.Embed(title=":ping_pong: Response Times :ping_pong:", color=discord.Colour.blue())
    embed.add_field(name="API", value=f"`Loading...`")
    embed.add_field(name="Websocket", value=f"`{int(client.latency * 1000)}ms`")
    embed.add_field(name="Uptime", value=f"`{str(datetime.timedelta(seconds=int(round(time.time()-startTime))))}`")
    time_before = time.time()
    edit = await ctx.send(embed=embed, content=f"{ctx.author.mention}")
    time_after = time.time()
    difference = int((time_after - time_before) * 1000)
    embed = discord.Embed(title=":ping_pong: Response Times :ping_pong:", color=discord.Colour.green())
    embed.add_field(name="API", value=f"`{difference}ms`")
    embed.add_field(name="Websocket", value=f"`{int(client.latency * 1000)}ms`")
    embed.add_field(name="Uptime", value=f"`{str(datetime.timedelta(seconds=int(round(time.time()-startTime))))}`")
    await edit.edit(embed=embed, content=f"{ctx.author.mention}")


@slash.slash(description="Send bots the the kahoot")
async def flood(ctx, pin, name, n):
    await ctx.send(f"Sending {n} bots too {pin}...\n")
    print(f"Recived request from {ctx.author.mention} sending {n} bots to {pin} with the name {name}")

    n = int(n)
    index = 0
    while (index != n):
        bot = account()
        bot.join(pin, f"{name}{index + 1}")
        bots.append(bot)
        index += 1

    await ctx.send("Bots sent successfully")
    print(f"Completed request from {ctx.author.mention} sending {n} bots to {pin} with the name {name}")
    await ctx.message.add_reaction("✅")


@slash.slash(description="Remove bots from the kahoot")
async def leave(ctx):
    await ctx.message.add_reaction("👋")
    await ctx.send("Disconnecting the bots...")

    for bot in bots:
        bot.leave()

    bots.clear()
    await ctx.send("Bots disconnected")


@slash.slash(description="Invite the bot too your server!")
async def invite(ctx):
    embed = discord.Embed(
        title="We are migrating too slash commands",
        colour=discord.Colour.purple()
    )
    embed.set_footer(text=f"Requested by {ctx.author}")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/894342726210945054/f4075ae8075d339297c1b24e44752c26.png?size=256")
    embed.add_field(name="Bot Invite",
                    value="You can add the bot [here](https://discord.com/api/oauth2/authorize?client_id=894342726210945054&permissions=397284502592&scope=bot%20applications.commands)", inline=True)
    embed.add_field(name="You must reinvite the bot too this server too use slash commands if they are not already present", value="https://kahootbotter.live/bot/", inline=True)
                                 
    await ctx.send(embed=embed)
    

@client.command()
async def invite(ctx):
    embed = discord.Embed(
        title="We are migrating too slash commands",
        colour=discord.Colour.purple()
    )
    embed.set_footer(text=f"Requested by {ctx.author}")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/894342726210945054/f4075ae8075d339297c1b24e44752c26.png?size=256")
    embed.add_field(name="Bot Invite",
                    value="You can add the bot [here](https://discord.com/api/oauth2/authorize?client_id=894342726210945054&permissions=397284502592&scope=bot%20applications.commands)", inline=True)
    embed.add_field(name="You must reinvite the bot too this server too use slash commands if they are not already present", value="https://kahootbotter.live/bot/", inline=True)
                                 
    await ctx.send(embed=embed)
    

@client.command()
async def ping(ctx):
    embed = discord.Embed(title=":ping_pong: Response Times :ping_pong:", color=discord.Colour.blue())
    embed.add_field(name="API", value=f"`Loading...`")
    embed.add_field(name="Websocket", value=f"`{int(client.latency * 1000)}ms`")
    embed.add_field(name="Uptime", value=f"`{str(datetime.timedelta(seconds=int(round(time.time()-startTime))))}`")
    time_before = time.time()
    edit = await ctx.send(embed=embed, content=f"{ctx.author.mention}")
    time_after = time.time()
    difference = int((time_after - time_before) * 1000)
    embed = discord.Embed(title=":ping_pong: Response Times :ping_pong:", color=discord.Colour.green())
    embed.add_field(name="API", value=f"`{difference}ms`")
    embed.add_field(name="Websocket", value=f"`{int(client.latency * 1000)}ms`")
    embed.add_field(name="Uptime", value=f"`{str(datetime.timedelta(seconds=int(round(time.time()-startTime))))}`")
    await edit.edit(embed=embed, content=f"{ctx.author.mention}")



@client.command(aliases=["bot"])
async def flood(ctx):
    await ctx.send(f"Sending {n} bots too {pin}...\n")
    print(f"Recived request from {ctx.author.mention} sending {n} bots to {pin} with the name {name}")

    n = int(n)
    index = 0
    while (index != n):
        bot = account()
        bot.join(pin, f"{name}{index + 1}")
        bots.append(bot)
        index += 1

    await ctx.send("Bots sent successfully")
    print(f"Completed request from {ctx.author.mention} sending {n} bots to {pin} with the name {name}")
    await ctx.message.add_reaction("✅")


@client.command()
async def leave(ctx):
    await ctx.message.add_reaction("👋")
    await ctx.send("Disconnecting the bots...")

    for bot in bots:
        bot.leave()

    bots.clear()
    await ctx.send("Bots disconnected")


@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="https://kahootbotter.live",
        colour=discord.Colour.purple()
    )
    embed.set_footer(text=f"Requested by {ctx.author}")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/894342726210945054/f4075ae8075d339297c1b24e44752c26.png?size=256")
    embed.add_field(name="help", value="● Displays all bot commands.", inline=False)
    embed.add_field(name="ping", value="● Displays bot latancy and uptime.", inline=True)
    embed.add_field(name="invite", value="● Invite the bot too your server!.", inline=True)
    embed.add_field(name="flood / bot <pin> <name> <n>",
    value="● Kahoot Pin <pin>.\n⠀⠀<name> Name the bots. \n⠀⠀<n> How many bots you want to send.\n⠀⠀(Ex: k!flood 1234567 Botted 1000)", inline=False)
    embed.add_field(name="leave", value="● Disconnects the bots from the kahoot", inline=False)
    await ctx.send(embed=embed)


client.run(token)
