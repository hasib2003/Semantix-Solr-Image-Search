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
        self.infer = Inference("http://localhost:8983/solr","image_vector_collection","description_vector_collection")

    def query_by_image(self,image_path):

        assert os.path.isfile(image_path),f"No file found at {image_path}"
        
        img = Image.open(image_path).convert("L")
        # converting to feature vector
        img_vector = torch.squeeze(self.vectorizer.vectorize_img(img)).tolist()

        # matches from image vector collection
        img_best_matches = self.infer.query_images(img_vector)
        
        # matches from descriptions vector collection
        desc_best_matches = self.infer.query_descriptions(img_vector)

        master_result = img_best_matches + desc_best_matches 

        return set(master_result)

    def query_by_text(self,text):
        
        assert type(text) is str ,f"Input should be of type str"
        query_vector = torch.squeeze(self.vectorizer.vectorize_text(text)).tolist()

        img_best_matches = self.infer.query_images(query_vector)
        
        # matches from descriptions vector collection
        desc_best_matches = self.infer.query_descriptions(query_vector)

        master_result = img_best_matches + desc_best_matches 

        return set(master_result)






        