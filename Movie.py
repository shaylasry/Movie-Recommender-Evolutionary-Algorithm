class Movie:
    GENRES_MAP = dict()
    LANGUAGES = set()

    def __init__(self, genres, language, timeInMinutes, year, title, imdb_rank):
        self.genres = genres
        self.language = language
        Movie.LANGUAGES.add(self.language)
        self.timeInMinutes = timeInMinutes
        self.year = year
        self.title = title
        self.imdb_rank = imdb_rank

    def __str__(self):
        return "Movie title: " + self.title + \
               "\nGenres: " + str(self.genres) + "\nLanguage: " + self.language + "\nTime in minutes: " + str(self.timeInMinutes) + "\nYear: " + str(self.year) + "\nIMDB ranking: " + str(self.imdb_rank)

    @staticmethod
    def setGenres(genres):
        Movie.GENRES_MAP = genres

