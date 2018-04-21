import numpy as np


def m1_numerator(R1, M1):
    return (R1 - 1) * (M1**2) + M1


def m1_denominator(R1, R2, M1):
    return R2 * (-2 * M1 - M1**2 + 1) + R1 * M1**2 - 2 * M1**2 + 2*M1


def m1(R1, R2, M1):
    return m1_numerator(R1, M1) / m1_denominator(R1, R2, M1)


if __name__ == "__main__":
    m1_experimental_data = np.array([0.09, 0.17, 0.28, 0.32, 0.35, 0.41])
    M1_experimental_data = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    print("starting gradient descent optimization")