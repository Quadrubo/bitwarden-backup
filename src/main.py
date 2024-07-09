from dotenv import load_dotenv
from notifiers.ntfy import NTFY
from notifiers.mock import Mock
from bitwarden import Bitwarden
import os
from backup import Backup
from cli import CLI

load_dotenv()


def inject_cli():
    bw_binary = os.getenv("BW_BINARY")

    return CLI(bw_binary)


def inject_bitwarden(cli: CLI):
    bw_binary = os.getenv("BW_BINARY")
    bw_server = os.getenv("BW_SERVER")
    bw_client_id = os.getenv("BW_CLIENT_ID")
    bw_client_secret = os.getenv("BW_CLIENT_SECRET")
    bw_master_password = os.getenv("BW_MASTER_PASSWORD")

    return Bitwarden(cli, bw_server, bw_client_id, bw_client_secret, bw_master_password)


def inject_notifier():
    ntfy_server = os.getenv("NTFY_SERVER")
    ntfy_topic = os.getenv("NTFY_TOPIC")
    ntfy_username = os.getenv("NTFY_USERNAME")
    ntfy_password = os.getenv("NTFY_PASSWORD")

    if ntfy_server and ntfy_topic:
        return NTFY(ntfy_server, ntfy_topic, ntfy_username, ntfy_password)
    else:
        return Mock()


def main():
    cli = inject_cli()
    bitwarden = inject_bitwarden(cli)
    notifier = inject_notifier()

    backup = Backup(
        bitwarden,
        notifier
    )

    backup.start()


if __name__ == "__main__":
    main()
