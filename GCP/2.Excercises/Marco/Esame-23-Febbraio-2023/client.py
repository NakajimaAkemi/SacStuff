import argparse
from google.cloud import pubsub_v1
from uuid import uuid1

def callback(message):
    print(message.data)
    msg = message.data.decode('utf-8')
    message.ack()
    print(msg)
    

parser = argparse.ArgumentParser()
parser.add_argument('topic', type=str)
args = parser.parse_args()
topic=args.topic
print(topic)

topic = topic.replace('#', '')
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id='uaas070120252',
    topic=topic,  
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id='uaas070120252',
    sub=f'sac-sub-{uuid1()}',
)

with pubsub_v1.SubscriberClient() as subscriber:
    subscriber.create_subscription(
        name=subscription_name,
        topic=topic_name
    )
    print(f"listening on {topic}")
    fut = subscriber.subscribe(subscription_name, callback)
    try:
        fut.result()
    except KeyboardInterrupt:
        fut.cancel()