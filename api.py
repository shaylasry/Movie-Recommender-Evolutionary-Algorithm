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
        "X-RapidAPI-Key": "ccaf10462cmsh2b3ce0a88004f5dp19c27cjsn1044a7006e1b",
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
    }

    @staticmethod
    def loadFromJson():
        try:
            with open('db.json', 'r') as openfile:
                # Reading from json file
                json_object = json.load(openfile)
                Movie.setGenres(json_object['genres'])
                movies = []
                for movie_data in json_object['movies']:
                    movies.append(Movie(movie_data['genres'],
                                        movie_data['originalLanguage'],
                                        movie_data['runtime'],
                                        movie_data['year'],
                                        movie_data['originalTitle'],
                                        movie_data['imdbRating']))
                return movies
        except:
            return False

    @staticmethod
    def loadFromApi():
        numOfPages = 70
        movies_raw = []
        for page in range(20, 20 + numOfPages + 1):
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

        return {'movies': movies, 'movies_raw': movies_raw}

    @staticmethod
    def loadMovies():
        movies = MoviesApi.loadFromJson()
        if not movies:
            movies_arr = MoviesApi.loadFromApi()
            movies = movies_arr['movies']
            MoviesApi.saveToJson(movies_arr['movies_raw'])
        return movies

    @classmethod
    def saveToJson(cls, movies):
        movies_dict = {"genres": Movie.GENRES_MAP, "movies": movies}
        json_obj = json.dumps(movies_dict, indent=4)
        with open("db.json", "w") as outfile:
            outfile.write(json_obj)

