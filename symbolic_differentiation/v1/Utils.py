from sympy import *
import random

class Utils:
    @staticmethod
    def is_symbolically_integrable(expr, symbol):
        try:
            result = integrate(expr, symbol, risch=True)
