# create one
```bash
ansible-vault create secrets.yaml
```
and add the following content to it:
```yaml
# secrets.yaml
# Add your sensitive variables here, for example:
MQTT_USERNAME: your_mqtt_username
MQTT_PASSWORD: your_mqtt_password

# When running the playbook, make sure to include the --ask-vault-pass flag to decrypt the secrets file during execution.
```
