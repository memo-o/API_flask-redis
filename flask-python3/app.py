from flask import Flask, render_template, jsonify, request, json, stream_with_context
from redis import Redis, RedisError
import logging, pickle, json, time
app = Flask(__name__)


@app.route('/')
def main():
#    return render_template('index.html')
    redisKey = request.args.get('rediskey')
    return jsonify({"Output":redisKey})

    return jsonify({"about": "Hello World! from my pc"})


@app.route('/basic', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
        some_json = request.get_json()
        #return '''<h1>The language value is: {} </h1>'''.format(jsonify({'you sent':some_json}), 201)
        return jsonify({'you sent in POST':some_json}), 201
    else:
        return jsonify({"about":"GET Methood"})

@app.route('/multi/<int:num>', methods=['GET'])
def get_multiply10(num):
    return jsonify({'result from GET':num*10})

@app.route('/redisAPI', methods=['GET', 'POST'])
def API():
    r = Redis(host='redisserver', port='6379', db=0, decode_responses=True)
#    r = Redis(host='127.0.0.1', port='6379', db=0, decode_responses=True) //Local redis server

    if (request.method == 'POST'):
        input_json = json.dumps(request.json)
        prop_json = json.loads(input_json)
        for i in prop_json:
            logging.debug("Checking json key: " + i + " value:" + prop_json[i])
            r.set(i, prop_json[i])
        return input_json  
    else:
        redisKey = request.args.get('rediskey')
        if(redisKey):
            return jsonify({"Output":r.get(redisKey)})
        else:
            return jsonify({"Output":"No query rediskey requested"})
    

@app.route('/food')
def food():
    leaves = [
        {
            'name': 'lettuce',
            'size': 'big'
        },
        {
            'name': 'parsley',
            'size': 'small'
        }
    ]
    list_of_fruits = ['banana', 'orange', 'apple', 'strawberry']
    list_of_vegetables = ['poteto', 'tomato', 'carrot', leaves]
    return jsonify(Fruits=list_of_fruits, Vegetables=list_of_vegetables)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')