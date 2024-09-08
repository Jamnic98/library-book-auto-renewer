from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "ENV": os.getenv("ENV", "development"),
    "LIBRARY_URL": os.getenv("LIBRARY_URL"),
    "USER_NAME": os.getenv("USER_NAME"),
    "PASSWORD": os.getenv("PASSWORD"),
    "CHROME_DRIVER_LOCATION": os.getenv("CHROME_DRIVER_LOCATION")
}
