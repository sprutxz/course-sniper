import discord
from discord.ext import commands, tasks
import config_loader
import clsretrieval
import asyncio

# Opening the file that stores the bot token
with open('token.txt', 'r') as f:
    token = f.read().strip()
    
with open('user-id.txt', 'r') as f:
    USR_ID = int(f.read().strip())

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        
    async def setup_hook(self) -> None:
        # Start the task to run in the background
        self.check_for_new_sections.start()
    
    @tasks.loop(seconds=2)
    async def check_for_new_sections(self):
        print('Checking for new sections...')
        
        params = config_loader.load_config_from_file()
        semester = params['term'] + params['year']
        desired_sections = config_loader.load_desired_classes_from_file()
        open_sections = clsretrieval.get_open_classes()
        
        indexes = clsretrieval.check_open_classes(open_sections, desired_sections)
        
        if indexes:
            print('New sections found!')
            for index in indexes:
                url = f'https://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&semesterSelection={semester}&indexList={index}'
                print(f'Index: {index}')
                
                # Send a message to the user
                user = await self.fetch_user(USR_ID)
                await user.send(f'Open Section: {index} \n url: {url}')
                
                # Remove the section from the text file
                desired_sections.remove(index)
                with open('class-index.txt', 'w') as f:
                    for index in desired_sections:
                        f.write(str(index) + '\n')
                
        print('Done checking for new sections.')
    
    @check_for_new_sections.before_loop
    async def before(self):
        await self.wait_until_ready()
        
class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def add_section(self, ctx, arg):
        with open('class-index.txt', 'a') as f:
            f.write(arg + '\n')
    
    @commands.command()
    async def remove_section(self, ctx, arg):
        desired_classes = config_loader.load_desired_classes_from_file()
        
        if arg in desired_classes:
            desired_classes.remove(arg)
        
        with open('class-index.txt', 'w') as f:
            for index in desired_classes:
                f.write(str(index) + '\n')

bot = MyBot(command_prefix='>', intents=intents)
# Adding the Cog
async def main():
    async with bot:
        await bot.add_cog(Commands(bot))
        await bot.start(token)

# Running the bot
if __name__ == "__main__":
    asyncio.run(main())


# info_text = '''
# Enter the index number of the section you want to track.

# Enter "-1" when finished.
# '''

# @bot.command()
# async def add_multiple_sections(ctx):
#     # Get input from the user
#     section_indexes = []
    
#     await ctx.author.send(info_text)
    
#     while True:
#         index = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
#         index = index.content
        
#         if index != '-1':
#             section_indexes.append(index)
        
#         else: 
#             ctx.author.send('Finished adding sections.')
#             break
        
#     with open('class-index.txt', 'w') as f:
#         for index in section_indexes:
#             f.write(str(index) + '\n')
            
# @bot.command()
# async def add_section(ctx, arg):
#     with open('class-index.txt', 'a') as f:
#         f.write(arg + '\n')
    
# @bot.command()
# async def remove_section(ctx):
#     await ctx.author.send('Enter the index number of the section you want to remove.')
    
#     index = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
#     index = index.content
    
#     desired_classes = config.load_desired_classes_from_file()
    
#     if index in desired_classes:
#         desired_classes.remove(index)
    
#     with open('class-index.txt', 'w') as f:
#         for index in desired_classes:
#             f.write(str(index) + '\n')
    
#     await ctx.author.send('Section removed.')

# @bot.command()
# async def purge_sections(ctx):
#     with open('class-index.txt', 'w') as f:
#         f.write('')
        
#     await ctx.author.send('All sections removed.')
    
# @bot.command()
# async def show_sections(ctx):
#     desired_classes = config.load_desired_classes_from_file()
    
#     await ctx.author.send('Your desired sections are:')
    
#     for index in desired_classes:
#         await ctx.author.send(index)

# @bot.command()
# async def create_config(ctx):
#     # Ask for year
#     await ctx.author.send('Enter the year:')
    
#     msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    
#     year = msg.content.strip()

#     # Ask for term
#     await ctx.author.send('Enter the term (spring, summer, fall, winter):')

#     while True:
#         msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        
#         term = msg.content.strip().lower()

#         if term == 'spring':
#             term = '1'
#             break
#         elif term == 'summer':
#             term = '7'
#             break
#         elif term == 'fall':
#             term = '9'
#             break
#         elif term == 'winter':
#             term = '0'
#             break
#         else:
#             await ctx.author.send('Invalid term. Please enter a valid term (spring, summer, fall, winter):')
#             continue

#     # Ask for campus
#     await ctx.author.send('Enter desired campus (New Brunswick, Newark, Camden):')

#     while True:
#         msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        
#         campus = msg.content.strip().lower()

#         if campus == 'new brunswick':
#             campus = 'NB'
#             break
#         elif campus == 'newark':
#             campus = 'NK'
#             break
#         elif campus == 'camden':
#             campus = 'CM'
#             break
#         else:
#             await ctx.author.send('Invalid campus. Please enter a valid campus (New Brunswick, Newark, Camden):')
#             continue

#     # Construct config dictionary
#     config = {
#         'year': year,
#         'term': term,
#         'campus': campus,
#     }

#     # Save config to file (optional)
#     with open('config.txt', 'w') as f:
#         for key, value in config.items():
#             f.write(f'{key}:{value}\n')

#     # Send confirmation message to user
#     await ctx.author.send('Configuration saved successfully.')
    
# @bot.command()
# async def leroysucks(ctx):
#     await ctx.send('No u.')

# bot.run(token)