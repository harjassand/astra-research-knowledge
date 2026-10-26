"""Odd-polarity intermediate construction and its exposed-end counterconstruction.
Modelled A=alkyne/alkyne monomer, B=azide/azide monomer (swap possible).
Only intramolecular terminal CuAAC competence is addressed by parity.
This is an abstract reaction-graph model, not measured chemistry.
"""
from fractions import Fraction
from itertools import permutations
from math import sqrt, log2
from functools import lru_cache


def complementary(u,v):return u!=v


def is_alternating(seq):
    return all(seq[i]!=seq[i+1] for i in range(len(seq)-1))


def can_terminal_cyclize(seq):
    assert is_alternating(seq)
    return complementary(seq[0],seq[-1])


def merge(left,right,bridge='B'):
    assert left[0]==left[-1]==right[0]==right[-1]=='A'
    output=left+bridge+right
    assert is_alternating(output) and output[0]==output[-1]=='A'
    assert not can_terminal_cyclize(output)
    return output


def bridge_good_probability(alpha=1.,leak=1.):
    """Sequential choice of two DIFFERENT A termini by homobifunctional B.

    Two intended termini have equal hazard alpha, two undesired outer
    termini have equal hazard leak. The two B reactive ends are identical.
    Once one terminus reacts, the other B end chooses among remaining three.
    These relative hazards are assumed unchanged by the first covalent join.
    This explicitly ignores potential intramolecular effective-molarity rise.
    """
    assert alpha>0 and leak>=0
    return (alpha/(alpha+leak))*(alpha/(alpha+2*leak))


def min_selectivity_for_target(target):
    """solve x^2/((x+1)(x+2)) = target, x=alpha/leak."""
    assert 0<target<1
    # (1-t)x^2-3tx-2t=0
    return (3*target+sqrt(9*target*target+8*target*(1-target)))/(2*(1-target))


def n_A_leaves(L):
    assert L%2==1
    return (L+1)//2


def tree_cost_A_leaves(nA,p):
    """Unit-cost A leaves, unit-cost B bridge per accepted binary merger.
    Every rejection destroys all submitted material. nA is power of 2.
    """
    assert nA&(nA-1)==0 and 0<p<=1
    C=1.
    for _ in range(nA.bit_length()-1):
        C=(2*C+1)/p
    return C


def brute_uniform_good():
    # The B linker selects two different termini among four without ordering.
    ports=('L_in','L_outer','R_in','R_outer')
    draws=list(permutations(ports,2))
    correct=sum(set(pair)=={'L_in','R_in'} for pair in draws)
    rings=sum(set(pair)=={'L_in','L_outer'} or set(pair)=={'R_in','R_outer'} for pair in draws)
    wrong=sum(set(pair) not in ({'L_in','R_in'},{'L_in','L_outer'},{'R_in','R_outer'}) for pair in draws)
    return Fraction(correct,len(draws)),Fraction(rings,len(draws)),Fraction(wrong,len(draws))


def test():
    for n in range(1,16):
        seq=('AB'*n)[:n]
        assert can_terminal_cyclize(seq)==(n%2==0)
    for nl in range(1,16,2):
        for nr in range(1,16,2):
            l=('AB'*(nl+1))[:nl];r=('AB'*(nr+1))[:nr]
            out=merge(l,r)
            assert out==('AB'*len(out))[:len(out)]
    assert brute_uniform_good()==(Fraction(1,6),Fraction(1,3),Fraction(1,2))
    assert abs(bridge_good_probability()-1/6)<1e-12
    for p in (.5,.9,.95,.99):
        ratio=min_selectivity_for_target(p)
        assert abs(bridge_good_probability(ratio)-p)<1e-12
    assert is_alternating(merge(merge('A','A'),'A'))
    return True

if __name__=='__main__':
    assert test()
    print('EXHAUSTIVE_PARITY_AND_TWO_END_PORT_CHECKS PASS')
    print('UNGUIDED_TWO_LINK_BRIDGE CORRECT RING OTHER',brute_uniform_good())
    for target in (.8,.9,.95,.99,.999):
        print('MIN_TARGET_VS_WRONG_PORT_RATE_RATIO',target,min_selectivity_for_target(target))
    for factor in (1,3,10,30,100):
        print('RELATIVE_RATE',factor,'BRIDGE_CORRECT',bridge_good_probability(factor))
    for q in (.90,.95):
        print('ODD_FRAGMENT_TREE_A_512_OUTPUT_1023_COST',q,tree_cost_A_leaves(512,q))
    print('ODD_FRAGMENT_TREE_UNGUIDED_Q_1/6_COST',tree_cost_A_leaves(512,1/6))
