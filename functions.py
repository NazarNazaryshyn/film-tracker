import os

import requests

# API_KEY = str(os.environ.get('API_KEY'))


def get_films(url):
    res = []
    response = requests.get(url)
    for card in response.json()['results']:
        try:
            title = card['title']
        except Exception as er:
            title = card['name']
        image = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2' + str(card['poster_path'])

        try:
            date = card['release_date'][:4]
        except Exception as er:
            date = card['first_air_date'][:4]
        id = card['id']
        vote = card['vote_average']

        res.append({
            'title': title,
            'image': image,
            'date': date,
            'id': int(id),
            'vote': str(vote)[:3]
        })

    return res


def find_film_by_id(id):

    response = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key=a267871a22077a6a1c13f4399b28887f').json()

    return {
            'title':response['original_title'],
            'image':'https://www.themoviedb.org/t/p/w600_and_h900_bestv2' + str(response['poster_path']),
            'date':response['release_date'][:4],
            'vote':str(response['vote_average'])[:3],
            'id':response['id']
        }


def search_movie(title):
    res = []
    response = requests.get(
        f'https://api.themoviedb.org/3/search/movie?api_key=a267871a22077a6a1c13f4399b28887f&'
        f'language=en-US&query={title}&page=1&include_adult=false')

    for card in response.json()['results']:
        try:
            title = card['title']
        except Exception as er:
            title = card['name']

        image = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2' + str(card['poster_path'])

        try:
            date = card['release_date'][:4]
        except Exception as er:
            date = card['first_air_date'][:4]
        id = card['id']
        vote = card['vote_average']

        res.append({
            'title': title,
            'image': image,
            'date': date,
            'id': int(id),
            'vote': str(vote)[:3]
        })

    return res


def form_url(query):
    url_dict = {
        'popular_this_week': '/trending/movie/week?api_key=',
        'popular_this_day': '/trending/movie/day?api_key=',
        'top_rated': '/movie/top_rated?api_key=',
        'on_the_air': '/movie/on_the_air?api_key=',
        'airing': '/movie/airing_today?api_key=',
    }

    if query.split('_')[-1] == 'serials':
        url = 'https://api.themoviedb.org/3' + url_dict[query[:-8]].replace('movie', 'tv') + f'a267871a22077a6a1c13f4399b28887f'
        print(url)
        return get_films(url)

    url = f'https://api.themoviedb.org/3' + url_dict[query] + f'a267871a22077a6a1c13f4399b28887f'
    print(url)

    return get_films(url)



