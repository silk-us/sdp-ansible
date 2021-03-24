#!/usr/bin/python


DOCUMENTATION = r'''
---
module: sdp_hostroupmapping

short_description: Module for host group mapping events on the Silk SDP platform. 

version_added: "0.1.1"

description: This is the module you would use to declare a host group mapping event on any Silk SDP deployment. 

options:
    hostgroupname:
        description: The name for the host group you wish to map the volume to.
        required: true
        type: str
    volumename:
        description: The name of the volume you wish to map. 
        required: true
        type: str


author:
    - J.R. Phillips (@JayAreP)
'''

EXAMPLES = r'''
# Create a host group mapping event.
- name: "Create Test Host mapping"
    sdp_hostgroupmapping:
        hostgroupname: "ATHG01"
        volumename: "ATV01"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: The id of the working event.
    type: str
    returned: always
    sample: '44'
hostgroup:
    description: The host group name of the working event.
    type: str
    returned: always
    sample: 'ATHG01'
volume:
    description: The volume name of the working event.
    type: str
    returned: always
    sample: 'ATV01'
'''

# Import the SDP module here as well. 
from krest import EndPoint
from ansible.module_utils.basic import *
import json
import os

try:
    import krest
    krestload = True
except ImportError:
    krestload = False

# Declare the class string 
sdpclass = "mappings"

def main():
  module_args = dict(
    hostgroupname=dict(type='str', required=True),
    volumename=dict(type='str', required=True),
    remove=dict(type='bool', required=False)
  )

  module = AnsibleModule(argument_spec=module_args)

# store the params as a reference hashtable for use later as vars["value"]
  vars = module.params

# temp username, password, server vars
  sdpuser = os.environ.get('SDPUSER', '-1')
  sdppass = os.environ.get('SDPPASS', '-1')
  sdphost = os.environ.get('SDPHOST', '-1')

# KREST Check, fail if no module. 
  if not krestload:
      module.fail_json(msg='The krest module is required for this module (pip install krest).')

# Connect to server

  try:
    sdp = krest.EndPoint(sdphost, sdpuser, sdppass, ssl_validate=False)
  except Exception as error:
    module.fail_json(msg=str(error))

# ----- Below here is specific endpoint ops ------
# Create the volume object (do not save yet)
  
  obj_request = sdp.new(sdpclass)

  # Store the volume
  volreqclass = "volumes"
  vols = sdp.search(volreqclass, name=vars["volumename"])

  # Store the host
  hostreqclass = "host_groups"
  hosts = sdp.search(hostreqclass, name=vars["hostgroupname"])

  if len(vols.hits) == 1:
      vol = vols.hits[0]
      obj_request.volume = vol
  else:
      error = "Volume {} was not found.".format(vars["volumename"])
      module.fail_json(msg=str(error))

  if len(hosts.hits) == 1:
      host = hosts.hits[0]
      obj_request.host = host
  else:
      error = "Host {} was not found.".format(vars["hostgroupname"])
      module.fail_json(msg=str(error))

  find = sdp.search(sdpclass, __limit=9999)
  for f in find.hits:
    if f.host.id == host.id and f.volume.id == vol.id:
        sdpobj = f
        break

# Since python can't simply test if a var exists...
  try: sdpobj
  except NameError: sdpobj = None

# Custom removal since the query for sdpobj is so fubar
  if vars["remove"] == True:
    if sdpobj == None:
        module.exit_json(
        changed=False,
        removed=False
      )
    elif sdpobj != None:
      sdpobj.delete()
      module.exit_json(
        changed=True,
        removed=True,
        id=sdpobj.id
      )

# If it does not, then save the above object as is.
  if sdpobj is None:
    try:
        result = obj_request.save()
    except Exception as error:
        module.fail_json(msg=str(error))
    changed=True
  else:
      result = sdpobj
      changed=False
    
# ------ No further change operations beyond this point. ------
# Once saved, invoke a find operation for the just-created object and use that to respond. 
  find = sdp.search(sdpclass, id=result.id)
  sdpobj = find.hits[0]
  if len(find.hits) == 1:
    response = {}
    response["id"] = sdpobj.id
    response["hostgroupname"] = sdpobj.host.name
    response["volume"] = sdpobj.volume.name

  module.exit_json(
    changed=changed,
    meta=response
  )

if __name__ == '__main__':
    main()