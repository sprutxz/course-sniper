Course-Sniper is a discord bot developed in python to snipe courses for Rutgers. It checks for open sections every 2 seconds (Because 1 second was too fast for the API) and notifies the user about an open section with the link the register for the class.

`config_loader.py` contains some helper methods to load various information

`clsretrieval.py` is a module containing functions that makes the API calls and checks for open sections

`bot.py` is the main bot file that is responsible for the complete functioning of the bot

### Running the Bot

#### Setup
The dependencies managed in `pyproject.toml` can be installed through poetry by using 'poetry install'.

Use a virtual environment to prevent polluting the global environment with necessary packages causing conflicts.

#### Run

To run the course-sniper, invite the bot to a discord server through this [invite link](https://discord.com/oauth2/authorize?client_id=1255239764005748826&permissions=124928&integration_type=0&scope=bot) and then create a private dm with the bot (I do not know how to create a private DM without inviting the bot to the server first).

After activating the virtual environment where the dependencies are downloaded, run the `bot.py` file using `$ python3 bot.py` in the command line
