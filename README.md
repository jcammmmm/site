## About
This `buildsite.py` script must be run on _development_ machine in order to populate 
the `site` folder. This folder should be versioned in a remote repository in order
to pull its changes within the webserver.
If the project does not have a remote repository, that project does not exist.

## Environment
This software shall be installed on the host system:
- `Python 3.10.6`
- `git`

## About pprojdescritor.json
- Every project has the following madatory attributes: 
    * **id**: a compact and unique name to fetch this project from webserver    
    * **name**: name with dashes uses at file system level  
    * **descr**: a short description of the project   
    * **repourl**: where a copy of the entire project is located   
- And the following optional attributes:   
    * **assets**: A list of objects that describes how the project assets should be deployed   
        The asset action object has the following attributes:   
        - **src**: The file or folder to be deployed on webserver
        - **dst**: The destination or new name to be used as deployemnt. If ommited
                   the destination name is the same as in **src**
        - **lnk**: If the file shall be linked instead of copyted
    * **linkall**: if the project should be cloned and linked with that local copy
- If a project has de attribute **linkall** set to true, it means that
  the project should be cloned in the webserver at the same level of the folder containing
  this script, because will be served directly; for that reason assets list will be ignored
  if are present.

## Usage
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


## Additional considerations
- Avoid data duplication. For that, the project linking approach was implemented when almost
  the entire repository was copied.

# Server setup
```sh
sudo apt update
sudo apt install apache2
sudo systemctl status apache2
hostname -I

sudo apt install git
git clone https://github.com/jcammmmm/site
```

# TODOs
[] Write the main script as a bash script.
[] Write the main script as a windows shell script.
