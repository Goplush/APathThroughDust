from flask import Flask, jsonify
from TimestampGenerator import TimestampGenerator


app = Flask(__name__)

timestamp_generator = TimestampGenerator()

@app.route('/get_timestamp')
def get_timestamp():
    timestamp = timestamp_generator.get_timestamp()
    response = {'timestamp': timestamp}
    return jsonify(response)

if __name__ == '__main__':
    app.run(threaded=True, port=50003)