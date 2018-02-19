#!/bin/bash
# This script creates a virtual environment for python 3.5
# Reference: https://docs.python.org/3/library/venv.html

set -e # if occur any error, exit

function to_console {
    echo -e "\n*** $1 ***\n"
}

cd $(dirname $0) && cd ..

to_console "creating a python virtual environment (venv) on folder 'venv-sandbox'"
python3 -m venv venv-sandbox

# in case of error on above statement run:
# python3 -m virtualenv venv-sandbox

to_console "activate virtual environment sandbox"
source venv-sandbox/bin/activate

to_console "verify and upgrade the pip version"
pip install --upgrade pip

to_console "checking and installing dependencies with pip"
pip install -r venv-script/requirements.txt

# if requirements.txt has the line 'pkg-resources==0.0.0'
# the source of it is a related bug in 'pip freeze' command, remove it
# reference: https://github.com/pypa/pip/issues/4022
