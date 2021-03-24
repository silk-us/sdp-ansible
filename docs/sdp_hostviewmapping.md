# sdp_hostviewmapping

This module allows you to create and manage host view mapping objects on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `hostname` - (`string`) - The desired name for the host object.
* `snapshotname` - (`string`) - The desired name for the snapshot view object. This should include the entire name string in the form of volumegroup:snapshotview. 

### Optional
* `remove` - (`bool`) - Remove the object. 

## Examples
### 1. 
This example creates a mapping action for the host `ATH01` to the snapshot view named `ATSnap01-view` in the volumegroup `ATVG01`.
```yaml
sdp_hostmappingview:
    hostname: "ATH01"
    snapshotview: "ATVG01:ATSnap01-view"

```

## Register response:
```json
{
    "changed": bool,
    "failed": bool,
    "meta": {
        "id": int,
        "hostname": string,
        "volume": string
    }
}
```