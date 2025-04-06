from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import os
from openai import OpenAI

# Import the tools and functions from example.py
from internet.search.tools import google_search
from internet.browse.tools import get_website_url_content
from utils.tool_decorator import get_tool_definition, create_tools_list

# Initialize FastAPI app
app = FastAPI(title="PowerUp Demo API")

# Add CORS middleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # In production, replace with specific origins
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class PowerUpRequest(BaseModel):
	tools: List[str]
	message: str

# Response model
class PowerUpResponse(BaseModel):
	response: str
	tool_calls_executed: List[Dict[str, Any]]

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

@app.post("/powerup-demo", response_model=PowerUpResponse)
async def powerup_demo(request: PowerUpRequest):
	"""
	Execute a PowerUp demo with the provided tools and user message.
	
	This endpoint will:
	1. Process the user message with the available tools
	2. Execute any tool calls requested by the AI
	3. Return the final AI response
	"""
	# Map tool names to their function definitions
	tool_map = {
		"google_search": google_search,
		"get_website_url_content": get_website_url_content
	}
	
	# Filter and create tool definitions based on requested tools
	available_tools = []
	for tool_name in request.tools:
		if tool_name in tool_map:
			available_tools.append(get_tool_definition(tool_map[tool_name]))
		else:
			raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
	
	# Initialize conversation with user message
	input_messages = [{"role": "user", "content": request.message}]
	tool_calls_executed = []
	
	# Continue processing until we get a text response (no more tool calls)
	while True:
		# Call the model with current conversation
		response = openai_client.responses.create(
			model="gpt-4o",
			input=input_messages,
			tools=available_tools
		)
		
		# Check if there are any tool calls to process
		has_tool_calls = False
		for tool_call in response.output:
			if tool_call.type == "function_call":
				has_tool_calls = True
				
				# Execute the tool call
				result = await execute_tool_call_async(tool_call)
				
				# Track executed tool calls for response
				tool_calls_executed.append({
					"name": tool_call.name,
					"arguments": json.loads(tool_call.arguments),
					"result": result
				})
				
				# Add the function call and result to messages
				input_messages.append(tool_call)
				input_messages.append({
					"type": "function_call_output",
					"call_id": tool_call.call_id,
					"output": json.dumps(result) if not isinstance(result, str) else result
				})
		
		# If no tool calls were made, we have our final text response
		if not has_tool_calls:
			break
	
	return PowerUpResponse(
		response=response.output_text,
		tool_calls_executed=tool_calls_executed
	)

