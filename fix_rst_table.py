#!/usr/bin/env python3

__description__ = \
"""
Hacked utility script that fixes column widths in restructured text tables
so I do not have to type all of the spaces, etc.  It shrinks/expands each 
column to fit the existing cell contents.

The program assumes a simple grid layout of rows and columns. 
"""
__author__ = "Michael J. Harms"
__usage__ = "fix_rst_tables.py rst_file"
__date__ = "2018-09-22"

import sys, re

def fix_rst_tables(rst_file):
   
    plus_pattern = re.compile("\+")
    bar_pattern = re.compile("\|")
 
    f = open(rst_file,'r')
    lines = f.readlines()
    f.close()
    
    in_table = False
    table_lines = []

    # Find all individual tables in the file
    for i,l in enumerate(lines):

        if not in_table:
            if l.startswith("+-"):
                in_table = True
                table_lines.append([])
        
        if in_table:
            if l[0] in ["+","|"]:
                table_lines[-1].append(i)
            else:
                in_table = False

    out_lines = lines[:]

    # For each table           
    for table_index, table in enumerate(table_lines):
     
        # How many vertical lines in this table.  Find by looking for all "+"
        # in first line in table. 
        num_verticals = len(plus_pattern.findall(lines[table[0]]))
        target_col_widths = [0 for i in range(num_verticals-1)]

        # Now find the widest entry in each column

        line_verts = []
            
        # Go through each line
        for table_line in table:

            l = lines[table_line]

            # Find column breaks in this row
            if l.startswith("+"):
                cols = plus_pattern.finditer(l) 
            else:
                cols = bar_pattern.finditer(l)  
   
            # Find positions of column breaks 
            verts = []
            for c in cols:
                verts.append(c.span()[0])

            if len(verts) != num_verticals:
                err = "mangled row. \n\n{}\n\n".format(l)
                raise ValueError(err)

            # Now record the width of each column if it is bigger than the width
            # of the widest column yet seen
            line_verts.append([verts[0]])
            for i in range(num_verticals - 1):
                line_verts[-1].append(verts[i+1])

                # don't record width if this is a +--+ sort of line
                if l.startswith("+"):
                    continue

                # Find width of contents in the cell
                contents = l[verts[i] + 1:verts[i+1]]
                total_contents = " {} ".format(contents.strip())
                col_width = len(total_contents)

                # If bigger than we've yet seen, record it
                if target_col_widths[i] < col_width:
                    target_col_widths[i] = col_width 
 
        # Now process columns so every column has the max width.  Do so by
        # padding with spaces.          
        for line_index, table_line in enumerate(table):

            l = lines[table_line]

            processed_line = []

            if l.startswith("+"):
                pad_char = l[1]
                vert_char = "+"
            else:
                pad_char = " "
                vert_char = "|"

            current_verts = line_verts[line_index]
            for i in range(len(current_verts) - 1):
                
                target_size = target_col_widths[i]

                # If this is a +--+ sort of row, the contents should be a
                # single pad_char (-, for example)
                if l.startswith("+"):
                    contents = pad_char

                # otherwise, it's whatever is in the cell
                else:
                    contents = l[current_verts[i] + 1:current_verts[i+1]].strip()

                # formatting magic to pad with " " (content cell) or "-" (+--+) cell
                contents = "{}{}{}".format(pad_char,contents,pad_char)
                new_contents = "{s:{c}<{n}}".format(s=contents,n=target_size,c=pad_char) 
            
                processed_line.append(new_contents)


            # assemble whole line
            processed_line = "{}{}{}\n".format(vert_char,
                                               vert_char.join(processed_line),
                                               vert_char)

            out_lines[table_line] = processed_line
           
    
    f = open(rst_file,"w")
    f.write("".join(out_lines))
    f.close()


def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    try:
        rst_file = argv[0]
    except IndexError:
        err = "Incorrect arguments. Usage:\n\n{}\n\n".format(__usage__)
        raise IndexError(err)

    fix_rst_tables(rst_file)

if __name__ == "__main__":
    main()
