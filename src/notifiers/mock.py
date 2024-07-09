from notifier import Notifier

class Mock(Notifier):
    def send_start(self):
        pass

    def send_success(self, files):
        pass

    def send_failure(self, error):
        pass