"""

LOADS DATASET IN FORM OF BATCHES AND SEND THEM TO THE SOLR SERVER

"""

from torch.utils.data import DataLoader
from dataset import FlickrImageDataset, FlickrDescDataset
from tqdm import tqdm

from SolrDataUpdater import SolrDataUpdater
# from SolrDataUpdater_ import SolrDataUpdater


solr_url = 'http://localhost:8983'
image_collection = 'image_vector_collection'
description_vector_collection = 'description_vector_collection'

indexer = SolrDataUpdater(solr_url,description_vector_collection,image_collection)

img_vector_dataset =  FlickrImageDataset("../data/flickr30k_images")
desc_vector_dataset = FlickrDescDataset("../data/captions.txt")



img_vector_loader = DataLoader(dataset=img_vector_dataset, batch_size=15, num_workers=4, shuffle=False)

# Wrap the DataLoader with tqdm


for batch in tqdm(img_vector_loader, desc="Processing batches", leave=False):
    indexer.IndexImageCluster(batch)
    




