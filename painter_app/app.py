from flask import Flask, Response
from .library import painter_engine as engine

app = Flask(__name__)


@app.route('/paint')
def paint():
    engine.paint('https://i.imgur.com/oZ67OF4.jpg')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
