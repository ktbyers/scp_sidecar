# netsidecar
Ansible modules for Cisco IOS Devices based upon an SCP file transfer and an SSH control channel

### This is totally experimental at this point.
  
#### Modules:
* cisco_file_transfer     [Idempotent, works reasonably well]  
* cisco_config_merge      [Not idempotent, experimental]  
* cisco_config_replace    [Not idempotent, experimental]  

#### Requires:
* paramiko>=1.13.0  
* scp>=0.10.0  
* netmiko>=0.2.0  

#### Router configuration:
'ip scp server enable' must be configured on the Cisco IOS device.  

#### Notes and caveats:
An enable secret is not supported for the SCP file transfer operation. The username/password 
provided must have sufficient access to write a file to the remote filesystem. The lack of support 
of enable secret is due to problems encountered on the SCP connection (probably due to how Cisco's 
SSH is implemented).


<br>
---   
Kirk Byers  
Python for Network Engineers  
https://pynet.twb-tech.com  
