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
                in_ul_list = False
                # Flag for ordered list
                in_ol_list = False
                in_paragraph = False

                for i in range(len(content)):
                    line = content[i]

                    # HAndle headings
                    if line.startswith('#'):
                        # count the number of # symbols
                        level = line.count('#')
                        # remove the #s and extra spaces
                        heading_text = line.strip('#').strip()
                        html_tag = f"<h{level}>{heading_text}</h{level}>"
                        output_file.write(html_tag + '\n')
                        # Skip the next checks and go straight to next iteration
                        continue


                    # Handle unordered lists
                    if line.startswith('-'):
                        # if it's the first list element
                        if not in_ul_list:
                            output_file.write("<ul>\n")
                            # set the flag that indicates that we're inside the list to true
                            in_ul_list = True
                        list_item = line.strip('-').strip()
                        output_file.write(f"\t<li>{list_item}</li>\n")
                        continue
                    else:
                        # Close <ul> if not in a list item anymore
                        if in_ul_list:
                            output_file.write("</ul>\n")
                            in_ul_list = False
                    

                    # Handle ordered lists
                    if line.startswith('*'):
                        # if it's the first list element
                        if not in_ol_list:
                            output_file.write("<ol>\n")
                            # set the flag that indicates that we're inside the list to true
                            in_ol_list = True
                        list_item = line.strip('*').strip()
                        output_file.write(f"\t<li>{list_item}</li>\n")
                        continue
                    else:
                        # Close <ul> if not in a list item anymore
                        if in_ol_list:
                            output_file.write("</ol>\n")
                            in_ol_list = False
                    

                    # Handle paragraphs
                    if line.strip():
                        if not in_paragraph:
                            output_file.write("<p>\n")
                            in_paragraph = True
                        output_file.write(f"\t{line.strip()}\n")

                        if i+1 < len(content) and content[i+1].strip():
                            output_file.write("\t\t<br/>\n")
                    else:
                        if in_paragraph:
                            output_file.write("</p>\n")
                            in_paragraph = False


                # Close any open tags at the end
                if in_ul_list:
                    output_file.write("</ul>\n")
                if in_ol_list:
                    output_file.write("</ol>\n")
                if in_paragraph:
                    output_file.write("</p>\n")
                                                
                        


    except FileNotFoundError:
        sys.stderr.write("Missing {}\n".format(markdown_file_name))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()