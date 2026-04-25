import unittest
from hashlib import sha256

from block import Block
from transaction import Transaction


class TestBlock(unittest.TestCase):
    def testCalculateMerkleRoot(self):
        # Mock data: create some transactions
        tx1 = Transaction("Alice", "Bob", "Transfer 10 coins")
        tx2 = Transaction("Charlie", "Dave", "Transfer 5 coins")
        transactions = [tx1, tx2]
        
        # Calculate expected Merkle root manually
        h1 = sha256(tx1.to_string().encode()).digest()
        h2 = sha256(tx2.to_string().encode()).digest()
        combined = h1 + h2
        expected_merkle_root = sha256(combined).digest()
        
        # Call the method
        actual_merkle_root = Block.calculateMerkleRoot(transactions)
        
        # Assert
        self.assertEqual(actual_merkle_root, expected_merkle_root)

    def testCalculateMerkleRootSingleTransaction(self):
        tx = Transaction("Alice", "Bob", "Transfer 10 coins")
        transactions = [tx]
        
        expected = sha256(tx.to_string().encode()).digest()
        actual = Block.calculateMerkleRoot(transactions)
        self.assertEqual(actual, expected)

    def testCalculateMerkleRootEmptyList(self):
        transactions = []
        
        expected = sha256(b"").digest()
        actual = Block.calculateMerkleRoot(transactions)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()