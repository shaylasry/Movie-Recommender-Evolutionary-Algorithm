from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.ga_creators.bit_string_vector_creator import GABitStringVectorCreator
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
from eckity.genetic_operators.mutations.vector_random_mutation import BitStringVectorNFlipMutation
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.genetic_operators.selections.elitism_selection import ElitismSelection

from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation
from eckity.termination_checkers.threshold_from_target_termination_checker import ThresholdFromTargetTerminationChecker

from Movie import Movie
from api import MoviesApi
from prioritizedvectornpointmutation import PrioritizedVectorNPointMutation
from movieEvaluator import movieEvaluator
from vectorkpointscrossoverstrongestcross import VectorKPointsCrossoverStrongestCross

# 28 genres , languages to check, years from 1932 - 2022 jump of ten so we get 9 places -> 28 + 9 + 3 +language? = 40 + ?
# fitness categories:
# hard constrains : category ,langauge
# soft constrains : rating, year, runtime

MAX_GENERATION = 150


def main():
    lowerBoundGrade = 1.5
    movies = MoviesApi.loadMovies()
    numOfmovies = len(movies)
    finish_all = False
    while not finish_all:
        criterionsSize = {"genres": float, "language": float, "year": float, "timeInMinutes": float}
        print(
            "Please rate the importance of each criterion. Write for each criterion a number from 0 to 1, where the sum of all criteria together is 1.")
        finish = False

        while not finish:
            genres_rate = float(input("Enter your rate for genres criterion:"))
            language_rate = float(input("Enter your rate for language criterion:"))
            year_rate = float(input("Enter your rate for minimum publish year criterion:"))
            timeInMinutes_rate = float(input("Enter your rate for max length for a movie criterion:"))
            total_rate = genres_rate + language_rate + year_rate + timeInMinutes_rate

            if total_rate == 1.0:
                finish = True
                criterionsSize["genres"] = genres_rate
                criterionsSize["language"] = language_rate
                criterionsSize["year"] = year_rate
                criterionsSize["timeInMinutes"] = timeInMinutes_rate
            else:
                print("the sum of all criteria together is not 1! please try again")
                continue

        userRequest = {"genres": set(), "languages": set(), "year": None, "timeInMinutes": None}
        print("Hello! Enjoy our recommender!")
        print("Please choose your preferred genres from this list: (enter the key)")
        print(Movie.GENRES_MAP)
        finish = False
        while not finish:
            genres_choice = input("Enter the key of the genre, for finish enter 'finish'")
            finish = genres_choice == "finish"
            if finish and not userRequest["genres"]:
                print("You did not entered any genres! please try again")
                finish = False
                continue
            if not finish:
                userRequest["genres"].add(int(genres_choice))

        print("Please choose your preferred languages from this list: ")
        print(Movie.LANGUAGES)
        finish = False
        while not finish:
            languages_choice = input("Enter the language, for finish enter 'finish'")
            finish = languages_choice == "finish"
            if finish and not userRequest["languages"]:
                print("You did not entered any languages! please try again")
                finish = False
                continue
            if not finish:
                userRequest["languages"].add(languages_choice)

        userRequest['year'] = int(input("Please choose your minimum publish year: "))
        userRequest['timeInMinutes'] = int(input("Please choose your preferred max length for a movie (in minutes): "))

        moviesScores = grading_movies(movies, userRequest, criterionsSize)

        max_fitness = 0
        matched_movies = 0
        for movie_score in moviesScores:
            if (movie_score >= 1.5):
                max_fitness += movie_score
                matched_movies += 1
        print("max_fitness:" + str(max_fitness))
        print("matched_movies:" + str(matched_movies))
        threshold = 0.2 * max_fitness

        algo = SimpleEvolution(
            Subpopulation(creators=GABitStringVectorCreator(length=numOfmovies),
                          population_size=300,
                          # user-defined fitness evaluation method with the lower bound of matching criteria for each movie
                          evaluator=movieEvaluator(moviesScores, lowerBoundGrade),
                          # minimization problem (fitness is MAE), so higher fitness is worse
                          higher_is_better=True,
                          elitism_rate=5/300,
                          # genetic operators sequence to be applied in each generation
                          operators_sequence=[
                              # VectorKPointsCrossover(probability=0.5, arity=2, k=1),
                              VectorKPointsCrossoverStrongestCross(probability=0.5, arity=2, events=None, moviesScores=moviesScores,
                                                                   lowerBound=lowerBoundGrade),
                              PrioritizedVectorNPointMutation(probability=0.2, probability_for_each=0.02, n=numOfmovies, moviesScores=moviesScores, lowerBound=lowerBoundGrade)

                          ],
                          selection_methods=[
                              # (selection method, selection probability) tuple
                              (TournamentSelection(tournament_size=2, higher_is_better=True), 1)
                          ]
                          ),
            breeder=SimpleBreeder(),
            max_workers=4,
            max_generation=MAX_GENERATION,
            termination_checker=ThresholdFromTargetTerminationChecker(optimal=max_fitness, threshold=threshold),
            statistics=BestAverageWorstStatistics()
        )
        algo.evolve()
        result = algo.execute()
        if (result.count(1) < 1):
            print("Sadly, our recommender did not found enough recommendations for you..")
            print("Please try to change some of your choiceses, thank u")
            continue
        else:
            finish_all = True

    print("Our recommendations for you:")
    for i in range(len(movies)):
        if result[i]:
            print(str(i) + ". " + str(movies[i]))
    # print_results(algo.best_of_run_)
    # print(f'Run time: {end_time-start_time}s')


