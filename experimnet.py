
from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.ga_creators.bit_string_vector_creator import GABitStringVectorCreator
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
from eckity.genetic_operators.mutations.vector_random_mutation import BitStringVectorNFlipMutation
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation
from eckity.termination_checkers.threshold_from_target_termination_checker import ThresholdFromTargetTerminationChecker

from Movie import Movie
from api import MoviesApi
from movieEvaluator import movieEvaluator
#28 genres , languages to check, years from 1932 - 2022 jump of ten so we get 9 places -> 28 + 9 + 3 +language? = 40 + ?
#fitness categories:
#hard constrains : category ,langauge
#soft constrains : rating, year, runtime

MAX_GENERATION = 500


def main():
    movies = MoviesApi.loadMovies()
    numOfmovies = len(movies)
    userRequest = {"genres": set(), "languages": set(), "year": None, "timeInMinutes": None}
    print("Hello user, enjoy your Netflix & Chill!!")
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

    moviesScores = grading_movies(movies, userRequest)

    print(movies)
    print(moviesScores)

    algo = SimpleEvolution(
        Subpopulation(creators=GABitStringVectorCreator(length=numOfmovies),
                      population_size=400,
                      # user-defined fitness evaluation method with the lower bound of matching criteria for each movie
                      evaluator=movieEvaluator(moviesScores, 0.90),
                      # minimization problem (fitness is MAE), so higher fitness is worse
                      higher_is_better=True,
                      # TODO - Check what is elitism_rate
                      elitism_rate=1 / 400,
                      # genetic operators sequence to be applied in each generation
                      operators_sequence=[
                          VectorKPointsCrossover(probability=0.5, k=1),
                          BitStringVectorNFlipMutation(probability=0.2, probability_for_each=0.05, n=numOfmovies)
                      ],
                      selection_methods=[
                          # (selection method, selection probability) tuple
                          (TournamentSelection(tournament_size=3, higher_is_better=True), 1)
                      ]
                      ),
        breeder=SimpleBreeder(),
        max_workers=4,
        max_generation=MAX_GENERATION,
        # termination_checker=ThresholdFromTargetTerminationChecker(optimal=1000, threshold=0.0),
        statistics=BestAverageWorstStatistics()
    )
    algo.evolve()
    # end_time = time()
    result = algo.execute()
    for i in range(len(movies)):
        if result[i]:
            print(str(i) + ". " + str(movies[i]))
    # print_results(algo.best_of_run_)
    # print(f'Run time: {end_time-start_time}s')


def grading_movies(movies, userRequest):
    criterionsSize = {"genres": 0.60, "language": 0.20, "year": 0.10, "timeInMinutes": 0.10}
    genreWeight = criterionsSize["genres"] / len(userRequest["genres"])
    moviesScores = []
    for movie in movies:
        score = 0
        #sum all match genres
        for genre in userRequest["genres"]:
            if genre in movie.genres:
                score += genreWeight
        
        #if one of the requested languages match add language score
        for language in userRequest["languages"]:
            if language in movie.language:
                score += criterionsSize["language"]
                break
        
        if userRequest["year"] <= movie.year:
            score += criterionsSize["year"]
        
        if userRequest["timeInMinutes"] >= movie.timeInMinutes:
            score += criterionsSize["timeInMinutes"]

        moviesScores.append(score + movie.imdb_rank/100)

    return moviesScores


if __name__ == '__main__':
    main()

