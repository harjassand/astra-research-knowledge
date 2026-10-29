"""Established rooted polymer dynamics with the paid literal-history oracle.

No cutoff approximation or partition-function oracle. Expected-time contract;
seeded MT execution is an implementation diagnostic, not a validated RNG law.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib
import json
import random
import time
from literal_history import HistoryModel, bits
from polymer_sampler import uniform_constants, ceil_log2


class FairBits:
    def __init__(self,seed=20261029):
        self.rng=random.Random(seed)
        self.requested=0;self.calls=0;self.trials=0

    def below(self,n):
        if n==1:return 0
        self.calls+=1;width=(n-1).bit_length()
        while True:
            self.requested+=width;self.trials+=1
            value=self.rng.getrandbits(width)
            if value<n:return value


def rooted_proposal(model,root,B0,A,backend,stats):
    R=A*A;K=0
    while K<model.N and backend.below(R)==0:
        K+=1
    stats['depths'][str(K)]=stats['depths'].get(str(K),0)+1
    if not K:return 0
    current={1<<root};valid=[]
    for size in range(1,K+1):
        following=set()
        for support in current:
            stats['supports_tested']+=1
            if model.valid_polymer(support):
                energy=model.top_energy(support)
                assert energy>0 and size<=4*energy
                valid.append((support,energy,size))
            if size<K:
                boundary=set().union(*(model.adj[v] for v in bits(support)))
                boundary.difference_update(bits(support))
                following.update(support|(1<<v) for v in boundary)
        current=following
    if not valid:return 0
    Emax=max(e for _,e,_ in valid)
    denominator=B0**(4*Emax)
    numerators=[R**size*B0**(4*(Emax-e)) for _,e,size in valid]
    assert sum(numerators)<=denominator
    ticket=backend.below(denominator)
    for (support,_,_),numerator in zip(valid,numerators):
        if ticket<numerator:return support
        ticket-=numerator
    return 0


def sample(model,B0,epsilon):
    A=4*max(1,model.degree)
    # Computed-instance admission. Uniform all-level choice Abar**4 is safe.
    assert B0>=A**4
    q=Q(1,B0);c=(model.degree+1)*q/(1-A*q)**2
    assert c<Q(1,2)
    updates=4*model.N*ceil_log2(Q(8*model.N)/epsilon)
    backend=FairBits();owner=[0]*model.N;occupied=set()
    stats={'depths':{},'supports_tested':0}
    started=time.perf_counter()
    for _ in range(updates):
        v=backend.below(model.N)
        if backend.below(2)==0:
            support=owner[v]
            if support:
                occupied.remove(support)
                for u in bits(support):owner[u]=0
        else:
            support=rooted_proposal(model,v,B0,A,backend,stats)
            if not support or support in occupied:continue
            vs=tuple(bits(support))
            neighbourhood=set(vs).union(*(model.adj[u] for u in vs))
            if all(owner[u]==0 for u in neighbourhood):
                occupied.add(support)
                for u in vs:owner[u]=support
    history=sum(occupied)
    assert model.accepted(history)
    out={'route':'ordinary_rooted_polymer_expected_time','updates':updates,
         'seconds':time.perf_counter()-started,'weighted_incompatibility_c':str(c),
         'ideal_law_tv_upper':str(Q(2*model.N,1<<ceil_log2(Q(8*model.N)/epsilon))),
         'random_bit_requests':backend.requested,'integer_calls':backend.calls,
         'integer_trials':backend.trials,'proposal_stats':stats,
         'occupied_polymers':len(occupied),'returned_top_weight':model.top_energy(history),
         'time_contract':'finite almost surely; polynomial expected cost, not worst-case polylog-accuracy',
         'randomness_contract':'independent ideal fair bits for theorem; seeded MT run only diagnostic'}
    return history,out


def main():
    started=time.perf_counter();model=HistoryModel(2,3)
    build=time.perf_counter()-started
    # Match the already executed finite-list target temperature exactly.
    # This native instance passes B0>=A_actual**4; the all-level theorem
    # instead selects a uniform Abar**4 (or larger source-qualified value).
    B0=uniform_constants(3)['B0']
    _,out=sample(model,B0,Q(1,100))
    top_checks=sum(model.counts[s,model.levels] for s in (0,1))
    out.update({'model':model.sizes(),'B0':str(B0),'beta':'4 ln(B0)',
                'epsilon':'1/100','build_seconds':build,
                'ordinary_zero_tv_upper':str(Q(top_checks,B0**4-top_checks)),
                'force_engine_diagnostic':True,
                'computed_instance_temperature_admission':B0>=(4*max(1,model.degree))**4,
                'uniform_all_level_beta_claim_from_this_run':False,
                'scope':'same literal ell3 source; not primary-qualified geometry or hardware initialization',
                'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (Path(__file__).parent/'ROOTED_EXECUTION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
