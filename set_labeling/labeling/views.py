from django.shortcuts import render

def labeling_view(request):
    photos = ['labeling/img/5.jpg']
    sets = {
        'textures': ['lisses', 'ondulés', 'bouclés', 'frisés'],
        'colors': ['noir', 'blonde', 'brun', 'roux'],
        'lengths': ['longues', 'mi-longues', 'courts'],
        'volumes': ['volumineux', 'lâches', 'normaux'],
    }

    context = {
        'sets': sets,
        'photo': photos[0],
    }
    return render(request, 'labeling/index.html', context)
