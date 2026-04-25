from hashlib import sha256
from typing import List

from block import Block
from transaction import Transaction

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.createGenesisBlock()]
        self.mempool: List[Transaction] = []
        self.difficulty = 4

    def createGenesisBlock(self) -> Block:
        genesis_transaction = Transaction("Ace", "Osman", "The creation of my blockchain")
        block = Block([], genesis_transaction, None)
        self.chain.append(block)

    def getLatestBlock(self) -> Block:
        return self.chain[len(self.chain)-1]

    def addBlock(self, transaction: Transaction):
        latest_block = self.getLatestBlock()
        new_block = Block(
            latest_block.transactions,
            transaction,
            latest_block.blockHash,
            difficulty=self.difficulty)

    def isChainValid(self) -> bool:
        pass