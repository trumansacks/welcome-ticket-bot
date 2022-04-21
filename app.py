import discord
from discord.ext import commands, tasks
from logzero import logger
from dotenv import load_dotenv
import os

#discord permissions
Intents = discord.Intents.default()
Intents.members=True
Intents.guilds=True
Intents.messages=True
client = discord.Client(intents=Intents)

load_dotenv() #loads .env variables

#global variables
TICKET_ROLE = 'Tickets'
BOT_TOKEN = os.environ.get("BOT_TOKEN") 


@client.event
async def on_ready():
    logger.info(f'beep boop! [{len(client.guilds)} servers]')
    servers = client.guilds
    for server in servers:
        logger.warning(f'[{server.name}] [{server.owner}] [{server.member_count} members]')
    logger.warning('-----------------------------------')


@client.event
async def on_member_join(member):
    server_name = member.guild.name
    logger.warning(f'[{server_name}] {member} has joined the server')
    guild = member.guild

    category = discord.utils.get(member.guild.categories, name='WELCOME-TICKETS') #checks to see if there is a tickets category

    if category == None:
        logger.warning(f'[{server_name}] no tickets category found')
        try:
            category = await guild.create_category('WELCOME-TICKETS', position=0) #creates ticket category if there is no existing one detected
            logger.info(f'[{server_name}] tickets category created')
        except Exception as e:
            logger.error(e)
    else:
        logger.info(f'[{server_name}] ticket category detected')
   

    overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False), #sets the welcome channel as private to default users
    discord.utils.get(member.guild.roles,name=TICKET_ROLE): discord.PermissionOverwrite(read_messages=True), #allows anyone with the 'Ticket" role access to welcome channel
    guild.me: discord.PermissionOverwrite(read_messages=True), #gives discord bot access to the welcome channel
    member: discord.PermissionOverwrite(read_messages=True) #gives new member access to the welcome channel
}

    try:
        channel = await guild.create_text_channel(f'welcome-{member}', overwrites=overwrites, category=category, position=0) #creates the welcome channel
        embedVar = discord.Embed(title=f"Welcome {member}!", description=f'This channel has been created to welcome <@{member.id}> to {guild}. Say hi {member.name}!', color=0x33CAFF) #embed formatter
        await channel.send(embed=embedVar)
        logger.info(f'[{server_name}] new channel created with admins & {member}')
    except Exception as e:
        logger.error(e)
            
    

@client.event
async def on_message(message):
    server_name = message.guild.name
    author = message.author
    author_role = discord.utils.get(message.author.roles, name=TICKET_ROLE)
    
    welcome_ticket_category = discord.utils.get(message.guild.categories, name='WELCOME-TICKETS')
    message_channel_category = message.channel.category


    if author_role and message_channel_category == welcome_ticket_category:
        if message.content == '!close':
                try:
                    await message.channel.delete()
                    logger.info(f'[{server_name}] channel deleted by {message.author}')
                except Exception as e:
                    logger.error(e)

client.run(BOT_TOKEN)