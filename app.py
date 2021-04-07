from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/demo')
def hello_world():
    return 'Hello World!'


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({1: 'a', 2: 'b', 3: 'c'})     #（jsonify返回一个json格式的数据）


if __name__ == '__main__':
    app.run()