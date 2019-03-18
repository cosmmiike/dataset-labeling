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
        'volume': ['volumineux', 'normaux', 'faibles'],
    }

    dataset_dir = os.path.dirname(os.path.abspath(
        __file__)) + '/static/labeling/json/'

    with open(dataset_dir + 'dataset.json') as json_file:
        data = json.load(json_file)

    if request.GET.get('id_photo') is None:
        img_num = 0

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

            img_data = next((item for item in data['data'] if item['url'] == output['url']), None)
            if img_data:
                data['data'][:] = [d for d in data['data'] if d.get('url') != img_data['url']]

            data['data'].append(output)
            with open(dataset_dir + 'dataset.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)

    context = {
        'sets': sets,
        'photo_num': img_num,
        'photo': 'labeling/img/' + photos[img_num],
    }

    img_data = next((item for item in data['data'] if item['url'] == context['photo']), None)
    if img_data:
        context['img_data'] = img_data

    return render(request, 'labeling/index.html', context)
