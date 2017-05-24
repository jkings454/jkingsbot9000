import json

class Config():
    """
    Helper class for storing and saving messages
    """

    def __init__(self, file="settings.json"):
        self.file = file
        fo = open(self.file)
        self.settings = json.load(fo)
        fo.close()

    def save(self):
        fo = open(self.file, "w+")
        json.dump(self.settings, fo)
        fo.close()

    def create_empty_list(self, key):
        self.settings[key] = []

    def create_empty_dict(self, key):
        self.settings[key] = {}