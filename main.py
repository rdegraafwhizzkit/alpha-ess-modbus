from pymodbus.client.tcp import ModbusTcpClient
import yaml


def get_register_values(registers: dict, config: str = 'configuration.yaml') -> list:
    client_config = yaml.safe_load(open(config))
    device_id = client_config['device_id']

    modbus_tcp_client = ModbusTcpClient(
        host=client_config['host'],
        port=client_config['port']
    )

    modbus_tcp_client.connect()

    register_values = [{f'{address:x}': modbus_tcp_client.read_holding_registers(
        address,
        count=count,
        device_id=device_id
    ).registers} for address, count in registers.items()]

    # Restart EMS (not tested!)
    # modbus_tcp_client._write_register_(
    #     address=0x1100,  # Reset Mode
    #     value=8,
    #     device_id=device_id,
    #     no_response_expected=True
    # )

    modbus_tcp_client.close()

    return register_values

# According to the docs, I could send an "8" to register 1100H to "restart EMS"
if '__main__' == __name__:
    print(get_register_values({
        0x102: 1,  # Battery SOC, 0.1
        0x01b: 2,  # Active power of A phase(Grid)
        0x01d: 2,  # Active power of B phase(Grid)
        0x01f: 2,  # Active power of C phase(Grid)
        0x111A: 1,  # EMS BOOT Version High
        0x111B: 1,  # EMS BOOT Version Middle
        0x111C: 1,  # EMS BOOT Version Low
        0x11B8: 1,  # Grid Freq
    }))
