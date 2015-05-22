# netsidecar
Ansible modules using SCP and SSH to transfer files to Cisco IOS devices.

General pattern is to create a Paramiko SSH control channel and then create a
separate SCP channel to transfer a file to the remote network device.

'ip scp server enable' must be configured on the Cisco IOS device.  

Requires:  
paramiko>=1.13.0  
scp>=0.10.0  
netmiko>=0.2.0  

<h4>This is totally experimental at this point</h4>



<br>
---   
Kirk Byers  
Python for Network Engineers  
https://pynet.twb-tech.com  
