import os
from bitwarden import Bitwarden
from notifier import Notifier
from dotenv import load_dotenv
from datetime import datetime


class Backup:
    def __init__(self, bitwarden: Bitwarden, notifier: Notifier):
        self.bitwarden = bitwarden
        self.notifier = notifier

        self.export_timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        load_dotenv()

        self.backup_path = os.getenv("BACKUP_PATH")
        self.backup_format = os.getenv("BACKUP_FORMAT")
        self.backup_password = os.getenv("BACKUP_PASSWORD")

        backup_organizations = os.getenv("BACKUP_ORGANIZATIONS").strip()

        if backup_organizations:
            self.backup_organizations = backup_organizations.split(",")
        else:
            self.backup_organizations = []

    def generate_export_filename(self, organization_id=None):
        filename = "bitwarden-encrypted_" + self.export_timestamp

        if organization_id:
            filename += "_" + organization_id

        filename += ".json"

        return filename

    def generate_export_path(self, organization_id=None):
        return self.backup_path + "/" + self.generate_export_filename(organization_id)

    def start(self):
        export_files = []

        self.notifier.send_start()

        # Logout is needed before configuring the server
        self.bitwarden.logout()

        self.bitwarden.configure_server()
        self.bitwarden.login()
        self.bitwarden.unlock()

        self.bitwarden.export(
            self.generate_export_path(),
            self.backup_format,
            self.backup_password
        )

        export_files.append(self.generate_export_filename())

        for organization_id in self.backup_organizations:
            self.bitwarden.export(
                self.generate_export_path(organization_id),
                self.backup_format,
                self.backup_password
            )

            export_files.append(self.generate_export_filename(organization_id))

        self.bitwarden.logout()

        self.notifier.send_success(export_files)
