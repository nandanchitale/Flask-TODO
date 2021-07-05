from flask import Flask, render_template, request, jsonify
from pusher import Pusher
import json

# Create flask app
app = Flask(__name__)

# Configure Pusher project
pusher_client = Pusher(
    app_id='1230537',
    key='07a3bba45c3289588396',
    secret='f881400406f1f585a487',
    cluster='ap2',
    ssl=True
)

# Index route, shows index.html view
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint for storing todo item
@app.route('/add-todo', methods = ['POST'])
def addToDo():
    data = json.loads(request.data) # Loads json data from request
    pusher_client.trigger('todo','item-added', data)

    return jsonify(data)

# Endpoint for deleting todo item
@app.route('/remove-todo/<item_id>')
def removeToDo(item_id):
    data = {
        'id':item_id
    }
    pusher_client.trigger('todo','item-removed', data)


# Endpoint for updating todo item
@app.route('/update-todo/<item_id>', methods = ['POST'])
def updateToDo(item_id):
    data = {
        'id':item_id,
        'completed':json.loads(request.data).get('completed',0)
    }
    pusher_client.trigger('todo','item-removed', data)
    return jsonify(data)

# Run app in debug mode
app.run(debug=True)

