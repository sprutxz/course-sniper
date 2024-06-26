import config
import clsretrieval
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_ERROR
from discord.ext import tasks
import discord

USR_ID = 451248085360967681

#opening the file that stores the bot token
with open('token.txt', 'r') as f:
    token = f.read().strip()

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.check_for_new_sections.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=2)
    async def check_for_new_sections(self):
        print('Checking for new sections...')
        desired_sections = config.load_desired_classes_from_file()
        open_sections = clsretrieval.get_open_classes()
        
        indexes = clsretrieval.check_open_classes(open_sections, desired_sections)
        
        if indexes:
            print('New sections found!')
            for index in indexes:
                print(f'Index: {index}')
                
                # Send a message to the user
                user = await self.fetch_user(USR_ID)
                await user.send(f'New section found: {index}')
                
                # Remove the section from the text file
                desired_sections.remove(index)
                with open('class-index.txt', 'w') as f:
                    for index in desired_sections:
                        f.write(str(index) + '\n')
                
        print('Done checking for new sections.')

    @check_for_new_sections.before_loop
    async def before(self):
        await self.wait_until_ready()
    
client = MyClient(intents=discord.Intents.default())
client.run(token)
