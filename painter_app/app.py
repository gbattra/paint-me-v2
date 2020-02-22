from google.cloud import pubsub_v1
from library import painter_engine as engine

if __name__ == '__main__':
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = 'projects/sylvan-terra-269023/subscriptions/new-painter-request-pull'
    # subscriber.create_subscription(subscription_path, topic=TOPIC_NAME)

    def callback(message):
        print("Received message: {}".format(message))
        engine.paint('https://i.imgur.com/oZ67OF4.jpg')
        message.ack()

    future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        future.result()
    except (KeyboardInterrupt, SystemExit):
        future.cancel()
        raise
    except:
        future.cancel()
