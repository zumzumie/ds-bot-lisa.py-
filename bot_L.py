import discord, random, json, riotwatcher, datetime 

from discord.ext import commands

from discord.utils import find

from riotwatcher import LolWatcher, ApiError

from datetime import date 

bot = commands.Bot(command_prefix = '>', intents = discord.Intents.all(), help_command = None)

pics_array = {}
with open('C:/py/pics_base.json', 'r') as database:
     pics_array = json.load(database)

watcher = LolWatcher('RGAPI-13c76a1c-6243-4949-ae55-6e04a49d4411')     

def random_pic(category):
    return random.choice(pics_array[category])

def getTEXT(author, who, command):
    if command == 'kiss':
        return f'{author} kisses {who.name} '
    if command == 'catgirl':
        return f'{author} nyan\`s {who.name} '

async def getPIC(ctx, who, command):
    await ctx.channel.trigger_typing()
    author = ctx.message.author.name
    
    pic = random.choice(pics_array[command])

    embed = discord.Embed(color = 0xff8888)
    if who != None:
        embed = discord.Embed(color = 0xff8888, title = getTEXT(author, who, command))  
    embed.set_image(url = pic)
    await ctx.send(embed = embed)           

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}!'.format(guild.name))      

@bot.command()
async def hello(ctx):
    await ctx.send('hello sweety')
    
@bot.command(name = 'random')
async def _random(ctx):
    num = random.randint(0, 100)
    
    await ctx.send(num)

#-----------
# test commands
#-----------

@bot.command()
async def insult(ctx):
    phrases_array = ["быдло", "мусор", "алкаш", "сброд", "деревенщина"]

    await ctx.send(f' ты {random.choice(phrases_array)}.')


#--------------
# fun
#--------------

@bot.command()
async def kiss(ctx, who: discord.Member = None): 
    await getPIC(ctx, who, command = 'kiss')

@bot.command()
async def ship(ctx, user: discord.Member):
    if user.id == 864226877248766012 :
            _embed = discord.Embed(color = 0xffffff, title = f'Ship with Lisa', description = 'i love u 1000\% cutie!')
            _embed.set_image(url = random_pic(category = 'kiss'))
            return await ctx.send(embed = _embed)
        
    _embed = discord.Embed(color = 0xffffff, title = f'Ship with {user.name}', description = f'{random.randint(0, 100)}%')
    _embed.set_image(url = random_pic(category = 'kiss'))
    await ctx.send(embed = _embed)
    
    

@bot.command()
async def catgirl(ctx, who: discord.Member = None):
    await getPIC(ctx, who, command = 'catgirl')

@bot.command()
async def jean(ctx):
    embed = discord.Embed(color = 0xff8888)
    embed.set_image(url = random_pic(category = 'jean'))
    await ctx.send(embed = embed )

#---------
# temporary commands
#---------

@bot.command()
async def compliments(ctx):
    compliments_array = ["sweety", "cutie", "honey", "Lisa\`s little helper", "dear", "dear traveler"]

    await ctx.send(f' hi {random.choice(compliments_array)}~')

@bot.command()
async def say(ctx, *, message = None):
  if message == None:
    await ctx.send('Please try `>say <your_message>`')
  else:
    await ctx.message.delete()
    await ctx.channel.send(message)

@bot.command()
async def day(ctx):
    d1 = datetime.datetime.today()
    await ctx.send(d1)

@bot.command()
async def whatday(ctx):
    current_time = date.today()
    await ctx.send(current_time)

@bot.command()
async def stats(ctx, region = None, *, nick = None):
    await ctx.channel.trigger_typing() 
    
    if region is None or nick is None:
        return await ctx.send('Please type a region and nick.\n\n**!stats ru naz1x**')
    
    specific_regions = ('br', 'eun', 'euw', 'jp', 'la', 'na', 'oc', 'tr')
    
    if region in specific_regions: 
        region += '1' 
    elif region == 'ru' or region == 'kr':
        pass
    else:
        return await ctx.send(f'**{region.upper()}** that was incorrect region.')
  
    try:
      summoner = watcher.summoner.by_name(region, nick)
      stats = watcher.league.by_summoner(region, summoner['id']) 
    except ApiError:
      return await ctx.send(f'Cannot found user **{nick}** in region **{region}.**')

    tier = stats[0]['tier']
    rank = stats[0]['rank']
    LP = stats[0]['leaguePoints']
    wins = stats[0]['wins']
    losses = stats[0]['losses']

 
    description = f""" {tier} {rank} {LP} 
    {wins} wins , {losses} losses | winrate - {round(wins / (wins + losses) * 100)}%
    """

    embed = discord.Embed(color = 0xff8888, title = f'{stats[0]["summonerName"]} ( {region} ) stats', description = description) 

    await ctx.send(embed = embed)

@bot.command()
async def roll(ctx, n1:int = None, n2:int = None):
    if n1 == None and n2 == None:
        await ctx.send(random.randint(0, 100))
    elif n1 != None and n2 == None:
        await ctx.send(random.randint(0, n1))
    elif n1 != None and n2 != None:
        await ctx.send(random.randint(n1, n2))

@bot.command()
async def mid(ctx, user:discord.Member = None):
    if user is None:
        return await ctx.send('please select a member')
    user = [ctx.author.name, user.name]
    await ctx.send( random.choice(user) )

@bot.command()
async def member_(ctx, user:discord.Member = None):
    if user is None:
        return await ctx.send('doldaeb?')
    await ctx.send(user)  

@bot.command()
async def avatar(ctx, user:discord.Member = None):
    if user is None:
        return await ctx.send('select a user')
    await ctx.send(user.avatar_url)    

@bot.command()
async def test(ctx):
    guild = bot.get_guild( 859865278989074472 )
    
    for member in guild.members:
        if member.id == 864226877248766012: # skip if member is your bot
            continue

        if str(member.status) != 'offline':
            user = await bot.fetch_user(member.id)
            
            try: # if user not close hes DM
                await user.send('ку')
            except: # dont send msg if user close hes DM
                pass    
@bot.command()
async def doodle(ctx, *, message ):
        ds_symbols = ['**' , '||' , "~~", "__"]
        new_message = ''
        for char in message:
            symbol = random.choice(ds_symbols)
            new_message += symbol + char + symbol
            if char == ' ':
                continue
            
        await ctx.send(new_message)

    





bot.run('ODY0MjI2ODc3MjQ4NzY2MDEy.YOyYAA.sGRWWz7egH04FTUfYrExTTy84do')