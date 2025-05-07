from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
import asyncio
import httpx  # <-- THIS IS THE CRITICAL MISSING IMPORT

class MCPAdapter:
    def __init__(self, mcp_server_url: str):
        self.base_url = mcp_server_url
    
    async def execute(self, protocol: str, payload: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/mcp",
                json={"protocol": protocol, "payload": payload},
                timeout=30.0
            )
            return response.json()

class AgentState(TypedDict):
    messages: List[HumanMessage]

# Initialize components
mcp = MCPAdapter("http://localhost:8000")  # Update if your server runs on different port

async def fetch_news_node(state: AgentState):
    try:
        response = await mcp.execute(
            protocol="news_fetch",
            payload={"query": state["messages"][-1].content}
        )
        return {"messages": [HumanMessage(content=str(response))]}
    except Exception as e:
        return {"messages": [HumanMessage(content=f"Error: {str(e)}")]}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("fetch_news", fetch_news_node)
workflow.set_entry_point("fetch_news")
workflow.add_edge("fetch_news", END)
graph = workflow.compile()

async def main():
    result = await graph.ainvoke(
        {"messages": [HumanMessage(content="poltical news")]}
    )
    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())