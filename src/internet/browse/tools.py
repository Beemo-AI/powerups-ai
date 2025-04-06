"""
The actual functions that are called when a tool is used by the assistant.
The entire file is passed and using the function name specified in the tools to the 
assistant, the function is called and its results are returned.
NOTE: tenant_name and other extra_args are passed to all the functions to prevent
an unexpected keyword error from happening.
"""
from datetime import datetime
import traceback
import httpx
import html2text
import os
from utils.tool_decorator import tool

def clean_results(results):
	"""
	Clean the results for the Assistants tool call processing.
	:param results: The results to clean.
	:return: The cleaned results as a string.
	"""
	final_str = ''
	for result in results:
		# Parse any datetime values in the result metadata
		for key, value in result.items():
			if isinstance(value, datetime):
				result[key] = value.isoformat()
		final_str += str(result) + '\n'
	return final_str


def html_to_text(html,ignore_links=False,bypass_tables=False,ignore_images=True):
	'''
	This function is used to convert html to text.
	It converts the html to text and returns the text.
	
	Args:
		html (str): The HTML content to convert to text.
		ignore_links (bool): Ignore links in the text. Use 'False' to receive the URLs of nested pages to scrape.
		bypass_tables (bool): Bypass tables in the text. Use 'False' to receive the text of the tables.
		ignore_images (bool): Ignore images in the text. Use 'False' to receive the text of the images.
	Returns:
		str: The text content of the webpage. If max_length is provided, the text will be truncated to the specified length.
	'''
	text = html2text.HTML2Text()
	text.ignore_links = ignore_links
	text.bypass_tables = bypass_tables
	text.ignore_images = ignore_images
	return text.handle(html,)

@tool(
    description="Fetch and extract text content from a webpage URL"
)
async def get_website_url_content(url: str, ignore_links: bool = False, max_length: int = None, tenant_name: str = None):
	'''
	This function is used to scrape a webpage.
	It converts the html to text and returns the text.
	
	Args:
		url (str): The URL to scrape.
		ignore_links (bool): Ignore links in the text. Use 'False' to receive the URLs of nested pages to scrape.
		max_length (int): Maximum length of text to return. If None, return all text.
		tenant_name (str): Tenant name for tracking purposes.

	Returns:
		str: The text content of the webpage. If max_length is provided, the text will be truncated to the specified length.
	'''
	header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
	try:
		async with httpx.AsyncClient(follow_redirects=True) as client:
			response = await client.get(str(url), headers=header, timeout=5)
	except Exception as e:
		print('Error in webscrape: ', e)
		return {"error": f"Error fetching the url {url}: {str(e)}"}
	
	
	try:
		out = html_to_text(response.text, ignore_links=ignore_links)
		print("\n\nOut: ", out)
		if max_length:
			return out[0:max_length]
		else:
			return out
	except Exception as e:
		print('Error in html_to_text: ', e)
		return response.text

# Define the tool parameters
get_website_url_content._tool_params = {
	"type": "object",
	"properties": {
		"url": {
			"type": "string",
			"description": "The URL of the webpage to scrape"
		},
		"ignore_links": {
			"type": "boolean",
			"description": "Whether to ignore links in the text. Use 'false' to receive URLs of nested pages.",
			"default": False
		},
		"max_length": {
			"type": "integer",
			"description": "Maximum length of text to return. If not provided, returns all text.",
			"default": None
		}
	},
	"required": ["url"],
	"additionalProperties": False
}

