#!/usr/bin/python3
import time
from datetime import datetime
import json
import os
from google.cloud import pubsub_v1

#temp_threshold=50
temp_threshold=60

UPDATE_ALERT=True

update_interval=5.0
topic_name=os.environ['TOPIC'] if 'TOPIC' in os.environ.keys() else 'cpu_temperature'
topic_name2=os.environ['TOPIC2'] if 'TOPIC2' in os.environ.keys() else 'cpu_temperature_alert'
project_id=os.environ['PROJECT_ID'] if 'PROJECT_ID' in os.environ.keys()  else 'myprj'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
topic_path2 = publisher.topic_path(project_id, topic_name2)
print(topic_path)

# create CPU spike with stress --cpu $(nproc) --timeout 20
def get_cpu_temp():
    # look at /sys/class/thermal/thermal_zone*/type to understand where CPU is
    with open("/sys/class/thermal/thermal_zone10/temp") as f:
        return float(f.read())/ 1000 

def notify_cpu_temp(temp):
    now = datetime.now()
    data={'timestamp': now.timestamp(), 'time': str(now), 'temperature': temp}
    res = publisher.publish(topic_path, json.dumps(data).encode('utf-8'))
    print(data, res.result())
    if UPDATE_ALERT and temp>=temp_threshold:
        # write same data packet
        publisher.publish(topic_path2, json.dumps(data).encode('utf-8'))
        print(topic_path2)

if __name__=='__main__':
    old_temp=0.0
    while True:
        notify_cpu_temp(get_cpu_temp())
        time.sleep(update_interval)
