import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY is missing from .env")

client = TavilyClient(api_key=api_key)


def search_web(query):
    response = client.search(
        query=query,
        max_results=5
    )

    return response["results"]

if __name__ == "__main__":
    results = search_web("What is artificial intelligence?")

    for result in results:
        print(result["title"])
        print(result["url"])
        print()