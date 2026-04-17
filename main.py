from pymodbus.client.tcp import ModbusTcpClient
import yaml


def get_modbus_client(config: str = 'configuration.yaml'):
    client_config = yaml.safe_load(open(config))
    return ModbusTcpClient(
        host=client_config['host'],
        port=client_config['port']
    ), client_config


def write_register_values(registers: dict, config: str = 'configuration.yaml'):
    modbus_tcp_client = get_modbus_client(config)
    raise NotImplementedError()


def get_register_values(registers: dict, config: str = 'configuration.yaml', register_type='holding') -> list:
    modbus_tcp_client, client_config = get_modbus_client(config)
    modbus_tcp_client.connect()

    register_function = {
        'holding': modbus_tcp_client.read_holding_registers,
        'input': modbus_tcp_client.read_input_registers,
        'coils': modbus_tcp_client.read_coils,
        'discrete': modbus_tcp_client.read_discrete_inputs
    }.get(
        register_type,
        modbus_tcp_client.read_holding_registers
    )

    register_values = [{f'{address}': register_function(
        address,
        count=count,
        device_id=client_config.get('device_id', 1)
    ).registers} for address, count in registers.items()]

    modbus_tcp_client.close()

    return register_values


if '__main__' == __name__:
    # print({i:1 for i in range(256)})
    # print(get_register_values({159: 2}))  # Requested compressor speed
    # print(get_register_values({475: 2}))  # Real compressor speed

    # v=get_register_values({295: 1}, register_type='input')[0].get('295')[0]  # Compressor voltage
    # i=get_register_values({476: 1})[0].get('476')[0]/10  # Compressor current
    # print(i)
    # print(v*i/1000)
    print(get_register_values({433: 1}, register_type='coils'))

    # print(get_register_values({298: 1}, register_type='holding'))  # Drive status: 0:Stop, 1:Run, 2:Alarm
    # print(get_register_values({443: 1}, register_type='holding'))  # Compressor voltage
    # print(get_register_values({211: 1}, register_type='holding'))  # Compressor voltage
