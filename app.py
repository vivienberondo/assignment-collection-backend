import json

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

from scheduling.views import evaluate


app = Flask(__name__)
cors = CORS(app, resources={r'/cpu-scheduling': {'origins': '*'}})


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/cpu-scheduling', methods=['POST', 'GET'])
def schedule_processes():
    data = {
        'algo': request.values.get('algo'),
        'processes': json.loads(request.values.get('processes')),
        'quantum': int(request.values.get('quantum'))
    }
    print(f'data{data}')
    gantt = evaluate(data)
    # return jsonify(gantt)
    return gantt


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
