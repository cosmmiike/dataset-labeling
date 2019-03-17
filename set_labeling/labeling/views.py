from django.shortcuts import render
import os
import json


def labeling_view(request):
    img_dir = os.path.dirname(os.path.abspath(
        __file__)) + '/static/labeling/img'
    photos = [i for i in os.listdir(img_dir) if i.endswith('.jpg')]

    sets = {
        'frisure': ['lisses', 'ondulés', 'bouclés', 'frisés'],
        'couleur': ['noir', 'blonde', 'brun', 'châtain', 'roux', 'gris'],
        'longeur': ['longues', 'mi-longues', 'courts', 'extra-courts'],
        'volume': ['volumineux', 'lâches', 'normaux'],

    }

    if request.GET.get('id_photo') is None:
        context = {
            'sets': sets,
            'photo_num': 0,
            'photo': 'labeling/img/' + photos[0],
        }
        return render(request, 'labeling/index.html', context)

    else:
        img_num = int(request.GET.get('id_photo'))
        if img_num > len(photos) - 1:
            img_num = 0

        elif request.POST.get('frisure-radio') is None or\
             request.POST.get('couleur-radio') is None or\
             request.POST.get('longeur-radio') is None or\
             request.POST.get('volume-radio') is None:
            img_num -= 1

        else:
            output = {
                'url': request.POST.get('photo-url'),
                'frisure': request.POST.get('frisure-radio'),
                'couleur': request.POST.get('couleur-radio'),
                'longeur': request.POST.get('longeur-radio'),
                'volume': request.POST.get('volume-radio'),
            }

            dataset_dir = os.path.dirname(os.path.abspath(
                __file__)) + '/static/labeling/json/'

            with open(dataset_dir + 'dataset.json') as json_file:
                data = json.load(json_file)
            data['data'].append(output)

            with open(dataset_dir + 'dataset.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)

        context = {
            'sets': sets,
            'photo_num': img_num,
            'photo': 'labeling/img/' + photos[img_num],
        }


        return render(request, 'labeling/index.html', context)
