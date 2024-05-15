"""
SENDS DATA TO SOLR CLOUD FOR INDEXING
"""

import json
import os

class SolrDataUpdater:
    def __init__(self, solr_url, collection_name):
        self.solr_url = solr_url
        self.collection_name = collection_name

    def index(self, data):
        json_data = []
        for i in range(len(data[0])):
            document = {
                "image_path": data[0][i],
                "image_vector": data[1][i].tolist()
            }
            json_data.append(document)

        json_file = 'data.json'
        with open(json_file, 'w') as file:
            json.dump(json_data, file, indent=4)

        # Call curl command to update dataset in Solr
        os.system(f'curl "{self.solr_url}/api/collections/{self.collection_name}/update?commit=true" -H "Content-Type: application/json" --data-binary @{json_file}')
     

