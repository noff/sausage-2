import os
from google.cloud import vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './vision.json'
from flask import Flask
from google.protobuf.json_format import MessageToJson
import proto
from flask import request
import random

app = Flask(__name__)

@app.route("/reco")
def reco():
    try:
        file_uri = request.args.get('url')
        if file_uri:
            client = vision.ImageAnnotatorClient()
            image = vision.Image()
            image.source.image_uri = file_uri
            response = client.label_detection(image=image)
            labels = response.label_annotations
            serialized = ' '.join([proto.Message.to_dict(tag)['description'].lower() for tag in labels])

            if 'cucumber' in serialized:
                variants = [
                    'Вот зеленый молодец. Он зовется…',
                    'сервис не поддерживает определение огурцов',
                    'куда вы со своими огурцами лезете?'
                ]
                return {'result': random.choice(variants)}
            elif 'sausage' in serialized:
                variants = [
                    'сосиска!!!!11111',
                    'о, сосисон!',
                    'да, это оно',
                    '42'
                ]
                return {'result': random.choice(variants)}
            elif 'wurst' in serialized or 'würst' in serialized:
                variants = [
                    'сосиска... или сарделька...',
                    'сосиска или что-то похожее',
                    'das ist sosiskish'
                ]
                return {'result': random.choice(variants)}
            elif 'cervelat' in serialized or 'kielbasa' in serialized:
                variants = [
                    'ну колбаса наверно',
                    'больше похоже на колбасу',
                    'уберите колбасу от ребенка!'
                ]
                return {'result': random.choice(variants)}
            elif 'food' in serialized or 'fast food' in serialized:
                variants = [
                    'возможно, сосиска',
                    'скорее всего тут есть сосиска',
                    '50/50'
                ]
                return {'result': random.choice(variants)}
            else:
                variants = [
                    'что-то непонятное',
                    'загадочно',
                    'я не знаю, что это'
                ]
                print(serialized)
                return {'result': random.choice(variants)}
        else:
            return {'result': 'ссылку забыл, ссылочку!'}
    except TypeError:
        return {'result': 'что-то не срослось'}
