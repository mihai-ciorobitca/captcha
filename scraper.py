import subprocess
from PIL import Image
import numpy as np
from os import listdir
import sys
import cv2


def allCharacters():
    files = listdir("characters")
    characters = [Image.open("characters/" + file) for file in files]
    return characters

def convertToBinary(path):
    img = Image.open(path).convert("RGB")
    px = np.array(img)
    for rows in range(px.shape[0]):
        for columns in range(px.shape[1]):
            if not np.all(px[rows, columns] == 255):
                px[rows, columns] = [0, 0, 0]

    return Image.fromarray(px)

def createBoundedBox(img):
    px = np.array(img)
    for rows in range(px.shape[0]):
        for columns in range(px.shape[1]):
            if np.all(px[rows, columns] == 0):
                if rows > 0:
                    if np.all(px[rows - 1, columns] == 255):
                        px[rows, columns] = [255, 0, 0]
                        continue
                    if columns > 0:
                        if np.all(px[rows - 1, columns - 1] == 255):
                            px[rows, columns] = [255, 0, 0]
                            continue
                    if columns < px.shape[1] - 1:
                        if np.all(px[rows - 1, columns + 1] == 255):
                            px[rows, columns] = [255, 0, 0]
                            continue
                if rows < px.shape[0] - 1:
                    if np.all(px[rows + 1, columns] == 255):
                        px[rows, columns] = [255, 0, 0]
                        continue
                    if columns > 0:
                        if np.all(px[rows + 1, columns - 1] == 255):
                            px[rows, columns] = [255, 0, 0]
                            continue
                    if columns < px.shape[1] - 1:
                        if np.all(px[rows + 1, columns + 1] == 255):
                            px[rows, columns] = [255, 0, 0]
                            continue
                if columns > 0:
                    if np.all(px[rows, columns - 1] == 255):
                        px[rows, columns] = [255, 0, 0]
                        continue
                if columns < px.shape[1] - 1:
                    if np.all(px[rows, columns + 1] == 255):
                        px[rows, columns] = [255, 0, 0]
                        continue

    return Image.fromarray(px)

def extractCharacters(img):
    image = np.array(img.convert("L"))
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    for i, contour in enumerate(contours):
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [contour], -1, color=255, thickness=-1)
        object_extracted = cv2.bitwise_and(image, image, mask=mask)
        x, y, w, h = cv2.boundingRect(contour)
        object_cropped = object_extracted[y:y+h, x:x+w]
        object_pil = Image.fromarray(object_cropped)
        objects.append(object_pil)
    for i, object in enumerate(objects):
        object.save(f"{i}.png")
    return objects


def checker():
    characters = allCharacters()
    index = len(characters) + 1
    image = convertToBinary("temp.png")
    extractedCharacters = extractCharacters(image)
    for extractedCharacter in extractedCharacters:
        characters = allCharacters()
        if len(characters) == 36:
            sys.exit()
        found = False
        for character in characters:
            if np.array_equal(np.array(character), np.array(extractedCharacter)):
                found = True
                break
        if not found:
            extractedCharacter.save(f"characters/{index}.png")
            index += 1
            print(f"Saved image: {index}")
        else:
            print("Image already exists")


while True:
    subprocess.call(['curl', '-o', f'temp.png', 'https://famdev.ro/captcha.php'])
    checker()
