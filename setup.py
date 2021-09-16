from setuptools import setup

setup(
    name="dblptobib",
    version="1.0",
    description="create clean bibtex entries based on dblp",
    url="https://github.com/thobl/dblptobib",
    author="Thomas Bläsius",
    author_email="thomas.blaesius@kit.edu",
    license="ISC",
    scripts=["dblptobib.py"],
    install_requires=["urllib3", "xmltodict", "appdirs"],
)
