# TODOS
[ ] Add 4 audio recordings in each language    
[ ] Link your English certificate to your profile description    
[ ] Link something (e.g. youtube vid) in order to demo. your speaking    
[ ] Rearrange your skillset more comprehesively    
[ ] Link the companies names with their web pages
[ ] Add side projects to your curriculum   

# Usage
1. edit the main source of truth aka cv.yml
2. `$> cd multiform-cv`
3. `$> python -m venv venv`
4. `$> venv\Scripts\activate.bat`
5. `$> pip install -r requirements.txt`
6. `$> cd src`
7. `$> python3 multiform-gen.py`
8. output in ../cv folder

# About
Python script that generate Juan Camilo's CV in several template formats    
but with the same content.
The formats are:
    - LaTeX
    - HTML for desktop browsers
    - HTML for mobile browsers

This script does not provide you with the entire html o latex document, 
only provides well formated content that should be placed by hand (at least
for this version) in your templates.

## Development setup
1. Install python
2. Install PIP
3. Create your environment: `$ python3 -m venv env`
4. Activate your environment: `$ source env/bin/activate`
5. Deactivate your environment: `$ deactivate`

## How to run
`$ python3 src/multiform-gen.py`

## How to update deps.
`$ pip freeze > requirements.txt`

# Docs's docs
## venv
https://docs.python.org/3/library/venv.html#how-venvs-work
## Jinja2
https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters
https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-filters
## PyYAML
https://pyyaml.org/wiki/PyYAMLDocumentation

