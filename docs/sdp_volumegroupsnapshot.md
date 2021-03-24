# sdp_volumegroupsnapshot

This module allows you to create and manage sdp_volumegroupsnapshot objects on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `name` - (`string`) - The desired name for the host object.
* `volumegroup` - (`string`) - The desired name for the host object.
* `retentionpolicy` - (`string`) - The desired name for the host object.

### Optional
* `exposable` - (`bool`) - Sets the exposable flag for the snapshot. 
* `deletable` - (`bool`) - Sets the deletable flag for the snapshot. 
* `remove` - (`bool`) - Remove the object. 

## Examples
### 1. 
This example creates a snapshot object of the `VolumeGroup01` volume group, named `ATSnap01` against the `Backup` retention policy. 
```yaml
sdp_volumegroupsnapshot: 
    name: "ATSnap01"
    volumegroup: "ATVG01"
    retentionpolicy: "Backup"
```

## Register response:
```json
{
    "changed": bool,
    "failed": bool,
    "meta": {
        "deletable": bool,
        "exposable": bool,
        "id": int,
        "name": string,
        "retentionpolicy": string
    }
}
```

