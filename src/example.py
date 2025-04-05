from openai import OpenAI
import json
from internet.search.tools import google_search
from utils.tool_decorator import get_tool_definition, create_tools_list
import os

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def execute_tool_call(tool_call):
    """Execute a tool call based on the name and arguments"""
    name = tool_call.name
    args = json.loads(tool_call.arguments)
    
    if name == "google_search":
        query = args.get("query")
        api_key = os.getenv("GOOGLE_CONSTELLA_API_KEY")
        search_id = os.getenv("GOOGLE_SEARCH_CX_ID")
        return google_search(query, api_key, search_id)
    
    return {"error": f"Unknown tool: {name}"}

def search_and_summarize(user_query, api_key=os.getenv("GOOGLE_CONSTELLA_API_KEY"), search_id=os.getenv("GOOGLE_SEARCH_CX_ID")):
    """
    Search Google and generate a summary using OpenAI function calling
    
    Args:
        user_query: The user's question or search query
        api_key: Google API key
        search_id: Google Custom Search Engine ID
        
    Returns:
        A summary based on the search results
    """
    # Get the tool definition using the decorator utility
    tools = [get_tool_definition(google_search)]
    
    # First call to get tool execution request
    response = openai_client.responses.create(
        model="gpt-4o",
        input=[{"role": "user", "content": user_query}],
        tools=tools
    )
    
    # Process tool calls and collect results
    input_messages = [{"role": "user", "content": user_query}]
    
    for tool_call in response.output:
        if tool_call.type != "function_call":
            continue
            
        # Execute the function
        result = execute_tool_call(tool_call)
        
        # Add the function call and result to messages
        input_messages.append(tool_call)
        input_messages.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": json.dumps(result)
        })
    
    # Get the final response with a summary
    final_response = openai_client.responses.create(
        model="gpt-4o",
        input=input_messages,
        tools=tools
    )
    
    return final_response.output_text

def test_search_tool(search_query, api_key=os.getenv("GOOGLE_CONSTELLA_API_KEY"), search_id=os.getenv("GOOGLE_SEARCH_CX_ID")):
    """
    Test function that demonstrates the search process and provides a summary
    
    Args:
        search_query: The search query to process
        api_key: Google API key (optional)
        search_id: Google Search Engine ID (optional)
        
    Returns:
        A formatted report showing both raw data and summary
    """
    print(f"SEARCH QUERY: {search_query}")
    print("-" * 50)
    
    # Perform the direct search first to show raw results
    raw_results = google_search(search_query, api_key, search_id)
    
    print("RAW SEARCH RESULTS:")
    if isinstance(raw_results, dict) and "error" in raw_results:
        print(f"Error: {raw_results['error']}")
    else:
        for i, result in enumerate(raw_results[:3], 1):  # Show just first 3 for brevity
            print(f"{i}. {result.get('title', 'No title')}")
            print(f"   Link: {result.get('link', 'No link')}")
            print(f"   {result.get('snippet', 'No description')[:100]}...")
            print()
    
    print("-" * 50)
    
    # Now get the AI summary
    print("GENERATING AI SUMMARY...")
    summary = search_and_summarize(search_query, api_key, search_id)
    
    print("\nAI SUMMARY:")
    print(summary)
    
    return {
        "raw_results": raw_results,
        "ai_summary": summary
    }

# Example usage
if __name__ == "__main__":
	# print(get_tool_definition(google_search))
	
    # Example with provided credentials
    test_search_tool(
        "What are the latest developments in AI?",
    )