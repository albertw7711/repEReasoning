from sympy import *
from Generator import Generator
from objs import *
from copy import deepcopy
import numpy as np

class DifferentiationGenerator(Generator):
    ATTEMPT_LIMIT = 30
