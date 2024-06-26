"""
The main module that runs the discord bot.
The bot constantly checks for new sections and sends a message to the user if a new section is found.
It also allows the user to use various commands, which can be found through '>help'.
"""

import discord
from discord.ext import commands, tasks
import asyncio

import config_loader
import clsretrieval

# Opening the file that stores the bot token
with open('token.txt', 'r') as f:
    token = f.read().strip()
    
# loading the usr-id to send the message to
with open('usr-id.txt', 'r') as f:
    USR_ID = int(f.read().strip())

#setting up the intents
intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    """
    This is the main class responsible for the functioning of the bot. 
    It initializes the bot and starts the task to check for new sections every 2 seconds.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # Logging
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        
    async def setup_hook(self) -> None:
        # Start the task to run in the background
        self.check_for_new_sections.start()
    
    # Open Section checker task that runs every 2 seconds
    @tasks.loop(seconds=2)
    async def check_for_new_sections(self):
        
        desired_sections = config_loader.load_desired_classes_from_file() #loading the classes to snipe
        
        open_sections = clsretrieval.get_open_classes() # finding the open sections on Rutgers SOC
        
        indexes = clsretrieval.check_open_classes(open_sections, desired_sections) # checking if the desired sections are open
        
        # If new sections are found, send a message to the user
        if indexes:
            print('New open sections found!')
            
            params = config_loader.load_config_from_file()
            semester = params['term'] + params['year']
            
            for index in indexes:
                
                url = f'https://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&semesterSelection={semester}&indexList={index}'
                
                # Send a message to the user
                user = await self.fetch_user(USR_ID)
                await user.send(f'Open Section: {index} \n url: {url}')
                
                # Remove the section from the text file
                desired_sections.remove(index)
                with open('class-index.txt', 'w') as f:
                    for index in desired_sections:
                        f.write(str(index) + '\n')
    
    # wait for bot to initialize before starting the task
    @check_for_new_sections.before_loop
    async def before(self):
        await self.wait_until_ready()

class Commands(commands.Cog):
    """
    This class contains the commands that the user can use to interact with the bot.
    """
    def __init__(self, bot):
        self.bot = bot
    
    # Add a section to snipe
    @commands.command(name='add',
                      brief='Usage: >add <section>',
                      description='Add a section to snipe')
    
    async def add_section(self, ctx, arg):
        with open('class-index.txt', 'a') as f:
            f.write(arg + '\n')
        
        await ctx.send(f'Section {arg} has been added to the list')
    
    # Remove a section to snipe
    @commands.command(name='remove',
                      brief='Usage: >remove <section>',
                      description='Remove a section to snipe')
    async def remove_section(self, ctx, arg):
        desired_classes = config_loader.load_desired_classes_from_file()
        
        if arg in desired_classes:
            desired_classes.remove(arg)
        
        with open('class-index.txt', 'w') as f:
            for index in desired_classes:
                f.write(str(index) + '\n')
        
        await ctx.send(f'Section {arg} has been removed from the list')
    
    # Remove all sections to snipe
    @commands.command(name='purge',
                      brief='Usage: >purge',
                      description='Remove all sections from the sniping list')
    async def purge_sections(self, ctx):
        with open('class-index.txt', 'w'):
            pass
        
        await ctx.send('All sections have been removed)')
        
    # List all sections that are being sniped
    @commands.command(name='sniped',
                      brief='Usage: >sniped',
                      description='List all sections that are being sniped')
    async def list_sections(self, ctx):
        desired_classes = config_loader.load_desired_classes_from_file()
        await ctx.send(f'Desired Sections: {desired_classes}')
    
    @commands.command()
    async def create_config(self,ctx):
        await ctx.send('Enter the year the semester starts (YYYY):')
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        year = await bot.wait_for('message', check=check)
        
        while True:
            await ctx.send('Enter the semester you are sniping classes for (Winter, Spring, Summer, Fall):')
            semester = await bot.wait_for('message', check=check)
            
            semester = semester.content.lower()
            if semester == 'winter':
                semester = '0'
                break
            
            elif semester == 'spring':
                semester = '1'
                break
            
            elif semester == 'summer':
                semester = '7'
                break
            
            elif semester == 'fall':
                semester = '9'
                break
            
            else:
                await ctx.send('Invalid semester')
                continue
        
        while True:
            await ctx.send('Enter the campus (New Brunswick, Newark, Camden):')
            campus = await bot.wait_for('message', check=check)
            
            campus = campus.content.lower()
            
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
                await ctx.send('Invalid campus')
                continue
            
        
        with open('config.txt', 'w') as f:
            f.write(f'year:{year.content}\n')
            f.write(f'term:{semester}\n')
            f.write(f'campus:{campus}\n')
            
        await ctx.send('Config file created')    

# Creating the bot
bot = MyBot(command_prefix='>', intents=intents)

# Adding the Cog
async def main():
    async with bot:
        await bot.add_cog(Commands(bot))
        await bot.start(token)

# Running the bot
if __name__ == "__main__":
    asyncio.run(main())