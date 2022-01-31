import sys
from fastgame.version import version


def main():
    if len(sys.argv) > 1:
        value = sys.argv[1]
        if value in ('-v', 'version'):
            print(version)
            

if __name__ == '__main__':
    main()
