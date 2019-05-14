import numpy as np
import cv2
import requests

import matplotlib.pyplot as plt
from PIL import Image
import os
import datetime
import json

class EmotionCapture():

    def __init__(self):
        self.flow = cv2.VideoCapture(1)
        self.subscription_key = "bbe9aa125b48403c9c6190284d593b93"
        assert self.subscription_key
        self.face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
        now = datetime.datetime.now()
        self.path_folder = now.strftime("%Y-%m-%d-%Hh%Mm%Ss")
        os.mkdir(self.path_folder)
        os.mkdir(self.path_folder + '/logs')
        os.mkdir(self.path_folder + '/img')

    def detect_emotion(self, frame, count):

        image_path = self.path_folder + "/img/frame%d.jpg" % count
        image_data = open(image_path, "rb")

        headers = {'Content-Type': 'application/octet-stream',
           'Ocp-Apim-Subscription-Key': self.subscription_key}
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
            'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
        }

        response = requests.post(self.face_api_url, params=params, headers=headers, data=image_data)
        response.raise_for_status()
        faces = response.json()
        frame = self.add_square(frame, faces)

        with open(self.path_folder + "/logs/logs%d.json" % count, 'w') as outfile:
            json.dump(faces, outfile)

        return frame


    def capture_frame(self):
        count = 0
        while(True):
            ret, frame = self.flow.read()
            cv2.imwrite(self.path_folder + "/img/frame%d.jpg" % count, frame)
            frame = self.detect_emotion(frame, count)
            count += 1
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def add_square(self, image, faces):


        for face in faces:
            fr = face["faceRectangle"]
            fa = face["faceAttributes"]
            print(fr)
            origin = (fr["left"], fr["top"])
            print(origin, fr["width"], fr["height"])
            cv2.rectangle(image, (fr["left"], fr["top"]+fr["height"]), (fr["left"]+fr["width"], fr["top"]-fr["height"]),(0,255,0),3)
            # cv2.putText(image, "%s, %d"%(fa["gender"].capitalize(), fa["age"]),fontsize=10, weight="regular", va="bottom")
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image,"%s, %d"%(fa["gender"].capitalize(), fa["age"]),(fr["left"]+fr["width"], fr["top"]-fr["height"]), font, 2,(255,255,255),2,cv2.LINE_AA)

        return image



capture = EmotionCapture()
capture.capture_frame()
