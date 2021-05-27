import binascii
import json
from collections import OrderedDict
from urllib.parse import urlparse

import requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from block import Block
from utils import get_utc_timestamp


class Blockchain:
    # Difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.nodes = set()
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to the chain.
        The block has index 0, previous_hash as 0, and a valid hash.
        """
        genesis_block = Block(0, [], get_utc_timestamp(), "0")
        self.proof_of_work(genesis_block)
        self.chain.append(genesis_block.__str__())

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = Block.compute_hash(self.last_block)
        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        self.chain.append(block.__str__())
        return True

    @staticmethod
    def is_valid_proof(block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == Block.compute_hash(block))

    @staticmethod
    def proof_of_work(block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = Block.compute_hash(block)
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = Block.compute_hash(block)

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = json.loads(self.last_block)

        new_block = Block(index=last_block['index'] + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=get_utc_timestamp(),
                          previous_hash=Block.compute_hash(last_block))
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index

    @classmethod
    def check_chain_validity(cls, chain):
        """
        A helper method to check if the entire blockchain is valid.
        """
        result = True
        previous_hash = "0"
        # Iterate through every block
        for block in chain:
            block = json.loads(block)
            block_hash = Block.compute_hash(block)
            if not cls.is_valid_proof(block, block_hash) or previous_hash != block['previous_hash']:
                result = False
                break

            previous_hash = block_hash

        return result

    @staticmethod
    def sign_transaction(private_key, data):
        """
        Sign transaction with private key
        """
        try:
            signer_private_key = RSA.importKey(binascii.unhexlify(private_key))
            signer = PKCS1_v1_5.new(signer_private_key)
            hashed_data = SHA256.new(data.__str__().encode())
            return binascii.hexlify(signer.sign(hashed_data)).decode()
        except Exception as e:
            return "Private key format error", e

    @staticmethod
    def verify_transaction_signature(sender_public_key, signature, data):
        """
        Check that the provided signature corresponds to transaction
        signed by the public key (sender_address)
        """
        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)
        hashed_data = SHA256.new(data.__str__().encode())
        return verifier.verify(hashed_data, binascii.unhexlify(signature))

    def submit_transaction(self, sender_username, sender_address, data, signature):
        """
        Add a transaction to transactions array if the signature verified
        """

        transaction = OrderedDict({'sender_username': sender_username,
                                   'sender_address': sender_address,
                                   'data': data,
                                   'timestamp': get_utc_timestamp()})

        transaction_verification = self.verify_transaction_signature(sender_address, signature, data)

        if transaction_verification:
            self.unconfirmed_transactions.append(transaction)
            return len(self.chain) + 1
        else:
            return False

    def consensus(self):
        """
        Resolve conflicts between blockchain's nodes
        by replacing our chain with the longest one in the network.
        """
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get('http://' + node + '/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.check_chain_validity(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def register_node(self, node_url):
        """
        Add a new node to the list of nodes
        """
        # Checking node_url has valid format
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')
