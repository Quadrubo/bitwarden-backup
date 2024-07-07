import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv
from bitwarden import Bitwarden

load_dotenv()

BW_BINARY = os.getenv("BW_BINARY")

BACKUP_PATH = os.getenv("BACKUP_PATH")

CLIENT_ID = os.getenv("BW_CLIENT_ID")
CLIENT_SECRET = os.getenv("BW_CLIENT_SECRET")
MASTER_PASSWORD = os.getenv("BW_MASTER_PASSWORD")

BACKUP_FORMAT = os.getenv("BACKUP_FORMAT")
BACKUP_PASSWORD = os.getenv("BACKUP_PASSWORD")

SERVER = os.getenv("BW_SERVER")

bitwarden = Bitwarden(BW_BINARY)

# Logout is needed before configuring the server
bitwarden.logout()

bitwarden.configure_server(SERVER)

bitwarden.login(CLIENT_ID, CLIENT_SECRET)
bitwarden.unlock(MASTER_PASSWORD)

current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
output = BACKUP_PATH + "/bitwarden-encrypted-" + current_time + ".json"

bitwarden.export(output, BACKUP_FORMAT, BACKUP_PASSWORD)

bitwarden.logout()