import imgaug as ia
from imgaug import augmenters as iaa
import os
import numpy as np
from PIL import Image

# Путь к папке с изображениями
image_folder = 'C:\\Users\\USER\\Desktop\\diplom\\dataset\\tile'

# Путь к папке с масками
mask_folder = 'C:\\Users\\USER\\Desktop\\diplom\\dataset\\mask'

# Путь к папке для сохранения аугментированных изображений
output_folder = 'C:\\Users\\USER\\Desktop\\diplom\\dataset\\augment'

# Создание объекта аугментации
augmenter = iaa.Sequential([
    iaa.Fliplr(0.5),  # Отражение по горизонтали с вероятностью 50%
    iaa.Affine(rotate=(-10, 10))  # Вращение на случайный угол в диапазоне от -10 до 10 градусов
])

# Получение списка файлов в папке с изображениями
image_file_list = os.listdir(image_folder)

# Перебор файлов
for image_file_name in image_file_list:
    # Полный путь к исходному изображению
    image_path = os.path.join(image_folder, image_file_name)

    # Загрузка изображения
    image = Image.open(image_path)

    # Имя соответствующей маски
    mask_file_name = image_file_name.replace('-map.png', '-mask.png')  # Изменение имени файла для маски

    # Полный путь к маске
    mask_path = os.path.join(mask_folder, mask_file_name)

    # Загрузка маски
    mask = Image.open(mask_path)

    # Применение аугментации к изображению
    augmented_image = augmenter(image=np.array(image))

    # Применение аугментации к маске
    augmented_mask = augmenter(image=np.array(mask))

    # Преобразование обратно в объекты PIL.Image
    augmented_image = Image.fromarray(augmented_image)
    augmented_mask = Image.fromarray(augmented_mask)

    # Имя аугментированного файла изображения
    output_image_file_name = image_file_name.replace('.png', '_augmented.png')  # Изменение расширения файла

    # Полный путь для сохранения аугментированного изображения
    output_image_path = os.path.join(output_folder, output_image_file_name)

    # Сохранение аугментированного изображения
    augmented_image.save(output_image_path)

    # Имя аугментированного файла маски
    output_mask_file_name = mask_file_name.replace('.png', '_augmented.png')  # Изменение расширения файла

    # Полный путь для сохранения аугментированной маски
    output_mask_path = os.path.join(output_folder, output_mask_file_name)

    # Сохранение аугментированной маски
    augmented_mask.save(output_mask_path)