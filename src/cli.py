import subprocess


class CLI:
    def __init__(self, binary_path):
        self.binary_path = binary_path

    def execute(self, command, arguments=None, environment=None):
        if arguments is None:
            arguments = []

        if environment:
            process = subprocess.run([self.binary_path, command] + arguments, env=environment, capture_output=True)
        else:
            process = subprocess.run([self.binary_path, command] + arguments, capture_output=True)

        stdout = process.stdout.decode('utf-8')
        stderr = process.stderr.decode('utf-8')

        return stdout, stderr
