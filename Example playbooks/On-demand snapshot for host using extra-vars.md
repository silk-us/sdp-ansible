## On-demand snapshot to host
Using 2 vars (`host` and `volumegroup`) this playbook will invoke a new snapshot, view, and host mapping for the specified host and volume group.

### Example 
```
ansible-playbook on-demand-snapshot.yaml --extra-vars "host=ATH02 volumegroup=ATVG01"
```

Using this playbook:  
File: `on-demand-snapshot.yaml`
```yaml
- hosts: localhost
  vars: 
    snapshotname: "{{ volumegroup }}-snap01"
  tasks:
    - name: "Create Volume Group Snapshot"
      sdp_volumegroupsnapshot: 
        name: "{{ snapshotname }}"
        volumegroup: "{{ volumegroup }}"
        retentionpolicy: "Backup"
      register: snapshot

    - name: "Create Volume Group Snapshot View"
      sdp_snapshotview: 
        name: "{{ snapshotname }}-view"
        snapshot: "{{ snapshot.meta.name }}"
        retentionpolicy: "Backup"
      register: view

    - name: "Create Host snapshot view mapping"
      sdp_hostviewmapping:
        hostname: "{{ host }}"
        snapshotview: "{{ view.meta.name }}"
```