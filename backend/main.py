from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from agents import MasterAgent
from blockchain import loan_blockchain
import json

app = FastAPI(title="LoanMaster AI", version="1.0.0")

app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.agents: dict = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.agents[client_id] = MasterAgent()
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        self.active_connections.remove(websocket)
        if client_id in self.agents:
            del self.agents[client_id]
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Get agent for this client
            agent = manager.agents.get(client_id)
            if not agent:
                agent = MasterAgent()
                manager.agents[client_id] = agent
            
            # Process message
            response = agent.process_message(
                message_data.get("message", ""),
                message_data.get("customer_id")
            )
            
            # Send response
            await manager.send_personal_message(
                json.dumps(response), 
                websocket
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)

@app.get("/")
async def root():
    return RedirectResponse(url="/frontend/index.html")

# Blockchain API Endpoints
@app.get("/api/blockchain/stats")
async def get_blockchain_stats():
    """Get blockchain statistics"""
    try:
        stats = loan_blockchain.get_stats()
        return JSONResponse(content=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blockchain/chain")
async def get_blockchain_chain():
    """Get the entire blockchain"""
    try:
        chain = loan_blockchain.get_chain()
        return JSONResponse(content={"chain": chain, "length": len(chain)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blockchain/block/{block_index}")
async def get_block(block_index: int):
    """Get a specific block by index"""
    try:
        chain = loan_blockchain.get_chain()
        if 0 <= block_index < len(chain):
            return JSONResponse(content=chain[block_index])
        else:
            raise HTTPException(status_code=404, detail="Block not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blockchain/validate")
async def validate_blockchain():
    """Validate the blockchain integrity"""
    try:
        is_valid = loan_blockchain.is_valid()
        return JSONResponse(content={"valid": is_valid})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blockchain/customer/{customer_id}")
async def get_customer_transactions(customer_id: str):
    """Get all blockchain transactions for a customer"""
    try:
        transactions = loan_blockchain.get_transactions_by_customer(customer_id)
        return JSONResponse(content={"customer_id": customer_id, "transactions": transactions})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/blockchain/loan/application")
async def add_loan_application(data: dict):
    """Add a loan application to the blockchain"""
    try:
        required_fields = ["customer_id", "loan_amount", "loan_purpose"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        block = loan_blockchain.add_loan_application(
            customer_id=data["customer_id"],
            loan_amount=float(data["loan_amount"]),
            loan_purpose=data["loan_purpose"],
            status=data.get("status", "pending")
        )
        
        return JSONResponse(content={
            "success": True,
            "block": block.to_dict() if block else None,
            "message": "Loan application added to blockchain"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/blockchain/loan/approval")
async def add_loan_approval(data: dict):
    """Add a loan approval/rejection to the blockchain"""
    try:
        required_fields = ["customer_id", "loan_id", "approved"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        block = loan_blockchain.add_loan_approval(
            customer_id=data["customer_id"],
            loan_id=data["loan_id"],
            approved=bool(data["approved"]),
            reason=data.get("reason", "")
        )
        
        return JSONResponse(content={
            "success": True,
            "block": block.to_dict() if block else None,
            "message": "Loan approval added to blockchain"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/blockchain/payment")
async def add_payment(data: dict):
    """Add a payment to the blockchain"""
    try:
        required_fields = ["customer_id", "loan_id", "amount"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        block = loan_blockchain.add_payment(
            customer_id=data["customer_id"],
            loan_id=data["loan_id"],
            amount=float(data["amount"]),
            payment_type=data.get("payment_type", "installment")
        )
        
        return JSONResponse(content={
            "success": True,
            "block": block.to_dict() if block else None,
            "message": "Payment added to blockchain"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
