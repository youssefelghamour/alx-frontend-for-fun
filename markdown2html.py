#!/usr/bin/python3
""" module for a script that takes 2 arguments """
import sys
import os


def main():
    """ Script that takes 2 arguments """
    
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    try:
        with open(markdown_file_name, 'r') as input_file:
            # read the content of the markdown file into a list of lines (content)
            content = input_file.readlines()

            # create and open the output file
            with open(output_file_name, "w") as output_file:

                for line in content:
                    # split the line into a list of words
                    words = line.split()

                    # create opening and closing tag base on the markdwon title syntax
                    match words[0]:
                        case "#":
                            html_tag = ["<h1>", "</h1>\n"]
                        case "##":
                            html_tag = ["<h2>", "</h2>\n"]
                        case "###":
                            html_tag = ["<h3>", "</h3>\n"]
                        case "####":
                            html_tag = ["<h4>", "</h4>\n"]
                        case "#####":
                            html_tag = ["<h5>", "</h5>\n"]
                        case "######":
                            html_tag = ["<h6>", "</h6>\n"]

                    # convert the line title into html
                    line = html_tag[0] + " ".join(words[1:]) + html_tag[1]
                    
                    # add the formated html line into it
                    output_file.write(line)

    except FileNotFoundError:
        sys.stderr.write("Missing {}\n".format(markdown_file_name))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()