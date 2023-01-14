import json

from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.ga_creators.bit_string_vector_creator import GABitStringVectorCreator
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
from eckity.genetic_operators.mutations.vector_n_point_mutation import VectorNPointMutation
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


MAX_GENERATION = 300


def main():
    lower_bound_grade = 1.5
    movies = MoviesApi.loadMovies()
    num_of_movies = len(movies)
    finish_all = False

    while not finish_all:
        movies_scores = get_user_req_and_generate_movie_scores(movies)
        max_fitness = 0
        matched_movies = 0
        for movie_score in movies_scores:
            if movie_score >= lower_bound_grade:
                max_fitness += movie_score
                matched_movies += 1
        # print("max_fitness:" + str(max_fitness))
        # print("matched_movies:" + str(matched_movies))
        threshold = 0.2 * max_fitness

        algo = SimpleEvolution(
            Subpopulation(creators=GABitStringVectorCreator(length=num_of_movies),
                          population_size=300,
                          # user-defined fitness evaluation method with the lower bound of matching criteria for each movie
                          evaluator=movieEvaluator(movies_scores, lower_bound_grade),
                          # minimization problem (fitness is MAE), so higher fitness is worse
                          higher_is_better=True,
                          elitism_rate=5/300,
                          # genetic operators sequence to be applied in each generation
                          operators_sequence=[
                              # VectorKPointsCrossover(probability=0.5, k=1),
                              VectorKPointsCrossoverStrongestCross(probability=0.5, arity=2, events=None, moviesScores=movies_scores,
                                                                   lowerBound=lower_bound_grade),
                              # BitStringVectorNFlipMutation(probability=0.2, probability_for_each=0.05, n=num_of_movies)
                              PrioritizedVectorNPointMutation(probability=0.2, probability_for_each=0.02, n=num_of_movies, moviesScores=movies_scores, lowerBound=lower_bound_grade)
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
        if result.count(1) < 1:
            print("Sadly, our recommender did not found enough recommendations for you..")
            print("Please try to change some of your choiceses, thank u")
            continue
        else:
            finish_all = True

    print("Our recommendations for you:")
    rec = []
    for i in range(len(movies)):
        if result[i]:
            print(str(i) + ". " + movies[i].title)
            rec.append(movies[i].json())
    print("total movies in db: " + str(len(movies)))
    print("recommended movies in db: " + str(len(rec)))
    json_res = json.dumps({"results": rec}, indent=4)
    with open("results.json", "w") as outfile:
        outfile.write(json_res)






def get_user_req_and_generate_movie_scores(movies):
    criterionsSize = {"genres": float, "language": float, "year": float, "timeInMinutes": float}
    print(
        "Please rate the importance of each criterion. "
        "Write for each criterion a number from 0 to 1, where the sum of all criteria together is 1.")
    finish = "y" == str(input("Do you want to use our recommendation for it? y/n"))

    if finish:
        criterionsSize["genres"] = 0.6
        criterionsSize["language"] = 0.2
        criterionsSize["year"] = 0.1
        criterionsSize["timeInMinutes"] = 0.1

    while not finish:
        genres_rate = float(input("Enter your rate for genres criterion:"))
        language_rate = float(input("Enter your rate for language criterion:"))
        year_rate = float(input("Enter your rate for minimum publish year criterion:"))
        time_in_minutes_rate = float(input("Enter your rate for max length for a movie criterion:"))
        total_rate = genres_rate + language_rate + year_rate + time_in_minutes_rate

        if total_rate == 1.0:
            finish = True
            criterionsSize["genres"] = genres_rate
            criterionsSize["language"] = language_rate
            criterionsSize["year"] = year_rate
            criterionsSize["timeInMinutes"] = time_in_minutes_rate
        else:
            print("the sum of all criteria together is not 1! please try again")
            continue

    user_request = {"genres": set(), "languages": set(), "year": None, "timeInMinutes": None}
    print("Hello! Enjoy our recommender!")
    print("Please choose your preferred genres from this list: (enter the key)")
    for m in list(Movie.GENRES):
        print(str(m) + ". " + Movie.GENRES_MAP[str(m)])

    finish = False
    while not finish:
        genres_choice = input("Enter the key of the genre, for finish enter 'finish'")
        finish = genres_choice == "finish"
        if finish and not user_request["genres"]:
            print("You did not entered any genres! please try again")
            finish = False
            continue
        if not finish:
            user_request["genres"].add(int(genres_choice))

    print("Please choose your preferred languages from this list: ")
    print(Movie.LANGUAGES)
    finish = False
    while not finish:
        languages_choice = input("Enter the language, for finish enter 'finish'")
        finish = languages_choice == "finish"
        if finish and not user_request["languages"]:
            print("You did not entered any languages! please try again")
            finish = False
            continue
        if not finish:
            user_request["languages"].add(languages_choice)

    user_request['year'] = int(input("Please choose your minimum publish year: "))
    user_request['timeInMinutes'] = int(input("Please choose your preferred max length for a movie (in minutes): "))

    return grading_movies(movies, user_request, criterionsSize)


def grading_movies(movies, user_request, criterions_size):
    genre_weight = criterions_size["genres"] / len(user_request["genres"])
    movies_scores = []
    for movie in movies:
        score = 0
        # sum all match genres
        for genre in user_request["genres"]:
            if genre in movie.genres:
                score += genre_weight

        # if one of the requested languages match add language score
        for language in user_request["languages"]:
            if language in movie.language:
                score += criterions_size["language"]
                break

        if user_request["year"] <= movie.year:
            score += criterions_size["year"]

        if user_request["timeInMinutes"] >= movie.timeInMinutes:
            score += criterions_size["timeInMinutes"]

        movies_scores.append(score + (movie.imdb_rank / 100))

    return movies_scores


if __name__ == '__main__':
    main()
