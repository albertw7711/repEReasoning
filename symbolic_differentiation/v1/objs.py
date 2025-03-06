from __future__ import annotations
from itertools import combinations
from typing import Optional, List
from enum import Enum
from sympy import *
from Utils import Utils
import random
from copy import deepcopy
from math import ceil

class ReverseDifferentiatingRuleType(Enum):
    SUM = 0,
    PRODUCT = 1,
    WIDE_PRODUCT = 2,
    CHAIN = 3,
    WIDE_CHAIN = 4,
TRIGS = [sin, cos, tan]
REC_TRIGS = [sec, csc, cot]
INV_TRIGS = [asin, acos, atan]
INV_REC_TRIGS = [asec, acsc, acot]

RULE_WEIGHTS = [1] * 5
class DifferentiatingRule:
    def __init__(self, rule_type: ReverseDifferentiatingRuleType,
                 weight: int, fns=None, is_poly: bool=false, is_reuse: bool=False):
        if fns is None:
            fns = []
        self.rule_type = rule_type
        self.weight = weight
        self.fns = fns
        self.is_poly = is_poly
        self.is_reuse = is_reuse


    def sum_apply_native(self, parent):
        if self.is_poly:
            self.fns[-1] = parent.symbol ** random.randint(1, 10)
        term_new = random.choice(self.fns)
        if isinstance(term_new, DifferentiableEquationNode):
            print()
        if isinstance(term_new, FunctionClass):
