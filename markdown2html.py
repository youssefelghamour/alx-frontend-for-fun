#!/usr/bin/python3
""" module for a script that takes 2 arguments """
import sys
import os


def main():
    """ Script that takes 2 arguments """
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    else:
        markdown_file_name = sys.argv[1]
        output_file_name = sys.argv[2]

        if not os.path.exists(markdown_file_name):
            sys.stderr.write("Missing {}\n".format(markdown_file_name))
            exit(1)

    exit(0)


if __name__ == "__main__":
    main()