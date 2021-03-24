# sdp_volumegroup

This module allows you to create and manage volume group objects on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `name` - (`string`) - The desired name for the volume group object.

### Optional
* `quotaInGB` - (`int`) - The desired quota (in GB) for the volume group object. 
* `dedupe` - (`bool`) - Enable (or disable) de-duplication for volumes contained in this volume group. 
* `remove` - (`bool`) - Remove the object. Volume Groups must be empty prior to removal. 


## Examples
### 1. 
This example creates a volume group object named "VolumeGroup01" a quota of 500GB and dedupe enabled. 
```yaml
sdp_volumegroup: 
    name: "VolumeGroup01"
    quotaInGB: 500
    dedupe: True
```

## Register response:
```json
{
    "changed": bool,
    "failed": bool,
    "meta": {
        "id": int,
        "name": string,
        "quota": int,
        "dedupe": bool
    }
}
```