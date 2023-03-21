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

# Environment
This software shall be installed on the host system:
- `Python 3.10.6`
- `git`

# Usage
This is script was written on `Python 3.10.6`. Update the site:   
  1. Copy and update the documents to publish on your website:  
      `py buildsite.py --only-this projectname`
  2. Launch a development server and test your results    
      `py -m http.server 9988`  
  2. Save your changes locally:     
      `git commit -m ""`
  3. Upload your changes to the remote server:   
      `git push`

Then, in your webserver:
  4. Pull the changes made previously:   
      `git pull`

# TODOs
[] Write the main script as a bash script.
[] Write the main script as a windows shell script.
