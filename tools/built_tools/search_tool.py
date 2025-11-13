from langchain_community.tools import DuckDuckGoSearchResults

search = DuckDuckGoSearchResults(output_format="list")

result = search.invoke("Obama")

print(f"Result : ", result)