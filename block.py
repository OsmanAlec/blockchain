
from hashlib import sha256
import time
from typing import List

from transaction import Transaction


class Block(object):
    def __init__(self,
                transactions: List[Transaction],
                transaction_to_add: Transaction,
                previousHash,
                version = 1.0,
                difficulty = 4,
                nonce = 0
                ):
        # Data
        self.transactions = transactions + [transaction_to_add]
        # Header
        self.timestamp = time.time()
        self.version = version
        self.merkleRoot = Block.calculateMerkleRoot(self.transactions)
        self.difficulty = difficulty
        self.nonce = nonce
        self.previousHash = previousHash
        self.blockHash = self.calculateBlockHash()

    @staticmethod
    def calculateMerkleRoot(transactions: List[Transaction]) -> bytes:
        if not transactions:
            return sha256(b"").digest()
        if len(transactions) == 1:
            return sha256(transactions[0].to_string().encode()).digest()
        
        # Get hashes of all transactions
        hashes = [sha256(tx.to_string().encode()).digest() for tx in transactions]
        
        # Build the merkle tree
        while len(hashes) > 1:
            # If odd duplicate last hash
            if len(hashes) % 2 == 1:
                hashes.append(hashes[-1])
            newHashes = []
            for i in range(0, len(hashes), 2):
                newHash = sha256(hashes[i] + hashes[i+1]).digest()
                newHashes.append(newHash)
            hashes = newHashes
        
        return hashes[0]
    
    def calculateBlockHash(self):
        return sha256(
            str(self.timestamp).encode() +
            str(self.version).encode() +
            self.merkleRoot +
            str(self.difficulty).encode() +
            str(self.nonce).encode() +
            self.previousHash.encode()
        ).hexdigest()
    
    def mine(self, difficulty: int, extra_nonce: int, timestamp: time):
        target = "0" * difficulty
        while not self.blockHash.startswith(target):
            self.nonce += 1
            # Rollover if reached the 32-bit limit
            # Like in bitcoin :)
            if (self.nonce > 4294967296):
                self.nonce = 0
            self.blockHash = self.calculateBlockHash()
            # TODO: add extra nonce
            # TODO: allow miners to change the timestamp.
            # TODO: handle if mining succeeds :D
