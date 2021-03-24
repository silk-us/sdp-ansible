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
sdpclass = "retention_policies"

def main():
  module_args = dict(
    name=dict(type='str', required=True),
    snapshots=dict(type='int', required=False, default=0),
    weeks=dict(type='int', required=False, default=0),
    days=dict(type='int', required=False, default=0),
    hours=dict(type='int', required=False, default=0),
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
  obj_request.name = vars["name"]
  obj_request.num_snapshots = vars["snapshots"]
  obj_request.weeks = vars["weeks"]
  obj_request.days = vars["days"]
  obj_request.hours = vars["hours"]

# Check to see if object already exists. 
  find = sdp.search(sdpclass, name=obj_request.name)
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
        sdpobj = obj_request.save()
    except Exception as error:
        module.fail_json(msg=str(error))
    
    changed=True
# Otherwise, check the current object's secondary parameters against the request, and adjust as needed. 
  else:
    sdpobj = find.hits[0]
    if vars["snapshots"]:
      if sdpobj.num_snapshots != vars["snapshots"]:
        sdpobj.num_snapshots = vars["snapshots"]
        try:
          sdpobj.save()
        except Exception as error:
          module.fail_json(msg=str(error))
        changed=True
      else:
        changed=False
    if vars["weeks"]:
      if sdpobj.weeks != vars["weeks"]:
        sdpobj.weeks = vars["weeks"]
        try:
          sdpobj.save()
        except Exception as error:
          module.fail_json(msg=str(error))
        changed=True
      else:
        changed=False
    if vars["days"]:
      if sdpobj.days != vars["days"]:
        sdpobj.days = vars["days"]
        try:
          sdpobj.save()
        except Exception as error:
          module.fail_json(msg=str(error))
        changed=True
      else:
        changed=False
    if vars["hours"]:
      if sdpobj.hours != vars["hours"]:
        sdpobj.hours = vars["hours"]
        try:
          sdpobj.save()
        except Exception as error:
          module.fail_json(msg=str(error))
        changed=True
      else:
        changed=False

# ------ No further change operations beyond this point. ------
# Once saved, invoke a find operation for the just-created object and use that to respond. 
  find = sdp.search(sdpclass, name=obj_request.name)
  sdpobj = find.hits[0]
  if len(find.hits) == 1:
    response = {}
    response["id"] = sdpobj.id
    response["name"] = sdpobj.name
    response["snapshots"] = sdpobj.num_snapshots
    response["weeks"] = sdpobj.weeks
    response["days"] = sdpobj.days
    response["hours"] = sdpobj.hours



  module.exit_json(
    changed=changed,
    meta=response
  )

if __name__ == '__main__':
    main()