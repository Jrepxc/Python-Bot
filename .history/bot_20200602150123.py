import discord
import asyncio
import random
import time
import os
import json
from discord.ext import commands
from discord.utils import get


def get_prefix(client, message):   
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
        
    return prefixes[str(message.guild.id)]    

    



client = commands.Bot(command_prefix = '?p ') #prefix is ?p
client.remove_command('help')#Clears help for a customization

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:   
        json.dump(prefixes, f, indent=4) 
        
@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefises - json.load(f)  

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)     

@client.command()
async def changeprefix(ctx, prefix):  
    with open('prefixes.json', 'r') as f:
        prefixes - json.load(f)  

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)     
           


#random bool
def rand_bool():
    x = random.randint(1,2)
    if x == 1:
        return True 
    else:
        return False
#Tests for no status
def test_status(s):
    no_status = ['n','none']
    for elements in no_status:
        upper = elements.capitalize()
        if s == elements or s == upper:
            return True
    return False
#Tests Version Status
def version_status(s):
    vIn = 'version status'
    if s == vIn.title() or s == vIn:
        return True
    else:
        return False
     
#Setup
@client.event 
async def on_ready():
    custom_status = input("What do you want as the Bot's status: ")
    ver = "Iron Nexus Bot Version 0.5.0"
    print("Iron Nexus Bot is up and running!")
    version = version_status(custom_status)
    if test_status(custom_status):
        await client.change_presence(status=discord.Status.online)
    elif version_status(custom_status):
        await client.change_presence(status=discord.Status.online, activity=discord.Game(ver))
    else:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(custom_status))
#Assigns roles
@client.event
async def on_member_join(member):
    channel = get(member.guild.channels, name='welcome')
    role = get(member.guild.roles, name="Non-members")
    await member.add_roles(role)
    await channel.send(f"Hello {member.mention}! Welcome to the Iron Nexus Discord! Don't forget to go to #how-to-apply!")
#Says EZ LOG in the welcome chat when someone leaves or gets kicked
@client.event
async def on_member_remove(member):
    channel = get(member.guild.channels, name='welcome')
    await channel.send(f"EZZ LOG **{member}**")
#Antispam
@client.event
async def on_message(message):
    content = message.content
    if not content.startswith('?p '):
        msg_channel = message.channel
        channel = get(message.guild.channels, name='nexus-bot-testing')
        if msg_channel == channel.name:
            print(f"The message was created at {message.created_at} in the channel {message.channel}")
    else:
        await client.process_commands(message)
    bad_words = ["imp", "IMP", "Imp", "iMp", "iMP"]

    for word in bad_words:
        if message.content.count(word) > 0:
            print("A bad word was said")
            await message.channel.purge(limit=1)         
#custom help command
@client.command()
async def help(ctx):
    embed=discord.Embed(title="Help", description="Help Menu ", color=0xff0000)
    embed.set_author(name="Iron Nexus Bot", icon_url="https://i.imgur.com/FmGhlVY.jpg")
    embed.add_field(name="helpcommands", value="Shows commands", inline=False)
    embed.add_field(name="helpadmin",value="Only admin's can use this command", inline=False)
    embed.add_field(name="about", value="This is a bot specially made for Iron Nexus", inline=False)
    await ctx.send(embed=embed) 
#About Command   
@client.command()
async def about(ctx):
    embed=discord.Embed(title="About", description="About", color=0xff0000)
    embed.set_author(name="Iron Nexus Bot", icon_url="https://i.imgur.com/FmGhlVY.jpg")
    embed.add_field(name="About", value="This is a bot specially made for Iron Nexus by Jrepxc.", inline=False)
    await ctx.send(embed=embed)
#help commands
@client.command()
async def helpcommands(ctx):
    embed = discord.Embed(title="Help Commands", description="Commands that work with the bot", color=0xff0000)
    embed.set_author(name="Iron Nexus Bot", icon_url="https://i.imgur.com/FmGhlVY.jpg")
    embed.add_field(name="cool", value="Sees if someone you ping or if you are cool",inline=False)
    embed.add_field(name="talk",value="Specify a member and an amount of pings and it pings someone. Max pings are 15",inline=False)
    embed.add_field(name="youtube",value="Sends Iron Nexus's youtube channel. Subscribe!",inline=False)
    await ctx.send(embed=embed)
