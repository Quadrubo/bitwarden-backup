import requests
from base64 import b64encode
from notifier import Notifier

class NTFY(Notifier):
    def __init__(self, server, topic, username = None, password = None):        
        if (server == None or topic == None):
            raise Exception("Server and topic must be provided")

        self.server = server
        self.topic = topic
        self.username = username
        self.password = password

    def send(self, message, headers = {}):
        if (self.username):
            headers["Authorization"] = "Basic " + b64encode((self.username + ":" + self.password).encode()).decode()

        response = requests.post(
            self.server + "/" + self.topic,  
            data=message,
            headers=headers
        )

        if (response.status_code == 403):
            raise Exception("[" + str(response.status_code) + "] The ntfy topic you are trying to send to requires authentication: " + response.text)
        elif (response.status_code != 200):
            raise Exception("[" + str(response.status_code) + "] Failed to send message to NTFY server: " + response.text)

    def send_start(self):
        title = "A Bitwarden backup has started"
        message = "Look out for follow up messages regarding the status of the backup"
        priority = 1

        headers = {
            "Title": title,
            "Priority": str(priority)
        }

        self.send(message, headers)

    def send_success(self, files):
        title = "A Bitwarden backup has finished successfully"
        message = "The files" + ", ".join(files) + " have been successfully backed up"
        priority = 1

        headers = {
            "Title": title,
            "Priority": str(priority)
        }

        self.send(message, headers)

    def send_failure(self, error):
        title = "A Bitwarden backup has failed"
        message = "An error occurred during the backup: " + error
        priority = 5

        headers = {
            "Title": title,
            "Priority": str(priority)
        }

        self.send(message, headers)