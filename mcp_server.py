from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json

app = FastAPI()

class MCPRequest(BaseModel):
    protocol: str
    payload: dict

@app.post("/mcp")
async def handle_mcp_request(request: MCPRequest):
    if request.protocol == "news_fetch":
        try:
            query = request.payload.get("query", "")
            cmd = f'python news_service.py \'{json.dumps({"query": query})}\''
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return {"status": "success", "data": json.loads(result.stdout)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    return {"status": "error", "message": "Unsupported protocol"}

