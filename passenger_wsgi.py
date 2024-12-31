import os
import sys

# Adjust to your symlink path
app_path = os.getenv('APP_ROOT', '/home/hwzfvzql/repositories/simplePhysiotherapyCentreHMS')

if not app_path:
    raise RuntimeError("APP_ROOT environment variable not set.")

sys.path.insert(0, app_path)

from main import app as application
