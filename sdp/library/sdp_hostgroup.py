#!/usr/bin/python

DOCUMENTATION = r'''
---
module: sdp_hostgroup

short_description: Module for host group objects on the Silk SDP platform. 

version_added: "0.1.1"

description: This is the module you would use to declare a host group object on any Silk SDP deployment. 

options:
    name:
        description: The name for the host group object
        required: true
        type: str
    description:
        description: Description for the host group. 
        required: false
        type: str
    allowDifferentHostTypes:
        description: Flag for allowing different host times. 
        required: false
        type: bool

author:
    - J.R. Phillips (@JayAreP)
'''

EXAMPLES = r'''
# Create a host group object.
- name: "Create Test Host Group"
    sdp_hostgroup:
        name: "ATHG01"
        description: "test host group"
        allowDifferentHostTypes: True
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: The id of the working object.
    type: str
    returned: always
    sample: '44'
name:
    description: The name of the working object.
    type: str
    returned: always
    sample: hostgroup06
description:
    description: Description for the host group. 
    returned: sometimes
    sample: "Group description"
allowDifferentHostTypes:
    description: Flag for allowing different host times. 
    returned: sometimes
    sample: False
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
sdpclass = "host_groups"

def main():
  module_args = dict(
    name=dict(type='str', required=True),
    description=dict(type='str', required=False),
    allowDifferentHostTypes=dict(type='bool', required=False),
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
  if vars["description"]:
    obj_request.description = vars["description"]
  if vars["allowDifferentHostTypes"]:
    obj_request.allow_different_host_types = vars["allowDifferentHostTypes"]
  

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
    if vars["allowDifferentHostTypes"]:
      if sdpobj.allow_different_host_types != vars["allowDifferentHostTypes"]:
        sdpobj.allow_different_host_types = vars["allowDifferentHostTypes"]
        try:
          sdpobj.save()
        except Exception as error:
          module.fail_json(msg=str(error))
        changed=True
      else:
        changed=False
    if vars["description"]:
      if sdpobj.description != vars["description"]:
        sdpobj.description = vars["description"]
        try:
          sdpobj.save()
        except Exception as error:
          module.fail_json(msg=str(error))
        changed=True
      else:
        changed=False
    else:
      changed=False


# Check variables that may change here (size, group membership, etc)


# ------ No further change operations beyond this point. ------
# Once saved, invoke a find operation for the just-created object and use that to respond. 
  find = sdp.search(sdpclass, name=obj_request.name)
  sdpobj = find.hits[0]
  if len(find.hits) == 1:
    response = {}
    response["id"] = sdpobj.id
    response["name"] = sdpobj.name
    response["description"] = sdpobj.description
    response["allowDifferentHostTypes"] = sdpobj.allow_different_host_types


  module.exit_json(
    changed=changed,
    meta=response
  )

if __name__ == '__main__':
    main()