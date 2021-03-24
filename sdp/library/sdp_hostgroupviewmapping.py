#!/usr/bin/python

DOCUMENTATION = r'''
---
module: sdp_hostgroupviewmapping

short_description: Module for host mapping events on the Silk SDP platform. 

version_added: "0.1.1"

description: This module allows you to create and manage host group view mapping objects on the SDP platform. 

options:
    hostgroupname:
        description: The host group name name for the host mapping event
        required: true
        type: str
    snapshotview:
        description: The snapshot view name for the host mapping event.
        required: true
        type: str

author:
    - J.R. Phillips (github - @JayAreP)
'''

EXAMPLES = r'''
# Create a host mapping event.
- name: "Create Test Host mapping"
    sdp_hostgroupviewmapping:
        hostgroupname: "ATHG01"
        snapshotview: "VolGrp01:backup_02-view"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: The id of the working event.
    type: int
    returned: always
    sample: '44'
hostname:
    description: The host name of the working event.
    type: str
    returned: always
    sample: 'ATH01'
volume:
    description: The snapshot view name of the working event.
    type: str
    returned: always
    sample: 'VolGrp01:backup_02-view'

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
    snapshotview=dict(type='str', required=True),
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

  # Store the snapshot view
  viewrequest = "snapshots"
  views = sdp.search(viewrequest, name=vars["snapshotview"])

  # Store the host
  hostreqclass = "hosts_groups"
  hosts = sdp.search(hostreqclass, name=vars["hostgroupname"])

  if len(views.hits) == 1:
      view = views.hits[0]
      obj_request.volume = view
  else:
      error = "Snapshot view {} was not found.".format(vars["snapshotview"])
      module.fail_json(msg=str(error))

  if len(hosts.hits) == 1:
      host = hosts.hits[0]
      obj_request.host = host
  else:
      error = "Host {} was not found.".format(vars["hostname"])
      module.fail_json(msg=str(error))

  find = sdp.search(sdpclass, __limit=9999)
  for f in find.hits:
      if f.host.id == host.id and f.volume.id == view.id:
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
        changed = True
    except Exception as error:
        module.fail_json(msg=str(error))
  else:
      result = sdpobj
      changed = False
    
# ------ No further change operations beyond this point. ------
# Once saved, invoke a find operation for the just-created object and use that to respond. 
  find = sdp.search(sdpclass, id=result.id)
  sdpobj = find.hits[0]
  if len(find.hits) == 1:
    response = {}
    response["id"] = sdpobj.id
    response["hostname"] = sdpobj.host.name
    response["volume"] = sdpobj.volume.name

  module.exit_json(
    changed=changed,
    meta=response
  )

if __name__ == '__main__':
    main()