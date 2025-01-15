from google.cloud import pubsub_v1
import json

project_id = 'uaas070120252'
publisher = pubsub_v1.PublisherClient()

def check_topic_exists(topic_path):    
    try:
        publisher.get_topic(request={"topic": topic_path})
        print("Topic exists.")
        return True
    except:
        print("Topic does not exist.")
        return False


def send_message(topic, message):
    my_topic = topic.replace("#","")
    topic_path = publisher.topic_path(project_id, my_topic)
    if not check_topic_exists(topic_path):
        publisher.create_topic(request={"name": topic_path})
        print(f"Created topic: {my_topic}")
    publisher.publish(topic_path, json.dumps(message).encode('utf-8'))