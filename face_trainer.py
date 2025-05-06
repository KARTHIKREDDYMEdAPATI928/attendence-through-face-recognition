import cv2
import numpy as np
from PIL import Image
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataset'

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        gray_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(gray_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split('.')[1])
        faceSamples.append(img_numpy)
        ids.append(id)

    return faceSamples, ids

faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
recognizer.write('trainer/trainer.yml')

print(f"Training complete. {len(np.unique(ids))} unique student(s) trained.")
