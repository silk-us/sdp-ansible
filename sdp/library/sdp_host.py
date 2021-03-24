#!/usr/bin/python

DOCUMENTATION = r'''
---
module: sdp_host

short_description: Module for host objects on the Silk SDP platform. 

version_added: "0.1.1"

description: This is the module you would use to declare a host object on any Silk SDP deployment. 

options:
    name:
        description: The name for the host object
        required: true
        type: str
    type:
        description: The host type. Linux, Windows, or ESX
        required: true
        type: str
    hostgroup:
        description: The name of the existing host group to include this host object in. 
        required: false
        type: str
    iqn:
        description: The initiator name (iqn) for the host object. Only valid on SDPs configured for iSCSI. 
        required: false
        type: str
    pwwn:
        description: The Port WWNs for the host object. Only valid on SDPs configured for FibreChannel. 
        required: false
        type: list

author:
    - J.R. Phillips (github - @JayAreP)
'''

EXAMPLES = r'''
- name: "Create Host"
  sdp_host: 
    name: "testHost01"
    type: "Linux"
    hostgroup: "testGroup01"
    pwwn: 
      - 00:11:22:33:44:55:66:77
      - 00:11:22:33:44:55:66:88
'''

RETURN = r'''
id:
    description: The id of the working object.
    type: int
    returned: always
    sample: '44'
name:
    description: The name of the working object.
    type: str
    returned: always
    sample: 'host06'
volumegroup:
    description: The name of the Host Group of the working object.
    type: str
    returned: sometimes
    sample: 'hg2'
pwwn:
    description: The PWWN list of the working object in bytes.
    type: list
    returned: sometimes
    sample: '41984000'
iqn:
    description: The iqn of the working object.
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
sdpclass = "hosts"

def main():
  module_args = dict(
    name=dict(type='str', required=True),
    type=dict(type='str', required=True),
    iqn=dict(type='str', required=False),
    pwwn=dict(type='list', required=False),
    hostgroup=dict(type='str', required=False),
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
# Create the host object (do not save yet)
  obj_request = sdp.new(sdpclass)
  obj_request.name = vars["name"]
  obj_request.type = vars["type"]

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
  else:
    sdpobj = find.hits[0]
    changed=False

# Check variables that may change here (size, group membership, etc)
  if vars["hostgroup"]:
    find = sdp.search(sdpclass, name=obj_request.name)
    sdpobj = find.hits[0]
    findhg = sdp.search("host_groups", name=vars["hostgroup"])
    if len(findhg.hits) == 1:
      hg = findhg.hits[0]
    if sdpobj.host_group:
      if sdpobj.host_group.name == vars["hostgroup"]:
        changed=False
      else:
        sdpobj.host_group = hg
        sdpobj.save()
        changed=True
    else:
      sdpobj.host_group = hg
      sdpobj.save()
      changed=True
  elif sdpobj.host_group:
    sdpobj.host_group = ""
    sdpobj.save()
    changed=True

  if vars["pwwn"]:
    portclass = "host_fc_ports"
    for i in vars["pwwn"]:
      findports = sdp.search(portclass, pwwn__in=i)
      if len(findports.hits) == 0:
          port_request = sdp.new(portclass)
          port_request.pwwn = i
          port_request.host = sdpobj
          port_request.save()
          changed=True
      else:
          portobj = findports.hits[0]
          if portobj.host != sdpobj:
            portobj.host = sdpobj
            portobj.save()
            changed=True
          else:
            changed=False

  if vars["iqn"]:
    iqn = vars["iqn"]
    portclass = "host_iqns"
    findports = sdp.search(portclass, pwwn__in=iqn)
    if len(findports.hits) == 0:
        port_request = sdp.new(portclass)
        port_request.iqn = iqn
        port_request.host = sdpobj
        port_request.save()
        changed=True
    else:
        portobj = findports.hits[0]
        if portobj.host != sdpobj:
          portobj.host = sdpobj
          portobj.save()
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
    if vars["hostgroup"]:
      response["hostgroup"] = sdpobj.host_group.name
    else:
      response["hostgroup"] = ""
    
    if vars["pwwn"]:
      response["pwwn"] = vars["pwwn"]

    if vars["iqn"]:
      response["iqn"] = vars["iqn"]

  module.exit_json(
    changed=changed,
    meta=response
  )


if __name__ == '__main__':
    main()