"""Exact local sampler under a supplied independent unbiased-bit primitive.
No finite-state host PRNG is asserted to supply an ideal infinite IID law.
"""
from fractions import Fraction
from math import gcd

def randbelow(n,get_bits):
    if n<1:raise ValueError('positive range required')
    if n==1:return 0
    k=(n-1).bit_length()
    while True:
        value=get_bits(k)
        if not 0<=value<2**k:raise ValueError('invalid bit primitive')
        if value<n:return value

def draw_rational(weights,get_bits):
    probabilities=list(map(Fraction,weights))
    if min(probabilities)<0 or sum(probabilities)!=1:raise ValueError('not a distribution')
    denominator=1
    for p in probabilities:denominator=denominator*p.denominator//gcd(denominator,p.denominator)
    value=randbelow(denominator,get_bits);end=0
    for j,p in enumerate(probabilities):
        end+=p.numerator*(denominator//p.denominator)
        if value<end:return j
    raise AssertionError('unreachable')

class LocalKernel:
    def __init__(self,serialized):
        self.columns=serialized['kernels']
        self.reserve=Fraction(serialized['reserved_uniform_product_probability'])
        if self.reserve!=Fraction(1,64):raise ValueError('different kernel reserve')
    def update(self,left,right,get_bits):
        if not(0<=left<24 and 0<=right<24):raise ValueError('frame index outside0..23')
        if randbelow(64,get_bits)==0:
            return randbelow(24,get_bits),randbelow(24,get_bits)
        column=self.columns[24*left+right]
        choice=draw_rational(column['remainder_probabilities'],get_bits)
        pair=column['output_pair_indices'][choice]
        return divmod(pair,24)
