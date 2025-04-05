"""
The actual functions that are called when a tool is used by the assistant.
The entire file is passed and using the function name specified in the tools to the 
assistant, the function is called and its results are returned.
NOTE: tenant_name and other extra_args are passed to all the functions to prevent
an unexpected keyword error from happening.
"""
from db.weaviate.operations.general import query_by_vector
from ai.embeddings import create_embedding
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field
import traceback
import httpx
import html2text
from googleapiclient.discovery import build
import os

google_constella_api_key = os.environ.get('GOOGLE_CONSTELLA_API_KEY')
google_search_cx_id = 'c41e4d932d6f543f2'


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

async def search_user_notes_similarity(query:str = '', similarity_setting:float = 0.5, tenant_name:str=None):
	try:
		query_vector = create_embedding(query)
		results = query_by_vector(tenant_name, query_vector, similarity_setting=similarity_setting, include_vector=False)["results"]
		return clean_results(results)
	except Exception as e:
		print('Error in search_user_notes_similarity: ', e)
		traceback.print_exc()
		return []

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

async def get_website_url_content(url: HttpUrl, ignore_links: bool = False, max_length: int = None, tenant_name:str=None):
	'''
	This function is used to scrape a webpage.
	It converts the html to text and returns the text.
	
	Args:
		plain_json (dict): The JSON data containing the URL to scrape. It is meant to be called as a tool call from an assistant.
		the json should be in the format of {"url": "https://www.example.com", "ignore_links": False, "max_length": 1000}

	Returns:
		str: The text content of the webpage. If max_length is provided, the text will be truncated to the specified length.
	'''
	header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
	try:
		async with httpx.AsyncClient(follow_redirects=True) as client:
			response = await client.get(str(url), headers=header, timeout=5)
	except Exception as e:
		print('Error in webscrape: ', e)
		return "Error fetching the url "+str(url)
	print('response: ', response.text)
	out = html_to_text(response.text,ignore_links=ignore_links)
	if max_length:
		return out[0:max_length]
	else:
		return out

