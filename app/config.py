from dotenv import load_dotenv
import os

load_dotenv()

settings = {
    "ENV": os.getenv("ENV", "development")
}
