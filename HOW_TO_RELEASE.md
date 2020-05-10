# How to release

1. do all the usual Git stuff
2. build Python binaries, use the interpreter where all the required libraries are installed:
    ```bash
    python setup.py sdist bdist_wheel bdist_egg
    ```
    > - the command above will populate the `dist/` directory with package binaries
    > - package `wheel` needs to be installed in order for `bdist_wheel` to work
3. upload binaries to *PyPi*, use the interpreter where the package `twine` is installed
    ```bash
    python -m twine upload -s -i <key_id> dist/*
    ```
    > - `-s` - require signing of packages
    > - `-i` - identity of the PGP key to use for signing

## How to install into local virtual environment:

1. do all the usual Git stuff
2. run 
    ```bash
    cd ddalg
    pip install .
    ```
