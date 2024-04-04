import os
import db_functions as db
from dotenv import load_dotenv
from discord import Intents, Client, Member

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
switch_roles = {
    'Hacker': HACKER_ID,
    'Sponsor': SPONSOR_ID,
    'Guest Speaker': GUEST_SPEAKER_ID,
    'Judge': JUDGE_ID,
    'Committee Member': COMMITTEE_MEMBER_ID
}

intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
client: Client = Client(intents=intents)

@client.event
async def on_member_join(member: Member):
    print(f'{member} has joined the server.')
    user = db.get_user(member.name)
    if user == None: # username not in database. Maybe try user display name
        user = db.get_user(member.display_name)
    if user == None:
        return # Have only @Everyone permissions.
    
    # Fetch the appropriate Role ID. Fallback to a default role (Verified) if none is found.
    user_role_id = switch_roles.get(user['discord_role'], VERIFIED_ID)

    role = member.guild.get_role(user_role_id)
    
    # All users are verified, expect if their username is not on the database
    verified = member.guild.get_role(VERIFIED_ID)
    await member.add_roles(verified)

    # Check if the role exists
    if role:
        # If the role exists, assign it to the member
        await member.add_roles(role)
        print(f"Assigned {role.name} to {member.display_name}")
    else:
        # If the role doesn't exist, you might want to log this information.
        print(f"Role with ID {user_role_id} not found.")



@client.event
async def on_presence_update(member: Member, before):
    print(f'{member} has updated their presence status.')
    if member.bot:
        return  # Ignore updates from bots

    # Getting member name
    print("Getting member name...")
    
    # Fetching roles
    print("Fetching roles...")

    # Get user information from the database
    user = db.get_user(member.name)
    print(f'Found User: {member}')
    display = member.display_name
    if user is None:
        print(f'Using display name {display}.')
        user = db.get_user(member.display_name)    

    print(f'{user}')
    # Fetch the appropriate Role ID. Fallback to a default if none is found.
    user_role_id = switch_roles.get(user['discord_role'], VERIFIED_ID)

    # use 'await' to fetch the role as it's an asynchronous operation
    role = member.guild.get_role(user_role_id)
    print(role)

    # Check if the role exists
    if role:
        # If the role exists, assign it to the member
        await member.add_roles(role)
        print(f"Assigned {role.name} to {member.display_name}")
    else:
        # If the role doesn't exist, you might want to log this information.
        print(f"Role with ID {user_role_id} not found.")

    # Check if the role exists
    if role:
        # If the role exists, assign it to the member
        await member.add_roles(role)
        print(f"Assigned {role.name} to {member.display_name}")
    else:
        # If the role doesn't exist, you might want to log this information.
        print(f"Role with ID {user_role_id} not found.")
    


@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')



def start_bot() -> None:
    client.run(token=TOKEN)



if __name__ == '__main__':
    start_bot()