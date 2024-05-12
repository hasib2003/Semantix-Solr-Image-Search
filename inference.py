from vectorizer import Vectorizer
import os
import torch
import pysolr


vectorizer = Vectorizer()

text = "cars"
text_vector = torch.squeeze(vectorizer.vectorize_text(text)).to(torch.float16)
print(text_vector.size())
text_vector = text_vector.tolist()


import pysolr

# Connect to Solr
solr = pysolr.Solr('http://localhost:8983/solr/Semantic_Search', always_commit=True)
# solr.delete(q='*:*')
# Define your query parameters
# query = {
 
#     'fq':  f'{"{!func}"}vector(description_vector,{text_vector} )', # Define your vector field and query
#     'sort': 'score desc',  # Sort by score
# }

# Execute the query
# # results = solr.search(q="*:*")
q = f'{{!knn f=image_vector topK=10}}{text_vector}'
print("->",q)
results = solr.search(q=q)


for result in results:
    print(result)
    print("\n\n")



