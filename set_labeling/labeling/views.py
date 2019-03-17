from django.shortcuts import render

def labeling_view(request):
    photos = ['labeling/img/5.jpg']
    sets = {
        'frisure': ['lisses', 'ondulés', 'bouclés', 'frisés'],
        'couleur': ['noir', 'blonde', 'brun', 'roux'],
        'longeur': ['longues', 'mi-longues', 'courts', 'extra-courts'],
        'volume': ['volumineux', 'lâches', 'normaux'],

    }

    context = {
        'sets': sets,
        'photo': photos[0],
    }
    return render(request, 'labeling/index.html', context)
