"""Task-conditioned stochastic network abstraction.

Native model: finite-state individual sites; unary transitions and directed pair-
triggered transitions.  No groups or coarse coordinates are supplied to the
compiler. A finite symmetrization/projection is computed from raw local rates.

This is a research pilot, not a general theorem prover or an external benchmark.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from itertools import product
import math
import time
from typing import Optional
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

@dataclass
class Model:
    unary: np.ndarray          # (n,q,q): site j, old, new
    pair: np.ndarray           # (n,n,q,q,q): trigger i, target j, trigger_state, old, new
    name: str = ''
    @property
    def n(self): return self.unary.shape[0]
    @property
    def q(self): return self.unary.shape[1]

    def validate(self):
        n,q=self.n,self.q
        assert self.unary.shape==(n,q,q)
        assert self.pair.shape==(n,n,q,q,q)
        assert np.min(self.unary)>=0 and np.min(self.pair)>=0
        assert np.max(np.abs(np.diagonal(self.unary,axis1=1,axis2=2)))==0
        assert np.max(np.abs(np.diagonal(self.pair,axis1=3,axis2=4)))==0
        assert np.max(np.abs(self.pair[np.arange(n),np.arange(n)]))==0
        return self


def make_model(sizes, q, unary_by_group, pair_by_group, name=''):
    """Convenience for constructing native experiments, NOT part of learner API."""
    sizes=list(sizes); n=sum(sizes)
    unary=np.zeros((n,q,q)); pair=np.zeros((n,n,q,q,q))
    labels=np.repeat(np.arange(len(sizes)),sizes)
    for j in range(n): unary[j]=unary_by_group[labels[j]]
    for i in range(n):
        for j in range(n):
            if i!=j: pair[i,j]=pair_by_group[labels[i],labels[j]]
    return Model(unary,pair,name).validate(),labels


def detect_exchangeable_classes(m:Model, forced_singletons=()):
    """Discover permutation invariance directly from the *complete native rule arrays*.

    A swap is accepted only if it preserves all unary/pair coefficients.
    Transpositions that are automorphisms generate a product of symmetric groups.
    O(n^3 q^3) comparisons using incident-array equivalence.
    """
    n=m.n
    forced=set(forced_singletons)
    parent=list(range(n))
    counters={'swaps_tested':0,'swap_rejections':0,'array_scalar_comparisons_upper':0}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]];x=parent[x]
        return x
    for a in range(n):
        for b in range(a+1,n):
            if a in forced or b in forced:continue
            counters['swaps_tested']+=1
            # Only entries incident to a or b can change under their swap.
            # This check is algebraically equivalent to whole-tensor equality,
            # with O(n*q^3) instead of O(n^2*q^3) scalar comparisons per swap.
            others=[i for i in range(n) if i!=a and i!=b]
            counters['array_scalar_comparisons_upper']+=(2*m.q*m.q+4*(n-2)*m.q**3+2*m.q**3)
            ok=(np.array_equal(m.unary[a],m.unary[b])
                and np.array_equal(m.pair[a,b],m.pair[b,a])
                and np.array_equal(m.pair[a,others],m.pair[b,others])
                and np.array_equal(m.pair[others,a],m.pair[others,b]))
            if ok:parent[find(a)]=find(b)
            else:counters['swap_rejections']+=1
    groups=defaultdict(list)
    for i in range(n):groups[find(i)].append(i)
    return sorted(groups.values(),key=lambda x:x[0]),counters


def all_compositions(n,k):
    if k==1:yield (n,)
    else:
        for i in range(n+1):
            for rest in all_compositions(n-i,k-1):yield (i,)+rest


def coarse_states(groups,q):
    per=[tuple(all_compositions(len(g),q)) for g in groups]
    flat=list(product(*per))
    return flat,{x:i for i,x in enumerate(flat)}


def coefficient_project(m,groups):
    """Acquire orbit-averaged unary and directed-pair coefficients without
    querying a hidden microstate or assuming exact exchangeability.
    O(n^2 q^3) reads; averaging is explicitly paid.
    """
    g=len(groups);q=m.q
    a=np.zeros((g,q,q)); b=np.zeros((g,g,q,q,q))
    for z,sites in enumerate(groups):a[z]=m.unary[sites].mean(axis=0)
    for h,hi in enumerate(groups):
        for z,zi in enumerate(groups):
            denom=len(hi)*len(zi)-(len(hi) if h==z else 0)
            if denom==0:continue
            total=np.zeros((q,q,q))
            for i in hi:
                for j in zi:
                    if i!=j:total+=m.pair[i,j]
            b[h,z]=total/denom
    return a,b


def build_coarse(m:Model,groups):
    """Conservative projected CTMC R=H Q B on orbit counts; exact lumping when
    transpositions preserve the generator, and a meaningful averaged reference
    otherwise.  `groups` is discovered, never passed from experiment labels.
    """
    q=m.q;G=len(groups);a,b=coefficient_project(m,groups)
    states,index=coarse_states(groups,q);rows=[];cols=[];vals=[]
    for row,c in enumerate(states):
        exit_rate=0.
        for z in range(G):
            for s in range(q):
                if c[z][s]==0:continue
                for t in range(q):
                    if t==s:continue
                    rate=a[z,s,t]
                    for h in range(G):
                        for r in range(q):
                            rate+=b[h,z,r,s,t]*(c[h][r]-(int(h==z and r==s)))
                    rate*=c[z][s]
                    if rate< -1e-10:raise ArithmeticError('Negative projected rate')
                    if rate<=0:continue
                    updated=[list(v) for v in c]
                    updated[z][s]-=1;updated[z][t]+=1
                    nxt=index[tuple(tuple(v) for v in updated)]
                    rows.append(row);cols.append(nxt);vals.append(rate)
                    exit_rate+=rate
        rows.append(row);cols.append(row);vals.append(-exit_rate)
    Q=csr_matrix((vals,(rows,cols)),shape=(len(states),len(states)))
    assert np.max(np.abs(np.asarray(Q.sum(axis=1)))) < 1e-8
    return Q,states,index,(a,b)


def full_generator(m):
    """Strong exact individual-state comparator for SMALL instances only."""
    n,q=m.n,m.q
    states=list(product(range(q),repeat=n));index={v:i for i,v in enumerate(states)}
    rows=[];cols=[];vals=[]
    for idx,x in enumerate(states):
        exit_rate=0.
        for j in range(n):
            s=x[j]
            for t in range(q):
                if s==t:continue
                rate=m.unary[j,s,t]
                for i in range(n):
                    if i!=j:rate+=m.pair[i,j,x[i],s,t]
                if rate<=0:continue
                y=list(x);y[j]=t
                rows.append(idx);cols.append(index[tuple(y)]);vals.append(rate)
                exit_rate+=rate
        rows.append(idx);cols.append(idx);vals.append(-exit_rate)
    Q=csr_matrix((vals,(rows,cols)),shape=(len(states),len(states)))
    return Q,states,index


def state_to_counts(x,groups,q):
    return tuple(tuple(sum(x[j]==s for j in g) for s in range(q)) for g in groups)


def expm_distribution(Q,p0,T):
    v=expm_multiply(Q.T*T,p0)
    assert abs(v.sum()-1)<5e-9,(v.sum(),Q.shape)
    return v


def observable_extinct(states, infectious=1):
    return np.array([float(all(v[infectious]==0 for v in x)) for x in states])


def observable_infected(states, infectious=1):
    return np.array([sum(v[infectious] for v in x) for x in states],float)


def observable_full_extinct(states,infectious=1):
    return np.array([float(infectious not in x) for x in states])


def uniform_initial_micro(initial_counts,groups,q,index_full):
    """Randomized preparation uniform among assignments with given counts.
    This is an actual restriction for the quadratic theorem.
    """
    v=np.zeros(len(index_full))
    for x,idx in index_full.items():
        if state_to_counts(x,groups,q)==initial_counts:v[idx]=1
    assert v.sum()>0
    return v/v.sum()


def uniformization_time(Q,T,K=None):
    # Honest explicit Poisson truncation report, useful for smaller coarse models.
    # Numerics are float64; this is NOT a machine-checked interval proof.
    from scipy.stats import poisson
    Lam=float(np.max(-Q.diagonal()))
    if Lam==0:return 0,0.
    lt=Lam*T
    if K is None:K=int(math.ceil(lt+12*math.sqrt(lt+1)+30))
    return K,float(poisson.sf(K,lt))


def deviations(m,groups):
    """Conservative O(n^2q^3) upper bound on the row sum of abs(Q-Q_sym)
    and on ||(Q-Q_sym)B||. Uses all typed local transition rules.
    """
    n,q=m.n,m.q;a,b=coefficient_project(m,groups)
    label=np.zeros(n,dtype=int)
    for g,nodes in enumerate(groups):label[nodes]=g
    sum_unary=0.; sum_pair=0.
    for j in range(n):
        sum_unary+=float(np.abs(m.unary[j]-a[label[j]]).sum())
    for i in range(n):
        for j in range(n):
            if i!=j:sum_pair+=float(np.abs(m.pair[i,j]-b[label[i],label[j]]).sum())
    eta=sum_unary+sum_pair
    return {'eta_upper':eta,'generator_inf_upper':2*eta,'projected_leakage_inf_upper':2*eta,
            'unary_total':sum_unary,'pair_total':sum_pair}


def quadratic_certificate(eta,T):
    """Bound |E_mu f(X_T) - E_mu f(Xbar_T)| for 0<=f<=1,
    with initial uniform within orbit, via Duhamel cancellation.
    For 0<=f<=1: ||E e^{tQ_sym} f||_infty <= eta; generator row norm
    ||E||_infty<=2eta. Duhamel + symmetry cancellation gives
    Error <= min(1, eta**2*T**2). Known rates, no observation oracle.
    """
    return min(1.,eta*eta*T*T)


def linear_certificate(eta,T):
    return min(1.,1.-math.exp(-eta*T))


def inspect_observable_compatibility(groups, singled_out=()):
    anchors=set(singled_out)
    return all(not (set(g)&anchors) or len(g)==1 for g in groups)