#Help menu for admin commands
@client.command()
@commands.has_permissions(administrator=True,manage_messages=True,manage_roles=True)
async def helpadmin(ctx):
    embed = discord.Embed(title="Admin Commands", description="Commands for admins", color=0xff0000)
    embed.set_author(name="Iron Nexus Bot", icon_url="https://i.imgur.com/FmGhlVY.jpg")
    embed.add_field(name="Kick",value="Kicks members",inline=False)
    embed.add_field(name="Ban",value="Bans members from the discord",inline=False)
    embed.add_field(name="Unban", value="Unbans members from the discord",inline=False)
    embed.add_field(name="Purge",value="Clears chat by a set amount. Default is 5")
    embed.add_field(name="Mute and Unmute", value="Stops someone from talking",inline=False)
    await ctx.send(embed=embed)
#kick 
@client.command()
@commands.has_permissions(administrator=True,manage_messages=True,manage_roles=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    user : discord.User = member
    await user.send(f"You have been kicked for {reason}")
    await member.kick(reason=reason)
    await ctx.send(f"***{member}*** has been kicked for {reason}")
#ban
@client.command()
@commands.has_permissions(administrator=True,manage_messages=True,manage_roles=True)
async def ban(ctx,member : discord.Member, *, reason=None):
    user : discord.User = member
    await user.send(f"You have been banned for {reason}")
    await member.ban(reason=reason)
    await ctx.send(f"***{member.mention}*** get banned by the Nexus hammer!(Was banned for: {reason})")
#unban
@client.command()
@commands.has_permissions(administrator=True,manage_messages=True,manage_roles=True)
async def unban(ctx, *, member):
    banned_members = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_members:
        user = ban_entry.user
        if(user.name, user.member_discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return
#purges chat
@client.command()
@commands.has_permissions(administrator=True,manage_messages=True,manage_roles=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
#mute
@client.command()
@commands.has_permissions(administrator=True,manage_messages=True,manage_roles=True)
async def mute(ctx, member : discord.Member, *, reason=None):
    role = get(member.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f"{member.mention} has been muted!\n Reason:{reason}")
#unmute
@client.command()
@commands.has_permissions(administrator=True,manage_messages=True,manage_roles=True)
async def unmute(ctx,member : discord.Member, *, reason=None):
    role = get(member.guild.roles, name="Muted")
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} has been unmuted!")
    else:
        await ctx.send("That user is not muted!")
#Does sunglasses emoji
@client.command()
async def cool(ctx, member : discord.Member = None):
    if member == None:
        bool = rand_bool()
        if bool == True:
            await ctx.send("You are cool :sunglasses:")
        else:
            await ctx.send("You are not cool :neutral_face:")
    else:
        bool = rand_bool()
        if bool == True:
            await ctx.send(f"{member.mention} is cool :sunglasses:")
        else:
            await ctx.send(f"{member.mention} is not cool :neutral_face:")
# #lol?
# @client.command()
# async def lol(ctx):
#     file = discord.File('images\lol.png')
#     await ctx.send(content=None, file=file)
# #nexus logo    
# @client.command()
# async def logo(ctx):
#     file = discord.File('images\logo.png')
#     await ctx.send(content=None, file=file)    
#talk
@client.command()
async def talk(ctx, member : discord.Member, x):
    number = int(x)
    if number <= 15:
        for i in range(number):
            await ctx.send(f"{member.mention} TALK!")
        else:
            await ctx.send(f"{number} is too big of a number!")
@client.command()
async def youtube(ctx):
    await ctx.send("insert youtube here")

#Runs the client
client.run("NzE3MDc0NDU2MjE1OTQ1MjI5.XtWWzA.IcA9lPLcn8-VkZb-OKYBnJlS4u4")