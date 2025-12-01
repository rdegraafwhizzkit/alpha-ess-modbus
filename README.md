# alpha-ess-modbus
```
deactivate || :
rm -rf .venv/
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt 
```

Be careful, the below is not tested. According to the docs, you could send an "8" to register 1100H to "Restart EMS"
```python
# Restart EMS
modbus_tcp_client.write_register(
    address=0x1100,  # Reset Mode
    value=8,
    device_id=device_id,
    no_response_expected=True
)

```