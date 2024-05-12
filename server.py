
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os 
from vectorizer import Vectorizer



app = Flask(__name__)

CORS(app)

# @app.route('/upload_image', methods=['GET','POST'])
# def upload_image():
    
    
@app.route('/Text', methods=['POST'])
def Text():

    data = request.get_json()
   
    print(data)

    with open("alpha.txt", 'w') as file:
        file.write(data + '\n')

    return jsonify({'message': 'Received text successfully'}), 200







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
        image_path = image_path1


        






        print("global image path",image_path)
        return jsonify({'message': 'Image path received successfully.'}), 200
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
            image_data.append({'filename': filename, 'data': base64_encoded_data})

    return jsonify(images=image_data)




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)