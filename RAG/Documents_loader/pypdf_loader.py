from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('documents/Ai.pdf')

docs = loader.load()

print("Page 1 : " , docs[0].page_content)
print("Page 2 : ", docs[1].page_content)