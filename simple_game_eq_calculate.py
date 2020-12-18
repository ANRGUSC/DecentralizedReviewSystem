import nashpy as nash
import numpy as np

# Parameters

pF = 0.5  # probablity of test/fake product
R = 400  # Reward
W = 400  # Reward for passing test
pL = 1  # probability of laziness (close to 1 means very lazy)
# pF close to 0 means real product, whereas close to 1 translates to a fake product
c = 25  # Cost for the review
pQ = 1  # probability of high quality (close to 1 means very high quality)


# calculate random guess
def guess(pF, R, W):
    return np.round(((1 - pF) * 0.5 * R) + (pF * 0.5 * W), 2)


# # calculate correct review

def review(pF, pQ, R, W, pL, c):
    return np.round(
                    (1-pF) * 0.5 * R +
                    pF * pQ * W +
                    pF * (1 - pQ) * 0.5 * W -
                    pL * c
    ,2)

# calculate payoff when both do correct review
def both_review(pF, pQ, R, W, pL, c):
    return np.round(
            ((1 - pF) * pow(pQ, 2) * R) +
            (2 * pQ * (1 - pQ) * 0.5 * R) +
            (pow((1 - pQ), 2) * 0.5 * R) +
            (pF * pQ * W) +
            (pF * (1 - pQ) * 0.5 * W) -
            (pL * c)
    ,2)


R1_array = []
R2_array = []

R1_array = [[guess(pF, R, W), review(pF, pQ, R, W, pL, c)],
            [guess(pF, R, W), both_review(pF, pQ, R, W, pL, c)]]
R2_array = [[guess(pF, R, W), guess(pF, R, W)],
            [review(pF, pQ, R, W, pL, c), both_review(pF, pQ, R, W, pL, c)]]

print(R1_array)
print(R2_array)

rating_game = nash.Game(R2_array, R1_array)
print(rating_game)

# R1_sigma=[1,0]
# R2_sigma=[0,1]

# rating_game[R1_sigma,R2_sigma]

# eqs = rating_game.support_enumeration(non_degenerate=True)
eqs = rating_game.vertex_enumeration()
print(list(eqs))


for eq in rating_game.vertex_enumeration():
    print(np.round(eq[0], 2), np.round(eq[1], 2))
