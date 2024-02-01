import json
from PIL import Image, ImageDraw
import random
import os


def generate_random_color():
    r = 255
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def draw_arrows(image, arrows_list):

    width = 5
    """
    Draws multiple arrows on an image based on a list of arrow coordinate pairs.

    Arguments:
    image: Image object (from PIL)
    arrows_list: List of arrow coordinate pairs [ [(x1, y1), (x2, y2)], [(x3, y3), (x4, y4)], ... ]
    color: Tuple (R, G, B) representing the arrow color (default: red)
    width: Width of the arrow line (default: 2)
    """

    draw = ImageDraw.Draw(image)

    for arrow in arrows_list:
        start_point, end_point, color = arrow
        # Calculating arrow length and angle
        length = 20
        angle = 0.3  # Adjust this value to change the arrow's slant

        # Calculating coordinates to draw the arrow
        x1, y1 = start_point
        x2, y2 = end_point
        dx = x2 - x1
        dy = y2 - y1
        arrow_length = ((dx ** 2) + (dy ** 2)) ** 0.5

        # If arrow length is too small, skip drawing the arrow
        if arrow_length <= length:
            continue

        sin_angle = dy / arrow_length
        cos_angle = dx / arrow_length

        # Calculating coordinates to draw the arrow
        x3 = x2 - int(length * cos_angle - length * angle * sin_angle)
        y3 = y2 - int(length * sin_angle + length * angle * cos_angle)
        x4 = x2 - int(length * cos_angle + length * angle * sin_angle)
        y4 = y2 - int(length * sin_angle - length * angle * cos_angle)

        # Drawing the arrow line
        draw.line([start_point, end_point], fill=color, width=width)

        # Drawing arrow parts
        draw.line([end_point, (x3, y3)], fill=color, width=width)
        draw.line([end_point, (x4, y4)], fill=color, width=width)

    return image



def generate_routes_images(route, WIDTH_CONSTRAINT, HEIGHT_CONSTRAINT):
    index = 1
    for item in route:
        image = Image.open('./masterpiece.jpg')
        image_draw = ImageDraw.Draw(image)
        coordinates = []
        for i in range(0, len(item) - 1):
            current = item[i]
            next = item[i+1]
            color = generate_random_color()
            
            start_coord = (current["x"] * WIDTH_CONSTRAINT, current["y"] * HEIGHT_CONSTRAINT)
            end_coord = (next["x"] * WIDTH_CONSTRAINT, next["y"] * HEIGHT_CONSTRAINT)
            coordinates_item = [start_coord, end_coord, color]
            coordinates.append(coordinates_item)
            
        image_with_arrows = draw_arrows(image, coordinates)
        image_with_arrows.save(f'routes{index}.jpg')
     
        index += 1

def list_files_by_substring(directory, substrings):
    files_with_substring = []
    
    # Check each file in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if the filename contains the specified substring
        score = 0
        for substring in substrings:
            if substring in filename:
                score += 1
        
        if score == len(substrings):
            files_with_substring.append(file_path)
    
    return files_with_substring

def generate_gif():
    directory = "./"
    sub = ["routes", ".jpg"]
    files = list_files_by_substring(directory, sub)
    images = [Image.open(file) for file in files]
    images[0].save("route.gif", save_all=True, append_images=images[1:], duration=6000, loop=0)