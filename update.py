#!/usr/bin/python3

"""Load data from dblp and create corresponding outputs.

"""

papers = [
    "conf/icalp/BlasiusF0KMT18",
]

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
for output_type in [output_html, output_bib]:
    output.write(output.Output(output_type))
