from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "ENV": os.getenv("ENV", "dev"),
    "LIBRARY_URL": os.getenv("LIBRARY_URL"),
    "USER_NAME": os.getenv("USER_NAME"),
    "PASSWORD": os.getenv("PASSWORD"),
    'SENDER_EMAIL_ADDRESS': os.getenv('SENDER_EMAIL_ADDRESS')
}
