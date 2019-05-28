import dash
import dash_core_components as dcc
import dash_html_components as html

from flask import Flask, Response
import cv2

import numpy as np
import requests

import matplotlib.pyplot as plt
from PIL import Image
import os
import datetime
import json
import sqlite3

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

class VideoCamera(object):
    def __init__(self):

        self.flow = cv2.VideoCapture(1)

        # SETUP API
        self.subscription_key = 'a4c51bb3b2f04086b706f15ff6142cdd'
        assert self.subscription_key
        self.face_api_url = ' https://westeurope.api.cognitive.microsoft.com/face/v1.0/detect'

        # BUILDING NEW FOLDERS
        now = datetime.datetime.now()
        self.path_folder = now.strftime("%Y-%m-%d-%Hh%Mm%Ss")
        os.mkdir(self.path_folder)
        os.mkdir(self.path_folder + '/logs')
        os.mkdir(self.path_folder + '/img')

        # LINK TO DB
        self.connexion_db = sqlite3.connect('faces.db')
        self.cursor = self.connexion_db.cursor()

    def __del__(self):
        self.flow.release()

    def get_frame(self):
            success, image = self.flow.read()
            jpeg_emotion_detected= self.detect_emotion(image)
            ret, jpeg = cv2.imencode('.jpg', jpeg_emotion_detected)
            return jpeg.tobytes()

    def detect_emotion(self, image):

        headers = {'Content-Type': 'application/octet-stream',
           'Ocp-Apim-Subscription-Key': self.subscription_key}
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
            'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
            }
        _, img = cv2.imencode('.jpg', image)
        img = img.tobytes()
        response = requests.post(self.face_api_url, params=params, headers=headers, data=img)
        response.raise_for_status()
        faces = response.json()
        squared_frame = self.add_square(image, faces)
        return squared_frame

    def add_square(self, image, list_faces):

        for face in list_faces:
            fr = face["faceRectangle"]
            fa = face["faceAttributes"]
            fe = fa["emotion"]

            age = fa["age"]
            gender = fa["gender"]

            surprise = fe["surprise"]
            neutral = fe["neutral"]
            happiness = fe["happiness"]

            # print(fr)
            origin = (fr["left"], fr["top"])
            # print(origin, fr["width"], fr["height"])
            cv2.rectangle(image, (fr["left"], fr["top"]+fr["height"]), (fr["left"]+fr["width"], fr["top"]),(253,253,253),2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image,"%s"%(gender.capitalize()),(fr["left"]+fr["width"], fr["top"]), font, 1,(255,255,255))
            cv2.putText(image,"%s"%(age),(fr["left"]+fr["width"], fr["top"]+ 40), font, 1,(255,255,255))

            emotion = "default"
            color = (255,255,255)

            if surprise > 0.5:
                emotion = "surprise"
                color = (0,0,255)
            elif neutral > 0.5:
                emotion = "neutral"
                color = (255,0,0)
            elif happiness > 0.5:
                emotion = "happy"
                color = (0,255,0)
            cv2.putText(image,"%s"%(emotion),(fr["left"]+fr["width"], fr["top"]+ 80), font, 1,color)

            # self.cursor.execute("INSERT INTO faces VALUES (?, ?, ?, ?, ?)", (gender, age, surprise, neutral, happiness))
            self.connexion_db.commit()

        return image


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


@server.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1("Multi faces emotion detection"),
    html.Img(src="/video_feed"),

    html.H1(
        children='TechIsMagic by MagicLab',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])





if __name__ == '__main__':
    app.run_server(debug=True)
