"""
Helps creates logs files
"""
from datetime import datetime

class Logger():
    def __init__(self, log_path="", log_file="jkingsbot.log", noisy=True):
        self.log_path = log_path
        self.log_file = log_file
        self.noisy = noisy

    def log_event(self, text):
        event = "[%s] %s" % (datetime.now().strftime("%H:%M:%S"), text)
        if self.noisy:
            print(event)

        fo = open(self.log_path + self.log_file, "a")
        fo.write(event + "\n")
        fo.close()