from openai import OpenAI
import json
import asyncio
from internet.search.tools import google_search
from internet.browse.tools import get_website_url_content
from utils.tool_decorator import get_tool_definition, create_tools_list
import os

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def execute_tool_call_async(tool_call):
    """Execute a tool call based on the name and arguments, supporting async functions"""
    name = tool_call.name
    args = json.loads(tool_call.arguments)
    
    if name == "google_search":
        query = args.get("query")
        api_key = os.getenv("GOOGLE_CONSTELLA_API_KEY")
        search_id = os.getenv("GOOGLE_SEARCH_CX_ID")
        return google_search(query, api_key, search_id)
    
    elif name == "get_website_url_content":
        url = args.get("url")
        ignore_links = args.get("ignore_links", False)
        max_length = args.get("max_length", None)
        # Call the async function and await its result
        result = await get_website_url_content(url, ignore_links, max_length)
        return result
    
    return {"error": f"Unknown tool: {name}"}

def execute_tool_call(tool_call):
    """Execute a tool call, running async functions in an event loop if needed"""
    name = tool_call.name
    
    if name == "get_website_url_content":
        # For async functions, run them in an event loop
        return asyncio.run(execute_tool_call_async(tool_call))
    else:
        # For synchronous functions
        args = json.loads(tool_call.arguments)
        
        if name == "google_search":
            query = args.get("query")
            api_key = os.getenv("GOOGLE_CONSTELLA_API_KEY")
            search_id = os.getenv("GOOGLE_SEARCH_CX_ID")
            return google_search(query, api_key, search_id)
        
        return {"error": f"Unknown tool: {name}"}

async def browse_and_analyze_async(url, question, ignore_links=False, max_length=None):
    """
    Fetch content from a webpage and have the AI analyze it
    
    Args:
        url: The URL to browse
        question: What question to answer about the webpage content
        ignore_links: Whether to ignore links in the page
        max_length: Maximum length of content to return
        
    Returns:
        AI analysis of the webpage content
    """
    # Get the tool definition
    tools = [get_tool_definition(get_website_url_content)]
    
    # First call to get tool execution request
    response = openai_client.responses.create(
        model="gpt-4o",
        input=[{"role": "user", "content": f"Please fetch and analyze the content from this URL: {url}. {question}"}],
        tools=tools
    )
    
    # Process tool calls and collect results
    input_messages = [{"role": "user", "content": f"Please fetch and analyze the content from this URL: {url}. {question}"}]
    
    for tool_call in response.output:
        if tool_call.type != "function_call":
            continue
            
        # Execute the function (which is async)
        result = await execute_tool_call_async(tool_call)
        
        # Add the function call and result to messages
        input_messages.append(tool_call)
        input_messages.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": json.dumps(result) if isinstance(result, dict) else result
        })
    
    # Get the final response with analysis
    final_response = openai_client.responses.create(
        model="gpt-4o",
        input=input_messages,
        tools=tools
    )
    
    return final_response.output_text

def browse_and_analyze(url, question, ignore_links=False, max_length=None):
    """Wrapper to run the async function"""
    return asyncio.run(browse_and_analyze_async(url, question, ignore_links, max_length))

def test_browse_tool(url, question, ignore_links=False, max_length=10000):
    """
    Test function that demonstrates the browser tool and provides analysis
    
    Args:
        url: The URL to browse
        question: Question to answer about the content
        ignore_links: Whether to ignore links
        max_length: Maximum content length to process
        
    Returns:
        A formatted report showing both raw data and analysis
    """
    print(f"BROWSING URL: {url}")
    print(f"QUESTION: {question}")
    print("-" * 50)
    
    # First get the raw content
    raw_content = asyncio.run(get_website_url_content(url, ignore_links, max_length))
    
    print("RAW CONTENT PREVIEW:")
    if isinstance(raw_content, dict) and "error" in raw_content:
        print(f"Error: {raw_content['error']}")
    else:
        # Show a preview of the content (first 500 chars)
        preview = raw_content[:500] + "..." if len(raw_content) > 500 else raw_content
        print(preview)
    
    print("-" * 50)
    
    # Now get the AI analysis
    print("GENERATING AI ANALYSIS...")
    analysis = browse_and_analyze(url, question, ignore_links, max_length)
    
    print("\nAI ANALYSIS:")
    print(analysis)
    
    return {
        "raw_content": raw_content,
        "ai_analysis": analysis
    }

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
    # Test the search tool
    print("=== TESTING SEARCH TOOL ===")
    test_search_tool("What are the latest developments in AI?")
    
    print("\n\n")
    
    # Test the browse tool
    print("=== TESTING BROWSE TOOL ===")
    test_browse_tool(
        "https://docs.github.com/en/rest?apiVersion=2022-11-28", 
        "What are the main topics covered in the blog posts?",
        ignore_links=True,
        max_length=20000
    )