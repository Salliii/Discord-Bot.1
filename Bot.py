import discord
from discord.ext import commands, tasks
from discord.utils import get
from bs4 import BeautifulSoup
from random import randint
import validators
import requests
import datetime
import time
import sys
import os



intents = discord.Intents.all()
client = commands.Bot(command_prefix = '-', intents=intents)
client.remove_command('help')
token = ''

TempList = [(10, 'Aufgehts Jürgen schmeiß den Grill an')]
HelpList = [('help\t|\t-help <Command>', 'Listet alle Befehle mit einer kurzen Beschreibung auf.'),\
            ('join', 'Bot joint in den jeweiligen Sprachchannel.'),\
            ('leave', 'Bot verlässt den Sprachchannel in welchem er ist.'),\
            ('weather', 'Teilt die Temperatur in Wiesental mit'),\
            ('sherlock <Username>', 'Durchsucht die Sozialen Medien nach dem Username')]
SherlockDir = 'C:/Users/silas/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/sali/sherlock/sherlock/sherlock.py'
__WetterUrl = 'https://www.wetteronline.de/wetter/waghaeusel/wiesental'
__Watch2getherUrl = 'https://w2g.tv/?lang=de'
Status = ''
SherlockUsername = ''

def Setup():
    try:
        with open('SherlockLib.txt', 'r')as SetupRead:
            pass
    except:
        with open('SherlockLib.txt', 'w')as CreateSherlock:
            CreateSherlock.write('')
Setup()

def console(input, type):
    if type == 0:
        console_entry = str(datetime.datetime.now())[:19] + ' | >>> ' + str(input)
    elif type == 1:
        if input.author != client.user:
            console_entry = str(datetime.datetime.now())[:19] + ' | ' + str(input.author) + ' ' + str(input.content)
    try:
        print(console_entry)                                                                                       #Consol Log hinzufügen
    except:
        pass
console('bot starting...', 0)


#EVENTS
@client.event
async def on_ready():
    console('bot started', 0)
    if Status != '':
        await client.change_presence(activity=discord.Game(Status))

@client.event
async def on_message(message):
    console(message, 1)
    await client.process_commands(message)


#HELP
@client.group(invoke_without_command=True)
async def help(ctx, *command):
    if command == ():
        console(f'Sucessfully issued general help to {ctx.message.author} in {ctx.message.channel}', 0)
        embed = discord.Embed(title='Help', description='Hier stehen alle ausführbaren Befehle mit einer kurzen Beschreibung:')
    else:
        console(f'Sucessfully issued help for -{command[0]} to {ctx.message.author} in {ctx.message.channel}', 0)
        embed = discord.Embed(title='Help', description=f'Hier wird der Befehl -{command[0]} beschrieben:')
    for HelpCommand in HelpList:
        if command == ():
            embed.add_field(name=f'-{HelpCommand[0]}', value=f'   {HelpCommand[1]}', inline=False)
        elif command[0] == str((HelpCommand[0])[:len(command[0])]):
            embed.add_field(name=f'-{HelpCommand[0]}', value=f'   {HelpCommand[1]}', inline=False)
        else:
            pass
    await ctx.send(embed=embed)


#VOICECHANNEL
@client.command(pass_context = True)
async def join(ctx):
    #await ctx.channel.purge(limit=1)
    if (ctx.voice_client):
        console('join failure ! bot already in a channel', 0)
    else:
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
            checkVoiceChannel.start(ctx)
            console(f'successfully joined to {channel}', 0)
        else:
            console(f'join failure ! user in no voice channel', 0)

@client.command(pass_context = True)
async def leave(ctx):
    #await ctx.channel.purge(limit=1)
    if (ctx.voice_client):
        checkVoiceChannel.cancel()
        channel = ctx.voice_client.channel
        await ctx.guild.voice_client.disconnect()
        console(f'successfully disconnected from {channel}', 0)
    else:
        console('disconnect failure ! bot in no voice channel', 0)

