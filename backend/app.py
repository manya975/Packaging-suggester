from flask import Flask, request, jsonify
from flask_cors import CORS
from classify import classify_image

app = Flask(__name__)
CORS(app)

@app.route("/classify", methods=["POST"])
def classify_route():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    image_bytes = image_file.read()

    result = classify_image(image_bytes)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
