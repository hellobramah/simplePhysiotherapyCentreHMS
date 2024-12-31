import os
import sys

base_dir = os.getenv('APP_BASE_DIR', '/default/path/to/app')
if not base_dir:
    raise RuntimeError("Environment variable APP_BASE_DIR is not set.")

sys.path.insert(0, base_dir)

activate_env = os.path.join(base_dir, os.getenv('VENV_RELATIVE_PATH', '../3.9/bin/activate_this.py'))
if os.path.exists(activate_env):
    with open(activate_env) as file_:
        exec(file_.read(), dict(__file__=activate_env))
else:
    raise RuntimeError(f"Virtual environment activation script not found at {activate_env}")

from main import app as application
