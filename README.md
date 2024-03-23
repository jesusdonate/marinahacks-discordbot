# marinahacks-discordbot
MarinaHacks' discord bot is used for giving roles to new discord users on the MarinaHacks discord server. It uses a personal MongoDB database to determine what role new users are assigned to.
### How to set-up environment
1. Open terminal and enter these installations
 `pip install discord`, `pip install pymongo`, `pip install python-dotenv`
2. Create a new file called `.env`. This file will store the tokens for connecting with the dicord bot and database.
3. Ask author (jesusdonate) for the discord bot token and database token. The tokens should be named DISCORD_TOKEN and DATABASE_TOKEN and should be stored inside of the `.env` file. 
4. Make sure `.env` is in .gitignore. If not, type `.env` inside of it and save file. DO NOT HARD CODE THE TOKENS SINCE THIS REPOSITORY IS PUBLIC AND OTHER UNAUTHORIZED USERS WILL SEE IT!!!

Note: If you want access to the MongoDB database, ask me to invite you to the project.