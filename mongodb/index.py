from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-minilm-l6-v2')

#
connection_string = os.getenv('mdb')

# Connect to MongoDB
client = MongoClient(connection_string)
db = client['sample_mflix']
collection = db['embedded_movies']


async def encode(self, text):
    loop = asyncio.get_event_loop()
    embedding = await loop.run_in_executor(None, model.encode, [text])
    return embedding[0].tolist()


# Get all documents
documents = collection.find()

# Update each document
for doc in documents:
    print(doc['title'])
    if 'plot' not in doc:
        continue
    embedding = model.encode([doc['plot']])[0].tolist()
    collection.update_one(
        {'_id': doc['_id']},
        {'$set': {'plot_embedding_368': embedding}}
    )
