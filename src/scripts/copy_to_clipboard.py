import sys
import pyperclip
from scripts.util.copy_file_content import copy_file_contents_recursively


def main():
    result = copy_file_contents_recursively(sys.argv[1])
    pyperclip.copy(result)
    print("✅ Copied to clipboard!")


if __name__ == "__main__":
    main()
