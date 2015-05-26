#!/usr/bin/python
'''
Ansible module to transfer files to Cisco IOS devices.
'''

from ansible.module_utils.basic import *
from netmiko import ConnectHandler, FileTransfer

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
            enable_scp=dict(required=False, default=False, choices=BOOLEANS),
            overwrite=dict(required=False, default=True, choices=BOOLEANS),
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
    enable_scp = module.boolean(module.params['enable_scp'])
    overwrite = module.boolean(module.params['overwrite'])
    check_mode = module.check_mode
    scp_changed = False

    with FileTransfer(ssh_conn, source_file, dest_file) as scp_transfer:

        # Check if file already exists and has correct MD5
        if scp_transfer.check_file_exists() and scp_transfer.compare_md5():
            module.exit_json(msg="File exists and has correct MD5", changed=False)

        if not overwrite and scp_transfer.check_file_exists():
            module.fail_json(msg="File already exists and overwrite set to false")

        if check_mode:
            if not scp_transfer.verify_space_available():
                module.fail_json(msg="Insufficient space available on remote device")

            module.exit_json(msg="Check mode: file would be changed on the remote device",
                             changed=True)

        # Verify space available on remote file system
        if not scp_transfer.verify_space_available():
            module.fail_json(msg="Insufficient space available on remote device")

        # Transfer file
        if enable_scp:
            scp_transfer.enable_scp()
            scp_changed = True

        scp_transfer.transfer_file()
        if scp_transfer.verify_file():
            if scp_changed:
                scp_transfer.disable_scp()
            module.exit_json(msg="File successfully transferred to remote device",
                             changed=True)

        module.fail_json(msg="File transfer to remote device failed")


if __name__ == "__main__":
    main()
