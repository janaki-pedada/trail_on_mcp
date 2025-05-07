import httpx
from typing import Dict, Any

class MCPAdapter:
    def __init__(self, mcp_server_url: str):
        self.base_url = mcp_server_url
    
    async def execute(self, protocol: str, payload: Dict[str, Any]):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/mcp",
                json={
                    "protocol": protocol,
                    "payload": payload
                },
                timeout=30.0
            )
            return response.json()