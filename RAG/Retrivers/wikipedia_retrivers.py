
from langchain_community.retrievers import WikipediaRetriever

retrivers = WikipediaRetriever(top_k_results=2 , lang='en')

Query = 'About bcci'

results = retrivers.invoke(Query)

for i , result in enumerate(results):
    print(f"Result {i+1} :", result.page_content)