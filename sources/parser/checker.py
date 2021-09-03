
class Checker:
    def __init__(self, strings):
        self.lst_full = strings
        self.lst_without_comments = [line for line in strings if line.split("#")[0]]
        self.line_no_space = []
        for line in self.lst_without_comments:
            for subline in line.split():
                self.line_no_space.append(subline)
        print(self.line_no_space)
        # self.line_split = self.line_no_space.split()
