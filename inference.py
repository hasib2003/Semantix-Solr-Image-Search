from vectorizer import Vectorizer
import pysolr




class Inference:
    def __init__(self,solr_url , image_collection,description_collection) -> None:

        self.vectorizer = Vectorizer()
        self.solr_images_instance = pysolr.Solr(f"{solr_url}/{image_collection}", always_commit=True)
        self.solr_description_instance = pysolr.Solr(f"{solr_url}/{description_collection}", always_commit=True)



    def query_images(self,query_vector):

        """
        sends request to image_vector_collection, returns the list of paths of best matches
        """
        
        assert type(query_vector) is list and len(query_vector)==512, "input should be the list of 512 dimension"
        
        q = f'{{!knn f=image_vector topK=3}}{query_vector}'
        results = self.solr_images_instance.search(q)

        img_list = []

        for result in results:
            img_list.append(result["image_path"])
        

        return img_list
    
    def query_descriptions(self,query_vector):

        """
        sends request to description_vector_collection, returns the list of paths of best matches
        """
        
        assert type(query_vector) is list and len(query_vector)==512, "input should be the list of 512 dimension"
        
        q = f'{{!knn f=description_vector topK=3}}{query_vector}'
        results = self.solr_description_instance.search(q)

        img_list = []

        for result in results:
            img_list.append(result["image_path"])
        

        return list(set(img_list))
        