import flask
import copy
from flask import request, jsonify
from player import Player

app = flask.Flask(__name__)
app.config["DEBUG"] = True

listOfPlayers = {}

@app.route('/', methods=['GET'])
def home():
    responseString = "<h1>Gator Hold 'Em</h1><h2>List of players</h2>"
    for x, y in listOfPlayers.items():
        responseString = responseString + "<h3>" + str(y) + "</h3>"
    return responseString

@app.route('/api/players/all', methods=['GET'])
def get_players():
    tempList = copy.deepcopy(listOfPlayers)
    for x, y in tempList.items():
        tempList[x] = y.__dict__
    return jsonify(tempList)

@app.route('/api/player', methods=['GET'])
def get_player():
    if 'name' in request.args:
        name = str(request.args['name'])
        for x, y in listOfPlayers.items():
            if y.name == name:
                return jsonify(y.__dict__)
        return "Player with name " + name + " not in game"
    elif 'id' in request.args:
        client_number = str(request.args['id'])
        for x, y in listOfPlayers.items():
            if y.client_number is client_number:
                return jsonify(y.__dict__)
        return "Player with client number " + client_number + " not in game"
    else:
        return "Error: you need params fam"

@app.route('/api/players', methods=['POST'])
def add_player():
    if 'name' in request.args:
        name = str(request.args['name'])
    else:
        name = "Gator"
    client_number = len(listOfPlayers)
    newPlayer = Player(client_number, name, False)
    listOfPlayers[str(client_number)] = newPlayer
    return name

app.run()