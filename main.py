import os
import db_functions as db
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Member, Reaction

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Role IDs:
roles_array = []
HACKER_ID = 1217710575153446943
SPONSOR_ID = 1219805305547001938
GUEST_SPEAKER_ID = 1220822872172400752
JUDGE_ID = 1220823893149745233
COMMITTEE_MEMBER_ID = 1217712596556189778
VERIFIED_ID = 1217711607140843610
ADMIN_ID = 1227752395879088168
switch_roles = {
    'Hacker': HACKER_ID,
    'Sponsor': SPONSOR_ID,
    'Guest Speaker': GUEST_SPEAKER_ID,
    'Judge': JUDGE_ID,
    'Committee Member': COMMITTEE_MEMBER_ID
}

intents: Intents = discord.Intents.all()
client: Client = Client(intents=intents)

# @client.event
# async def on_member_join(member: Member):
#     print(f'{member} has joined the server.')
#     user = db.get_user_discord(member.name)
#     if user == None: # username not in database. Maybe try user display name
#         user = db.get_user_discord(member.display_name)
#     if user == None:
#         return # Have only @Everyone permissions.
    
#     role_ids = []
#     user_roles = db.get_user_roles(user['discord_username'])
    
#     for role in user_roles:
#         # Fetch the appropriate Role ID. Fallback to a default role (Verified) if none is found.
#         role_ids.append(switch_roles.get(role))


#     if role_ids != []:
#         roles = [member.guild.get_role(role_id) for role_id in role_ids]
#     role_names = list(role.name for role in roles)

#     # Check if the role exists
#     if roles:
#         # If the role exists, assign it to the member
#         await member.add_roles(*roles)
#         print(f"Assigned {role_names} to {member.display_name}")

#     else:
#         # If the role doesn't exist, you might want to log this information.
#         print(f"Role with ID {role_ids} not found.")


@client.event
async def on_raw_reaction_add(payload):
    if payload.guild_id is not None:
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is None or member.bot:
            return
        SPECIFIC_MESSAGE_ID = 1227711533866287194
        if payload.message_id == SPECIFIC_MESSAGE_ID:

            if payload.emoji.name != "sharkira":
                return # Do nothing if not sharkira
            
            print(f'{member} has accepted the rules.')
            user = db.get_user_discord(member.name)
            if user == None: # username not in database. Maybe try user display name
                user = db.get_user_discord(member.display_name)
            
            if user:
                user_roles = db.get_user_roles(user['discord_username'])

            role_ids = []
            for role in user_roles:
                # Fetch the appropriate Role ID. Fallback to a default role (Verified) if none is found.
                role_ids.append(switch_roles.get(role))
            
            # All people get verified if they accept the rules
            role_ids.append(VERIFIED_ID)

            if role_ids != []:
                roles = [member.guild.get_role(role_id) for role_id in role_ids]
            role_names = list(role.name for role in roles)

            # Check if the role exists
            if roles:
                # If the role exists, assign it to the member
                await member.add_roles(*roles)
                print(f"Assigned {role_names} to {member.display_name}")

            else:
                # If the role doesn't exist, you might want to log this information.
                print(f"Role with ID {role_ids} not found.")


@client.event
async def on_raw_reaction_remove(payload):
    if payload.guild_id is not None:
        guild = client.get_guild(payload.guild_id)

        # Fetch the member from the guild using the user ID from the payload
        member = await guild.fetch_member(payload.user_id)

        if member is None or member.bot:
            return

        SPECIFIC_MESSAGE_ID = 1227711533866287194
        if payload.message_id == SPECIFIC_MESSAGE_ID:
            if payload.emoji.name != "sharkira":
                return  # Do nothing if not the specified emoji
            
            print(f'{member} has removed their acceptance of the rules.')

            # Exclude @everyone role and the Admin role
            ADMIN_ROLE_ID = 1227752395879088168
            roles_to_remove = [role for role in member.roles if role.id != ADMIN_ID and role != guild.default_role]
            
            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)
                print(f"All roles, except Admin, have been removed from {member.display_name}.")



# @client.event
# async def on_presence_update(member: Member, before):
#     print(f'{member} has updated their presence status.')
#     if member.bot:
#         return  # Ignore updates from bots

#     # Getting member name
#     print("Getting member name...")
    
#     # Fetching roles
#     print("Fetching roles...")

#     # Get user information from the database
#     user = db.get_user_discord(member.name)
#     print(f'Found User: {member}')
#     display = member.display_name
#     if user is None:
#         print(f'Using display name {display}.')
#         user = db.get_user_discord(member.display_name)    

#     print(f'{user}')
#     # Fetch the appropriate Role ID. Fallback to a default if none is found.
#     user_role_id = switch_roles.get(user['discord_role'], VERIFIED_ID)

#     # use 'await' to fetch the role as it's an asynchronous operation
#     role = member.guild.get_role(user_role_id)
#     print(role)

#     # Check if the role exists
#     if role:
#         # If the role exists, assign it to the member
#         await member.add_roles(role)
#         print(f"Assigned {role.name} to {member.display_name}")
#     else:
#         # If the role doesn't exist, you might want to log this information.
#         print(f"Role with ID {user_role_id} not found.")

#     # Check if the role exists
#     if role:
#         # If the role exists, assign it to the member
#         await member.add_roles(role)
#         print(f"Assigned {role.name} to {member.display_name}")
#     else:
#         # If the role doesn't exist, you might want to log this information.
#         print(f"Role with ID {user_role_id} not found.")
    


@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')



def start_bot() -> None:
    client.run(token=TOKEN)



if __name__ == '__main__':
    start_bot()