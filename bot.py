"""
The main module that runs the discord bot.
The bot constantly checks for new sections and sends a message to the user if a new section is found.
It also allows the user to use various commands, which can be found through '>help'.
"""

import discord
from discord.ext import commands, tasks
import asyncio
from aiofiles import open as aio_open
import json

import config_loader
import clsretrieval

import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")


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
        self.file_lock = asyncio.Lock() 
    
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
        print('Checking for new sections...')
        
        user_data = config_loader.load_desired_classes_from_file() #loading the classes to snipe
        
        open_sections = clsretrieval.get_open_classes() # finding the open sections on Rutgers SOC
        
        tasks = []
        
        for user in user_data['users']:
            
            task = asyncio.create_task(self.check_open_sections_and_notify(user, open_sections))
            
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        
    # Helper method
    async def check_open_sections_and_notify(self, user, open_sections):
        """Check if the desired sections are open and notify the user"""
        
        
        user_id = user['usr_id']
        desired_sections = user['desired_sections']
        
        
        indexes = clsretrieval.check_open_classes(open_sections, desired_sections)
        
        if indexes:
            print(f'New open sections found for user {user_id}!')
            
            params = config_loader.load_config_from_file()
            semester = params['term'] + params['year']
            
            for index in indexes:
                url = f'https://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&semesterSelection={semester}&indexList={index}'
                
                # Send a message to the user
                user = await self.fetch_user(user_id)
                await user.send(f'Open Section: {index} \nRegistration url: {url}')
                
                # Remove the section from the text file
                await self.remove_section(user_id, index)
    
    # Helper method
    async def remove_section(self, user_id, section):
        """Remove the section from the text file"""
        
        async with self.file_lock:
            # Load data from file
            with open('class-index.json', 'r') as f:
                user_data = json.load(f)
            
            # Find the user and remove the section
            for user in user_data['users']:
                if user['usr_id'] == user_id:
                    user['desired_sections'].remove(section)
                    break
            
            # Write updated data back to file
            async with aio_open('class-index.json', 'w') as f:
                await f.write(json.dumps(user_data, indent=4))
    
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
                      description='Add a section to snipe',
                      )
    
    async def add_section(self, ctx, arg):
        
        desired_classes = config_loader.load_desired_classes_from_file()
        
        existing_user = False
        for usr in desired_classes['users']:
            if usr['usr_id'] == ctx.author.id:
                usr['desired_sections'].append(arg)
                existing_user = True
                break
        
        if not existing_user:
            desired_classes['users'].append({
                'usr_id': ctx.author.id,
                'desired_sections': [arg]
            })
            
        with open('class-index.json', 'w') as f:
            json.dump(desired_classes, f, indent=4)
        
        await ctx.send(f'Section {arg} has been added to the list')
    
    # Remove a section to snipe
    @commands.command(name='remove',
                      brief='Usage: >remove <section>',
                      description='Remove a section to snipe')
    async def remove_section(self, ctx, arg):
        desired_classes = config_loader.load_desired_classes_from_file()
        
        for usr in desired_classes['users']:
            if usr['usr_id'] == ctx.author.id:
                usr['desired_sections'].remove(arg)
                break
            
        with open('class-index.json', 'w') as f:
            json.dump(desired_classes, f, indent=4)
        
        await ctx.send(f'Section {arg} has been removed from the list')
    
    # Remove all sections to snipe
    @commands.command(name='purge',
                      brief='Usage: >purge',
                      description='Remove all sections from the sniping list')
    async def purge_sections(self, ctx):
        desired_classes = config_loader.load_desired_classes_from_file()
        
        for usr in desired_classes['users']:
            if usr['usr_id'] == ctx.author.id:
                usr['desired_sections'] = []
                break
            
        with open('class-index.json', 'w') as f:
            json.dump(desired_classes, f, indent=4)
        
        await ctx.send('All sections have been removed)')
        
    # List all sections that are being sniped
    @commands.command(name='sniped',
                      brief='Usage: >sniped',
                      description='List all sections that are being sniped')
    async def list_sections(self, ctx):
        desired_classes = config_loader.load_desired_classes_from_file()
        
        for usr in desired_classes['users']:
            if usr['usr_id'] == ctx.author.id:
                sections = usr['desired_sections']
                break
            
        if not sections:
            await ctx.send('No sections are being sniped')
            return
        
        await ctx.send('Sections being sniped:')
        for section in sections:
            await ctx.send(section)
    
    @commands.command(name='create_config',
                      breif='Usage: >create_config',
                      description='Create a config file to set the year, semester, and campus'
                      
    )
    async def create_config(self,ctx):
        if ctx.author.id != 451248085360967681:
            await ctx.send('You do not have permission to use this command')
            return
        
        config = {}
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
            
        config['year'] = year.content
        config['term'] = semester
        config['campus'] = campus
        
        with open('config.json', 'w') as f:
            json.dump(config, f)
            
            
        await ctx.send('Config file created')    

# Creating the bot
bot = MyBot(command_prefix='!', intents=intents)

# Adding the Cog
async def main():
    async with bot:
        await bot.add_cog(Commands(bot))
        await bot.start(token)

# Running the bot
if __name__ == "__main__":
    asyncio.run(main())