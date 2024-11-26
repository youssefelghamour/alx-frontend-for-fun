#!/usr/bin/python3
""" module for a script that converts from markdown to html """
import sys
import os
import hashlib


def main():
    """ Script that takes an input markdown file and converts it to HTML, writing the result to an HTML file
    
        The conversion can be done automatically with the markdown library:
        import markdown

        # Read the markdown file
        with open('README.md', 'r') as input_file:
            markdown_text = input_file.read()

        # Convert markdown to HTML
        html_output = markdown.markdown(markdown_text)

        # Write HTML output to a file
        with open('README.html', 'w') as output_file:
            output_file.write(html_output)
    """
    
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
                # Flag for paragraph
                in_paragraph = False


                for i in range(len(content)):
                    line = content[i]

                    start_index = None
                    end_index = None
                    
                    # Process for ((content))
                    if '((' in line and '))' in line:
                        start_index = line.find('((')
                        # Looking for )) starting from the position start_index
                        end_index = line.find('))', start_index)
                        # Extract the substring (between (( )) ) and apply the replacement
                        substr = line[start_index + 2:end_index]
                        # Remove all 'c' & 'C' characters
                        substr = substr.replace('c', '').replace('C', '')
                        # Replace the original substring with the modified one
                        line = line[:start_index] + substr + line[end_index + 2:]

                    # Process for [[content]]
                    if '[[' in line and ']]' in line:
                        start_index = line.find('[[')
                        end_index = line.find(']]', start_index)
                        substr = line[start_index + 2:end_index]
                        # Covert substring to MD5 hash
                        md5_hash = hashlib.md5(substr.encode()).hexdigest()
                        line = line[:start_index] + md5_hash + line[end_index + 2:]


                    # the third argument 1 is to replace only one occurence, otherwise  the replace will replace all the ** on the line
                    # Replace the first  ** with the opening bold tag
                    line = line.replace('**', '<b>', 1)
                    # Replace the second ** with the closing bold tag
                    line = line.replace('**', '</b>', 1)

                    # Replace the first  __ with the opening emphasis tag
                    line = line.replace('__', '<em>', 1)
                    # Replace the second __ with the closing emphasis tag
                    line = line.replace('__', '</em>', 1)

                    # Handle headings
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