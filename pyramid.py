#!/usr/bin/env python3
"""Print a pyramid to the terminal

A pyramid of height 3 would look like:

--=--
-===-
=====

"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import math as maths

def print_pyramid(rows):
    """Print a pyramid of a given height

    :param int rows: total height
    """
    
    # convert to int
    # needed due to command line args being strings instead of ints
    rows = int(rows)

    # calcuate width of the pyramid
    width = 1 + (2 * (rows - 1))
    
    # calculate the half-way pointi
    pyr_start = maths.floor(width / 2)
    pyr_end = pyr_start
    
    # store strings in here for printing later
    print_buffer = []

    for i in range(rows):
        
        # empty string that will be appended too
        tmp = ""

        for j in range(width):
            
            # determine with char we should append
            if j >= pyr_start and j <= pyr_end:
                new_char = "="
            else:
                new_char = "-"

            tmp = tmp + new_char
        
        print_buffer.append(tmp)
        
        # move these by one 
        pyr_start = pyr_start - 1
        pyr_end = pyr_end + 1
    
    # print whatever is in the buffer
    for item in print_buffer:
        print(item)
    
    # not needed functionally, but nice for reading the code
    return
     



if __name__ == "__main__":
    parser = ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument("-r", "--rows", default=10, help="Number of rows")

    args = parser.parse_args()
    print_pyramid(args.rows)
