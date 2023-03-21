import os
import argparse
import json
import shutil
import subprocess
from pathlib import Path

def main():
  parser = argparse.ArgumentParser(description='Generate personal website shelving. Available: ' + str(PPROJ_DESCR))
  parser.add_argument('--check-clone', action='store_true',
                      help='Mostly used the first time. Check if shelv projects should be cloned.')
  parser.add_argument('--only-this', 
                      help='Only checks for updates for this project')
  args = parser.parse_args()
  if (args.check_clone):
    pproj_clone = PPROJ_DESCR.get_clone_list()
    clone_pprojects(pproj_clone)
    return
  pproject = args.only_this
  if (pproject):
    deploy_project_assets(pproject)
  generate_index()

"""
The index of this shelving website is generated
"""
def generate_index():
  pass
    
def deploy_project_assets(pproject):
  pprojpath = Path(PPROJ_ORIGN)/pproject
  assets = PPROJ_DESCR.get(pproject).assets
  if not (PPROJ_DPLOY/pproject).exists():
    os.makedirs(PPROJ_DPLOY/pproject)

  for a in assets:
    src = pprojpath/a
    dst = PPROJ_DPLOY/pproject/a
    if (src).is_file():
      shutil.copy(src, dst)
    else:
      try:
        shutil.copytree(src, dst, dirs_exist_ok=True)
      except FileNotFoundError:
        print('"{}" does not exist in "{}" folder'.format(src, pproject))
      

"""
Reads the pprojdescriptor.json file in order to retrieve information about the main
relevant paths etc. See the file fore more details.
Markdown file to publish, descriptions, relative projects, if the project has another
"""  
def parse_project_descriptor():
  descr = open('pprojdescriptor.json', 'r', encoding='utf-8').read()
  return json.loads(descr).get('pprojects')

"""
If the folder name exists within the pproject list of the current
pprojects tree, it means that the folder can be served in some way
and the project can be published also.

Return
------
list:
  a list of projects that are not cloned.
"""
# REMOVE THIS
def check_if_projects_were_cloned():
  to_clone = []
  os.chdir(PPROJ_ORIGN)
  for p in os.listdir():
    # print('#> ' + str(PPROJ_DESCR.pprojects))
    if p not in PPROJ_DESCR.pprojects:
      to_clone.append(p)
  return to_clone;  

"""
Parameters
----------
pprojects:
  list of projects to clone

"""
def clone_pprojects(pprojects_clone):
  for p in pprojects_clone:
    ppath = Path(PPROJ_ORIGN)/p
    if ppath.exists():
      subprocess.run('git status', cwd=ppath)
    else:
      pproject = PPROJ_DESCR.get(p)
      subprocess.run('git clone {0}'.format(pproject.repourl), cwd=PPROJ_ORIGN)

"""
Attributes
----------
id: str
  It is an allias for name attribute, it is used mostly than name
  becuase it should not contain blank character and only lower case 
  letters
name: str
  The name given to the associated git remote repository
descr: str
  Description
assets: list: str
  Strings that references the resource file or name to be published
  on the web server.
pprojects: list: PProject
  The child projects related to this project. They are not dependencies,
  the often are specialization on the main topic or a series of posts
  on the same topic.
clone_complete: boolean
  Flag if that project should be cloned also on the webserver.
"""
class PProject:
  clone_list = []

  def __init__(self, id, name, descr, assets, repourl, clone_complete):
    self.id = id
    self.name = name
    self.descr = descr
    self.assets = assets
    self.pprojects = []
    self.repourl = repourl
    self.clone_complete = clone_complete

  def __str__(self):
    return str(self.__dict__)
  
  def __repr__(self):
    return self.__str__()
  
  def get_clone_list(self):
    try:
      for p in self.pprojects:
        if p.clone_complete:
          PProject.clone_list.append(p.name)
        p.get_clone_list()
    except AttributeError:
      pass
    return PProject.clone_list
  
  def get(self, pprojname):
    pproj = None
    for p in self.pprojects:
      if p.name == pprojname:
        return p
      pproj = p.get(pprojname)
    return pproj
  
  def build_pproject_tree(jsondescriptor):
    root = PProject(
      'root', 
      'rootproject', 
      'this is a root project that points to other projects', 
      [], 
      None,
      False)
    pprojdescriptor = open(jsondescriptor, 'r', encoding='utf-8').read()
    pprojects = json.loads(pprojdescriptor).get('pprojects')

    def parse_pprojects(parent, jsonpprojects):
        for pproj in jsonpprojects: 
          ppj = PProject(
            id=pproj.get('id'),
            name=pproj.get('name'),
            descr=pproj.get('descr'),
            assets=pproj.get('assets'),
            repourl=pproj.get('repourl'),
            clone_complete=True if pproj.get('cloneComplete') else None
          )
          parent.pprojects.append(ppj)
          ppjchildren = pproj.get('pprojects')
          if ppjchildren != None:
            parse_pprojects(ppj, ppjchildren)
      
    parse_pprojects(root, pprojects)
    return root

"""
Utility class employed to serialize the PProject object. Converts the 
internal python dictionary snake case convention to camel case json
convention. Removes those pprojects list that does not have any 
related pprojects.
"""
class PProjectEncoder(json.JSONEncoder):
  def default(self, o):
    clone_complete = o.__dict__['clone_complete']
    del o.__dict__['clone_complete']
    if clone_complete == True:
      o.__dict__['cloneComplete'] = True

    url = o.__dict__['url']
    del o.__dict__['url']
    if url != None:
      o.__dict__['url'] = url

    if len(o.__dict__['pprojects']) == 0:
      del o.__dict__['pprojects']
    return o.__dict__

"""
Driver method
"""
if __name__ == '__main__':
    PPROJ_DPLOY = Path('./site')
    PPROJ_DESCR = PProject.build_pproject_tree('pprojdescriptor.json')
    # relative to this script
    PPROJ_ORIGN = '..'
    # print(json.dumps(PPROJ_DESCR, cls=PProjectEncoder, indent=4))
    main()