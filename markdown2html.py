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
                # Flag for unordered list
                in_list = False

                for i in range(len(content)):
                    line = content[i]

                    # Check for heading syntax and write corresponding HTML tag
                    if line.startswith('#'):
                        # count the number of # symbols
                        level = line.count('#')

                        # remove the #s and extra spaces
                        heading_text = line.strip('#').strip()

                        html_tag = f"<h{level}>{heading_text}</h{level}>"

                        output_file.write(html_tag + '\n')
                    # Check for list items
                    elif line.startswith('-'):
                        if not in_list:
                            output_file.write("<ul>\n")
                            in_list = True
                        list_item = line.strip('-').strip()
                        output_file.write(f"\t<li>{list_item}</li>\n")
                    else:
                        # Close <ul> if not in a list item anymore
                        if in_list:
                            output_file.write("</ul>\n")
                            in_list = False

                # Close <ul> at the end of the file if still open
                if in_list:
                    output_file.write("</ul>\n")
                                                
                        


    except FileNotFoundError:
        sys.stderr.write("Missing {}\n".format(markdown_file_name))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()