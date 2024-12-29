from dotenv import load_dotenv
load_dotenv()

import os
import sys

project_path = os.getenv('PROJECT_PATH', '/default/path')
sys.path.insert(0, project_path)
