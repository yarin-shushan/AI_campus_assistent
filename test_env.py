import os
from dotenv import load_dotenv

load_dotenv()
print("SYS:", os.getenv("SYSTEM_PROMPT"))
print("TOOL:", os.getenv("TOOL_PROMPT"))
print("DB:", os.getenv("DB_SCHEMA"))
