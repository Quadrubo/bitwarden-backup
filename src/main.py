from dotenv import load_dotenv
from notifier import Notifier
from notifiers.ntfy import NTFY
from notifiers.mock import Mock
from bitwarden import Bitwarden
import os
from datetime import datetime

load_dotenv()

# Path configuration
bw_binary = os.getenv("BW_BINARY")
backup_path = os.getenv("BACKUP_PATH")

# Bitwarden configuration
# authentication
bw_client_id = os.getenv("BW_CLIENT_ID")
bw_client_secret = os.getenv("BW_CLIENT_SECRET")
bw_master_password = os.getenv("BW_MASTER_PASSWORD")

# connection
bw_server = os.getenv("BW_SERVER")

# backups
backup_format = os.getenv("BACKUP_FORMAT")
backup_password = os.getenv("BACKUP_PASSWORD")
backup_organizations = os.getenv("BACKUP_ORGANIZATIONS")

# NTFY configuration
ntfy_server = os.getenv("NTFY_SERVER")
ntfy_topic = os.getenv("NTFY_TOPIC")
ntfy_username = os.getenv("NTFY_USERNAME")
ntfy_password = os.getenv("NTFY_PASSWORD")

def generate_output_path(path, current_time, organization_id = None):
    output_path = backup_path + "/bitwarden-encrypted_" + current_time

    if organization_id:
        output_path += "_" + organization_id

    output_path += ".json"

    return output_path

def inject_notifier():
    if ntfy_server and ntfy_topic:
        return NTFY(ntfy_server, ntfy_topic, ntfy_username, ntfy_password)
    else:
        return Mock()

def main(notifier: Notifier, bitwarden: Bitwarden, config):
    notifier.send_start()

    # Logout is needed before configuring the server
    bitwarden.logout()

    bitwarden.configure_server(config["bw_server"])

    bitwarden.login(config["bw_client_id"], config["bw_client_secret"])
    bitwarden.unlock(config["bw_master_password"])

    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    output_paths = []

    vault_output_path = generate_output_path(config["backup_path"], current_time)

    bitwarden.export(vault_output_path, config["backup_format"], config["backup_password"])

    output_paths.append(vault_output_path)

    if config["backup_organizations"]:
        backup_organizations = config["backup_organizations"].split(",")
    else:
        backup_organizations = []

    for organization_id in backup_organizations:
        organization_output_path = generate_output_path(config["backup_path"], current_time, organization_id)

        bitwarden.export(organization_output_path, config["backup_format"], config["backup_password"], organization_id)

        output_paths.append(organization_output_path)

    bitwarden.logout()

    notifier.send_success(output_paths)


if __name__ == "__main__":
    notifier = inject_notifier()
    main(
        notifier,
        Bitwarden(bw_binary),
        {
            "bw_server": bw_server,
            "bw_client_id": bw_client_id,
            "bw_client_secret": bw_client_secret,
            "bw_master_password": bw_master_password,
            "backup_path": backup_path,
            "backup_format": backup_format,
            "backup_password": backup_password,
            "backup_organizations": backup_organizations
        }
    )