def grading_movies(movies, userRequest, criterionsSize):
    genreWeight = criterionsSize["genres"] / len(userRequest["genres"])
    moviesScores = []
    for movie in movies:
        score = 0
        # sum all match genres
        for genre in userRequest["genres"]:
            if genre in movie.genres:
                score += genreWeight

        # if one of the requested languages match add language score
        for language in userRequest["languages"]:
            if language in movie.language:
                score += criterionsSize["language"]
                break

        if userRequest["year"] <= movie.year:
            score += criterionsSize["year"]

        if userRequest["timeInMinutes"] >= movie.timeInMinutes:
            score += criterionsSize["timeInMinutes"]

        moviesScores.append(score + (movie.imdb_rank / 100))

    return moviesScores


if __name__ == '__main__':
    main()

#
# from eckity.algorithms.simple_evolution import SimpleEvolution
# from eckity.breeders.simple_breeder import SimpleBreeder
# from eckity.creators.ga_creators.bit_string_vector_creator import GABitStringVectorCreator
# from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
# from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
# from eckity.genetic_operators.mutations.vector_random_mutation import BitStringVectorNFlipMutation
# from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
# from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
# from eckity.subpopulation import Subpopulation
# from eckity.termination_checkers.threshold_from_target_termination_checker import ThresholdFromTargetTerminationChecker
#
# from Movie import Movie
# from api import MoviesApi
# from movieEvaluator import movieEvaluator
# #28 genres , languages to check, years from 1932 - 2022 jump of ten so we get 9 places -> 28 + 9 + 3 +language? = 40 + ?
# #fitness categories:
# #hard constrains : category ,langauge
# #soft constrains : rating, year, runtime
#
# MAX_GENERATION = 1000
#
#
# def main():
#     lowerBoundGrade = 1.5
#     movies = MoviesApi.loadMovies()
#     numOfmovies = len(movies)
#     userRequest = {"genres": set(), "languages": set(), "year": None, "timeInMinutes": None}
#     print("Hello user, enjoy your Netflix & Chill!!")
#     print("Please choose your preferred genres from this list: (enter the key)")
#     print(Movie.GENRES_MAP)
#     finish = False
#     while not finish:
#         genres_choice = input("Enter the key of the genre, for finish enter 'finish'")
#         finish = genres_choice == "finish"
#         if finish and not userRequest["genres"]:
#             print("You did not entered any genres! please try again")
#             finish = False
#             continue
#         if not finish:
#             userRequest["genres"].add(int(genres_choice))
#
#     print("Please choose your preferred languages from this list: ")
#     print(Movie.LANGUAGES)
#     finish = False
#     while not finish:
#         languages_choice = input("Enter the language, for finish enter 'finish'")
#         finish = languages_choice == "finish"
#         if finish and not userRequest["languages"]:
#             print("You did not entered any languages! please try again")
#             finish = False
#             continue
#         if not finish:
#             userRequest["languages"].add(languages_choice)
#
#     userRequest['year'] = int(input("Please choose your minimum publish year: "))
#     userRequest['timeInMinutes'] = int(input("Please choose your preferred max length for a movie (in minutes): "))
#
#     moviesScores = grading_movies(movies, userRequest)
#
#     print(movies)
#     print(moviesScores)
#
#     algo = SimpleEvolution(
#         Subpopulation(creators=GABitStringVectorCreator(length=numOfmovies),
#                       population_size=300,
#                       # user-defined fitness evaluation method with the lower bound of matching criteria for each movie
#                       evaluator=movieEvaluator(moviesScores, lowerBoundGrade),
#                       # minimization problem (fitness is MAE), so higher fitness is worse
#                       higher_is_better=True,
#                       # TODO - Check what is elitism_rate
#                       elitism_rate=0.10,
#                       # genetic operators sequence to be applied in each generation
#                       operators_sequence=[
#                           VectorKPointsCrossover(probability=0.5, k=1),
#                           BitStringVectorNFlipMutation(probability=0.2, probability_for_each=0.05, n=numOfmovies)
#                       ],
#                       selection_methods=[
#                           # (selection method, selection probability) tuple
#                           (TournamentSelection(tournament_size=3, higher_is_better=True), 1)
#                       ]
#                       ),
#         breeder=SimpleBreeder(),
#         max_workers=4,
#         max_generation=MAX_GENERATION,
#         # termination_checker=ThresholdFromTargetTerminationChecker(optimal=1000, threshold=0.0),
#         statistics=BestAverageWorstStatistics()
#     )
#     algo.evolve()
#     # end_time = time()
#     result = algo.execute()
#     for i in range(len(movies)):
#         if result[i]:
#             print(str(i) + ". " + str(movies[i]))
#     # print_results(algo.best_of_run_)
#     # print(f'Run time: {end_time-start_time}s')
#
#
# def grading_movies(movies, userRequest):
#     criterionsSize = {"genres": 0.60, "language": 0.20, "year": 0.10, "timeInMinutes": 0.10}
#     genreWeight = criterionsSize["genres"] / len(userRequest["genres"])
#     moviesScores = []
#     for movie in movies:
#         score = 0
#         #sum all match genres
#         for genre in userRequest["genres"]:
#             if genre in movie.genres:
#                 score += genreWeight
#
#         #if one of the requested languages match add language score
#         for language in userRequest["languages"]:
#             if language in movie.language:
#                 score += criterionsSize["language"]
#                 break
#
#         if userRequest["year"] <= movie.year:
#             score += criterionsSize["year"]
#
#         if userRequest["timeInMinutes"] >= movie.timeInMinutes:
#             score += criterionsSize["timeInMinutes"]
#
#         moviesScores.append(score + movie.imdb_rank/100)
#
#     return moviesScores
#
#
# if __name__ == '__main__':
#     main()
#
