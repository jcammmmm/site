# About
This project mostly contains references to other projects and how
to build the personal website.   
JSON whas choosed as descriptor language since the parser is already 
in python default librery set. Another option can be use YAML but 
this requires additional library imports and we want that this script
will be the most lightweight possible.    
This project was made in order to be directly clone on your `public_html`
folder in your webserver. Given that the only thing that left is to
syncrhonize your changes here and the pull the changes in your web server.


# Usage
This is script was written on `Python 3.10.6`. Update the site:   
  1. `py generate.py --only-this projectname`
  2. `git commit -m ""`
  3. `git push`

Then pull the changes in your webserver:   
  1. `git pull`

# TODOs
[] Write the main script as a bash script.
[] Write the main script as a windows shell script.
