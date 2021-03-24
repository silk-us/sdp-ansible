#!/usr/bin/python

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
sdpclass = "snapshots"

def main():
  module_args = dict(
    name=dict(type='str', required=True),
    volumegroup=dict(type='str', required=True),
    retentionpolicy=dict(type='str', required=True),
    exposable=dict(type='bool', required=False, default=True),
    deletable=dict(type='bool', required=False, defaul=True),
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
# Create the object (do not save yet)
  
# Set up all of the object data
# Snapshot name (for searching)
  finalsnapname = vars["volumegroup"] + ':' + vars["name"]

  obj_request = sdp.new(sdpclass)
  obj_request.short_name = vars["name"]

# vg

  vgsearch = sdp.search('volume_groups', name=vars["volumegroup"])
  if vgsearch.total == 1:
    vg = vgsearch.hits[0]
  elif vgsearch.total == 0:
    errormessage = "The volume group does not exist"
    module.fail_json(msg=str(errormessage))

  obj_request.source = vg

# rp

  rpsearch = sdp.search('retention_policies', name=vars["retentionpolicy"])
  if rpsearch.total == 1:
    rp = rpsearch.hits[0]
  elif rpsearch.total == 0:
    errormessage = "The retntion policy does not exist"
    module.fail_json(msg=str(errormessage))
  
  obj_request.retention_policy = rp

# Set up the retention policy vars["retentionpolicy"]

# Check to see if object already exists. 
  find = sdp.search(sdpclass, name=finalsnapname)
  if vars["remove"] == True:
    if len(find.hits) == 1:
      sdpobj = find.hits[0]
      sdpobj.delete()
      module.exit_json(
        changed=True,
        removed=True,
        id=sdpobj.id
      )
    else:
        module.exit_json(
        changed=False,
        removed=False
      )

# If it does not, then save the above object as is.
  if len(find.hits) == 0:
    try:
        obj_request.save()
        changed=True
    except Exception as error:
        module.fail_json(msg=str(error))
  else:
    changed=False
    
# Otherwise, check the current object's secondary parameters against the request, and adjust as needed. 

# ------ No further change operations beyond this point. ------
# Once saved, invoke a find operation for the just-created object and use that to respond. 
  find = sdp.search(sdpclass, name=finalsnapname)
  sdpobj = find.hits[0]
  if len(find.hits) == 1:
    response = {}
    response["id"] = sdpobj.id
    response["name"] = sdpobj.name
    response["retentionpolicy"] = sdpobj.retention_policy.name
    response["deletable"] = sdpobj.is_auto_deleteable
    response["exposable"] = sdpobj.is_exposable


  module.exit_json(
    changed=changed,
    meta=response
  )

if __name__ == '__main__':
    main()