import discord
from discord.ext import commands
import config

#opening the file that stores the bot token
with open('token.txt', 'r') as f:
    token = f.read().strip()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

info_text = '''
Enter the index number of the section you want to track.

Enter "-1" when finished.
'''

@bot.command()
async def add_multiple_sections(ctx):
    # Get input from the user
    section_indexes = []
    
    await ctx.author.send(info_text)
    
    while True:
        index = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        index = index.content
        
        if index != '-1':
            section_indexes.append(index)
        
        else: 
            ctx.author.send('Finished adding sections.')
            break
        
    with open('class-index.txt', 'w') as f:
        for index in section_indexes:
            f.write(str(index) + '\n')
            
@bot.command()
async def add_section(ctx, arg):
    with open('class-index.txt', 'a') as f:
        f.write(arg + '\n')
    
@bot.command()
async def remove_section(ctx):
    await ctx.author.send('Enter the index number of the section you want to remove.')
    
    index = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    index = index.content
    
    desired_classes = config.load_desired_classes_from_file()
    
    if index in desired_classes:
        desired_classes.remove(index)
    
    with open('class-index.txt', 'w') as f:
        for index in desired_classes:
            f.write(str(index) + '\n')
    
    ctx.author.send('Section removed.')

@bot.command()
async def purge_sections(ctx):
    with open('class-index.txt', 'w') as f:
        f.write('')
        
    await ctx.author.send('All sections removed.')
    
@bot.command()
async def show_sections(ctx):
    desired_classes = config.load_desired_classes_from_file()
    
    await ctx.author.send('Your desired sections are:')
    
    for index in desired_classes:
        await ctx.author.send(index)

@bot.command()
async def create_config(ctx):
    # Ask for year
    await ctx.author.send('Enter the year:')
    
    msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    
    year = msg.content.strip()

    # Ask for term
    await ctx.author.send('Enter the term (spring, summer, fall, winter):')

    while True:
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        
        term = msg.content.strip().lower()

        if term == 'spring':
            term = '1'
            break
        elif term == 'summer':
            term = '7'
            break
        elif term == 'fall':
            term = '9'
            break
        elif term == 'winter':
            term = '0'
            break
        else:
            await ctx.author.send('Invalid term. Please enter a valid term (spring, summer, fall, winter):')
            continue

    # Ask for campus
    await ctx.author.send('Enter desired campus (New Brunswick, Newark, Camden):')

    while True:
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        
        campus = msg.content.strip().lower()

        if campus == 'new brunswick':
            campus = 'NB'
            break
        elif campus == 'newark':
            campus = 'NK'
            break
        elif campus == 'camden':
            campus = 'CM'
            break
        else:
            await ctx.author.send('Invalid campus. Please enter a valid campus (New Brunswick, Newark, Camden):')
            continue

    # Construct config dictionary
    config = {
        'year': year,
        'term': term,
        'campus': campus,
    }

    # Save config to file (optional)
    with open('config.txt', 'w') as f:
        for key, value in config.items():
            f.write(f'{key}:{value}\n')

    # Send confirmation message to user
    await ctx.author.send('Configuration saved successfully.')
    
@bot.command()
async def leroysucks(ctx):
    await ctx.send('No u.')

bot.run(token)