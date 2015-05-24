#!/usr/bin/python
'''
Ansible module to transfer files to Cisco IOS devices.

An enable secret is not supported, the username/password provided must have sufficient access
to write a file to the remote filesystem. The lack of support of enable secret is due to
problems encountered on the SCP connection (I think due to how Cisco's SSH is implemented).
'''

from ansible.module_utils.basic import *
from netmiko import ConnectHandler, SCPConn, FileTransfer

def main():
    '''
    Ansible module to transfer files to Cisco IOS devices.
    '''

    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True),
            port=dict(default=22, required=False),
            username=dict(required=True),
            password=dict(required=True),
            source_file=dict(required=True),
            dest_file=dict(required=True),
            dest_file_system=dict(required=False),
        ),
        supports_check_mode=True
    )

    net_device = {
        'device_type': 'cisco_ios',
        'ip': module.params['host'],
        'username': module.params['username'],
        'password': module.params['password'],
        'port': int(module.params['port']),
        'verbose': False,
    }


    ssh_conn = ConnectHandler(**net_device)
    source_file = module.params['source_file']
    dest_file = module.params['dest_file']

    scp_transfer = FileTransfer(ssh_conn, source_file, dest_file)

    check_mode = module.check_mode

    # Check if file already exists and has correct MD5
    if scp_transfer.check_file_exists() and scp_transfer.compare_md5():
        scp_transfer.close_scp_chan()
        module.exit_json(msg="File exists and has correct MD5", changed=False)

    else:
        if check_mode:
            scp_transfer.close_scp_chan()
            if not scp_transfer.verify_space_available():
                module.fail_json(msg="Insufficient space available on remote device",
                output=output)

            module.exit_json(msg="Check mode: file would be changed on the remote device",
                             changed=True)
        else:
            if not scp_transfer.verify_space_available():
                scp_transfer.close_scp_chan()
                module.fail_json(msg="Insufficient space available on remote device",
                                 output=output)

            scp_transfer.transfer_file()
            if scp_transfer.verify_file():
                scp_transfer.close_scp_chan()
                module.exit_json(msg="File successfully transferred to remote device",
                                 changed=True)

    if check_mode:
        scp_transfer.close_scp_chan()
        module.fail_json(msg="Check mode: File transfer to remote device failed")
    else:
        scp_transfer.close_scp_chan()
        module.fail_json(msg="File transfer to remote device failed")


if __name__ == "__main__":
    main()
