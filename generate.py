import os
import argparse
import json
import shutil
from pathlib import Path

def main():
  parser = argparse.ArgumentParser(description='Generate personal website shelving. Available: ' + str(PPROJ_DESCR))
  parser.add_argument('--check-clone', action='store_true',
                      help='Mostly used the first time. Check if shelv projects should be cloned.')
  parser.add_argument('--only-this', 
                      help='Only checks for updates for this project')
  
  args = parser.parse_args()
  
  if (args.check_clone):
    pproj_clone = check_if_projects_were_cloned()
    print(pproj_clone)
    clone_pprojects(pproj_clone) # <= TODO
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
  print(os.listdir())
  if not (PPROJ_DPLOY/pproject).exists():
    os.makedirs(PPROJ_DPLOY/pproject)

  for a in assets:
    src = pprojpath/a
    dst = PPROJ_DPLOY/pproject/a
    if (src).is_file():
      shutil.copy(src, dst)
    else:
      shutil.copytree(src, dst, dirs_exist_ok=True)
      

"""
Reads the pprojdescriptor.json file in order to retrieve information about the main
Markdown file to publish, descriptions, relative projects, if the project has another
relevant paths etc. See the file fore more details.
"""  
def parse_project_descriptor():
  descr = open('pprojdescriptor.json', 'r', encoding='utf-8').read()
  return json.loads(descr).get('pprojects')

"""
Return
------
list:
  a list of projects that are not cloned.
"""
def check_if_projects_were_cloned():
  to_clone = []
  os.chdir('..')
  for p in os.listdir():
    if p not in PPROJ_DESCR.get('pprojects'):
      to_clone.append(p)
  return to_clone;  

"""
Parameters
----------
pprojects:
  list of projects to clone

"""
def clone_pprojects(pprojects):
   # TODO
   pass

class PProject:
  def __init__(self, id, name, descr, assets):
    self.id = id
    self.name = name
    self.descr = descr
    self.assets = assets
    self.pprojects = []

  def __str__(self):
    return str(self.__dict__)
  
  def __repr__(self):
    return self.__str__()
  
  def get(self, pprojname):
    pproj = None
    for p in self.pprojects:
      if p.name == pprojname:
        return p
      pproj = p.get(pprojname)
    return pproj
  
  def build_pproject_tree(jsondescriptor):
    root = PProject('root', 'rootproject', 'this is a root project that points to other projects', [])
    pprojdescriptor = open(jsondescriptor, 'r', encoding='utf-8').read()
    pprojects = json.loads(pprojdescriptor).get('pprojects')

    def parse_pprojects(parent, jsonpprojects):
        for pproj in jsonpprojects: 
          ppj = PProject(
            id=pproj.get('id'),
            name=pproj.get('name'),
            descr=pproj.get('descr'),
            assets=pproj.get('assets'),
          )
          parent.pprojects.append(ppj)
          ppjchildren = pproj.get('pprojects')
          if ppjchildren != None:
            parse_pprojects(ppj, ppjchildren)
      
    parse_pprojects(root, pprojects)
    return root

class PProjectEncoder(json.JSONEncoder):
  def default(self, o):
    if len(o.__dict__['pprojects']) == 0:
      del o.__dict__['pprojects']
    return o.__dict__

if __name__ == '__main__':
    PPROJ_DPLOY = Path('./site')
    PPROJ_DESCR = PProject.build_pproject_tree('pprojdescriptor.json')
    # relative to this script
    PPROJ_ORIGN = '..'
    # print(json.dumps(PPROJ_DESCR, cls=PProjectEncoder, indent=4))
    main()