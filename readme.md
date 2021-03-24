# Silk Data Pod (formerly Kaminario K2) Ansible Modules
## This suite of modules is still pre-release and undergoing development. 

### Installation 
For now, clone this repo and copy the modules to `/usr/share/ansible/plugins/modules` or `~/.ansible/plugins/modules`

## Requirements
* Python 2.7 or 3.1 (tested)
* Silk krest python module
    ```
    sudo pip install krest
    ```

### Example usage: 

You will need to first export some credential vars to the shell. 

```
export SDPUSER="admin"
export SDPPASS="password"
export SDPHOST="10.10.10.200"
```

You can then invoke the deployment meta in any desired playbook. 
```yaml
- hosts: localhost

  tasks:
    - name: "Create Host"
      sdp_host: 
        name: "testhost"
        type: "Linux"

    - name: "Create Volume"
      sdp_volume: 
        name: "testvol"
        sizeInGB: 40
        volumegroup: "testvg"

```

Please see docs for specific parameters for each module. 

