import numpy as np
from matplotlib import pyplot as plt

# constant values
m1_data = np.array([0.09, 0.17, 0.28, 0.32, 0.35, 0.41])
M1_data = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
m2_data = 1.0 - m1_data
M2_data = 1.0 - M1_data
R1_init = 0.8
R2_init = 0.1
iters = 10000
alpha = 0.01

def G_numerator(M1, M2, R2):
    return R2 * np.square(M2) + np.multiply(M2, M1)


def G_denominator(M1, M2, R1, R2):
    return R2 * np.square(M2) + 2 * np.multiply(M1, M2) + R1 * np.square(M1)


def G(M1, M2, R1, R2):
    return G_numerator(M1, M2, R2) / G_denominator(M1, M2, R1, R2)


def COST(m2, M1, M2, R1, R2):
    return (1 / (2 * M1.shape[0])) * np.sum(np.square(m2 - G(M1, M2, R1, R2)))


def dGdR1(M1, M2, R1, R2):
    return -1 * G_numerator(M1, M2, R2) * np.square(M1) / np.square(G_denominator(M1, M2, R1, R2))


def dGdR2(M1, M2, R1, R2):
    return np.square(M2) * (G_denominator(M1, M2, R1, R2) - G_numerator(M1, M2, R2)) / np.square(G_denominator(M1, M2, R1, R2))


def dCOSTdR1(m2, M1, M2, R1, R2):
    return (1 / M1.shape[0]) * np.sum(np.multiply(G(M1, M2, R1, R2) - m2, dGdR1(M1, M2, R1, R2)))


def dCOSTdR2(m2, M1, M2, R1, R2):
    return (1 / M1.shape[0]) * np.sum(np.multiply(G(M1, M2, R1, R2) - m2, dGdR2(M1, M2, R1, R2)))


# plot results data
def visualize(costs, R1s, R2s):
    # plot costs
    plt.subplot(1, 3, 1)
    plt.plot(costs, 'r*')
    plt.ylabel("Cost Value")
    plt.xlabel("# Iterations")
    plt.title("Cost vs Iterations")
    # plot R1s
    plt.subplot(1, 3, 2)
    plt.plot(R1s, 'r*')
    plt.ylabel("R1 Value")
    plt.xlabel("# Iterations")
    plt.title("R1 vs Iterations")
    # plot R2s
    plt.subplot(1, 3, 3)
    plt.plot(R2s, 'r*')
    plt.ylabel("R2 Value")
    plt.xlabel("# Iterations")
    plt.title("R2 vs Iterations")
    plt.show()


# core gradient descent implementation
def gradient_descent():
    print("starting gradient descent optimization")
    R1 = R1_init
    R2 = R2_init
    costs = np.zeros(iters)
    R1s = np.zeros(iters)
    R2s = np.zeros(iters)
    for i in range(iters):

        current_cost = COST(m2_data, M1_data, M2_data, R1, R2)
        derivative_cost_R1 = dCOSTdR1(m2_data, M1_data, M2_data, R1, R2)
        derivative_cost_R2 = dCOSTdR2(m2_data, M1_data, M2_data, R1, R2)
        if R1 - alpha * derivative_cost_R1 >= 0.0:
            R1 -= alpha * derivative_cost_R1
        if R2 - alpha * derivative_cost_R2 >= 0.0:
            R2 -= alpha * derivative_cost_R2
        costs[i] = current_cost
        R1s[i] = R1
        R2s[i] = R2
        print("iteration=", i, " cost=", current_cost, "R1=", R1, "R2=", R2)
    visualize(costs, R1s, R2s)

if __name__ == "__main__":
    gradient_descent()