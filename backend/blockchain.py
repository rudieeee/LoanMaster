import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional


class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, timestamp: str, data: Dict[str, Any], 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate the SHA-256 hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        """Mine the block with proof of work"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce
        }


class Blockchain:
    """Blockchain for storing loan transactions immutably"""
    
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Dict[str, Any]] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            data={"type": "genesis", "message": "LoanMaster Blockchain Genesis Block"},
            previous_hash="0"
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Dict[str, Any]):
        """Add a transaction to pending transactions"""
        transaction["timestamp"] = datetime.now().isoformat()
        self.pending_transactions.append(transaction)
    
    def mine_pending_transactions(self) -> Optional[Block]:
        """Mine all pending transactions into a new block"""
        if not self.pending_transactions:
            return None
        
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data={
                "transactions": self.pending_transactions,
                "transaction_count": len(self.pending_transactions)
            },
            previous_hash=self.get_latest_block().hash
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        
        return new_block
    
    def add_loan_application(self, customer_id: str, loan_amount: float, 
                            loan_purpose: str, status: str = "pending"):
        """Add a loan application to the blockchain"""
        transaction = {
            "type": "loan_application",
            "customer_id": customer_id,
            "loan_amount": loan_amount,
            "loan_purpose": loan_purpose,
            "status": status
        }
        self.add_transaction(transaction)
        return self.mine_pending_transactions()
    
    def add_loan_approval(self, customer_id: str, loan_id: str, 
                         approved: bool, reason: str = ""):
        """Add a loan approval/rejection to the blockchain"""
        transaction = {
            "type": "loan_approval",
            "customer_id": customer_id,
            "loan_id": loan_id,
            "approved": approved,
            "reason": reason
        }
        self.add_transaction(transaction)
        return self.mine_pending_transactions()
    
    def add_payment(self, customer_id: str, loan_id: str, 
                   amount: float, payment_type: str = "installment"):
        """Add a loan payment to the blockchain"""
        transaction = {
            "type": "payment",
            "customer_id": customer_id,
            "loan_id": loan_id,
            "amount": amount,
            "payment_type": payment_type
        }
        self.add_transaction(transaction)
        return self.mine_pending_transactions()
    
    def is_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check proof of work
            if not current_block.hash.startswith("0" * self.difficulty):
                return False
        
        return True
    
    def get_chain(self) -> List[Dict[str, Any]]:
        """Get the entire blockchain as a list of dictionaries"""
        return [block.to_dict() for block in self.chain]
    
    def get_transactions_by_customer(self, customer_id: str) -> List[Dict[str, Any]]:
        """Get all transactions for a specific customer"""
        transactions = []
        for block in self.chain[1:]:  # Skip genesis block
            if "transactions" in block.data:
                for tx in block.data["transactions"]:
                    if tx.get("customer_id") == customer_id:
                        transactions.append({
                            **tx,
                            "block_index": block.index,
                            "block_hash": block.hash,
                            "block_timestamp": block.timestamp
                        })
        return transactions
    
    def get_stats(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        total_transactions = 0
        transaction_types = {}
        
        for block in self.chain[1:]:  # Skip genesis block
            if "transactions" in block.data:
                total_transactions += len(block.data["transactions"])
                for tx in block.data["transactions"]:
                    tx_type = tx.get("type", "unknown")
                    transaction_types[tx_type] = transaction_types.get(tx_type, 0) + 1
        
        return {
            "total_blocks": len(self.chain),
            "total_transactions": total_transactions,
            "transaction_types": transaction_types,
            "is_valid": self.is_valid(),
            "difficulty": self.difficulty,
            "latest_block_hash": self.get_latest_block().hash,
            "pending_transactions": len(self.pending_transactions)
        }


# Global blockchain instance
loan_blockchain = Blockchain(difficulty=2)
