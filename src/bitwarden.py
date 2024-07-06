import subprocess
import os
import json
import re

class Bitwarden:
    def __init__(self, binary_path):
        self.binary_path = binary_path
        self.session_key = None

    def get_session_environment(self):
        if (self.session_key):
            my_env = os.environ.copy()
            my_env["BW_SESSION"] = self.session_key
            return my_env
        else:
            raise Exception("Session key not set. Please login & unlock first.")

    def status(self):
        process = subprocess.run([self.binary_path, 'status'], capture_output=True)

        output = process.stdout.decode('utf-8')
        output_json = json.loads(output)
        status = output_json['status']
        
        return status

    def login(self, client_id, client_secret):
        if self.status() != 'unauthenticated':
            print("Already authenticated. Please logout first.")
            return

        my_env = os.environ.copy()
        my_env["BW_CLIENTID"] = client_id
        my_env["BW_CLIENTSECRET"] = client_secret

        process = subprocess.run([self.binary_path, 'login', '--apikey'], env=my_env)

    def logout(self):
        if self.status() == 'unauthenticated':
            print("Already unauthenticated. Please login first.")
            return

        process = subprocess.run([self.binary_path, 'logout'])

    def unlock(self, master_password):
        if self.status() == 'unlocked':
            print("Already unlocked. Please lock first.")
            return

        my_env = os.environ.copy()
        my_env["BW_PASSWORD"] = master_password

        process = subprocess.run([self.binary_path, 'unlock', '--passwordenv', 'BW_PASSWORD'], env=my_env, capture_output=True)

        output = process.stdout.decode('utf-8')
        session_key = re.search(r'(?<=BW_SESSION=").*?(?=")', output).group(0)
        
        self.session_key = session_key

    def export(self, output, cfg_format, password, organization_id = None):
        my_env = self.get_session_environment()

        export_command = [self.binary_path, 'export', '--output', output, '--format', cfg_format, '--password', password]

        if organization_id:
            export_command += ['--organizationid', organization_id]

        subprocess.run(export_command, env=my_env, check=True)
