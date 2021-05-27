import binascii
import json

import Crypto.Random
from Crypto.PublicKey import RSA
from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS

from blockchain import Blockchain
from utils import get_utc_timestamp
from message import Message, MessageList
from user import User
from userlist import UserList
from data import DataFolder

# Initialize flask application
app = Flask(__name__)

# Instantiate the Node
CORS(app)

# Instantiate the Blockchain
blockchain = Blockchain()
users = UserList()


@app.route('/')
def index():
    blockchain.register_node(request.url)
    return render_template('./index.html')


@app.route('/nodes', methods=['GET'])
def nodes_index():
    return render_template('./register_node.html')


@app.route('/nodes/get', methods=['GET'])
def get_nodes():
    nodes = blockchain.nodes
    response = {'nodes': list(nodes), 'length': len(nodes)}
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.form
    nodes = values['nodes'].replace(" ", "").split(',')

    if nodes is None:
        return "Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': [node for node in blockchain.nodes],
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.consensus()

    if replaced:
        response = 'Our chain was replaced'
    else:
        response = 'Our chain is authoritative'
    return response, 200


@app.route('/wallet')
def wallet():
    return render_template('./wallet.html', title="Wallet Generator")


@app.route('/wallet/new', methods=['GET', 'POST'])
def new_wallet():
    values = request.form

    # Check that the required fields are in the POST'ed data
    required = ['name', 'username', 'email_id']
    if not all(values[k] != "" for k in required):
        return 'Missing values', 400

    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()

    user = User(values["name"], values["username"], values["email_id"],
                binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    if users.add_user(user) != "Success":
        return 'Username already exists', 400

    response = {
        'username': values["username"],
        'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
        'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
    }
    # return render_template('index.html', response=response)
    return jsonify(response), 200


@app.route('/message/receive', methods=['POST'])
def receive_message():
    try:
        values = request.form
        required = ['sender', 'message', 'timestamp']
        if not all(values[k] != "" for k in required):
            return 'Missing values', 400

    except Exception:
        return "Error in format", 400


@app.route('/message/send', methods=['GET', 'POST'])
def send_message():
    try:
        if request.method == 'GET':
            return render_template('./sendmessage.html', title="Send Message")
        elif request.method == 'POST':
            values = request.form

            # Check that the required fields are in the POST'ed data
            required = ['sender', 'private_key', 'message']
            if not all(values[k] != "" for k in required):
                return 'Missing values', 400

            sender = values['sender']
            sender_private_key = values['private_key']

            user = users.get_user(sender)
            if user == "Username does not exist":
                return user, 400
            sender_public_key = user['public_key']

            msg = Message(user["username"], user['name'], values["message"], get_utc_timestamp())

            # Create a new Transaction
            signature = blockchain.sign_transaction(sender_private_key, msg.__str__())
            if len(signature) == 2:
                return signature[0], 400
            transaction_result = blockchain.submit_transaction(sender, sender_public_key, msg.__str__(), signature)

            if not transaction_result:
                return 'Invalid Transaction!', 406
            else:
                response = {
                    'message': 'Transaction will be added to Block ' + str(transaction_result),
                    'signature': signature
                }
                return jsonify(response), 200
    except Exception as e:
        return "Error in format", 400


@app.route('/mine', methods=['GET'])
def mine():
    try:
        new_block_index = blockchain.mine()
        if new_block_index == 0:
            return "No unconfirmed transactions", 400

        new_block = json.loads(blockchain.chain[new_block_index])

        response = {
            'message': "New Block Mined",
            'block_number': new_block['index'],
            'transactions': new_block['transactions'],
            'nonce': new_block['nonce'],
            'timestamp': new_block['timestamp'],
            'previous_hash': new_block['previous_hash'],
        }
        return jsonify(response), 200
    except Exception as e:
        return str(e), 400


@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = []
    for block in blockchain.chain:
        block = json.loads(block)
        transactions += block["transactions"]
    response = {
        'transactions': transactions,
        'length': len(transactions),
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.before_request
def before_request():
    # When you import jinja2 macros, they get cached which is annoying for local
    # development, so wipe the cache every request.
    if 'localhost' in request.host_url or '0.0.0.0' in request.host_url or '127.0.0.1' in request.host_url:
        app.jinja_env.cache = {}


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='Node port')
    args = parser.parse_args()
    port = args.port

    # create sub folder with port name
    data_folder = DataFolder('data')
    data_folder.sub_folder(str(port))

    # add node into blockchain
    blockchain.register_node(f"http://127.0.0.1/{port}")

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='127.0.0.1', port=port)
