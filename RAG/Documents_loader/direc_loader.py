from pydoc import doc
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader

# Create the loader
loader = DirectoryLoader(
    path="./documents",
    glob="*.txt",
    loader_cls=TextLoader
)

# Load all supported documents
documents = loader.load()

print(len(documents))
