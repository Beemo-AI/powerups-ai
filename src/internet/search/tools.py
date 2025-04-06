"""
The actual functions that are called when a tool is used by the assistant.
The entire file is passed and using the function name specified in the tools to the 
assistant, the function is called and its results are returned.
NOTE: tenant_name and other extra_args are passed to all the functions to prevent
an unexpected keyword error from happening.
"""
import traceback

import os
from googleapiclient.discovery import build

from utils.tool_decorator import tool

@tool(
	description="Search Google for information on a given query"
)
def google_search(query: str, api_key: str = None, search_id: str = None):
	"""
	Search Google and return relevant results for the given query.
	
	Args:
		query: The search query string
		api_key: Google API key (optional if set via environment variable)
		search_id: Google Custom Search Engine ID (optional if set via environment variable)
	
	Returns:
		List of search results with titles, links, and snippets
	"""
	
	# Use provided credentials or fall back to environment variables
	google_api_key = api_key 
	google_search_cx_id = search_id

	
	if not google_api_key or not google_search_cx_id:
		return {"error": "Google API key and Search Engine ID must be provided"}
	
	# Create the service
	service = build("customsearch", "v1", developerKey=google_api_key)
	
	try:
		# Execute the search
		result = service.cse().list(
			q=query,
			cx=google_search_cx_id,
			num=5  # Default to 5 results
		).execute()
		
		if result and result.get('items'):
			return result.get('items')
		else:
			return {"error": "No results found"}
			
	except Exception as e:
		return {"error": str(e)}

# Define the tool structure
google_search._tool_params = {
	"type": "object",
	"properties": {
		"query": {
			"type": "string",
			"description": "The search query to look up information"
		}
	},
	"required": ["query"],
	"additionalProperties": False
}
