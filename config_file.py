import config_builder as cb


config = cb.create_config()
mapping_config = cb.get_mapping_dict()

req = {
    'imei_no': '',
    'lattitude': '',
    'longitude': '',
    'lattitude_direction': 'N',
    'longitude_direction': 'E',
    'speed': '0',
    'digital_port1': '0',
    'digital_port2': '0',
    'digital_port3': '0',
    'digital_port4': '0',
    'analog_port1': '0',
    'analog_port2': '0',
    'angle': '0',
    'satellite': '0',
    'time': '',
    'battery_voltage': '20',
    'gps_validity': 'A'
}
