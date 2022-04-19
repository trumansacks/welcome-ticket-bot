import discord
from discord.ext import commands, tasks
from logzero import logger
from dotenv import load_dotenv
import os

#discord permissions
Intents = discord.Intents.default()
Intents.members=True
Intents.guilds=True
client = discord.Client(intents=Intents)

load_dotenv() #loads .env variables

#global variables
TICKET_ROLE = 'Tickets'
BOT_TOKEN = os.environ.get("BOT_TOKEN") 


@client.event
async def on_ready():
    logger.info('beep boop!')


@client.event
async def on_member_join(member):
    logger.warning(f'{member} has joined the server')
    guild = member.guild

    category = discord.utils.get(member.guild.categories, name='WELCOME-TICKETS') #checks to see if there is a tickets category

    if category == None:
        logger.warning('no tickets category found')
        try:
            category = await guild.create_category('WELCOME-TICKETS', position=0) #creates ticket category if there is no existing one detected
            logger.info('tickets category created')
        except Exception as e:
            logger.error(e)
    else:
        logger.info('ticket category detected')
   

    overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False), #sets the welcome channel as private to default users
    discord.utils.get(member.guild.roles,name=TICKET_ROLE): discord.PermissionOverwrite(read_messages=True), #allows anyone with the 'Ticket" role access to welcome channel
    guild.me: discord.PermissionOverwrite(read_messages=True), #gives discord bot access to the welcome channel
    member: discord.PermissionOverwrite(read_messages=True) #gives new member access to the welcome channel
}

    try:
        channel = await guild.create_text_channel(f'welcome-{member}', overwrites=overwrites, category=category, position=0) #creates the welcome channel
        embedVar = discord.Embed(title=f"Welcome {member}!", description=f'This channel has been created to welcome {member.name} to {guild}', color=0x33CAFF) #embed formatter
        await channel.send(embed=embedVar)
        logger.info(f'new channel created with admins & {member}')
    except Exception as e:
        logger.error(e)
            
    

client.run(BOT_TOKEN)