from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient
client = MongoClient(os.getenv("MONGO_URI"))
db = client["smartdocumentmanager"]
def get_db_client():
    try:
        client.admin.command("ping")
        print("Database connected successfully")
        return client
    except Exception as e:
        print(e)
        return None

client = get_db_client()


