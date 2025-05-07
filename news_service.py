import sys
import json
import requests

def fetch_news(query: str):
    api_key = "d630d1058ab844b291e884d68fe8a523"  # Replace with your actual key
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&pageSize=5"
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    try:
        # Fix 1: Read all input from stdin
        input_data = sys.stdin.read() if not sys.argv[1:] else ' '.join(sys.argv[1:])
        
        # Fix 2: Validate input isn't empty
        if not input_data.strip():
            raise ValueError("Empty input received")
            
        # Fix 3: Safe JSON parsing
        input_json = json.loads(input_data)
        query = input_json.get("query", "")
        
        # Debug print
        print(f"Received query: {query}", file=sys.stderr)
        
        results = fetch_news(query)
        print(json.dumps(results))
        
    except json.JSONDecodeError as e:
        print(json.dumps({
            "status": "error",
            "message": f"Invalid JSON input: {str(e)}",
            "received_input": repr(input_data)  # Shows what was actually received
        }))
    except Exception as e:
        print(json.dumps({
            "status": "error", 
            "message": str(e)
        }))