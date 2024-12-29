from dotenv import load_dotenv

load_dotenv()
import os
import sys

project_path = os.getenv('PROJECT_PATH', '/home/default_placeholder_path/public_html/seaside-hms')
sys.path.insert(0, project_path)

from main import app as application
