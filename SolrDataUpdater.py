import json
import os

class SolrDataUpdater:
    def __init__(self, solr_url, collection_caption,collection_image):
        self.solr_url = solr_url
        self.collection_caption = collection_caption
        self.collection_image = collection_image

    def IndexCaptionCluster(self, data):
        json_data = []
        for i in range(len(data[0])):
            document = {
                "image_path": data[0][i],
                "description_vector": data[1][i].tolist(),
            }
            json_data.append(document)

        json_file = 'CaptionCluster.json'
        with open(json_file, 'w') as file:
            json.dump(json_data, file, indent=4)

        # Call curl command to update dataset in Solr
        os.system(f'curl "{self.solr_url}/api/collections/{self.collection_caption}/update?commit=true" -H "Content-Type: application/json" --data-binary @{json_file}')
     
        # Remove JSON file after updating Solr
        # os.remove(json_file)
    
    def IndexImageCluster(self, data):
        json_data = []
        for i in range(len(data[0])):
            document = {
                "image_path": data[0][i],
                "image_vector": data[1][i].tolist()
            }
            json_data.append(document)

        json_file = 'ImageCluster.json'
        with open(json_file, 'w') as file:
            json.dump(json_data, file, indent=4)

        # Call curl command to update dataset in Solr
        os.system(f'curl "{self.solr_url}/api/collections/{self.collection_image}/update?commit=true" -H "Content-Type: application/json" --data-binary @{json_file}')
     
        # Remove JSON file after updating Solr
        # os.remove(json_file)

# # Example usage
# data = [
#     ['/path/to/image1.jpg', '/path/to/image2.jpg', '/path/to/image3.jpg'],
#     [[0.1,0.2,0.3,0.4], [0.2,0.3,0.4,0.5], [0.3,0.4,0.5,0.6]],
#     [[0.2,0.3,0.4,0.5], [0.3,0.4,0.5,0.6], [0.4,0.5,0.6,0.7]]
# ]

# solr_url = 'http://localhost:8983/solr'
# collection_caption = 'CaptionCollection'
# collection_image = 'ImageCollection'

# DataUpdater = SolrDataUpdater(solr_url, collection_caption,collection_image)
# DataUpdater.updater(data)
