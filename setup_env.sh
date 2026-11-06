#!/usr/bin/env bash
# Create the project virtual environment (.venv) and install dependencies.
#
# Usage, from the repo root in Git Bash, macOS or Linux:
#     ./setup_env.sh
#     PYTHON=python3.13 ./setup_env.sh    # use a specific Python

set -euo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-python}"

# venv puts the interpreter in Scripts/ on Windows and bin/ elsewhere
if [[ -f .venv/Scripts/python.exe ]]; then
    VENV_PYTHON=.venv/Scripts/python.exe
elif [[ -f .venv/bin/python ]]; then
    VENV_PYTHON=.venv/bin/python
else
    echo "Creating virtual environment in .venv ..."
    "$PYTHON" -m venv .venv
    if [[ -f .venv/Scripts/python.exe ]]; then
        VENV_PYTHON=.venv/Scripts/python.exe
    else
        VENV_PYTHON=.venv/bin/python
    fi
fi

echo "Installing dependencies from requirements.txt ..."
"$VENV_PYTHON" -m pip install --upgrade pip
"$VENV_PYTHON" -m pip install -r requirements.txt

echo
if [[ -f .venv/Scripts/activate ]]; then
    echo "Done. Activate the environment with:  source .venv/Scripts/activate"
else
    echo "Done. Activate the environment with:  source .venv/bin/activate"
fi
