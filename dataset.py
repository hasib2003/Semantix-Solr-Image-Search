""" creates the dataset required for solr collections """

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import transforms
import os
from PIL import Image
from vectorizer import Vectorizer

class FlickrImageDataset(Dataset):
    """
    Returns the pairs of ImagePath and Image Vectors
    """

    def __init__(self,pathToImgDir) -> None:
        super().__init__()

        self.vectorizer = Vectorizer() # to vectorize images and captions


        assert os.path.isdir(pathToImgDir), f"No Directory found at {pathToImgDir}"
        self.pathToImgDir = pathToImgDir
        
        self.files = []

        # finding all of files in given images dir
        result = os.walk(self.pathToImgDir)

        for root,  dirs, files in result:
            for file in files:
                self.files.append(file)

        self.num_samples = len(self.files)
        # print(f"Found {self.num_samples} in {self.pathToImgDir}")

        # print(files)

    def __len__(self):
        return self.num_samples - 26762
    
    def __getitem__(self, index):
        index += 26762
        
        entry = self.files[index]
        imgPath = os.path.join(self.pathToImgDir,entry)
        img = Image.open(imgPath).convert("L")
        img_vector = self.vectorizer.vectorize_img(img)
        img_vector = torch.squeeze(img_vector)

        # print("path ",entry,"img vector ",img_vector)

    
        return  entry,img_vector

        
# img_vector_dataset =  FlickrImageDataset("data/flickr30k_images")

# for i in img_vector_dataset:
#     print(i)
#     break

class FlickrDescDataset(Dataset):

    """
    Returns the pairs of ImagePath and Description Vectors
    """


    def __init__(self,pathToTxt) -> None:
        super().__init__()
    
        assert os.path.exists(pathToTxt),f"No file found at {pathToTxt}"

        self.vectorizer = Vectorizer() # to vectorize images and captions

    
        self.csvPath = pathToTxt

        self.meta_dataset = []
       
        with open(self.csvPath,"r") as file:
            # self.meta_dataset = file.readlines()
            line = file.readline()
            line = file.readline()
            while(line):
                
                line = line.split(",")
                self.meta_dataset.append(line)
                line = file.readline()

    def __getitem__(self, index):
        
        entry = self.meta_dataset[index]       
        desc_vector = self.vectorizer.vectorize_text(entry[1])
        desc_vector = torch.squeeze(desc_vector) 
        return  entry[0],desc_vector
    
    def __len__(self):
        return len(self.meta_dataset)

# obj = FlickerDescDataset("./data/captions.txt")
# for i in obj:
#     imgPath ,featureVector = i
#     print(imgPath ,featureVector.size() )
#     break;

# obj =FlickerImageDataset(pathToImgDir="data/flickr30k_images")
# for i in obj:
#     imgPath ,featureVector = i
#     print(imgPath ,featureVector.size() )
#     break;