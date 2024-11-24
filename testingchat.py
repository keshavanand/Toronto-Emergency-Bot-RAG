
from content_processing.processPdf import get_chunks
from content_processing.text_processing import process_text
import pandas as pd
from openai import AzureOpenAI
import os
import numpy as np


df = pd.read_csv('word_embeddings.csv')


# Convert the string representation of the embedding to a numpy array
# neeeded since we wrote it to a csv file
df['Embeddings'] = df['Embeddings'].apply(eval).apply(np.array)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# print the top 5 most similar words
print(df.sort_values("similarities", ascending=False).head(5))

search_term = "how to know if food is safe"

additional_content = df.sort_values("similarities", ascending=False).head(1)["Content"].to_string().replace("\n", " ")

chat_client = AzureOpenAI(
    api_key="67GUCiwqpyDvfEXFf5vgQ0uB1IHzDTw0QqyJR9CDjqAxps4zKlesJQQJ99AKACfhMk5XJ3w3AAAAACOGdsjD",  
    api_version="2024-02-01",
    azure_endpoint = "https://ksing-m3vuqiyj-swedencentral.cognitiveservices.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2024-08-01-preview"
)


response = chat_client.chat.completions.create(
    model="gpt-35-turbo", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "Assistant is a professional chatbot designed to help users in case of emergency"},
        {"role": "user", "content": search_term + additional_content}
    ]
)

print(response.choices[0].message.content)


