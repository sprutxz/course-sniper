### Overview

Course-Sniper is a discord bot developed in python to snipe courses for Rutgers. It checks for open sections every 2 seconds (Because 1 second was too fast for the API) and notifies the user about an open section with the link the register for the class.

`config_loader.py` contains some helper methods to load various information

`clsretrieval.py` is a module containing functions that makes the API calls and checks for open sections

`bot.py` is the main bot file that is responsible for the complete functioning of the bot

### Running the Bot


#### Setup
The dependencies managed in `pyproject.toml` can be installed through poetry by using 'poetry install'.

Use a virtual environment to prevent polluting the global environment with necessary packages causing conflicts.

Crete a .env file that stores the bot api token.

#### Run

To run the course-sniper, invite the bot you created to a discord server through and then create a private DM with the bot (I do not know how to create a private DM without inviting the bot to the server first).

After activating the virtual environment where the dependencies are downloaded, run the `bot.py` file using `$ python3 bot.py` in the command line

Make sure to use the command `>help` to understand how the bot commands work.
Use `>create_config` before adding any sections to snipe.
