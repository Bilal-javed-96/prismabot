import pinecone
from dotenv import load_dotenv  # For loading environment variables from .env file
import os
import time

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone
print("Initializing Pinecone...")
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"),
              environment=os.getenv("PINECONE_ENVIRONMENT"))
print("Pinecone initialized.")

# Delete the existing index (if it exists)
print("Deleting Pinecone index...")
pinecone.delete_index(os.getenv("PINECONE_INDEX_NAME"))
print("Index deleted.")

# Create a new Pinecone index
print("Creating a new Pinecone index...")
pinecone.create_index(os.getenv("PINECONE_INDEX_NAME"), dimension=1536, 
                      metric='cosine', 
                      pods=1, 
                      replicas=1, 
                      pod_type='p1.x1')
print("Index created.")
