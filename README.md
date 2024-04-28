# Forensics Automation

## Prerequisites
* python 3
* pipenv installed ``pip install pipenv``
* virtual environment created with ``pipenv install``

## Usage
### initial image hash comparision with:
````
pipenv run pytest ./scripts/test_integrity_checker.py -s --test-object "<path/to/image>" --initial-hash "<hash-value>"
````