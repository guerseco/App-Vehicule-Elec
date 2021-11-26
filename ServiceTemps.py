from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
        some_json = request.get_json()
        return jsonify({'you sent': some_json}), 201
    else:
        return jsonify({"about":"helloworld"})
    
@app.route('/tempsTrajet/<int:distance>/<int:nbArrets>/<int:tempsRecharge>', methods=['GET'])
def getTempsTrajet(distance,nbArrets,tempsRecharge):
    vMoy = 60
    return jsonify({'result': (distance/vMoy)*60 + nbArrets*tempsRecharge})
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)