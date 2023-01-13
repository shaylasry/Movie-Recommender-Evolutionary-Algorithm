import matplotlib.pyplot as plt
import csv

# opening the CSV file
with open('output.csv', mode='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)

    # creating empty lists
    generation_list = []
    fitness_list = []

    # iterating over each row and append
    # values to empty list
    for row in file:
        row = row.split(",")
        generation_list.append(int(row[0]))
        fitness_list.append(float(row[4]))

    plt.plot(generation_list, fitness_list)
    plt.xlabel('generation')
    plt.ylabel('fitness ')
    plt.title('Average Fitness')

    plt.show()

