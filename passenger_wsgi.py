import os
import sys


app_path = os.getenv('APP_PATH')
if not app_path:
    raise RuntimeError("Environment variable APP_PATH is not set.")

sys.path.insert(0, app_path)

# Load the application
from main import app as application  