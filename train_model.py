import tensorflow as tf
from tensorflow.keras import layers, models
import os

dataset_path = "dataset"

img_size = (64, 64)
batch_size = 32

train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=img_size,
    batch_size=batch_size,
    color_mode="grayscale"
)

val_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size,
    color_mode="grayscale"
)

model = models.Sequential([

    layers.Rescaling(1./255, input_shape=(64,64,1)),

    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Flatten(),

    layers.Dense(128, activation='relu'),

    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=10
)

os.makedirs("ai_model", exist_ok=True)

model.save("ai_model/malware_model.h5")

print("Model saved to ai_model/malware_model.h5")