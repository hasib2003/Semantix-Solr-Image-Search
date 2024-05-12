"""
This file is used to encode the images into clip vector
"""

import torch
import clip
from PIL import Image

class Vectorizer():
    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def vectorize_img(self,pilImg):

        assert isinstance(pilImg, Image.Image), "Input is not a PIL image."
        
        image = self.preprocess(pilImg).unsqueeze(0).to(self.device)     
        with torch.no_grad():   
            image_features = self.model.encode_image(image)

        return image_features


    def vectorize_text(self,text):        
        assert type(text) == str, "Expected text to be of type string"

        text = clip.tokenize([text]).to(self.device)

        with torch.no_grad():
            text_features = self.model.encode_text(text)
            
        return text_features
