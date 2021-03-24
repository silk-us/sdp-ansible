# sdp_snapshotview

This module allows you to create and manage snapshot view objects on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `name` - (`string`) - The desired name for the resulting view object.
* `volumegroup` - (`string`) - The source volume group for the snapshot. 
* `snapshot` - (`string`) - The name of the snapshot that the view is being created for. 
* `retentionpolicy` - (`string`) - The retention policy for the view to be created against. 

### Optional
* `remove` - (`bool`) - Remove the object. 

## Examples
### 1. 
This example creates a view of the snapshot `ATSnap01` for the volume group `ATVG01`. 
```yaml
sdp_snapshotview: 
    name: "ATSnap01-view"
    volumegroup: "ATVG01"
    snapshot: "ATSnap01"
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