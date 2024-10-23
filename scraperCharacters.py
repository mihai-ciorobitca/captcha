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
    image = np.array(img)
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    contoursSorted = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
    mask = np.zeros_like(image)
    for contour in contoursSorted:
        cv2.drawContours(mask, [contour], 0, color=255, thickness=-1) 
        # 0 is the index of contour and tickeness is set to -1 so that it fills the contour
        object_extracted = cv2.bitwise_and(image, image, mask=mask)
        x, y, w, h = cv2.boundingRect(contour)
        object_cropped = object_extracted[y:y+h, x:x+w]
        object_pil = Image.fromarray(object_cropped)
        objects.append(object_pil)
    return objects

def main():
    inputImages = listdir("output")
    characters = allCharacters()
    index = len(characters) + 1
    for i,image in enumerate(inputImages):
        print("Current image: " + image)
        image = convertToBinary("output/" + image)
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

main()