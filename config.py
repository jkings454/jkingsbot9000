import json

class Config():
    """
    Helper class for storing and saving messages
    """

    def __init__(self, file="settings.json"):
        self.fo = open(format(file, "rw+"))
        self.settings = json.load(self.fo)

    def save(self):
        json.dump(self.settings, self.fo)

    def close(self):
        self.fo.close()

    def create_empty_list(self, key):
        self.settings[key] = ""