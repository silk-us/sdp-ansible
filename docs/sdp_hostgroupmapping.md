# sdp_hostgroupmapping

This module allows you to create and manage mapping objects for hosts on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `hostgroupname` - (`string`) - The name of the host group for this mapping. 
* `volumename` - (`string`) - The name of the volume for this mapping. 

### Optional
* `remove` - (`bool`) - Remove the object. 


## Examples
### 1. 
This example creates a host object named `LinuxHost` with 3 PWWNs. 
```yaml
sdp_hostmapping:
    hostgroupname: "Host Group 01"
    volumename: "Volume01"
```

## Register response:
```json
{
    "changed": bool,
    "failed": bool,
    "meta": {
        "id": int,
        "hostgroupname": string,
        "volume": string
    }
}
```