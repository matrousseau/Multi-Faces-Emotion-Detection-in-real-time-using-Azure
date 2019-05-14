import json

with open('D:\\IA\\Projets\\Multi-Faces-Emotion-Detection-in-real-time-using-Azure\\2019-05-14-10h02m33s\\logs\logs8.json') as json_file:
    data = json.load(json_file)
    top = data[0]['faceRectangle']['top']
    left = data[0]['faceRectangle']['left']
    width = data[0]['faceRectangle']['width']
    height = data[0]['faceRectangle']['height']
    
    print(top, left, width, height)

    # for p in data[0]['faceRectangle']:
