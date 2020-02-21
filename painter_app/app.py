from flask import Flask, Response


app = Flask(__name__)


@app.route('/paint')
def paint():
    # engine.paint('content_image_url')
    return 'painting'


if __name__ == '__main__':
    app.run(debug=True, port=7000)
