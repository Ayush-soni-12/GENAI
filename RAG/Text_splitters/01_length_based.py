from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('../Documents_loader/documents/Ai.pdf')

docs = loader.load()

splitter = CharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 0,
    separator=''
)

results = splitter.split_documents(docs)

for  index , result in enumerate(results):
    print(f"line {index} : {result.page_content}")