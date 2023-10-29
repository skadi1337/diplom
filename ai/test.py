import tensorflow as tf
import keras
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

print("Версия TensorFlow:", tf.__version__)

# Загрузка модели U-Net из файла h5
loaded_model = keras.models.load_model('C:\\Users\\USER\\Desktop\\diplom\\ai\\unet_model.h5')


image_path = 'D:\\downloads\\18-map.png'
image = tf.keras.preprocessing.image.load_img(image_path, target_size=(640, 640))
image = tf.keras.preprocessing.image.img_to_array(image)
image = np.expand_dims(image, axis=0)  # Добавление размерности пакета (batch dimension)

# Применение модели к изображению
predicted_mask = loaded_model.predict(image)

image_array = predicted_mask

image_array = np.squeeze(image_array, axis=0)  # Remove the extra dimension

plt.imshow(image_array, cmap='gray')  # Use 'gray' colormap for grayscale image
plt.axis('off')
plt.show()
