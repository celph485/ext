from datetime import datetime
from datetime import timedelta
import time
import json

GMT_IMEI_LIST = ['864180036437825', '868683021584960', '351608085310261']
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
#time_str = "1594804575"
#print('time string: ' + time_str)
#print('length of time string: ', len(time_str))
#print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time_str))))

def convert_time(message):
    print('Converting time to expected format')
    msg_dict = eval(message)
    time_str = msg_dict['time']
    print('time string: ', time_str)
    print('length of time string: ', len(time_str))
    time_int = int(time_str)
    if len(time_str) == 13:
        print('time is in millisecond, converting it to second') 
        time_int /= 1000
    print('time in seconds: ', time_int)
    date_time_str = time.strftime(DATE_TIME_FORMAT, time.localtime(time_int))
    print('date time: ', date_time_str)





data_str = '{"imei_no":"868003032451697","lattitude":"21.698205","longitude":"72.59585833333334","lattitude_direction":"N","longitude_direction":"E","speed":"0.0","digital_port1":"0","digital_port2":"0","digital_port3":"0","digital_port4":"0","analog_port1":"0","analog_port2":"0","angle":"0","satellite":"0","time":"1594804575000","battery_voltage":"0.0","gps_validity":"A"}'
convert_time(data_str)