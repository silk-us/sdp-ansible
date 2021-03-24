## On-demand snapshot to host
This example will create:
* A `Host Group` named `ATHG01`
* A `Host` named `ATH01`
* A `Volume Group` named `ATVG01`
* 2 `Volumes` named `ATV01` and `ATV02`
* A `Mapping` of both volumes (`ATV01` and `ATV02`) to the host (`ATH01`)

### Example 
```
ansible-playbook new-host-and-volumes.yaml 
```

Using this playbook:  
File: `new-host-and-volumes.yaml `
```yaml
- hosts: localhost
  tasks:
    - name: "Create Host Group"
      sdp_hostgroup:
        name: "ATHG01"
        description: "host group"
        allowDifferentHostTypes: True

    - name: "Create Host"
      sdp_host: 
        name: "ATH01"
        type: "Linux"
        hostgroup: "ATHG01"
        pwwn: 
          - "00:33:44:33:44:55:66:66"
          - "00:33:44:33:44:55:66:77"

    - name: "Create Volume Group"
      sdp_volumegroup: 
        name: "ATVG01"
        quotaInGB: 2000
        dedupe: True

    - name: "Create Volume"
      sdp_volume: 
        name: "ATV01"
        sizeInGB: 80
        volumegroup: "ATVG01"

    - name: "Create Volume 2"
      sdp_volume: 
        name: "ATV02"
        sizeInGB: 50
        volumegroup: "ATVG01"

    - name: "Create Host Group mapping"
      sdp_hostgroupmapping:
        hostgroupname: "ATHG01"
        volumename: "ATV01"

    - name: "Create Host Group mapping"
      sdp_hostgroupmapping:
        hostgroupname: "ATHG01"
        volumename: "ATV02"
```