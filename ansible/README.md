# HOW TO

## PREREQUISITES
1. Ensure you have Ansible installed on your control machine (the machine from which you will run the playbook).
2. Set up SSH access to the target Raspberry Pi servers (ra_servers) with appropriate permissions.
3. Create the `inventory.yaml` (based on the provided example) file to include the IP addresses or hostnames of your Raspberry Pi servers under the `ra_servers` group.
4. Create the `vars/monitoring-vars.yaml` (based on the provided example) and `vars/secrets.yaml` files with the necessary variables and secrets for your setup.


## CREATING SECRET FILE
1. Create a secret file to store sensitive information such as passwords:
```bash
ansible-vault create secrets.yaml
```
2. Add the necessary variables to the `secrets.yaml` file, for example:
```yaml
server_password: your_secure_password
```
3. Save and exit the file.
4. When running the playbook, make sure to include the `--ask-vault-pass` flag to decrypt the secrets file during execution.

## VIEWING SECRET FILE CONTENTS
1. To view the contents of the secrets file, use the following command:
```bash
ansible-vault view secrets.yaml
```
2. Enter the vault password when prompted to see the decrypted contents of the file. 

## RUNNING THE PLAYBOOK
1. Run the playbook to install the media server and mount the disk:

```bash
ansible-playbook -i inventory.yaml install_monitoring_with_ha_playbook.yaml --ask-become-pass --ask-vault-pass
```
2. Follow the prompts to enter the sudo password and vault password when requested.

