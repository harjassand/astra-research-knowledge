"""Phase-2 finite component audit; no full certified FPRAS execution.

All output is owned by c06_s01. Production routines are imported read-only.
"""
from fractions import Fraction as F
from pathlib import Path
import sys, json, random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"revisions"))
import homogeneous_count as hc

def main():
    rng=random.Random(601130)
    mu=lambda s:F({1:2,2:3}.get(s,0))
    nu=lambda s:F({1:5,2:7}.get(s,0))
    p=hc.Problem(2,1,mu,nu,1,1,1,1)
    fields=[F(1,3),F(7,5)]
    tests=0
    for forced,forbidden in ((0,0),(1,0),(0,1)):
        m=hc.restricted(mu,forced,forbidden)
        seed=1 if m(1)>0 else 2
        pp=hc.Problem(2,1,m,nu,seed,1,1,1)
        states,kernel=hc.transition_matrix(pp,fields,F(1,1024))
        for row in kernel:
            assert sum(row,F(0))==1
        coins=hc.BoundedCoins(lambda:rng.getrandbits(1),1000000,64)
        state=(seed,1)
        for _ in range(10000):
            state=hc.exchange_step(pp,m,nu,fields,state,F(1,1024),coins)
            assert m(state[0])>0 and nu(state[1])>0
            assert state[0]&forced==forced and not state[0]&forbidden
            tests+=1
    # Last categorical weight zero is legal: a preceding p=1 decides first.
    for weights in ([F(1),F(0)],[F(0),F(1),F(0)],
                    [F(0),F(0),F(1)],[F(2),F(3),F(0)]):
        coins=hc.BoundedCoins(lambda:rng.getrandbits(1),1000,64)
        for _ in range(20):
            assert weights[coins.categorical(weights)]>0
    abort=hc.BoundedCoins(lambda:0,1,1)
    try:
        abort.bernoulli(F(1,3))
        raise AssertionError("ambiguity must abort")
    except hc.TapeAbort:
        pass
    # Exercise the production whole-count abort handler without shortening a
    # mixing loop: the diagnostic draw immediately raises its legal abort.
    original=hc.soft_sample
    def forced_abort(*args,**kwargs):
        raise hc.TapeAbort("diagnostic whole-count abort")
    hc.soft_sample=forced_abort
    try:
        assert hc.count(p,F(1,4),lambda:0,exact_cutoff=0)==0
    finally:
        hc.soft_sample=original
    # All small exact branches, degrees including 0/n, and all-zero overlap.
    exact=[]
    for n in range(1,8):
        for a in range(n+1):
            mu_u=lambda s,a=a:F(int(s.bit_count()==a))
            nu_u=lambda s,n=n,a=a:F(int(s.bit_count()==n-a))
            pp=hc.Problem(n,a,mu_u,nu_u,(1<<a)-1,(1<<(n-a))-1,0,0)
            v=hc.count(pp,F(1,5),lambda:rng.getrandbits(1))
            from math import comb
            assert v==comb(n,a)
            exact.append([n,a,str(v)])
    disjoint_mu=lambda s:F(int(s==1))
    disjoint_nu=lambda s:F(int(s==1))
    zero=hc.Problem(2,1,disjoint_mu,disjoint_nu,1,1,0,0)
    assert hc.exact_small(zero)==0
    result={"status":"PASS","executed_exchange_steps":tests,
       "all_small_exact_branches":len(exact),"exact_values":exact,
       "zero_intersection_exact":True,"whole_count_abort_handler":True,
       "trailing_zero_categorical_weights":True,
       "scope":"Finite component audit only. Whole-count abort used a test draw that aborts immediately; no certified long Markov loop was shortened or executed.",
       "imported_gap":"Chen--Liu Lemma5.5; remains a preprint premise"}
    Path(__file__).with_name("count_program_audit.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:result[k] for k in ("status","executed_exchange_steps","all_small_exact_branches","scope")},indent=2))

if __name__=="__main__":main()
