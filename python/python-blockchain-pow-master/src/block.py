from Crypto.Hash import SHA256
import json


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        """
        Constructor for the `Block` class.
        :param index:         Unique ID of the block.
        :param transactions:  List of transactions.
        :param timestamp:     Time of generation of the block.
        :param previous_hash: Hash of the previous block in the chain which this block is part of.
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    @staticmethod
    def compute_hash(_block):
        """
        Returns the hash of the block instance by first converting it
        into JSON string.
        """
        if isinstance(_block, Block):
            _block = _block.__str__()
        elif isinstance(_block, dict):
            _block = json.dumps(_block)
        return SHA256.new(_block.encode()).hexdigest()

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True)


if __name__ == "__main__":
    block = Block(1, [], 2, 3)
    print(block)
    print(Block.compute_hash(block))
