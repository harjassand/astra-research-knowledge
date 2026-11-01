#!/usr/bin/env python3
"""Finite, exact-coin forward protocol. Sampling provenance remains external."""
from fractions import Fraction
import random
import control as C

class CountedRandom(random.Random):
    def __init__(self,seed):
        super().__init__(seed);self.bit_requests=0;self.random_bits=0
    def getrandbits(self,k):
        self.bit_requests+=1;self.random_bits+=k
        return super().getrandbits(k)


def acquire(source,design,seed,*,retain_micro_paths=True):
    """source.step(i,a,rng) is ordinary named-row forward access only.

    All iterations and N/cap are fixed before outcomes. The optional path log
    retains actually observed source/destination labels, never invented tags.
    Exact source identity/iidness is not certified by this Python function.
    """
    n=C.integer(design['n'],1);m=C.integer(design['m'],1);N=C.integer(design['N'],1);cap=C.integer(design['cap']);gamma=C.rational(design['gamma'])
    if not 0<gamma<1:raise ValueError('discount')
    _,_,which=C.partitions(design['parts'],n);r=len(design['parts']);rng=CountedRandom(seed)
    counts=[[[0]*r for i in range(n)] for a in range(m)];logs=[];calls=0;coins=0;end_at_cap=0
    for a in range(m):
        for i in range(n):
            for episode in range(N):
                j=source.step(i,a,rng);C.integer(j);assert j<n;calls+=1;path=[i,j];steps=0
                while steps<cap:
                    coins+=1
                    if rng.randrange(int(gamma.q))>=int(gamma.p):break
                    k=source.step(j,0,rng);C.integer(k);assert k<n;calls+=1;path.append(k);j=k;steps+=1
                if steps==cap:end_at_cap+=1
                counts[a][i][which[j]]+=1
                if retain_micro_paths:logs.append({'action':a,'source_row':i,'episode':episode,'micro_path':path})
    record={'design':design,'counts':counts}
    ledger={'episodes':n*m*N,'actual_source_calls':calls,'stopping_coin_draws':coins,'actual_rng_bit_requests':rng.bit_requests,'actual_rng_bits':rng.random_bits,'episodes_ending_at_cap':end_at_cap,'retained_micro_path_records':len(logs),'retained_micro_labels':sum(len(x['micro_path']) for x in logs),'all_rows_and_actions_have_fixed_N':True,'source_metadata_available_to_comparators':True,'seed':seed,'randomness_scope':'Reproducible Python PRNG fixture; theorem uses ideal independent draws, not cryptographic randomness or physical provenance.'}
    return record,ledger,logs
