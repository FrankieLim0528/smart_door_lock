import os

# project root
current_dir = os.getcwd()
ROOT_DIR = os.path.dirname(os.path.dirname(current_dir))

# folder to store user's data
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# passphrase related
MAX_ATTEMPTS = 3
LOCKDOWN_PERIOD = 5 * 60        # 5 minutes