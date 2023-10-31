from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

try:
    # Initialize the Pinecone client with API key and environment
    pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))
except Exception as e:
    print("Failed to initialize Pinecone. Check your API key and environment settings.")
    print(f"Error: {str(e)}")

# Define keyword arguments for the text loader
text_loader_kwargs = {'autodetect_encoding': True}

# Create a directory loader to load documents from a specific path
loader = DirectoryLoader('E:\\DESKTOP\\FreeLanceProjects\\powlosmillion\\hlxsites prisma-cloud-docs main docs-en_enterprise-edition', glob="**/*.adoc", loader_cls=TextLoader, use_multithreading=True, show_progress=True, loader_kwargs=text_loader_kwargs)

try:
    # Load documents from the specified directory
    raw_docs = loader.load()
except Exception as e:
    print("Failed to load documents from the directory. Check the directory path and loader settings.")
    print(f"Error: {str(e)}")

# Create a text splitter to split the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1300,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)

# Split the loaded documents into smaller chunks
new_docs = text_splitter.split_documents(raw_docs)

# Create an instance of OpenAIEmbeddings
embedding = OpenAIEmbeddings()

print("Pushing docs to Pinecone...")

# Loop through the chunks and push them to Pinecone
for idx, doc in enumerate(new_docs):
    print(f"Pushing {idx+1}/{len(new_docs)} chunk...")
    try:
        # Push the documents to Pinecone for indexing
        Pinecone.from_documents(documents=[doc], embedding=embedding, index_name=os.getenv("PINECONE_INDEX_NAME"))
    except Exception as e:
        print(f"Failed to push chunk {idx+1} to Pinecone. Check Pinecone configuration and document format.")
        print(f"Error: {str(e)}")

print("Docs pushed to Pinecone.")