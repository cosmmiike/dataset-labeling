from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import os
import json


def labeling_view(request):
    img_dir = os.path.dirname(os.path.abspath(
        __file__)) + '/static/labeling/img'
    photos = [i for i in os.listdir(img_dir) if i.endswith('.jpg')]

    json_dir = os.path.dirname(os.path.abspath(__file__)) + '/static/labeling/json/'
    with open(json_dir + 'sets.json') as json_file:
        sets = json.load(json_file)
    sets_num = len(sets)
    set_titles = list(sets.keys())
    print(set_titles)
    with open(json_dir + 'dataset.json') as json_file:
        data = json.load(json_file)

    if request.POST:
        output = dict()
        output['url'] = request.POST.get('photo-url')
        for i in range(sets_num):
            output[set_titles[i]] = request.POST.get(set_titles[i] + '-radio')

        if None not in output.values():
            print(output)

            img_data = next((item for item in data['data'] if item['url'] == output['url']), None)
            if img_data:
                data['data'][:] = [d for d in data['data'] if d.get('url') != img_data['url']]

            data['data'].append(output)
            with open(json_dir + 'dataset.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)

    img_num = 0
    next_img = request.GET.get('id_photo')
    if next_img and int(next_img) < len(photos) - 1:
        if int(next_img) < 0:
            img_num = 0
        else:
            img_num = int(next_img)

    context = {
        'sets': sets,
        'photo_num': img_num,
        'photo': 'labeling/img/' + photos[img_num],
    }

    img_data = next((item for item in data['data'] if item['url'] == context['photo']), None)
    if img_data:
        context['img_data'] = img_data

    return render(request, 'labeling/index.html', context)
