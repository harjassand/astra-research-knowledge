"""Run a moderate heralded case and the recorded rare/bright stress case."""
from fractions import Fraction as F
import random
from rational_gaussian import RationalGaussian, mean_counts, log_herald_probability


def main():
    moderate=RationalGaussian.from_pure(
        [[F(1,10),F(1,5)],[F(1,5),F(1,8)]],
        [F(1,3),F(1,4)], [0],[2])
    rng=random.Random(42)
    print('Moderate conditional samples:',[moderate.sample(rng) for _ in range(5)])
    print('Exact conditional mean:',mean_counts(moderate))

    delta=F(1,10**40); coupling=F(1,10**60)
    B=[[0,coupling/2,coupling/3],
       [coupling/2,(1-delta)*F(3,5),(1-delta)*F(2,5)],
       [coupling/3,(1-delta)*F(2,5),(1-delta)*F(3,5)]]
    bright=RationalGaussian.from_pure(B,None,[0],[4])
    print('Rare/bright sample:',bright.sample(random.Random(76219),F(1,10**12)))
    print('Log herald probability (natural log):',log_herald_probability(bright))


if __name__=='__main__':
    main()
