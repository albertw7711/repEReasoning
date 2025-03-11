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
