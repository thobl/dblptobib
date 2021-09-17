# dblptobib #

Generate lists of papers in BibTeX or HTML format by gathering the
necessary information from [dblp](https://dblp.org/).  The goal here
is to get a consistent and clean bibliography without the hassle of
fiddling around with it manually.

## Installation ##

Download the repository and run `pip install .` from inside the
repository.  This should download all dependencies (urllib3,
xmltodict, appdirs) and give you excess to the command `dblptobib`
from anywhere in your system.

If you want to make changes to the code and want them to apply
immediately without rerunning the install command, you can run `pip
install -e .` instead, to install the package using symlinks.

## Usage ##

You have to specify two pieces of information when calling
`dblptobib`: the papers that should be included and the output file.
The output file is always the last argument; the format (BibTeX or
HTML) is automatically deduced from the suffix (.bib or .html).  For
which papers to include there are different options.

### List of Paper IDs ###

```console
dblptobib list.txt out.bib
```

This reads a list of paper ids from the file `list.txt`, gets the
information about the papers from dblp and writes the resulting BibTeX
entries to `out.bib`.  The paper ids are the ones used by dblp and
`list.txt` should contain one id per line.  Here is an example
`list.txt` and the resulting `out.bib`:

```
conf/stoc/Cook71
conf/coco/Karp72
```

```BibTeX
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 1972

@inproceedings{Reduc_Among_Combi_Probl_CCC1972,
  title     = {Reducibility Among Combinatorial Problems},
  author    = {Richard M. Karp},
  pages     = {85--103},
  year      = {1972},
  booktitle = {Computational Complexity Conference (CCC)},
  doi       = {10.1007/978-1-4684-2001-2_9}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 1971

@inproceedings{Compl_Theor_Proce_STOC1971,
  title     = {The Complexity of Theorem-Proving Procedures},
  author    = {Stephen A. Cook},
  pages     = {151--158},
  year      = {1971},
  booktitle = {Symposium on the Theory of Computing (STOC)},
  doi       = {10.1145/800157.805047}
}
```

### All Papers of One Author ###

```console
dblptobib author_id out.html
```

This gets all the papers of the author with the given id from dblp and
outputs the result to HTML.  As for the paper ids, the author ids are
the ones used by dblp, e.g., my author id is
[74/9125](https://dblp.org/pid/74/9125.html), so running `dblptobib
74/9125 out.html` outputs all my papers to `out.html`.

### All Papers in the Local Database ###

```console
dblptobib out.bib
```

This outputs all papers that are already in the local database, i.e.,
papers whose information have be gotten from dblp before.

## The Local Database ##

Information retrieved from dblp is cached in a local database in the
user data directory (e.g., `~/.local/share/dblptobib/` on Linux).  To
find this directory on your system, just run `dblptobib` without
arguments.

To save calls to the dblp API (and time), an API call is only done if
the information is not already in the local database.  The only
exception to this is when getting the list of papers of an author, as
this list changes regularly for active researchers.

## Manual Changes ##

In the rare occasion that the information from dblp is not to your
liking, you can apply manual changes.  This is done directly in the
local database, which contains two folders, `automatic/` and
`manual/`.  Do not touch `automatic/`, which contains all information
gotten from dblp distributed over many json files.  Instead, add your
changes to `manual/`, which has the same directory structure as
automatic.  Every information in `manual/` will overwrite the
corresponding information in `automatic/`.

So if you, e.g., have a paper where dblp got the title wrong, then
find the filename for this paper in the `automatic/` folder and create
a file with the same name in the `manual/` folder with the following
content.

```json
{
    "title": "New Corrected Title."
}
```

## Changing the Formatting and Other Features ##

If you want to adjust the formatting of the BibTeX or HTML output, you
have to adjust the `output_bib.py` or `output_html.py` accordingly.
They should be somewhat self-explanatory.

The python code supports other features like sorting/grouping by other
things than the year of publication or filtering of, e.g., preprints.
They are not accessible by just calling `dblptobib`, so you have to do
some adjustments to the python code if you want to use them.  Having a
look at `dblptobib.py` and `output.py` is probably a good start for
this.
