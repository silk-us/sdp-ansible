# sdp_volume

This module allows you to create and manage volume objects on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `name` - (`string`) - The desired name for the volume object.
* `sizeInGB` - (`int`) - The desired sie (in GB) for the volume object.

### Optional
* `volumegroup` - (`string`) - The desired volume group name for the volume object. 
* `remove` - (`bool`) - Remove the object. 

## Examples
### 1. 
This example creates a volume object named "volume05" and places it inside the volume group named "volumeGroup01". 
```yaml
sdp_volume: 
    name: "volume05"
    sizeInGB: 40
    volumegroup: "volumeGroup01"
```

## Register response:
```json
{
    "changed": bool,
    "failed": bool,
    "meta": {
        "id": int,
        "name": string,
        "size": int,
        "volumegroup": string
    }
}
```