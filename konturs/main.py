import cv2
import numpy as np
import os
import random
import re
import requests

res_path = 'C:\\Users\\USER\\Desktop\\diplom\\konturs\\tiles res'
tile_path = 'C:\\Users\\USER\\Desktop\\diplom\\konturs\\tiles5'
dots_path = 'C:\\Users\\USER\\Desktop\\diplom\\konturs\\dots'

def open_operation(img):
    n = 5
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (n, n))
    img_res = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return img_res

def binarization(img):
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lower_gray = 180
    upper_gray = 255
    mask = cv2.inRange(img_grey, lower_gray, upper_gray)
    img_grey = open_operation(img_grey)
    img_grey[mask != 0] = 255

    img_grey = open_operation(img_grey)

    img_thresh = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
   
    img_thresh = open_operation(img_thresh)

    return img_thresh


def find_contours(img_thresh):
    # Тут поменял ищу только внешние(родительские контуры)
    contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def find_approximate_contours(contours):
    approx_contours = []
    for contour in contours:
        eps = 3
        approx = cv2.approxPolyDP(contour, eps, True)        
        if len(approx) > 3:
            approx_contours.append(approx)
    return approx_contours 


def filter_contours_by_area(contours):
    areas = [cv2.contourArea(c) for c in contours]
    avg_area = sum(areas) / len(contours)

    filtered_contours = [c for c in contours if cv2.contourArea(c) >= 0.2 * avg_area]
    return filtered_contours


