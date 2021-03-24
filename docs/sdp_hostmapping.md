# sdp_hostmapping

This module allows you to create and manage mapping objects for hosts on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `hostname` - (`string`) - The name of the host for this mapping. 
* `volumename` - (`string`) - The name of the volume for this mapping. 

### Optional
* `remove` - (`bool`) - Remove the object. 

## Examples
### 1. 
This example creates a host mapping object that maps `Volume01` to `Host01`. 
```yaml
sdp_hostmapping:
    hostname: "Host01"
    volumename: "Volume01"
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