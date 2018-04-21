import numpy as np
from matplotlib import pyplot as plt

# constant values
m1_experimental_data = np.array([0.09, 0.17, 0.28, 0.32, 0.35, 0.41])
M1_experimental_data = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
R1_init = 0.5
R2_init = 0.5
iters = 800
alpha = 0.01


# return numerator of m1 equation
def m1_numerator(R1, M1):
    return (R1 - 1) * np.square(M1) + M1


# return denominator of m1 equation
def m1_denominator(R1, R2, M1):
    return R2 * (-2 * M1 - np.square(M1) + 1) + R1 * np.square(M1) - 2 * np.square(M1) + 2*M1


# return m1
def m1(R1, R2, M1):
    return m1_numerator(R1, M1) / m1_denominator(R1, R2, M1)


# return the cost of the estimated m1 array vs the experimental m1 array
def cost(m1E, m1C):
    return 0.5 * np.sum(np.square(m1E - m1C))


# derivative of m1 numerator w.r.t. R1
def d_m1_numerator_R1(M1):
    return np.square(M1)


# derivative of m1 numerator w.r.t. R2
def d_m1_numerator_R2():
    return 0


# derivative of m1 denominator w.r.t. R1
def d_m1_denominator_R1(M1):
    return M1**2


# derivative of m1 denominator w.r.t. R2
def d_m1_denominator_R2(M1):
    return -2*M1 - np.square(M1) + 1


# derivative of m1 w.r.t. R1
def d_m1_R1(R1, R2, M1):
    return (d_m1_numerator_R1(M1) * m1_denominator(R1, R2, M1) - m1_numerator(R1, M1) * d_m1_denominator_R1(M1)) / np.square(m1_denominator(R1, R2, M1))


# derivative of m1 w.r.t. R2
def d_m1_R2(R1, R2, M1):
    return (d_m1_numerator_R2() * m1_denominator(R1, R2, M1) - m1_numerator(R1, M1) * d_m1_denominator_R2(M1)) / np.square(m1_denominator(R1, R2, M1))


# derivative of cost w.r.t. m1
def d_cost_m1(m1E, m1C):
    return np.sum(m1E - m1C)


# derivative of cost w.r.t. R1
def d_cost_R1(m1E, m1C, R1, R2, M1):
    return np.sum(np.multiply((m1E - m1C), d_m1_R1(R1, R2, M1)))


# derivative of cost w.r.t. R2
def d_cost_R2(m1E, m1C, R1, R2, M1):
    return np.sum(np.multiply((m1E - m1C), d_m1_R2(R1, R2, M1)))


if __name__ == "__main__":
    print("starting gradient descent optimization")
    R1 = R1_init
    R2 = R2_init
    costs = np.zeros(iters)
    for i in range(iters):
        m1C = m1(R1, R2, M1_experimental_data)
        current_cost = cost(m1_experimental_data, m1C)
        derivative_cost_R1 = d_cost_R1(m1_experimental_data, m1C, R1, R2, M1_experimental_data)
        derivative_cost_R2 = d_cost_R2(m1_experimental_data, m1C, R1, R2, M1_experimental_data)
        if R1 >= 0.0:
            R1 += alpha * derivative_cost_R1
        if R2 >= 0.0:
            R2 += alpha * derivative_cost_R2
        costs[i] = current_cost
        print("iteration=", i, " cost=", current_cost, "R1=", R1, "R2=", R2)

    plt.plot(costs, 'r*')
    plt.ylabel("Cost Value")
    plt.xlabel("# iterations")
    plt.show()
