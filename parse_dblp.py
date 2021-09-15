"""Parse information from dblp.

This file gets information from dblp and stores it into the local
database.  The parsing of the individual properties of a paper is done
in `parse_properties.py`."""

import urllib3
import xmltodict
import json
import os.path

from parse_properties import props
import data as local


def get(url):
    """Download xml from dblp and parse it to a python object."""
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    data = xmltodict.parse(r.data)
    return data


def get_paper(paper_container):
    """Parse a paper, save it to a local file and return the dblp key of the paper.

    Parses all properties as specified in `parse_properties.py`."""
    paper_type = list(paper_container.keys())[0]
    dblp_paper = paper_container[paper_type]
    dblp_key = dblp_paper["@key"].replace("/", "_")
    paper = {"type": paper_type}
    for prop in props:
        # see if property exists and get the key
        key = prop.key
        if key not in dblp_paper:
            continue
        key_name = prop.key_name if prop.key_name else key

        # get the property value and save if non-empty
        prop_value = dblp_paper[key]
        if prop.parse:
            prop_value = prop.parse(prop_value)
        if prop_value and prop_value != "":
            paper[key_name] = prop_value

    # output paper
    with open(local.file_name("papers", dblp_key), "w") as out:
        json.dump(paper, out, ensure_ascii=False, indent=4)

    return dblp_key


def get_autor_with_papers(author_id):
    """Parse the author with given id and all their papers and store them
    in the local database."""
    data = get("https://dblp.org/pid/" + author_id + ".xml")["dblpperson"]
    author_id = author_id.replace("/", "_")
    author = {
        "name": data["@name"],
        "papers": [get_paper(paper_container) for paper_container in data["r"]],
    }

    with open(local.file_name("authors", author_id), "w") as out:
        json.dump(author, out, ensure_ascii=False, indent=4)


def get_paper_by_id(paper_id):
    """Get the paper with the given id from dblp."""
    dblp_key = paper_id.replace("/", "_")
    if local.paper_exists(dblp_key):
        return dblp_key

    data = get("https://dblp.org/rec/" + paper_id + ".xml")["dblp"]
    return get_paper(data)


def get_venue(venue_id):
    """Get venue information based on the venue id."""

    venue = venue_id.split("_")[1]

    # search for exact venue id
    data = get("https://dblp.org/search/venue/api?h=1000&q=" + venue + "$")
    data = data["result"]["hits"]
    if int(data["@total"]) == 0:
        data = []
    elif int(data["@total"]) == 1:
        data = [data["hit"]]
    elif int(data["@total"]) > 1:
        data = data["hit"]

    # verify venue
    matches = [
        x
        for x in data
        if x["info"]["url"] == "https://dblp.org/db/" + venue_id.replace("_", "/") + "/"
    ]
    if len(matches) > 0:
        match = matches[0]["info"]
        return {
            "name": match["venue"],
            "acronym": match["acronym"] if "acronym" in match else venue.upper(),
        }

    print("WARNING: venue not found (" + venue_id + ")")
    return None


def get_venues():
    """Parse all venues that appear in papers in the local database."""
    papers = local.papers().values()
    venues = {paper["venue"] for paper in papers if "venue" in paper}

    for venue_id in venues:
        file_name = local.file_name("venues", venue_id)
        if os.path.isfile(file_name):
            continue
        venue = get_venue(venue_id)
        if not venue:
            continue
        with open(file_name, "w") as out:
            json.dump(venue, out, ensure_ascii=False, indent=4)
