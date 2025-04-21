import sys
from scripts.util.copy_file_content import copy_file_contents_recursively


def main():
    result = copy_file_contents_recursively(sys.argv[1])
    print(result)


if __name__ == "__main__":
    main()
