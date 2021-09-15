#!/usr/bin/python3

"""Load data from dblp and create corresponding outputs.

"""

import sys

if len(sys.argv) != 3:
    print("Usage: ./dblptobib.py input output")
    sys.exit()

input_arg = sys.argv[1]
output_arg = sys.argv[2]

with open(input_arg) as f:
    papers = [line.rstrip() for line in f]

import data
import parse_dblp
import output
import output_html
import output_bib


# make sure local directories exist
data.setup_directories()

# get papers by id
for paper_id in papers:
    parse_dblp.get_paper_by_id(paper_id)

# get venue names
parse_dblp.get_venues()

# some output
output.write(output.Output(output_bib, filename=output_arg))
