"""Functions dealing with the local database of publications."""

from pathlib import Path
import glob
import json
import appdirs

data_dir_base = appdirs.user_data_dir("dblptobib")
data_dir = data_dir_base + "/automatic/"
mod_dir = data_dir_base + "/manual/"
subdirs = ["authors", "venues", "papers"]


def setup_directories():
    """Make sure that all necessary directories exits."""
    for subdir in subdirs:
        for dir in [data_dir, mod_dir]:
            Path(dir + subdir).mkdir(parents=True, exist_ok=True)


def file_name(subdir, name):
    """File name for data point `name` of type `subdir`."""
    return data_dir + subdir + "/" + name + ".json"


def paper_exists(dblp_key):
    """Check whether the paper with the given id exists in the local database."""
    path = Path(file_name("papers", dblp_key))
    return path.exists()


def load_data(subdir):
    """Helper function for loading all data from a specific subdir.

    Loads the data from the `data_dir` and applies manual
    modifications from the `mod_dir`.  The type of data is specified
    by `subdir`.

    For external use, use wrapper functions such as `autors()` or
    'papers()`.

    """
    # load data
    files = glob.glob(data_dir + subdir + "/*.json")
    results = {Path(file).stem: json.load(open(file)) for file in files}

    # load manual modifications
    mod_files = glob.glob(mod_dir + subdir + "/*.json")
    mod_results = {Path(file).stem: json.load(open(file)) for file in mod_files}

    # update papers according to modifications
    for result, props in mod_results.items():
        if result not in results:
            results[result] = {}
        for prop, value in props.items():
            results[result][prop] = value

    return results


def authors():
    """Return dictionary of authors in the database."""
    return load_data("authors")


def papers():
    """Return dictionary of papers in the database (augmented with venue information)."""
    all_papers = load_data("papers")
    venues = load_data("venues")
    for paper in all_papers.values():
        if "venue" not in paper or paper["venue"] not in venues:
            continue
        venue = venues[paper["venue"]]
        if paper["type"] == "article":
            paper["journal_full"] = venue["name"]
            paper["journal_acronym"] = venue["acronym"]
        elif paper["type"] == "inproceedings":
            paper["booktitle_full"] = venue["name"]
            paper["booktitle_acronym"] = venue["acronym"]

    return all_papers
