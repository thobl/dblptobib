"""Output to hmtl."""

from . import output_bib
import os

here = os.path.dirname(__file__) + "/"

filetype = "html"

head = f"""
<HTML>
<div class="pub_list">
<style type="text/css" scoped>
{open(here + "output_html.css").read()}
</style>
"""

foot = f"""
<script>
{open(here + "output_html.js").read()}
</script>
</div>
</HTML>"""


def write_paper(paper):
    author = ", ".join(paper["author"])
    title = paper["title"]
    venue = first_existing(
        paper, ["booktitle_full", "booktitle", "journal_full", "journal", "school"]
    )
    year = paper["year"]
    buttons = []

    buttons.append(
        """<a href="javascript:void(0)" class="pub_bibtex_toggle">bibtex</a>"""
    )

    if "url" in paper:
        buttons.append(url(paper["url"], "url"))
    elif "doi" in paper:
        buttons.append(url("https://doi.org/" + paper["doi"], "url"))

    bibtex = output_bib.write_paper(paper)

    type_class = "pub_preprint" if "preprint" in paper else "pub_" + paper["type"]
    res = f"""
<div class="pub_item {type_class}">
<div class="pub_author">{author}</div>
<div class="pub_title">{title}</div>
<div class="pub_venue">{venue} {year}</div>
<div class="pub_buttons">{"".join(buttons)}</div>
<div class="pub_bibtex" style="display: none">
<textarea class="pub_bibtex" rows="8" readonly style="white-space: pre;">
{bibtex}
</textarea>
</div>
</div>"""
    return res


def write_group(group):
    return f"""
<h3> {group}</h3>
"""


######################################################################
# helper functions
######################################################################


def first_existing(dictionary, keys, default=""):
    """The dictionary value for the first of a list of keys that is in the dictionary."""
    for key in keys:
        if key in dictionary:
            return dictionary[key]
    return default


def url(href, text):
    return f"""<a href="{href}">{text}</a>"""
