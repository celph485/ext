from datetime import datetime
from datetime import timedelta
from config_file import config, mapping_config
from log_config import LogConfig
import json
import stomp
import time
import requests


log = LogConfig(__name__).get_logger()


log.info('Starting application {}'.format(config['APP_NAME']))
log.debug('Listing all the config variables.')
for key in config:
    log.debug('{} = {}'.format(key, config[key]))


HOST_AND_PORTS = [(config['MQ_HOST'], config['MQ_PORT'])]
MQ_USER = config['MQ_USER']
MQ_PASS = config['MQ_PASS']
MQ_DEST = config['MQ_DESTINATION']
WS_URL = config['TARGET_WS_URL']
GMT_IMEI_LIST = config['GMT_IMEI'].split(',')
DATE_TIME_FORMAT = config['DEF_DATETIME_FORMAT']


def send_data_to_ws(message):
    log.info('Sending data to API. ')
    log.info(message)
    resp = requests.post(WS_URL, data=message)
    log.info('response from API: {}'.format(resp.text))


class SampleListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, header, body):
        log.error('received an error body: %s' % body)

    def on_message(self, header, message):
        log.info('received a data message: \n %s' % message)
        msg_dict = eval(message)
        imei = msg_dict['imei_no']
        if imei in mapping_config.values():
            time_str = msg_dict['time']
            log.debug('time: %s'% time_str)
            time_int = int(time_str)
            if len(time_str) == 13:
                log.debug('time is in millisecond, converting it to second') 
                time_int /= 1000
                log.debug('Time in seconds: %d' % time_int)

            if imei in GMT_IMEI_LIST:
                log.info('Updating timezone for the message, adding +0530 Hrs')
                time_int +=  19800
                log.debug('Time in seconds: %d' % time_int)

            date_time_str = time.strftime(DATE_TIME_FORMAT, time.localtime(time_int))
            msg_dict['time'] = date_time_str
            updated_message = json.dumps(msg_dict)
            send_data_to_ws(updated_message)
        else:
            log.warn('IMEI not whitelisted for sending data')

    def on_disconnected(self):
        log.warning('MQ disconnected')

    def on_heartbeat_timeout(self):
        log.warning('Heartbeat time out')

    def on_receiver_loop_completed(self, headers, body):
        log.warning('receiver loop completed')


conn = stomp.Connection(host_and_ports=HOST_AND_PORTS,
                        heartbeats=(4000, 4000))
conn.set_listener('SampleListener', SampleListener(conn))
conn.connect(MQ_USER, MQ_PASS, wait=True)
conn.subscribe(destination=MQ_DEST, id=1, ack='auto')
time.sleep(15)
conn.disconnect()