from flask import Flask, request, jsonify
from module import crop_image, process_ans_blocks, process_list_ans
import numpy as np
import cv2
import base64


app = Flask(__name__)
@app.route("/")
def home():
    return "Welcome to Vietnamese Answer Sheet Extraction"

@app.route('/answer', methods=['POST'])
def get_image_size():
    # Check if the request contains a file
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']

    # Check if the file has an allowed extension (you can customize this)
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in image_file.filename or \
            image_file.filename.split('.')[-1].lower() not in allowed_extensions:
        return jsonify({'error': 'Invalid image file'}), 400

    try:
        # Read the image using OpenCV
        image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_UNCHANGED)

        # Get answer
        list_ans_boxes = crop_image(image)
        list_ans = process_ans_blocks(list_ans_boxes)
        list_ans, result = process_list_ans(list_ans)

        # Process image to send back
        # Convert the image to base64
        _, img_encoded = cv2.imencode('.png', image)
        img_base64 = base64.b64encode(img_encoded.tobytes()).decode('utf-8')

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
