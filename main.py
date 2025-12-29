from pymodbus.client.tcp import ModbusTcpClient
import yaml


def get_modbus_client(config: str = 'configuration.yaml'):
    client_config = yaml.safe_load(open(config))
    return ModbusTcpClient(
        host=client_config['host'],
        port=client_config['port']
    )


def write_register_values(registers: dict, config: str = 'configuration.yaml'):
    modbus_tcp_client = get_modbus_client(config)
    raise NotImplementedError()


def get_register_values(registers: dict, config: str = 'configuration.yaml') -> list:
    modbus_tcp_client = get_modbus_client(config)

    modbus_tcp_client.connect()

    register_values = [{f'{address}': modbus_tcp_client.read_holding_registers(
        address,
        count=count,
        # device_id=device_id
    ).registers} for address, count in registers.items()]

    modbus_tcp_client.close()

    return register_values


if '__main__' == __name__:
    print({i:1 for i in range(256)})
