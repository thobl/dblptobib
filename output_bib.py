"""Output to bibtex."""

import re


filetype = "bib"
head = ""
foot = ""


def write_paper(paper):
    # list of keys as they appear in `paper`
    keys = [
        "title",
        "author",
        "pages",
        "year",
        "booktitle_full",
        "journal_full",
        "volume",
        "number",
        "school",
        "doi",
        "url",
    ]
    # transformations to the values for some of those keys
    vmap = {
        "title": lambda val: val.rstrip("."),
        "author": lambda val: " and ".join(val),
        "pages": lambda val: val.replace("-", "--"),
    }
    # renaming some of these keys into bibtex entries
    kmap = {"booktitle_full": "booktitle", "journal_full": "journal"}

    # collect all values that exist in paper and apply the maps if given
    bibtex_props = {
        kmap[k] if k in kmap else k: vmap[k](paper[k]) if k in vmap else paper[k]
        for k in keys
        if k in paper
    }

    # output to string
    props_string = ",\n  ".join(
        [f"""{key.ljust(9)} = {{{value}}}""" for key, value in bibtex_props.items()]
    )
    return f"""@{paper["type"]}{{{bibtex_key(paper)},\n  {props_string}\n}}\n"""


def write_group(group):
    return f"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% {group}
"""


######################################################################
# helper functions
######################################################################


def rm_special_char(string):
    """Remove all special characters from a string."""
    regex = re.compile("[^a-zA-Z ]")
    return regex.sub("", string)


def bibtex_key(paper):
    """The bibtex key for a given paper."""

    # combine the first few capitalized words of the title
    nr_words = 4
    trunc_len = 5
    min_len = 4
    title = [
        word[0:trunc_len]
        for word in rm_special_char(paper["title"]).split()
        if len(word) >= min_len
    ][0:nr_words]

    # conf name / journal / preprint
    if "preprint" in paper:
        conf = "pre"
    elif "booktitle_acronym" in paper:
        conf = paper["booktitle_acronym"]
    elif paper["type"] == "article":
        conf = "jour"
    else:
        conf = "other"

    return "_".join(title) + "_" + conf + paper["year"]
