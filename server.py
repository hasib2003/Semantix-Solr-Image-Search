
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os 
from queryHandler import QueryHandler

BASE_DIR = "/home/hasib/semester_6/Parallel&Dist/project/data/flickr30k_images"
query_handler = QueryHandler()
app = Flask(__name__)
print(1)
CORS(app)

# @app.route('/upload_image', methods=['GET','POST'])
# def upload_image():
    
def paths2base64(path_list):
    image_data = []
    for filename in path_list:
        with open(os.path.join(BASE_DIR, filename), 'rb') as f:
            base64_encoded_data = base64.b64encode(f.read()).decode('utf-8')
            image_data.append({'filename': filename, 'base64': base64_encoded_data})
    return image_data

@app.route('/Text', methods=['POST'])
def Text():

    data = request.get_json()
   
    print(data)

    # with open("alpha.txt", 'w') as file:
    #     file.write(data + '\n')


    # ASSUMING THAT DATA CONTAINS THE QUERY STRING

    best_matching_paths = query_handler.query_by_text(text=data)
    images_data = paths2base64(best_matching_paths)

    return jsonify(images_data)



    # return jsonify({'message': 'Received text successfully'}), 200







@app.route("/Upload_image", methods = ["POST"])
def Upload_image():
    try:
        data = request.get_json()
        image_data_url = data['imageUrl']

        # Extract the base64-encoded image data
        _, encoded_data = image_data_url.split(",", 1)
        image_data = base64.b64decode(encoded_data)

        image_path1 = os.path.join('pictures', 'uploaded_image.jpg')
        
        with open(image_path1, 'wb') as out_file:
            out_file.write(image_data)

        print(image_path1)

        # sending request to solr 
        best_matching_paths = query_handler.query_by_image(image_path=image_path1)
        # image_data = []


        # for filename in best_matching_paths:
        #     with open(os.path.join(BASE_DIR, filename), 'rb') as f:
        #         base64_encoded_data = base64.b64encode(f.read()).decode('utf-8')
        #         image_data.append({'filename': filename, 'base64': base64_encoded_data})

        images_data = paths2base64(best_matching_paths)

        # image_path = image_path1
        # print("global image path",image_path)
        # return jsonify({'message': 'Image path received successfully.'}), 200
        return jsonify(images_data)
    
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500
    
    
    
    
    
    


@app.route('/getImages',  methods = ["POST","GET"])
def get_images():
    image_data = []
    # Assuming images are stored in the directory "./pictures"
    image_directory = "./pictures"
    print(1)
    for filename in os.listdir(image_directory):
        with open(os.path.join(image_directory, filename), 'rb') as f:
            base64_encoded_data = base64.b64encode(f.read()).decode('utf-8')
            image_data.append({'filename': filename, 'base64': base64_encoded_data})
            

    return jsonify(images=image_data)



print(11)
if __name__ == '__main__':
    

    print(1)
    app.run(host='0.0.0.0',port=4000,debug=True)
    print(3)

