from sys import argv
from sources.parser.read_file import ReadFile
# from sources.parser.parser import Parser
from sources.parser.checker import Checker
def main(argv):
    kek = argv
    x = ReadFile(argv[1])
    lst = x.read()
    Checker(lst)
    pass


if __name__ == '__main__':
    main(argv)
