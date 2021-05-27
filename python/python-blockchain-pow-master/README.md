# PyBlock
Proof of Work based Python implementation of Blockchain with public-key cryptography-based user verification, message signature and one-way hashing of blocks using SHA256


## Dependencies

- `Python 3.6`
- `Pipenv` virtual environment tool

## Instructions to run

### Initial One-time Setup
Clone the Repo

```sh
git clone https://github.com/geetesh-gupta/python-blockchain-pow
```

Install the dependencies

```sh
cd python-blockchain-pow
pipenv install
```

### Start a blockchain node

```sh
# Activate the virtual environment
pipenv shell

# Run a node  
python3 src/node.py --port {port}
```

*Each node is differentiated based on it's IP address & port. If we run `python3 app.py -p 5000`, then IP address would be `127.0.0.1` and the port will be `5000`. Make sure to use port greater than 1024.*

## Features

### Create an account wallet of public-private key pair using RSA-algorithm
  - Click on `Wallet` / `Generate Wallet` button
  - Fill the details 
    - `name` : string
    - `username` : unique
    - `email_id` : email
  - Click on `Generate Wallet`

*A public-private key pair will be generated. Save the private key somewhere safely. You will need it when sending RSA signed messages.*

### Send a message transsaction signed with private key pair using RSA-algorithm
  - Click on `Send` / `Send Message` button
  - Fill the details
    - `username` : your unique username
    - `private_key` : your private key generated in the wallet
    - `message` : string
  - Click on `Send Message`

*A message confirmation will popup with `RSA signature` for the message based on the signed message using private_key and verification with the public_key of the user. Note that the messages will `not be visible until they are mined`. Remember to mine whenever you have made some message transactions*

### Mine available message transactions
  - Click on `Mine` button

*If some message transactions are available, then they will be mined and the messages will be available on the homepage*

### View/Register other Nodes
  - Click on `Nodes` / `Register Nodes` button
    - All the registered nodes will be shown on the page
  - To Register other nodes
    - Fill the addresses of other nodes separated with comma (`,`)
      - Example: `127.0.0.1:5001, 127.0.0.1:5002`
    - Click on `Register Nodes`

*Remember to `sync` after the registering the nodes to update the chain*


### Sync other nodes with the current node
  - Click on `Sync` button

*If other nodes are there in the network and are registered with the current node, then based on the `consensus`, the longest-chain among the nodes will be chosen the major chain and current chain will get replaced with the `longest-chain`*


### View Messages
  - Click on `Pyblock` logo to go to the homepage

*Messages can be viewed on the homepage. Remember to refresh whenever mined or synced or if new message transactions are not visible*