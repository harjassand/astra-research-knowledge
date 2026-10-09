"""Finite pool likelihood solver capped by distinct sampled molecule tags.

Unlike the event-count-layer reference, this solver does not retain the total
number of Poisson candidate events. It tracks only the distinct molecules ever
sampled by a free catalyst, capped at K. Repeated selections and no-ops remain
in the state generator. A trajectory omitted by the cap must have had at least
K+1 candidate events, so the same Poisson tail bounds its missing likelihood.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import lgamma
from time import perf_counter
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
from scipy.sparse import coo_matrix
from scipy.stats import poisson

from marked_pool_partial import weak_compositions, multinomial_pmf, partial_multinomial_pmf


@dataclass
class UniqueMarkResult:
    lower: float
    poisson_tail: float
    retained_mass: float
    dimension: int
    rtol: float
    atol: float
    seconds: float


class UniqueMarkLikelihood:
    def __init__(self, N, Q, bind, product, lam, koff, kcat, mu0, catalysts=1):
        self.N=int(N); self.Q=np.asarray(Q,dtype=float); self.q=len(self.Q)
        self.bind=int(bind); self.product=int(product); self.lam=float(lam)
        self.koff=float(koff); self.kcat=float(kcat); self.mu0=np.asarray(mu0,dtype=float)
        self.catalysts=int(catalysts)
        assert self.Q.shape==(self.q,self.q)
        assert np.allclose(self.Q.sum(axis=1),0.0)
        assert np.all(self.Q-np.diag(np.diag(self.Q))>=-1e-14)
        assert self.mu0.shape==(self.q,) and np.all(self.mu0>=0)
        assert abs(float(self.mu0.sum())-1.0)<1e-12
        assert 0<=self.bind<self.q and 0<=self.product<self.q
        assert self.N>=1 and self.lam>=0 and self.koff>=0 and self.kcat>=0 and self.catalysts>=1

    def _states(self,K,cap_state=None,cap_count=None):
        M=min(int(K),self.N)
        states=[]
        for b in range(min(self.catalysts,M)+1):
            for n in weak_compositions(M-b,self.q):
                if cap_state is not None and n[cap_state]>cap_count:
                    continue
                states.append((b,n))
        return states,{s:i for i,s in enumerate(states)}

    def solve(self,T,K,observed,observed_bound=None,rtol=2e-10,atol=1e-13,max_step=np.inf):
        start=perf_counter(); N,q=int(self.N),self.q; K=int(K)
        partial=isinstance(observed,dict)
        if partial:
            obs={int(a):int(y) for a,y in observed.items()}
            if not obs or any(a<0 or a>=q for a in obs) or any(y<0 for y in obs.values()):
                raise ValueError("partial observation must map valid state indices to nonnegative counts")
        else:
            if len(observed)!=q or any(int(y)<0 for y in observed):
                raise ValueError("observed must be a nonnegative q-vector")
            obs=tuple(map(int,observed))
        cap_state=cap_count=None
        product_obs=obs.get(self.product) if partial else obs[self.product]
        if product_obs is not None and self.product!=self.bind and self.mu0[self.product]==0:
            row=np.delete(self.Q[self.product,:],self.product)
            col=np.delete(self.Q[:,self.product],self.product)
            if np.all(row==0.0) and np.all(col==0.0):
                cap_state,cap_count=self.product,product_obs
        states,ix=self._states(K,cap_state,cap_count); D=len(states)
        # Time-homogeneous marked-particle generator between tag additions.
        rr=[]; cc=[]; vv=[]
        for src,(b,n) in enumerate(states):
            exit_rate=0.0
            for a in range(q):
                if not n[a]: continue
                for c in range(q):
                    rate=n[a]*self.Q[a,c] if c!=a else 0.0
                    if rate>0:
                        nn=list(n); nn[a]-=1; nn[c]+=1
                        dst=ix.get((b,tuple(nn)))
                        if dst is not None:
                            rr.append(src);cc.append(dst);vv.append(rate)
                        exit_rate+=rate
            if b>0:
                if self.koff>0:
                    nn=list(n);nn[self.bind]+=1
                    dst=ix.get((b-1,tuple(nn)))
                    if dst is not None:
                        rr.append(src);cc.append(dst);vv.append(b*self.koff)
                    exit_rate+=b*self.koff
                if self.kcat>0:
                    nn=list(n);nn[self.product]+=1
                    dst=ix.get((b-1,tuple(nn)))
                    if dst is not None:
                        rr.append(src);cc.append(dst);vv.append(b*self.kcat)
                    exit_rate+=b*self.kcat
            rr.append(src);cc.append(src);vv.append(-exit_rate)
        R=coo_matrix((vv,(rr,cc)),shape=(D,D)).tocsr()
        # Candidate-induced state changes. Self-loops are omitted exactly; an
        # untagged selection at m=K is a killed transition (dest=-1).
        esrc=[];edst=[];ecoef=[];eweight=[]
        candidate_rate=self.catalysts*self.lam
        for src,(b,n) in enumerate(states):
            m=sum(n)+b; U=N-m
            free_fraction=(self.catalysts-b)/self.catalysts
            if free_fraction<=0: continue
            if n[self.bind]>0:
                nn=list(n);nn[self.bind]-=1
                dest=(b+1,tuple(nn))
                esrc.append(src);edst.append(ix[dest]);ecoef.append(-1)
                eweight.append(free_fraction*n[self.bind]/N)
            if U<=0: continue
            base=free_fraction*U/N
            for a in range(q):
                if a==self.bind:
                    dest=(b+1,n)
                else:
                    nn=list(n);nn[a]+=1;dest=(b,tuple(nn))
                dst=ix.get(dest)
                if m>=K or dst is None:
                    # m=K guarantees no tag-cap state exists. A missing state
                    # below K can only be an impossible new product draw when
                    # product is structurally absorbing and initially absent.
                    if m>=K:
                        esrc.append(src);edst.append(-1);ecoef.append(a);eweight.append(base)
                    continue
                esrc.append(src);edst.append(dst);ecoef.append(a);eweight.append(base)
        esrc=np.asarray(esrc,dtype=np.int64);edst=np.asarray(edst,dtype=np.int64)
        ecoef=np.asarray(ecoef,dtype=np.int64);eweight=np.asarray(eweight,dtype=float)
        order=np.argsort(esrc);esrc=esrc[order];edst=edst[order];ecoef=ecoef[order];eweight=eweight[order]
        f0=np.zeros(D);f0[ix[(0,(0,)*q)]]=1.0
        def rhs(t,f):
            out=R.T@f
            if candidate_rate and len(esrc):
                p=self.mu0@expm(self.Q*t)
                factors=np.where(ecoef<0,1.0,p[np.maximum(ecoef,0)])
                rates=candidate_rate*eweight*factors*f[esrc]
                # Capped transitions are cemetery loss; all other candidate
                # transitions conserve mass within this finite state set.
                keep=edst>=0
                np.add.at(out,edst[keep],rates[keep])
                np.add.at(out,esrc,-rates)
            return out
        sol=solve_ivp(rhs,(0.0,T),f0,method="DOP853",rtol=rtol,atol=atol,max_step=max_step)
        if not sol.success: raise RuntimeError(sol.message)
        f=sol.y[:,-1]; pT=self.mu0@expm(self.Q*T); lower=0.0
        for mass,(b,n) in zip(f,states):
            if mass<=0 or (observed_bound is not None and b!=observed_bound): continue
            U=N-sum(n)-b
            if U<0: continue
            if partial:
                contribution=partial_multinomial_pmf(obs,n,U,pT)
            else:
                residual=tuple(obs[a]-n[a] for a in range(q))
                if any(x<0 for x in residual) or sum(residual)!=U: continue
                contribution=multinomial_pmf(residual,pT)
            lower+=float(mass)*contribution
        tail=float(poisson.sf(K,candidate_rate*T))
        return UniqueMarkResult(lower,tail,float(f.sum()),D,rtol,atol,perf_counter()-start)
