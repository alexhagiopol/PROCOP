import argparse
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')  # hack around bug in matplotlib. see https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python
from matplotlib import pyplot as plt


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
    plt.title("Cost")
    # plot R1s
    plt.subplot(1, 3, 2)
    plt.plot(R1s, 'r*')
    plt.ylabel("R1 Value")
    plt.xlabel("# Iterations")
    plt.title("R1")
    # plot R2s
    plt.subplot(1, 3, 3)
    plt.plot(R2s, 'r*')
    plt.ylabel("R2 Value")
    plt.xlabel("# Iterations")
    plt.title("R2")
    plt.show()


# core gradient descent implementation
def gradient_descent(m1_data, M1_data, R1_init, R2_init, iters, alpha):
    print("starting gradient descent optimization")
    m2_data = 1.0 - m1_data
    M2_data = 1.0 - M1_data
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
        print("iteration=", i, " cost=", current_cost, "r1=", R1, "r2=", R2)
    print("Reactivity ratios estimation completed.")
    print("Used m1 data", m1_data)
    print("Used M1 data", M1_data)
    print("Used initial r1=", R1_init, " and initial r2=", R2_init)
    print("Used learning rate = ", alpha)
    print("Used ", iters, " iterations")
    print("Computed optimized r1=", R1, " and optimized r2=", R2)
    visualize(costs, R1s, R2s)


def main():
    parser = argparse.ArgumentParser(description="Example: ReactivityRatios --data=data.csv")
    parser.add_argument("--data", type=str, default=None, help="Relative path to data file.")
    args = parser.parse_args()
    data_matrix = np.genfromtxt(args.data, delimiter=',')
    if data_matrix.shape[0] != 2:
        print(
            "Invalid data. CSV file should have 2 rows of comma separated values. One for m1 values and one for M1 values.")
        exit()
    m1_data = data_matrix[0, :]
    M1_data = data_matrix[1, :]
    R1_init = 0.143
    R2_init = 0.9626
    iters = 10000
    alpha = 0.1
    gradient_descent(m1_data, M1_data, R1_init, R2_init, iters, alpha)

if __name__ == "__main__":
    main()
