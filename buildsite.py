import os
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from enum import Enum

def main():
  print('Due to Simlink creation privileges. RUN THIS SCRIPT IN AN ELEVATED SHELL')
  parser = argparse.ArgumentParser(description='Generate personal website shelving. Available: ' + str(PPROJ_DESCR))
  parser.add_argument('--check-clone', action='store_true',
                      help='Mostly used the first time. Check if shelv projects should be cloned.')
  parser.add_argument('--only-this', 
                      help='Only checks for updates for this project')
  args = parser.parse_args()
 
  pprojname = args.only_this
  if (pprojname):
    deploy_project_assets(pprojname)
  generate_index()

"""
The index of this shelving website is generated
"""
def generate_index():
  pass

"""
Parameters
----------
pprojname : str 
  project's name to deploy
"""  
def deploy_project_assets(pprojname):
  pproject = PPROJ_DESCR.get(pprojname)
  if pproject == None:
    print('ERROR: There is no project called {}'.format(pprojname))
    

  if pproject.linkall:
    link_assets(pproject)


"""
Clones the pproject if the repository does not exist, otherwise pull any changes from 
the remote. Then makesa soft link to that repository.

Parameters
----------
pproject: PProject
  The pproject to link
"""
def link_assets(pproject):
  clone_pprojects(pproject)
  pprojpath = Path(PPROJ_ORIGN)/pproject.name
  deploypath = PPROJ_DPLOY/pproject.id
  if not Path(pproject.id).is_symlink():
    print('INFO: Linking local copy of {} repository to deploy folder at {}'.format(pproject.name, PPROJ_DPLOY))
    os.symlink(pprojpath, pproject.id, target_is_directory=True)

def copy_assets():
  pprojpath = Path(PPROJ_ORIGN)/pprojname
  deploypath = PPROJ_DPLOY/pproject.id
  if not (deploypath).exists():
    os.makedirs(deploypath)

  for a in pproject.assets:
    src = pprojpath/a.src
    dst = deploypath
    if a.action is AssetAction.COPY:
      dst /= a.dst
      if src.is_file():
        shutil.copy(src, dst)
      else:
        try:
          shutil.copytree(src, dst, dirs_exist_ok=True)
        except FileNotFoundError:
          print('"{}" does not exist in "{}" folder'.format(src, pprojname))
    elif a.action is AssetAction.LINK:
      os.symlink(src.resolve(), 'tmpname.html', target_is_directory=src.is_dir()) # resolve is relative to cwd
      shutil.move('tmpname.html', dst)
      # os.rename('tmpname.html', a.src) # TODO
    else:
      raise Error('UNKNOWN ACTION {}! !'.format(a.action))
  
"""
Reads the pprojdescriptor.json file in order to retrieve information about the main
relevant paths etc. See the file fore more details.
Markdown file to publish, descriptions, relative projects, if the project has another
"""  
def parse_project_descriptor():
  descr = open('pprojdescriptor.json', 'r', encoding='utf-8').read()
  return json.loads(descr).get('pprojects')

"""
Parameters
----------
pprojects:
  list of projects to clone

Notes
-----
The command must be passed as an array of strings in Python < 3.11.2
"""
def clone_pprojects(pproject):
  ppath = Path(PPROJ_ORIGN)/pproject.name
  if ppath.exists():
    print('Running git pull .. .')
    # subprocess.run('git pull', cwd=ppath)
  else:
    print('Running git clone .. .')
    subprocess.run('git clone {0}'.format(pproject.repourl).split(' '), cwd=PPROJ_ORIGN)

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
linkall: boolean
  Flag if that project should be cloned also on the webserver.
"""
class PProject:
  clone_list = []

  def __init__(self, id, name, descr, assets, repourl, linkall):
    self.id = id
    self.name = name
    self.descr = descr
    self.assets = assets
    self.pprojects = []
    self.repourl = repourl
    self.linkall = linkall

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

  def parse_asset_actions(jsonassets):
    if jsonassets == None:
      return None
    assetactions = []
    for aact in jsonassets:
      if aact.get('lnk') == None:
        adeploy = AssetDeploy(
          src=aact.get('src'),
          dst=aact.get('dst'),
          action=AssetAction.COPY
        )
      else:
        adeploy = AssetDeploy(
          src=aact.get('lnk'),
          dst=None,
          action=AssetAction.LINK
        )
      assetactions.append(adeploy)
    return assetactions
  
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
          assets=PProject.parse_asset_actions(pproj.get('assets')),
          repourl=pproj.get('repourl'),
          linkall=True if pproj.get('linkall') else None
        )
        parent.pprojects.append(ppj)
        ppjchildren = pproj.get('pprojects')
        if ppjchildren != None:
          parse_pprojects(ppj, ppjchildren)
      
    parse_pprojects(root, pprojects)
    return root

"""
Enum to represent the action to do with an asset: copy or link
"""
class AssetAction(Enum):
  COPY = 1
  LINK = 2

"""
Describes how the action should be performed. 
If COPY is specified, then de src file must be copyed to dst.
If LINK is specified, then de src file must be linked.
"""
class AssetDeploy:
  def __init__(self, src, dst, action):
    self.src = src
    self.dst = dst
    self.action = action

  def __str__(self):
    if self.action is AssetAction.COPY:
      return 'COPY {} to {}'.format(self.src, self.dst)
    elif self.action is AssetAction.LINK:
      return 'LINK to {}'.format(self.src)
    else:
      raise Error('UNKNOWN ACTION')

  def __repr__(self):
    return self.__str__()


"""
Utility class employed to serialize the PProject object. Converts the 
internal python dictionary snake case convention to camel case json
convention. Removes those pprojects list that does not have any 
related pprojects.
"""
class PProjectEncoder(json.JSONEncoder):
  def default(self, o):
    linkall = o.__dict__['linkall']
    del o.__dict__['linkall']
    if linkall == True:
      o.__dict__['linkall'] = True

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