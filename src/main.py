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

def generate_output_path(path, current_time, organization_id = None):
    output_path = BACKUP_PATH + "/bitwarden-encrypted_" + current_time

    if organization_id:
        output_path += "_" + organization_id

    output_path += ".json"

    return output_path

current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
output = BACKUP_PATH + "/bitwarden-encrypted-" + current_time + ".json"

bitwarden.export(generate_output_path(BACKUP_PATH, current_time), BACKUP_FORMAT, BACKUP_PASSWORD)

BACKUP_ORGANIZATIONS = os.getenv("BACKUP_ORGANIZATIONS").strip()

if (BACKUP_ORGANIZATIONS):
  BACKUP_ORGANIZATIONS = BACKUP_ORGANIZATIONS.split(",")
else:
  BACKUP_ORGANIZATIONS = []

for organization_id in BACKUP_ORGANIZATIONS:
    bitwarden.export(generate_output_path(BACKUP_PATH, current_time, organization_id), BACKUP_FORMAT, BACKUP_PASSWORD, organization_id)    

bitwarden.logout()