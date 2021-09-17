#!/usr/bin/python3

"""Load data from dblp and create corresponding outputs.

"""

import sys
from pathlib import Path

from . import data, parse_dblp, output, output_html, output_bib


def main():
    print("test2")
    # make sure directories for local database exist
    data.setup_directories()

    # getting input parameters
    if len(sys.argv) == 3:
        input_arg = sys.argv[1]
        output_arg = sys.argv[2]
    elif len(sys.argv) == 2:
        input_arg = None
        output_arg = sys.argv[1]
    else:
        print("Usage: ./dblptobib.py [input] output<.bib|.hmtl>")
        print("`input` (optional) must be a file containing paper ids or an author id")
        print("`output` specifies the output file, which must end on .bib or .html")
        print("")
        print("the data downloaded from dblp can be found in {}".format(data.data_dir))
        print("manual modifications can be added to {}".format(data.mod_dir))
        sys.exit()

    # type of output depending on the filename
    if output_arg.endswith(".bib"):
        output_type = output_bib
    elif output_arg.endswith(".html"):
        output_type = output_html
    else:
        print("output must be a *.bib or a *.html file")
        sys.exit()

    output_spec = output.Output(output_type, filename=output_arg)

    # getting the papers: either a specific list of papers, all papers
    # from one author or just using all papers in the local database
    if input_arg and Path(input_arg).exists():
        # file with list of papers
        with open(input_arg) as f:
            papers = [line.rstrip() for line in f]

        # get the papers from dblp
        for paper_id in papers:
            parse_dblp.get_paper_by_id(paper_id)

        # tell the output to only use these papers
        output_spec.paper_ids = papers
    elif input_arg:
        # get all papers of the given author from dblp
        parse_dblp.get_autor_with_papers(input_arg)

        # tell the output to only use these papers
        output_spec.author_id = input_arg

    # get venue names
    parse_dblp.get_venues()

    # write the output
    output.write(output_spec)
