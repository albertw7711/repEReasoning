from sympy import *
import random

class Utils:
    @staticmethod
    def is_symbolically_integrable(expr, symbol):
        try:
            result = integrate(expr, symbol, risch=True)
            if result.has(Integral):
                return False
            return True
        except:
            return False

    @staticmethod
    def generate_random_nonzero_fraction(min_val=-100, max_val=100):
        while True:
            numerator = random.randint(min_val, max_val)
            denominator = random.randint(min_val, max_val)
            if numerator != 0 and denominator != 0:
                return Rational(numerator, denominator)

    @staticmethod
    def sort_by_weighted_sum(array, weights):
        if any(len(sub) != len(weights) for sub in array):
            raise ValueError("Each sub-array must match the length of the weights list.")

        return sorted(array, key=lambda row: sum(x * w for x, w in zip(row, weights)))

    @staticmethod
    def easy_skewed_randint(lower_bound, upper_bound):
        values = list(range(lower_bound, upper_bound + 1))
        if (upper_bound - lower_bound) < 4:
            line = (upper_bound - lower_bound) // 2
        else:
            line = (upper_bound - lower_bound) // 4

        # Assign higher weight to the first half
        weights = [2 if i <= line else 1 for i in values]
