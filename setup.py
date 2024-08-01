"""Python setup.py for werp_projection_sfis package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("werp_projection_sfis", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="werp_projection_sfis",
    version=read("werp_projection_sfis", "VERSION"),
    description="Awesome werp_projection_sfis created by fre171csiro",
    url="https://github.com/fre171csiro/python-projects/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="fre171csiro",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["werp_projection_sfis = werp_projection_sfis.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
