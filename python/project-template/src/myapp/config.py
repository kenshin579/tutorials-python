import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME: str = os.getenv("APP_NAME", "myapp")
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
