import requests
import json
# first option - get movies by fitness from start,


# response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=90400376f2b7af3b89798cf44ac80723')
# print(response.status_code)
# print(response.json())
from Movie import Movie


class MoviesApi:
    url = "https://streaming-availability.p.rapidapi.com/search/basic"
    genres_url = "https://streaming-availability.p.rapidapi.com/genres"
    countries_url = "https://streaming-availability.p.rapidapi.com/countries"


    # querystring = {"country":"il","service":"netflix","type":"movie","page":{}.format(i),"output_language":"en","language":"en"}

    headers = {
        "X-RapidAPI-Key": 'c922141b9dmshedfa6dc0b3ebdb6p1ca41ejsn13bafd7188ba',
        'X-RapidAPI-Host': 'streaming-availability.p.rapidapi.com'
    }

    @staticmethod
    def loadMovies():
        numOfPages = 25
        movies_raw = []
        for page in range(20, numOfPages + 1):
            querystring = {"country": "il", "service": "netflix", "type": "movie", "page": "{}".format(page)}
            getMovies = requests.request("GET", MoviesApi.url, headers=MoviesApi.headers, params=querystring)
            movies_raw = movies_raw + getMovies.json()['results']

        print(len(movies_raw))

        movies = []

        for movie in movies_raw:
            movies.append(Movie(movie['genres'],
                                movie['originalLanguage'],
                                movie['runtime'],
                                movie['year'],
                                movie['originalTitle'],
                                movie['imdbRating']))

        # title
        # originalTitle
        # overview
        # age
        # originalLanguage
        # runtime
        # genres
        # countries
        # imdbRating

        # get all the posibble geners and print it
        getGenres = requests.request("GET", MoviesApi.genres_url, headers=MoviesApi.headers)
        genres = getGenres.json()
        Movie.setGenres(genres)

        # for key in movies_map:
        #     print(movies_map[key])

        return movies

