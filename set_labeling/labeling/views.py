from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import os
import json


def labeling_view(request):
    img_dir = os.path.dirname(os.path.abspath(
        __file__)) + '/static/labeling/img/hair/'
    photos = sorted([i for i in os.listdir(img_dir) if i.endswith('.jpg') or i.endswith('.jpg')])

    json_dir = os.path.dirname(os.path.abspath(__file__)) + '/static/labeling/json/'
    with open(json_dir + 'sets.json') as json_file:
        sets = json.load(json_file)
    sets_num = len(sets)
    set_titles = list(sets.keys())
    with open(json_dir + 'dataset.json') as json_file:
        data = json.load(json_file)

    if request.POST:
        output = dict()
        output['url'] = request.POST.get('photo-url')
        for i in range(sets_num):
            output[set_titles[i]] = request.POST.get(set_titles[i] + '-radio')

        if None not in output.values():

            img_data = next((item for item in data['data'] if item['url'] == output['url']), None)
            if img_data:
                data['data'][:] = [d for d in data['data'] if d.get('url') != img_data['url']]

            data['data'].append(output)
            with open(json_dir + 'dataset.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)

    img_num = 0
    next_img = request.GET.get('id_photo')
    if next_img and int(next_img) < len(photos):
        if int(next_img) < 0:
            img_num = len(photos) - 1
        else:
            img_num = int(next_img)

    context = {
        'sets': sets,
        'photo_num': img_num,
        'photo': 'labeling/img/hair/' + photos[img_num],
    }
    img_data = next((item for item in data['data'] if item['url'] == context['photo']), None)
    if img_data:
        context['img_data'] = img_data

    return render(request, 'labeling/index.html', context)


def stats_view(request):
    json_dir = os.path.dirname(os.path.abspath(__file__)) + '/static/labeling/json/'

    with open(json_dir + 'sets.json') as json_file:
        sets = json.load(json_file)

    sets_num = len(sets)
    set_titles = list(sets.keys())

    with open(json_dir + 'dataset.json') as json_file:
        data = json.load(json_file)

    data_num = len(data['data'])

    sets_output = dict()

    for title in set_titles:
        sets_output[title] = list()

        for i, set_class in enumerate(sets[title]):
            sets_output[title].append({})
            sets_output[title][i]['class_name'] = set_class

            count = 0
            for image in data['data']:
                if image[title] == str(i):
                    count += 1

            sets_output[title][i]['class_count'] = count

    context = dict()
    context['sets_output'] = sets_output

    return render(request, 'labeling/stats.html', context=context)
