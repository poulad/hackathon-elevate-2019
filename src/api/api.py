import flask
import requests
import transactions as t
from flask import jsonify, request
import logic

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#  GET requests (to send data from the application to the user) and POST requests (to receive data from a user).

def _url(path):
    return 'https://uniwards.com' + path

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/businessportal', methods=['GET','POST'])
def submit_promo():
    if request.method == 'GET':
        # send back all promotions
        data = logic.get_promotions()
        return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data=data), 200

    if request.method == 'POST':
        data = request.form # should be a json object?
        # format and pushes json promo to db
        l.create_promo(data)

@app.route('/uniwards', methods=['GET'])
def uniwards():
    if request.method == 'GET':
        # return all promos that you qualify for
        l.check_transactions()



app.run()