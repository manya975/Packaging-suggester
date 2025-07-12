import os
import gdown  # install this via pip
import tensorflow as tf
import json
import numpy as np
from PIL import Image
import io

MODEL_PATH = "packaging_model.h5"
MODEL_FILE_ID = "1KP_SBJ3RTECRI_j49ieOpit6rB3GEJnb/view?usp=sharing"  
MODEL_URL = f"https://drive.google.com/file/d/1KP_SBJ3RTECRI_j49ieOpit6rB3GEJnb/view?usp=sharing?id={MODEL_FILE_ID}"

if not os.path.exists(MODEL_PATH):
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

model = tf.keras.models.load_model(MODEL_PATH)

with open("label_map.json") as f:
    label_map = json.load(f)
inv_map = {v: k for k, v in label_map.items()}

with open("co2_data.json") as f:
    co2_data = json.load(f)

def classify_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))
    arr = np.expand_dims(np.array(img) / 255., axis=0)
    pred = model.predict(arr)[0]
    idx = int(np.argmax(pred))
    material = inv_map[idx]
    conf = round(float(pred[idx]) * 100, 2)
    
    info = co2_data.get(material, {
        "co2": 1.0,
        "recommend": "Use eco alternatives"
    })

    return {
        "material": material,
        "confidence": conf,
        "co2": info["co2"],
        "recommendation": info["recommend"]
    }
