"""Specification which properties to extract from dblp and how to parse them."""

from dataclasses import dataclass


def ee_to_url(ee_value):
    """"Transform ee-value of dblp into an url."""
    if isinstance(ee_value, str):
        return ee_value
    if "#text" in ee_value:
        return ee_value["#text"]
    if isinstance(ee_value, list):
        return ee_value[0]
    return ""


def doi(url):
    """Return the doi from a given url if it is a doi-url and False otherwise."""
    if "https://doi.org/" in url:
        return url.replace("https://doi.org/", "")
    return False


def parse_venue(pub_key):
    """Parse the venue from the publication key."""
    parts = pub_key.split("/")
    if parts[0] not in ["conf", "journals"]:
        return False
    return "_".join(parts[:-1])


def parse_author(author):
    """Parse list of authors in dblp format to simple list of strings."""
    if not isinstance(author, list):
        if not isinstance(author, str):
            author = author["#text"]
        return [author.rstrip("1234567890 ")]
    author_list = [parse_author(a)[0] for a in author]
    return author_list


@dataclass
class Prop:
    """Format for specifying a property.

    `key` has to be the key used in the dblp format, `key_name` is the
    name of the key used locally, and `parse` is a function that
    parses the value from the value as given by dblp.

    """

    key: str
    key_name: str = None
    parse: callable = None


# The properties that should be read from dblp.
props = [
    Prop(key="title"),
    Prop(key="author", parse=parse_author),
    Prop(key="pages"),
    Prop(key="year"),
    Prop(key="booktitle"),
    Prop(key="journal"),
    Prop(key="volume"),
    Prop(key="number"),
    Prop(key="school"),
    Prop(
        key="@publtype",
        key_name="preprint",
        parse=lambda type: "yes" if type == "informal" else False,
    ),
    Prop(
        key="ee",
        key_name="doi",
        parse=lambda ee: doi(ee_to_url(ee)),
    ),
    Prop(
        key="ee",
        key_name="url",
        parse=lambda ee: ee_to_url(ee) if not doi(ee_to_url(ee)) else False,
    ),
    Prop(key="@key", key_name="venue", parse=parse_venue),
]
