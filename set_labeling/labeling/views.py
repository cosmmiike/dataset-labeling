from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import os
import shutil
import json
import re


def sort_nicely(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    l.sort(key=alphanum_key)
    return l


@login_required
def labeling_view(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    static_dir = os.path.dirname(os.path.abspath(__file__)) + '/static'

    tmp_dir = static_dir + '/labeling/users/' + username + '/tmp/'
    with open(tmp_dir + 'settings.json') as json_file:
        settings = json.load(json_file)

    classes_json = static_dir + settings['classes']
    with open(classes_json) as json_file:
        classes = json.load(json_file)

    classes_num = len(classes)
    classes_titles = list(classes.keys())

    annotations_json = static_dir + settings['annotations']
    with open(annotations_json) as json_file:
        annotations = json.load(json_file)

    removed_json = os.path.dirname(annotations_json) + '/removed.json'
    if os.path.exists(removed_json):
        with open(removed_json) as json_file:
            removed = json.load(json_file)
        removed_images = removed['images']
    else:
        removed_images = list()

    dataset_dir = static_dir + settings['dataset']
    dataset = sort_nicely([i for i in os.listdir(dataset_dir) if i not in removed_images and (i.endswith('.jpg') or i.endswith('.png') or i.endswith('.jpeg'))])

    if request.POST:
        output = dict()
        output['name'] = request.POST.get('photo-name')
        for i in range(classes_num):
            output[classes_titles[i]] = request.POST.get(classes_titles[i] + '-radio')

        if None not in output.values():
            img_data = next((item for item in annotations['data'] if item['name'] == output['name']), None)
            if img_data:
                annotations['data'][:] = [d for d in annotations['data'] if d.get('name') != img_data['name']]

            annotations['data'].append(output)
            with open(annotations_json, 'w') as outfile:
                json.dump(annotations, outfile, indent=4)

    img_num = 0
    next_img = request.GET.get('id_photo')
    if next_img and int(next_img) < len(dataset):
        if int(next_img) < 0:
            img_num = len(dataset) - 1
        else:
            img_num = int(next_img)

    context = {
        'username': username,
        'sets': classes,
        'photo_num': img_num,
        'photo_url': settings['dataset'] + dataset[img_num],
        'photo_name': dataset[img_num],
    }

    img_data = next((item for item in annotations['data'] if item['name'] == context['photo_name']), None)
    if img_data:
        context['img_data'] = img_data

    return render(request, 'labeling/index.html', context)


@login_required
def remove_view(request):
    if request.GET:
        username = None
        if request.user.is_authenticated:
            username = request.user.username

        static_dir = os.path.dirname(os.path.abspath(__file__)) + '/static'

        tmp_dir = static_dir + '/labeling/users/' + username + '/tmp/'
        with open(tmp_dir + 'settings.json') as json_file:
            settings = json.load(json_file)

        annotations_json = static_dir + settings['annotations']
        with open(annotations_json) as json_file:
            annotations = json.load(json_file)

        removed_json = os.path.dirname(annotations_json) + '/removed.json'
        if os.path.exists(removed_json):
            with open(removed_json) as json_file:
                removed = json.load(json_file)
            removed_images = removed['images']
        else:
            removed_images = list()

        dataset_dir = static_dir + settings['dataset']
        dataset = sort_nicely([i for i in os.listdir(dataset_dir) if i not in removed_images and (i.endswith('.jpg') or i.endswith('.png') or i.endswith('.jpeg'))])

        image_id = int(request.GET.get('id_photo'))

        img_data = next((item for item in annotations['data'] if item['name'] == dataset[image_id]), None)
        if img_data:
            annotations['data'][:] = [a for a in annotations['data'] if a.get('name') != img_data['name']]
            with open(annotations_json, 'w') as outfile:
                json.dump(annotations, outfile, indent=4)

        removed_images.append(dataset[image_id])
        removed = dict()
        removed['images'] = removed_images

        with open(removed_json, 'w') as outfile:
            json.dump(removed, outfile, indent=4)

        return HttpResponseRedirect('/?id_photo=' + str(image_id))
    return HttpResponseRedirect('/')


@login_required
def stats_view(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    static_dir = os.path.dirname(os.path.abspath(__file__)) + '/static'

    tmp_dir = static_dir + '/labeling/users/' + username + '/tmp/'
    with open(tmp_dir + 'settings.json') as json_file:
        settings = json.load(json_file)

    classes_json = static_dir + settings['classes']
    with open(classes_json) as json_file:
        classes = json.load(json_file)

    classes_num = len(classes)
    classes_titles = list(classes.keys())

    annotations_json = static_dir + settings['annotations']
    with open(annotations_json) as json_file:
        annotations = json.load(json_file)

    classes_output = dict()
    for title in classes_titles:
        classes_output[title] = list()

        for i, class_title in enumerate(classes[title]):
            classes_output[title].append({})
            classes_output[title][i]['class_name'] = class_title

            count = 0
            for image in annotations['data']:
                if image[title] == str(i):
                    count += 1

            classes_output[title][i]['class_count'] = count

    context = dict()
    context['sets_output'] = classes_output

    return render(request, 'labeling/stats.html', context=context)


@login_required
def sort_view(request):
    # json_dir = os.path.dirname(os.path.abspath(__file__)) + '/static/labeling/json/'
    # img_dir = os.path.dirname(os.path.abspath(
    #     __file__)) + '/static/labeling/default/digital_hair_care/img/raw/'
    #
    # with open(json_dir + 'sets.json') as json_file:
    #     sets = json.load(json_file)
    #
    # with open(json_dir + 'dataset.json') as json_file:
    #     data = json.load(json_file)
    #
    # sorted_dir = os.path.exists(img_dir + '../sorted/')
    # if not sorted_dir:
    #     os.makedirs(img_dir + '../sorted/')
    #
    # sets_num = len(sets)
    # set_titles = list(sets.keys())
    #
    # for title in set_titles:
    #     dir = img_dir + '../sorted/' + title + '/'
    #     exists_dir = os.path.exists(dir)
    #     if exists_dir:
    #         shutil.rmtree(dir)
    #     os.makedirs(dir)
    #     print(sets[title])
    #
    #     for i, set_class in enumerate(sets[title]):
    #         class_dir = dir + str(i) + '/'
    #         exists_class_dir = os.path.exists(class_dir)
    #         os.makedirs(class_dir)
    #         image_url = data['data'][0]['name']
    #
    #         for image in data['data']:
    #             if image[title] == str(i):
    #                 print(image[title], set_class, image['name'])
    #                 image_fullpath = os.path.dirname(os.path.abspath(
    #                     __file__)) + '/static/' + image['name']
    #                 shutil.copy2(image_fullpath, class_dir)

    return stats_view(request)
