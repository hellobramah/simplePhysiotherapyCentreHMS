import os
import sys

# Dynamically resolve the application path
app_path = os.getenv('APP_PATH')
if not app_path:
    raise RuntimeError("Environment variable APP_PATH is not set.")

sys.path.insert(0, app_path)

# Load the application
from main import app as application  # Ensure `main.py` contains your Flask app instance