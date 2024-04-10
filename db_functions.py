import pymongo
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()
DB_TOKEN = os.getenv('DATABASE_TOKEN')

cluster = DB_TOKEN
print(DB_TOKEN)
client = MongoClient(cluster)

# db will be the way that we refer to the database from here on out.
DB = client["marinahacks_participants"]


def add_student(db):
    """
    :param collection:  The pointer to the students collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    collection = db["students"]
    unique_student_id: bool = False
    unique_email: bool = False
    unique_username: bool = False
    last_name: str = ''
    first_name: str = ''
    student_id: str = -1
    email: str = ''
    discord_username: str = ''
    discord_role: str = ''
    

    while True:
        try:
            first_name = input("First name --> ")
            last_name = input("Last name --> ")
            student_id = int(input("Student ID --> "))
            email = input("Student email --> ")
            discord_username = input("Discord username --> ")
            discord_role = input("Discord role --> ")

            id_count = collection.count_documents({"student_id": student_id})
            unique_student_id = id_count == 0

            if not unique_student_id:
                print("We already have a student with that student ID.  Try again.")
                continue

            email_count = collection.count_documents({"email": email})
            unique_email = email_count == 0

            if not unique_email:
                print("We already have a student with that email.  Try again.")
                continue

            username_count = collection.count_documents({"discord_username": discord_username})
            unique_username = username_count == 0

            if not unique_username:
                print("We already have a student with that discord username.  Try again.")
                continue

            student = {
                "first_name": first_name,
                "last_name": last_name,
                "student_id": student_id,
                "email": email,
                "discord_username": discord_username,
                "discord_role": discord_role
            }

            create_student_collection()

            collection.insert_one(student)
            print("student added!")
            break

        except Exception as e:
            # print a user-friendly message instead of the traceback string
            print("An error occurred:", end=" ")
            error_str = str(e)
            print(error_str)

            # if "'_id'" in error_str:
            #     print("student id error")
            #
            # if "'last_name'" in error_str:
            #     print("Inputted value for the 'last_name' field is invalid due "
            #           "to violation of validation constraint. {}".format(error_str))
            #
            # elif "'first_name'" in error_str:
            #     print("Inputted value for the 'student_name' field is invalid due to violation of "
            #           "validation constraint. {}".format(error_str))
            #
            # elif "'eMail'" in error_str:
            #     print("Inputted value for the 'eMail' field is invalid due to violation of "
            #           "validation constraint. {}".format(error_str))

            print("Please try again.")



def create_student_collection():
    # Create the student schema

    student_validator = {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'An individual who may or may not be enrolled at the university, who enrolls in '
                           'courses toward some educational objective.  That objective could be a formal '
                           'degree program, or it could be a specialized certificate.',
            'required': ['student_id', 'last_name', 'first_name', 'email', 'discord_username', 'discord_role'],
            'properties': {
                'student_id': {
                    'bsonType': 'int',
                    'description': 'student identification provided by the school',
                    'minLength': 7,
                    'maxLength': 9
                },
                'first_name': {
                    'bsonType': 'string',
                    'description': 'given name of the student',
                    'minLength': 2,
                    'maxLength': 50
                },
                'last_name': {
                    'bsonType': 'string',
                    'description': 'surname of the student',
                    'minLength': 2,
                    'maxLength': 50
                },
                'email': {
                    'bsonType': 'string',
                    'description': 'electronic mail address of the student',
                    'maxLength': 255
                }, 
                'discord_username': {
                    'bsonType': 'string',
                    'description': 'will be used for adding role to student',
                    'maxLength': 255
                },
                'discord_role': {
                    'bsonType': 'string',
                    'description': 'the role that will be given to the student',
                    'maxLength': 255, 
                    'enum': ['Hacker', 'Guest Speaker', 'Sponsor', 'Judge', 'Committee Member']
                }
            }
        }
    }

    if "students" not in DB.list_collection_names():
        DB.create_collection("students", validator=student_validator)
    else:
        # collMod command on the departments collection is used to modify properties of an existing collection
        # when this command is executed, the departments schema will be set as the validator for the collection.
        DB.command("collMod", "students", validator=student_validator)

    # Uniqueness Constraints
    DB['students'].create_index([('student_id', pymongo.ASCENDING)], unique=True)
    DB['students'].create_index([('email', pymongo.ASCENDING)], unique=True)
    DB['students'].create_index([('discord_username', pymongo.ASCENDING)], unique=True)

    print("student uniqueness constraints added to students collection")


def search_collection(collection, keyword):
    # 
    document = collection.find_one(keyword)
    if document:
        return document
    else:
        return None


def get_user_discord(username):
    for collection_name in DB.list_collection_names():
        collection = DB[collection_name]
        user = search_collection(collection, {'discord_username': username})
        if user:
            return user
    return None


def get_user_roles(username) -> list:
    # Iterate over all collections in the database
    all_roles = []
    for collection_name in DB.list_collection_names():
        collection = DB[collection_name]
        user_found = search_collection(collection, {'discord_username': username})
        if user_found:
            all_roles.append(user_found['discord_role'])
    if all_roles: # If not empty
        return all_roles
    else:
        return None

if __name__ == '__main__':
    print("Running db_functions.py means you want to add a student manually.")
    add_student(DB)
    print()