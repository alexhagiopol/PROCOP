import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')  # hack around bug in matplotlib. see https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python
from matplotlib import pyplot as plt


# numerator of G from Tidwell equation 6
def G_numerator(M1, M2, r2):
    return r2 * np.square(M2) + np.multiply(M2, M1)


# denominator of G from Tidwell equation 6
def G_denominator(M1, M2, r1, r2):
    return r2 * np.square(M2) + 2 * np.multiply(M1, M2) + r1 * np.square(M1)


# G from Tidwell equation 6
def G(M1, M2, r1, r2):
    return G_numerator(M1, M2, r2) / G_denominator(M1, M2, r1, r2)


# cost function for gradient descent. based on d from Tidwell equation 8
def COST(m2, M1, M2, r1, r2):
    return (1 / (2 * M1.shape[0])) * np.sum(np.square(m2 - G(M1, M2, r1, r2)))


# derivative of G w.r.t. r1
def dGdr1(M1, M2, r1, r2):
    return -1 * G_numerator(M1, M2, r2) * np.square(M1) / np.square(G_denominator(M1, M2, r1, r2))


# derivative of G w.r.t. r2
def dGdr2(M1, M2, r1, r2):
    return np.square(M2) * (G_denominator(M1, M2, r1, r2) - G_numerator(M1, M2, r2)) / np.square(G_denominator(M1, M2, r1, r2))


# derivative of cost w.r.t. r1
def dCOSTdr1(m2, M1, M2, r1, r2):
    return (1 / M1.shape[0]) * np.sum(np.multiply(G(M1, M2, r1, r2) - m2, dGdr1(M1, M2, r1, r2)))


# derivative of cost w.r.t. r2
def dCOSTdr2(m2, M1, M2, r1, r2):
    return (1 / M1.shape[0]) * np.sum(np.multiply(G(M1, M2, r1, r2) - m2, dGdr2(M1, M2, r1, r2)))


# plot results
def visualize(costs, r1s, r2s):
    # plot costs
    plt.subplot(1, 3, 1)
    plt.plot(costs, 'r*')
    plt.ylabel("Cost Value")
    plt.xlabel("# Iterations")
    plt.title("Cost")
    # plot r1s
    plt.subplot(1, 3, 2)
    plt.plot(r1s, 'r*')
    plt.ylabel("r1 Value")
    plt.xlabel("# Iterations")
    plt.title("r1")
    # plot r2s
    plt.subplot(1, 3, 3)
    plt.plot(r2s, 'r*')
    plt.ylabel("r2 Value")
    plt.xlabel("# Iterations")
    plt.title("r2")
    plt.show()


# core gradient descent implementation
def gradient_descent(m1_data, M1_data, r1_init, r2_init, iters, alpha):
    print("starting gradient descent optimization")
    # m2 = 1 - m1 ; M2 - 1 - M1
    m2_data = 1.0 - m1_data
    M2_data = 1.0 - M1_data
    # intitialize
    r1 = r1_init
    r2 = r2_init
    # store historical cost, r1, and r2 values for plotting
    costs = np.zeros(iters)
    r1s = np.zeros(iters)
    r2s = np.zeros(iters)
    # core loop
    for i in range(iters):
        current_cost = COST(m2_data, M1_data, M2_data, r1, r2)
        derivative_cost_r1 = dCOSTdr1(m2_data, M1_data, M2_data, r1, r2)
        derivative_cost_r2 = dCOSTdr2(m2_data, M1_data, M2_data, r1, r2)
        # simultaneous update rule
        if r1 - alpha * derivative_cost_r1 >= 0.0:
            r1 -= alpha * derivative_cost_r1
        if r2 - alpha * derivative_cost_r2 >= 0.0:
            r2 -= alpha * derivative_cost_r2
        # store historical cost, r1, and r2 values for plotting
        costs[i] = current_cost
        r1s[i] = r1
        r2s[i] = r2
        print("iteration=", i, " cost=", current_cost, "r1=", r1, "r2=", r2)
    # display results
    print("Reactivity ratios estimation completed.")
    print("Used m1 data", m1_data)
    print("Used M1 data", M1_data)
    print("Used initial r1=", r1_init, " and initial r2=", r2_init)
    print("Used learning rate = ", alpha)
    print("Used ", iters, " iterations")
    print("Computed optimized r1=", r1, " and optimized r2=", r2)
    # plot visualization
    visualize(costs, r1s, r2s)


def main():
    print("Reactivity Ratios Calculation with Gradient Descent")
    # get data for m1 and M1
    data_matrix_filename = input("Enter full file path containing m1 and M1 data."
    "You can just drag & drop the file into this window then press Enter:\n")
    # eliminate spaces that get added by OS at the end of filename
    if data_matrix_filename[-1] == ' ':
        data_matrix_filename = data_matrix_filename[0:-1]
    data_matrix = np.genfromtxt(data_matrix_filename, delimiter=',')
    if data_matrix.shape[0] != 2:
        print(
            "Invalid data. CSV file should have 2 rows of comma separated values. One for m1 values and one for M1 values.")
        exit()
    m1_data = data_matrix[0, :]
    M1_data = data_matrix[1, :]
    # get r1 and r2 initial guess
    r1_init = float(input("Enter initial guess for r1:\n"))
    r2_init = float(input("Enter initial guess for r2:\n"))
    # get final 2 tuning parameters
    iters = int(input("Enter number of iterations (10000 is recommended):\n"))
    alpha = float(input("Enter learning rate (0.1 is recommended):\n"))
    # execute function that does the calculations
    gradient_descent(m1_data, M1_data, r1_init, r2_init, iters, alpha)

if __name__ == "__main__":
    main()
