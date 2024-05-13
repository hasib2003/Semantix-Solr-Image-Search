"""
Provides methods for recieving the users query and preprocessing it, communicating with relevant servers and finally ranking and compiling results
"""


from vectorizer import Vectorizer
from inference import Inference

from PIL import Image
import torch
import os

class QueryHandler:
    def __init__(self) -> None:

        self.vectorizer = Vectorizer() # for preprocessing the query
        self.infer = Inference("http://localhost:8983/solr","image_vector_collection","")

    def query_by_image(self,image_path):

        assert os.path.isfile(image_path),f"No file found at {image_path}"
        
        img = Image.open(image_path).convert("L")
        img_vector = torch.squeeze(self.vectorizer.vectorize_img(img)).tolist()
        img_best_matches = self.infer.query_images(img_vector)
        # desc_best_matcher = self.infer.query_descriptions(img)
        print(img_best_matches)

        return img_best_matches

    def query_by_text(self,text):
        
        assert type(text) is str ,f"Input should be of type str"
        query_vector = torch.squeeze(self.vectorizer.vectorize_text(text)).tolist()
        best_matches = self.infer.query_images(query_vector)
        print(best_matches)

        return best_matches



# handler = QueryHandler()
# # handler.query_by_image





        