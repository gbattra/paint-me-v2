from google.cloud import pubsub_v1
from flask import Flask, Response

app = Flask(__name__)

app.config.from_envvar('APP_SETTINGS')


@app.route('/paint')
def paint():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = 'projects/%s/subscription/%s' % \
        (app.config['PUBSUB_PROJECT_ID'], app.config['NEW_PAINTER_REQUEST_SUBSCRIPTION'])

    def callback(message):
        print("Received message: {}".format(message))
        # message.ack()

    streampull = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streampull.result(timeout=10)
    except:
        streampull.cancel()
    # engine.paint('https://i.imgur.com/oZ67OF4.jpg')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