def draw_show_contours(img, img_bin, contours, approx_contours):
    img_bin = cv2.cvtColor(img_bin, cv2.COLOR_GRAY2BGRA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img_contours = np.uint8(np.zeros(img.shape))

    colors = [
        (255, 0, 0),    # красный
        (255, 127, 0),  # оранжевый
        (255, 255, 0),  # желтый
        (0, 255, 0),    # зеленый
        (0, 0, 255),    # синий
        (75, 0, 130),   # индиго
        (148, 0, 211)   # фиолетовый
    ]
    for countour in contours:
        i = random.randint(0, 6)
        color = colors[i]
        cv2.drawContours(img_contours, [countour], -1, color, 1)

    img_contours_approx = np.uint8(np.zeros(img.shape))

    for countour in approx_contours:
        i = random.randint(0, 6)
        color = colors[i]
        cv2.drawContours(img_contours_approx, [countour], -1, color, 1)
        cv2.drawContours(img, [countour], -1, color, 2)

    combined_img = np.concatenate((img, img_contours), axis=1)

    combined_img_1 = np.concatenate((img_bin, img_contours_approx), axis=1)

    combined_img = np.concatenate((combined_img, combined_img_1), axis=0)

    cv2.imshow('Result', combined_img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def sort_length(countour):
    return -countour.shape[0]


def read_file(tile_dict, dirpath):
    for f in os.listdir(dirpath):
        if f.endswith('.txt'):
            filepath = os.path.join(dirpath, f)            
            with open(filepath, 'r') as f:
                lines = f.readlines()
                parts = lines[0].split()

                width = float(parts[0])
                height = float(parts[1])

                pattern = r'^(\d+)\s+(-?[\d.]+)\s+(-?[\d.]+)$'

                for line in lines[1::]:
                    match = re.search(pattern, line)
                    if match:
                        tile_number = int(match.group(1))
                        centerX = float(match.group(2))
                        centerY = float(match.group(3))
                        tile_dict[tile_number] = (centerX, centerY)
    return (width, height)


def calculate_coordinates(center, width, height, approx_contours, size, filename):
    filepath = os.path.join(res_path, filename)
    # filepath = os.path.join('tiles res', 'result.txt')
    with open(filepath, 'a') as f:
        for contour in approx_contours:
            for point in contour:
                x = center[0] - width * (0.5 - point[0][0] / size)
                y = center[1]  +  height * (0.5 -  point[0][1] / size)               
                f.write(f' {x} {y}')
            f.write('\n')    

def calculate_coordinates_ai(center, width, height, approx_contours, size, tile_number, filename):
    filepath = os.path.join(res_path, filename)
    # filepath = os.path.join('tiles res', 'result.txt')
    with open(filepath, 'a') as f:
        for contour in approx_contours:
            f.write(f' {tile_number}')
            for point in contour:
                x = center[0] - width * (0.5 - point[0][0] / size)
                y = center[1]  +  height * (0.5 -  point[0][1] / size)               
                f.write(f' {x} {y}')
            f.write('\n')    


def parse_points(tile_points_dict, tile_dict, dirpath):
    for f in os.listdir(dirpath):
        if f.endswith('.txt'):
            filepath = os.path.join(dirpath, f)            
            with open(filepath, 'r') as f:
                lines = f.readlines()
                parts = lines[0].split(",")

                num_tiles = len(tile_dict)

                for i in range(num_tiles):
                    tile_points_dict[i] = list()

                for i in range(0, len(parts) , 3):
                    tile_number = int(parts[i])
                    point_x = float(parts[i + 1])
                    point_y = float(parts[i + 2])
                    #if tile_number in tile_points_dict:
                    tile_points_dict[tile_number].append((point_x, point_y))
                    #else:     
                    #    tile_points_dict[tile_number] = list()
                    #    tile_points_dict[tile_number].append((point_x, point_y))


def get_address(lat, lng):
    params = {
        "format": "json",
        "lat": lat,
        "lon": lng,
        "zoom": 18,
        "addressdetails": 1
    }

    response = requests.get("https://nominatim.openstreetmap.org/reverse", params=params, headers={'User-Agent': 'Mozilla/5.0'})

    result = response.json()

    address = "Не удалось получить адрес"
    if "display_name" in result:
        address = result["display_name"]

    return address

def get_area(contour, size):
    LAT_DELTA_METERS = 308.298566865291
    LON_DELTA_METERS = 308.3040143497024
    image_area = LAT_DELTA_METERS * LON_DELTA_METERS
    area = cv2.contourArea(contour) / pow(size, 2) * image_area
    return area

def calculate_points(tile_dict, tile_contours_dict, tile_points_dict, width, height, size):
    filepath = os.path.join(res_path, 'address_area.txt')
    with open(filepath, 'a', encoding="utf-8") as f:
        n = len(tile_dict)
        for i in range(0, n):
            centerX, centerY = tile_dict[i]
            address = get_address(centerY, centerX) 
            print("Calculating...")
            # print(centerX, centerY, address)
            res_contours = list()       
            if tile_points_dict[i]:
                for contour in tile_contours_dict[i]:
                    for point in tile_points_dict[i]:
                        pointX = size / 2 + (point[0] - centerX) / (0.5 * width) * size / 2
                        pointY = size / 2 - (point[1] - centerY) / (0.5 * height) * size / 2
                        distance = cv2.pointPolygonTest(contour, (pointX, pointY), False)
                        if distance > 0:
                            res_contours.append(contour)
                            area = get_area(contour, size)                            
                            f.write(f'{address} {area}')
                            f.write('\n')   
                            break

            calculate_coordinates((centerX, centerY), width, height, res_contours, size, 'result_filtered.txt')
            calculate_coordinates_ai((centerX, centerY), width, height, res_contours, size, i, 'result_filtered_ai.txt')



def main(dirpath, tile_dict, width, height, tile_contours_dict, img_size):
    for filename in os.listdir(dirpath):
        if filename.endswith('.png'):
            filepath = os.path.join(dirpath, filename)

            img = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)

            img_filter  = cv2.medianBlur(img, 7)

            img_bin = binarization(img_filter)

            contours = find_contours(img_bin)

            filtered_contours = list(contours)

            filtered_contours = filter_contours_by_area(contours)

            filtered_contours.sort(key=cv2.contourArea, reverse=True)

            approx_contours = find_approximate_contours(filtered_contours)

           
            # draw_show_contours(img, img_bin, filtered_contours, approx_contours)

            pattern = r'\d+'
            match = re.search(pattern, filename)
            number = int(match.group())

            img_size = 640
            #calculate_coordinates(tile_dict[number], width, height, approx_contours, img_size, 'result.txt')
            tile_contours_dict[number] = approx_contours


img_size = 640

path = tile_path
tile_dict = dict()
width, height = read_file(tile_dict, path)

tile_contours_dict = dict()
main(path, tile_dict, width, height, tile_contours_dict, img_size)

path = dots_path
tile_points_dict = dict()
parse_points(tile_points_dict, tile_dict, path)

print("Calculating...")
calculate_points(tile_dict, tile_contours_dict, tile_points_dict, width, height, img_size)
print("Calculated!")