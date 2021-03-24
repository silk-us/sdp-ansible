# sdp_hostgroupviewmapping

This module allows you to create and manage host group view mapping objects on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `hostgroupname` - (`string`) - The desired name for the host group object.
* `snapshotname` - (`string`) - The desired name for the snapshot view object. This should include the entire name string in the form of volumegroup:snapshotview. 

### Optional
* `remove` - (`bool`) - Remove the object. 

## Examples
### 1. 
This example creates a mapping action for the host `ATH01` to the snapshot view named `ATSnap01-view` in the volumegroup `ATVG01`.
```yaml
sdp_hostgroupmappingview:
    hostgroupname: "ATH01"
    snapshotview: "ATVG01:ATSnap01-view"

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