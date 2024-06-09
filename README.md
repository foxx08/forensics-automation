# Forensics Automation

## Prerequisites
* python 3
* pipenv installed ``pip install pipenv``
* virtual environment created with ``pipenv install``

### Jenkins Usage for total automation
* Requires Java > 11 for executing `Jenkins environment`
* Starting local Jenkins Controller ``./JenkinsController.sh``

## Tech Stack
| Components                  | Tool                                          | 
|-----------------------------|-----------------------------------------------|
| Pipeline Orchestration Tool | [Jenkins](Jenkins/JenkinsController.sh)       |
| Script Development          | [Python](Pipfile)                             | 
| Additional Forensic Tools   | [Foremost](https://foremost.sourceforge.net/) | 

## Usage
### image hash comparison
````
pipenv run pytest ./scripts/test_integrity_checker.py -s --test-object "<path/to/image>" --initial-hash "<hash-value>"
````

### image analysis 
````
 pipenv run python scripts/image_analyzer.py --image-path "<path/to/image>" --output-csv "<path/to/directory>"
````
#### further information
````
 pipenv run python scripts/image_analyzer.py --help
````
### data recovery 
#### active data
````
 pipenv run python scripts/data_retriever.py --image-path "<path/to/image>" --partitions-start "<partitions-startsector>" --output-directory "<path/to/directory>"
````
#### further information
````
 pipenv run python scripts/data_retriever.py --help
````
#### deleted data
````
foremost -i "<path/to/image>" -o "<path/to/directory>"
````

### file analysis
````
pipenv run python scripts/file_analyzer.py --folder-path "<path/to/directory>" --subfolder-path "<path/to/directory>"
````
#### further information
````
 pipenv run python scripts/file_analyzer.py --help
````
