# werp_projecting_sfis

[![codecov](https://codecov.io/gh/fre171csiro/python-projects/branch/main/graph/badge.svg?token=python-projects_token_here)](https://codecov.io/gh/fre171csiro/python-projects)
[![CI](https://github.com/fre171csiro/python-projects/actions/workflows/main.yml/badge.svg)](https://github.com/fre171csiro/python-projects/actions/workflows/main.yml)

Awesome werp_projecting_sfis created by fre171csiro

## Install it from PyPI

```bash
pip install werp_projecting_sfis
```

## Usage

```py
from werp_projecting_sfis import BaseClass
from werp_projecting_sfis import base_function

BaseClass().base_method()
base_function()
```

```bash
$ python -m werp_projecting_sfis
#or
$ werp_projecting_sfis
```

## Development
### Getting Started
**Dev setup**
1. Install `pyenv` if not already installed on your dev machine (see steps below), this is optional however it makes managing python easier
1. Install `poetry` (see steps below).  `poetry` is used to manage the python environment and is a alternative to `conda`

To enable pymc to compile a model (and infer parameter ~10 times faster)
1. Install `msys2` (http://www.msys2.org/, specifically download and run the x86_64 installer) , then in `msys2` add mingw-wc64 gcc/g++ compiler by executing `pacman -S mingw-w64-x86_64-gcc` in the msys2 terminal. Then add path to g++ compiler to the system PATH (e.g. `C:\msys64\mingw64\bin` ).

1. Setup the project environment
    1. Using the `cmd` change directory to your code parent directory and:
    1. Using `pyenv` install python 3.10.10, e.g. `pyenv install 3.10.10`
    1. Set the local version of python - `pyenv local 3.10.10`
    1. Build the python environment - `poetry install`
    1. Activate the environment - `poetry shell`
    1. Open a `.ipynb` file and set the kernel to `.venv/Scripts/python.exe`
1. Run the unit tests (make sure the existing code is passing all tests prior to use)
    1. Set the workspace interpreter to `.venv/Scripts/python.exe`
        1. ctrl+shift+p "Select Interpreter" and select '.venv':poetry
    1. Open the 'tests' directory or use the VS Code test extension to run all tests

### Installation process (Dev env)

Python Package Manager is a Python utility intended to simplify the tasks of locating, installing, upgrading and removing Python packages. It can determine if the most recent version of a software package is installed on a system, and can install or upgrade that package from a local or remote host. [Wikipedia](https://en.wikipedia.org/wiki/Python_Package_Manager)

1. Install (optional, but helpful) `pyenv` to manage python version for different scenarios
>>>'pyenv lets you easily switch between multiple versions of Python. It's simple, unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well.'
>>>- [pyenv overview](https://github.com/pyenv/pyenv#getting-pyenv)
>>>- [pyenv linux installer](https://github.com/pyenv/pyenv-installer)
>>>- [pyenv windows installer](https://github.com/pyenv-win/pyenv-win) Don't forget to put pyenv in you [PATH](https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md#add-system-settings)

[This](https://blog.teclado.com/how-to-use-pyenv-manage-python-versions/) is a useful page explaining the use of pyenv. 

2. Install `poetry` to manage project/venv dependencies
>>We use [poetry](https://python-poetry.org/docs/) to manage the python environment and dependencies.  If you don't have poetry installed please [install](https://python-poetry.org/docs/#installing-with-the-official-installer) it in your base environment and add poetry to your PATH.

>>[Basic usage](https://python-poetry.org/docs/basic-usage/) will help get you started using poetry.  If `pyproject.toml` does not exist in the project directory you can use `poetry init`.  If the project already has a `pyproject.toml` file you can just use `poetry install` and all dependencies will be installed in a environment folder `.venv` and a local lock file (`poetry.lock`) generated.  To add further dependencies run `poetry add [a package name]` or to remove an existing package/dependency `postry remove [package name to remove]`.

I like to keep the `.venv` in my project directory so I use `poetry config --local virtualenvs.in-project true`

You can specify a package to add in the following forms:
  - A single name (requests): this will search for matches on PyPI
  - A name and a constraint (requests@^2.23.0)
  - A git url (git+https://github.com/python-poetry/poetry.git)
  - A git url with a revision (git+https://github.com/python-poetry/poetry.git#develop)
  - A file path (../my-package/my-package.whl)
  - A directory (../my-package/)
  - A url (https://example.com/packages/my-package-0.1.0.tar.gz)

*Note*: Some systems will use a `requirements.txt` to build a python environment, therefore to easily generate a the `requirements.txt` run `refresh_requirements.sh` after any changes to the packages made with `poetry`

## Notebooks/Lab books
These can be used within Visual Studio Code or run in your local browser

If running in a Web browser users will need to install the kernel with `python -m ipykernel install --user --name .venv --display-name outlook-hydro`, which needs to be executed from the command prompt prior to opening the notebook.  Then when loading the notebook select the named `outlook-hydro` kernal.

To run in your browser open a terminal (make sure you have activated your environment) with the root folder and type `jupyter notebook` this will load a Jupyter Notebook in your browser. If you replace the url ending 'tree' with 'lab' the server should load a lab book which is more user friendly 

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Acknowledgments
[rockacbruno](https://github.com/rochacbruno) and his template https://github.com/rochacbruno/python-project-template
