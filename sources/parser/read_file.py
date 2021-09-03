class ReadFile:
    def __init__(self, filename):
        self.filename = filename
        self.lines = []
        pass

    def read(self):
        return [line.rstrip() for line in open(self.filename)]


    def data(self):
        return self.lines
