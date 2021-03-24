# sdp_retentionpolicy

This module allows you to create and manage retention policy objects on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `name` - (`string`) - The desired name for the retention policy object.

### Optional
* `snapshots` - (`int`) - The desired number of snapshots to cycle through for this policy. 
* `weeks` - (`int`) - The desired length of time in weeks in which to keep this policy. 
* `days` - (`int`) - The desired length of time in days in which to keep this policy. 
* `hours` - (`int`) - The desired length of time in hours in which to keep this policy. 
* `remove` - (`bool`) - Remove the object. 

## Examples
### 1. 
This example creates a retention policy object named `Retention Policy 01` that retains a limit of 5 snapshots. 
```yaml
sdp_retentionpolicy: 
    name: "Retention Policy 01"
    snapshots: 5
```

### 2. 
This example creates a retention policy object named `Retention Policy 01` that retains a snapshots for 4 weeks. 
```yaml
sdp_retentionpolicy: 
    name: "Retention Policy 02"
    weeks: 4
```

## Register response:
```json
{
    "changed": bool,
    "failed": bool,
    "meta": {
        "id": int,
        "name": string,
        "snapshots": string,
        "weeks": string,
        "days": string,
        "hours": string
     }
}
```