@tasks.loop(seconds=10)
async def checkVoiceChannel(ctx):
    if len((ctx.voice_client.channel).members) == 1:
        if ((ctx.voice_client.channel).members)[0] == client.user:
            channel = ctx.voice_client.channel
            await ctx.guild.voice_client.disconnect()
            console(f'successfully disconnected from {channel} ! timeout', 0)
            checkVoiceChannel.cancel()


#COMMANDS
@client.command()
async def weather(ctx):
    #await ctx.channel.purge(limit=1)
    RequestWetter = requests.get(__WetterUrl)
    soup = BeautifulSoup(RequestWetter.content, 'html.parser')

    Temp = soup.find('div', class_='value').text
    Loct = ((soup.find('h1', id='nowcast-card-headline').text).split(' '))[1]
    for checkTemps in range(len(TempList)):
        if int(Temp) >= int(TempList[checkTemps][0]):
            SpezialInfo = TempList[checkTemps][1]
    console(f'successfully issued the weather to {ctx.message.author} in {ctx.message.channel}', 0)
    try:
        await ctx.send(f'Gerade sind es {Temp}°C in {Loct}\n{SpezialInfo}')
    except:
        await ctx.send(f'Gerade sind es {Temp}°C in {Loct}')

@client.command()
async def clear(ctx):
    await ctx.channel.purge()
    console(f'successfully cleared {ctx.message.channel} by {ctx.message.author}', 0)

@client.command()
async def sherlock(ctx):
    #await ctx.channel.purge(limit=1)
    GetId = await ctx.channel.history(limit=1).flatten()
    Content = (await ctx.fetch_message(int(str(GetId)[13:31]))).content
    spy = Content[10:]
    availableSherlock = []
    console(f"check availability of {spy}'s Sherlock", 0)
    with open('SherlockLib.txt', 'r') as CheckSherlock:
        Single = str(CheckSherlock.read()).split('\n\n')
        for GetSegments in Single:
            Segments = GetSegments.split('\n')
            availableSherlock.append(Segments[0])

        if spy in availableSherlock:
            for GetSegments in Single:
                Segments = GetSegments.split('\n')
                if Segments[0] == spy:
                    Output = '\n'.join(Segments[1:])
                    console(f'successfully issued available Sherlock for {spy}', 0)
                    await ctx.send(f'Der Benutzername {spy} wurde auf folgenden Seiten gefunden:\n```{Output}```')
                    break
        else:
            console(f'starting Sherlock for {spy}', 0)
            starttime = time.time()
            waitMessage = await ctx.send(f'Die Suche nach {spy} wurde gestartet. Dies kann einige Sekunden dauern!')
            Output = ''
            sherlockOutput = os.popen(f'D: && cd "{os.path.dirname(sys.executable)}"&& python {SherlockDir} "{spy}"').read()
            for websherlock in sherlockOutput.split('\n'):
                if websherlock[0:3] == '[+]':
                    Output = str(str(Output) + ' - '+ str(websherlock[3:]) + '\n')
            endtime = time.time()
            console(f'finished Sherlock for {spy} after {round(int(endtime-starttime), 1)} sec', 0)
            with open('SherlockLib.txt', 'a')as SherlockInput:
                SherlockInput.write(str(spy)+'\n'+str(Output)+'\n')
            await waitMessage.delete()
            await ctx.send(f'Der Benutzername {spy} wurde auf folgenden Seiten gefunden:\n```{Output}```')


@client.command()
async def stalk(ctx, platform, *username):
    #await ctx.channel.purge(limit=1)
    if validators.url(platform) == True:
        for segments in platform.split('/'):
            for segment in segments.split('.'):
                if segment == 'youtube':
                    segmentslist = platform.split('/')
                    segmentslist[len(segmentslist)-1] = 'videos'
                    platform = '/'.join(segmentslist)
    else:
        pass

    RequestStalk = requests.get(platform).text
    soup = BeautifulSoup(RequestStalk, 'lxml')
    for content in soup.find_all('div', class_='yt-lockup-content'):
        print(content)

    print('fertig')



client.run(token)