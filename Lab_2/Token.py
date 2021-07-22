import hashlib


class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.hash = hashlib.sha256((self.name + self.value).encode('utf-8')).hexdigest()

    def print(self):
        print('|\t\t' + self.name + '\t\t|' + '|\t\t\t' + self.value + '\t\t\t|' + '|\t' + self.hash + '\t|')
