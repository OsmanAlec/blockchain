from hashlib import sha256
import time
from typing import List


class Transaction(object):
    def __init__(self, sender, receiver, data):
        self.sender = sender
        self.receiver = receiver
        self.data = data
    
    def to_string(self) -> str:
        return f"{self.sender}{self.receiver}{self.data}"


class Block(object):
    def __init__(self, transactions: List[Transaction], transaction_to_add: Transaction, previousHash):
        # Data
        self.transactions = transactions + [transaction_to_add]
        # Header
        self.timestamp = time.time()
        self.version = 1.0
        self.merkleRoot = Block.calculateMerkleRoot(self.transactions)
        self.difficulty = 0
        self.nonce = 0
        self.previousHash = previousHash
        self.blockHash = self.calculateBlockHash()

    # TODO: translate this to c++
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
            self.timestamp.encode() +
            self.version.encode() +
            self.merkleRoot +
            self.difficulty.encode() +
            self.nonce.encode() +
            self.previousHash.encode()
        )
        
