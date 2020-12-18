import os.path
import nashpy as nash
import numpy as np
import csv
import random
import time

# Set random seed
np.random.rand(1)

start = time.perf_counter()

# Create the CSV file with parameters and payoffs

filename = 'payoff_R_W_equal.csv'
file_exists = os.path.isfile(filename)

# N is the number of times the experiment is run

N = 10000


# generate parameters for the game


def create_combination_parameters_random():
    global pQ, pL, pT, c, W, R
    pQ = 1
    pT = 0.5
    pL = random.uniform(0, 1)
    c = random.randint(1, 50)
    W = random.randint(0, 100)
    R = W
    return


# Function to write a csv file with parameters and nash equilibrium

def write(pT, W, R, pL, c, pQ, R1, R2, Equilibriums):
    with open(filename, 'a', newline='') as csvfile:
        global Strategy_Played
        global Strategy
        Strategy_Played = []
        Strategy = []
        Number_Eqs = len(Equilibriums) / 2

        try:
            eq_exists = len(Equilibriums) > 0
        except:
            eq_exists = False
            Strategy_Played = "NULL"
            Strategy = "NA"
        if Number_Eqs == 1:
            if Equilibriums[0][0] == 1 and Equilibriums[0][1] == 0:
                Strategy_Played = "Guess"
                Strategy = 0
            else:
                Strategy_Played = "Review"
                Strategy = 1
        elif Number_Eqs > 1:
            Strategy_Played = "Not_Unique"
            Strategy = 2

        dict_params = {
            'pT': pT,
            'W': W,
            'R': R,
            'pL': pL,
            'c': c,
            'pL*c': (pL * c),
            'pQ': pQ,
            'R1_array': R1,
            'R2_array': R2,
            'Max_R1_Payoff': max(max(R1)),
            'Max_R2_Payoff': max(max(R2)),
            'Max_Payoff': np.max(np.concatenate((R1, R2))),
            'Eq': Equilibriums,
            'Number_Eqs': (len(Equilibriums) / 2),
            'Strategy_Name': Strategy_Played,
            'Strategy': Strategy
        }

        w = csv.DictWriter(csvfile, dict_params.keys())
        if csvfile.tell() == 0:
            w.writeheader()

        w.writerow(dict_params)


# Functions to define payoff using guess and review strategy

# calculate payoff from guess strategy

def guess(pT, R, W):
    return np.round(
        ((1 - pT) * 0.5 * R) +
        (pT * 0.5 * W)
        , 2)


# calculate payoff from review strategy

def review(pT, pQ, R, W, pL, c):
    return np.round(
        (1 - pT) * 0.5 * R +
        pT * pQ * W +
        pT * (1 - pQ) * 0.5 * W -
        pL * c
        , 2)


# calculate payoff when both do review

def both_review(pT, pQ, R, W, pL, c):
    return np.round(
        ((1 - pT) * pow(pQ, 2) * R) +
        (2 * pQ * (1 - pQ) * 0.5 * R) +
        (pow((1 - pQ), 2) * 0.5 * R) +
        (pT * pQ * W) +
        (pT * (1 - pQ) * 0.5 * W) -
        (pL * c)
        , 2)


# calculate payoff matrices and Nash equilibrium

R1_array = []
R2_array = []


def calculate_eq(R1_array, R2_array):
    rating_game = nash.Game(R1_array, R2_array)
    print(rating_game)
    eqs = rating_game.vertex_enumeration()
    print(list(eqs))

    Eq = []
    for eq in rating_game.vertex_enumeration():
        Eq.append(np.round(eq[0], 2))
        Eq.append(np.round(eq[1], 2))

    write(pT, W, R, pL, c, pQ, R1_array, R2_array, Eq)
    return


# Calculate Nash equilibrium for Review Game with combination of random parameters


for i in range(N):
    create_combination_parameters_random()
    R2_array = [[guess(pT, R, W), review(pT, pQ, R, W, pL, c)],
                [guess(pT, R, W), both_review(pT, pQ, R, W, pL, c)]]
    R1_array = [[guess(pT, R, W), guess(pT, R, W)],
                [review(pT, pQ, R, W, pL, c), both_review(pT, pQ, R, W, pL, c)]]

    calculate_eq(R1_array, R2_array)

# Time to complete the steps

finish = time.perf_counter()

print(f'Finished in {round(finish - start, 2)} seconds')
