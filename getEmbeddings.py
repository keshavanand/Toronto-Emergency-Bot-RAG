
from content_processing.processPdf import get_chunks
from content_processing.text_processing import process_text
import pandas as pd
from openai import AzureOpenAI
import os
import numpy as np

chunks = get_chunks("data/GetEmergencyReadyGuide_Toronto.pdf", 2, 3)
processed_chunks = process_text(chunks)

df = pd.DataFrame(([key, value] for key, value in processed_chunks.items()),columns=['Heading', 'Content'])

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )



def generate_embeddings(text, model="text-embedding-ada-002"): 
    return client.embeddings.create(input = [text], model=model).data[0].embedding

df['Embeddings'] = df["Content"].apply(lambda x : generate_embeddings (x, model = 'text-embedding-ada-002')) 

df.to_csv('word_embeddings.csv')


df = pd.read_csv('word_embeddings.csv')


# Convert the string representation of the embedding to a numpy array
# neeeded since we wrote it to a csv file
df['Embeddings'] = df['Embeddings'].apply(eval).apply(np.array)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Hotdog is not in the CSV. Let calculate the embedding for it
search_term = "how to know if food is safe"
search_term_vector = generate_embeddings(search_term, model="text-embedding-ada-002")


# now we can calculate the similarity between the search term and all the words in the CSV 
df["similarities"] = df['Embeddings'].apply(lambda x: cosine_similarity(x, search_term_vector))
# print the top 5 most similar words
print(df.sort_values("similarities", ascending=False).head(5))


df.to_csv('word_embeddings.csv')




