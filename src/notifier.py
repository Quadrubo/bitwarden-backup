import abc

class Notifier(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def send_start(self):
        """Send a backup starting message"""

    @abc.abstractmethod
    def send_success(self, files):
        """Send a backup success message"""

    @abc.abstractmethod
    def send_failure(self, error):
        """Send a backup failure message"""