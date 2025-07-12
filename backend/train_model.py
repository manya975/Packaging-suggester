import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.optimizers import Adam
import json

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5
TRAIN_DIR = r"C:\Users\manya\Downloads\archive (2)\Garbage classification\Garbage classification"

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_gen = datagen.flow_from_directory(TRAIN_DIR, target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE, subset='training')
val_gen = datagen.flow_from_directory(TRAIN_DIR, target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE, subset='validation')

base = MobileNetV2(weights='imagenet', include_top=False,
    input_shape=(*IMAGE_SIZE, 3))
x = GlobalAveragePooling2D()(base.output)
x = Dense(128, activation='relu')(x)
preds = Dense(len(train_gen.class_indices), activation='softmax')(x)

model = tf.keras.Model(inputs=base.input, outputs=preds)
model.compile(optimizer=Adam(1e-4),
              loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS)

model.save("packaging_model.h5")
with open("label_map.json","w") as f:
    json.dump(train_gen.class_indices, f)
