import subprocess
import os
import json
import re
from cli import CLI


class Bitwarden:
    def __init__(self, cli: CLI, server, client_id, client_secret, master_password):
        self.cli = cli
        self.server = server
        self.client_id = client_id
        self.client_secret = client_secret
        self.master_password = master_password
        self.session_key = None

    def get_client_environment(self):
        if not self.client_id or not self.client_secret:
            raise Exception("Client id or client secret not set.")

        environment = os.environ.copy()
        environment["BW_CLIENTID"] = self.client_id
        environment["BW_CLIENTSECRET"] = self.client_secret

        return environment

    def get_password_environment(self):
        if not self.master_password:
            raise Exception("Master password not set.")

        environment = os.environ.copy()
        environment["BW_PASSWORD"] = self.master_password

        return environment

    def get_session_environment(self):
        if not self.session_key:
            raise Exception("Session key not set. Please login & unlock first.")

        environment = os.environ.copy()
        environment["BW_SESSION"] = self.session_key

        return environment

    def configure_server(self):
        if self.status() != 'unauthenticated':
            print("Already authenticated. Please logout first.")
            return

        self.cli.execute("config", ["server", self.server])

    def status(self):
        stdout, stderr = self.cli.execute('status')

        status = json.loads(stdout)['status']

        return status

    def login(self):
        if self.status() != 'unauthenticated':
            print("Already authenticated. Please logout first.")
            return

        environment = self.get_client_environment()

        self.cli.execute("login", ["--apikey"], environment)

    def logout(self):
        if self.status() == 'unauthenticated':
            print("Already unauthenticated. Please login first.")
            return

        self.cli.execute("logout")

    def unlock(self):
        if self.status() == 'unlocked':
            print("Already unlocked. Please lock first.")
            return

        environment = self.get_password_environment()

        stdout, stderr = self.cli.execute("unlock", ["--passwordenv", "BW_PASSWORD"], environment)

        if "Invalid master password." in stderr:
            raise Exception("Invalid master password.")

        session_key = re.search(r'(?<=BW_SESSION=").*?(?=")', stdout).group(0)

        self.session_key = session_key

    def export(self, output, cfg_format, password=None, organization_id=None):
        environment = self.get_session_environment()

        arguments = ['--output', output, '--format', cfg_format]

        if password:
            arguments += ['--password', password]

        if organization_id:
            arguments += ['--organizationid', organization_id]

        self.cli.execute("export", arguments, environment)
