import os
import shutil


i = 8


# Путь к папке с изображениями
folder_path = 'C:\\Users\\USER\\Desktop\\diplom\\konturs\\masks5'
target_path = 'C:\\Users\\USER\\Desktop\\diplom\\konturs\\renamed_masks'

# Получение списка файлов в папке
file_list = os.listdir(folder_path)

# Перебор файлов
for file_name in file_list:
    # Полный путь к файлу
    file_path = os.path.join(folder_path, file_name)

    

    # Проверка расширения файла
    if file_name.lower().endswith('.png'):
        
        parts = file_name.split('-')
        number = int(parts[0])
        
        new_file_name = str(number + i) + '-mask.png'
        

        # Полный путь для нового файла
        new_file_path = os.path.join(target_path, new_file_name)

        print(file_path, new_file_path)

        # Переименование файла
        shutil.copy2(file_path, new_file_path)