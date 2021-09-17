from setuptools import setup, find_packages

setup(
    name="dblptobib",
    version="1.0",
    description="create clean bibtex entries based on dblp",
    url="https://github.com/thobl/dblptobib",
    author="Thomas Bläsius",
    author_email="thomas.blaesius@kit.edu",
    license="ISC",
    packages=["dblptobib"],
    entry_points={"console_scripts": ["dblptobib=dblptobib.dblptobib:main"]},
    install_requires=["urllib3", "xmltodict", "appdirs"],
    include_package_data=True,
)
