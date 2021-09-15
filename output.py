"""Generic definitions and functions for generating output.

To define a specific output, create a model containing the following:
  
  * filetype: A string.  It is used as file extension when writing a
    file.

  * head: A string. The output file starts with this string.

  * foot: A string. The output file ends with this string.

  * write_paper: A function.  It should take a paper (as dictionary)
    and return a string representation of the paper.

  * write_group: A function.  It should take a group name (as string)
    and return the desired string representation of the group (e.g., a
    headline).

"""

from itertools import groupby
import re
import data


class Output:
    """An output object derived from an output module and some options.

    The options are:

    * author_id: A string or `None`.  Specify for which authors the
      output should be generated (using their dblp-id).  `None`
      generates the output for all authors.

    * filter: A function.  It should take a paper and return `True` if
      the paper should be included and `False` if it should be
      excluded.

    * group_by: A string.  A paper property by which the output should
      be grouped.

    * group_sort_rev: A Boolean.  Specify whether the order of the
      groups should be reversed.

    """

    def __init__(
        self,
        module,
        author_id: str = None,
        filter: callable = None,
        group_by: str = "year",
        group_sort_rev: bool = True,
    ):
        self.filetype = module.filetype
        self.head = module.head
        self.foot = module.foot
        self.write_paper = module.write_paper
        self.write_group = module.write_group

        self.author_id = author_id
        self.filter = filter
        self.group_by = group_by
        self.group_sort_rev = group_sort_rev


def write(output):
    """Takes an output specification and writes the corresponding output."""
    papers = data.papers()
    if output.author_id:
        author = data.authors()[output.author_id.replace("/", "_")]
        papers = {key: papers[key] for key in author["papers"]}

    if output.filter:
        papers = {key: paper for key, paper in papers.items() if output.filter(paper)}

    if output.group_by:
        by = output.group_by
        rev = output.group_sort_rev
        key_fun = lambda item: item[1][by] if by in item[1] else "no group"
        groups = groupby(sorted(papers.items(), key=key_fun, reverse=rev), key=key_fun)
        grouped_papers = {group: dict(items) for group, items in groups}
    else:
        grouped_papers = {"group": "no group", "papers": papers}

    with open(file_name(output), "w") as out:
        print(output.head, file=out)

        for group, papers in grouped_papers.items():
            print(output.write_group(group), file=out)

            for paper in papers.values():
                print(output.write_paper(paper), file=out)

        print(output.foot, file=out)


def file_name(output):
    """The file name for a given output."""
    items = []
    if output.author_id:
        a_id = output.author_id.replace("/", "_")
        items.append(a_id)
        authors = data.authors()
        items.append(authors[a_id]["name"])
    else:
        items.append("all")

    if output.group_by:
        items.append("by" + output.group_by)

    if output.filter:
        items.append(output.filter.__name__)

    name = re.compile("[^a-zA-Z1-9_]").sub("", "_".join(items))
    return "output/" + name + "." + output.filetype


def nopreprint(paper):
    """Filter for excluding preprints."""
    return "preprint" not in paper
