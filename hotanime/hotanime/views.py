from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .model import Engine
engine = Engine()


def index(request):
    episodes = engine.get_episode_homePage(max=40)
    ongoing = engine.get_onGoing(max=30)
    return render(request, "index.html", {'episodes': episodes, 'onGoing': ongoing,'header':'Watch Anime Online Free | globalanime.com'})


def detail(request, slug):
    response = engine.check_slug(slug)
    response['info']['averageScore']/= 10
    #Converting dates
    if response['info']['start_date'] == None:
        response['info']['start_date'] = '?'
    else:
        response['info']['start_date'] = response['info']['start_date'].strftime('%b %d, %Y')
        
    if response['info']['end_date'] == None:
        response['info']['end_date'] = '?'
    else:
        response['info']['end_date'] = response['info']['end_date'].strftime('%b %d, %Y')
    # Displayed Episodes
    for episode in response['episodes']:
        try:
            episode['episodeDisplay'] = int(episode['episode'])
        except:
            episode['episodeDisplay'] = episode['episode']
    return render(request, "detail.html", {'info': response['info'], 'episodes': response['episodes'][::-1], 'genres': response['genres']})

def watch(request,episode):
    response = engine.get_episode_servers(episode)
    #return JsonResponse(response)
    return render(request, "watch.html",
                  {'episode': response['episode'],
                   'anime_url':response['anime_url'],
                   'last':response['last'],
                   'next':response['next'],
                   'loweredName':response['loweredName']
                   })

def anime_list(request):
    animes = engine.get_anime_list(page=0)
    pages = engine.get_total_pages()
    header = engine.get_header_title(request.META['PATH_INFO'])
    print(header)
    #return JsonResponse({'animes':animes,'pages':pages})
    return render(request, "animelist.html", {'animes':animes,'totalPages':pages,'page':1,'next':2,'header':header})
def anime_list_pagination(request,page):
    try:
        page = int(page)
    except:
        pass
    animes = engine.get_anime_list(page=page)
    header = engine.get_header_title(request.META['PATH_INFO'])
    pages = engine.get_total_pages()
    print(pages)
    return render(request, "animelist.html", {'animes':animes,'pages':pages,'header':header,'page':page,'next':page+1,'totalPages':pages})
    