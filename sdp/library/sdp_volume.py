#!/usr/bin/python

DOCUMENTATION = r'''
---
module: sdp_host

short_description: Module for volume objects on the Silk SDP platform. 

version_added: "0.1.1"

description: This is the module you would use to declare a volume object on any Silk SDP deployment. 

options:
    name:
        description: The name for the volume object
        required: true
        type: str
    sizeInGB:
        description: The size of the volume in GB
        required: true
        type: int
    volumegroup:
        description: The name of the existing volume group to include this volume object in. 
        required: false
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@JayAreP)
'''

EXAMPLES = r'''
# Create a host object.
- name: "Create Volume"
  sdp_volume: 
    name: "volume06"
    sizeInGB: 40
    volumegroup: "vg2"
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
    sample: 'volume06'
size:
    description: The size of the working object in bytes.
    type: str
    returned: always
    sample: '41984000'
volumegroup:
    description: The name of the Volume Group of the working object.
    type: str
    returned: sometimes
    sample: 'vg2'
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
sdpclass = "volumes"

def main():
  module_args = dict(
    name=dict(type='str', required=True),
    sizeInGB=dict(type='int', required=True),
    volumegroup=dict(type='str', required=True),
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

  size = vars["sizeInGB"]*2**20
  obj_request.size = size

  findvg = sdp.search("volume_groups", name=vars["volumegroup"])
  if len(findvg.hits) == 1:
    vg = findvg.hits[0]
    obj_request.volume_group = vg

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
    if sdpobj.volume_group.name != vars["volumegroup"]:
      sdpobj.volume_group = vg
      try:
        sdpobj.save()
      except Exception as error:
        module.fail_json(msg=str(error))
      changed=True
    elif sdpobj.size < size:
      sdpobj.size = size
      try:
        sdpobj.save()
      except Exception as error:
        module.fail_json(msg=str(error))
      changed=True
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
    response["size"] = sdpobj.size
    response["volumegroup"] = sdpobj.volume_group.name

  module.exit_json(
    changed=changed,
    meta=response
  )


if __name__ == '__main__':
    main()