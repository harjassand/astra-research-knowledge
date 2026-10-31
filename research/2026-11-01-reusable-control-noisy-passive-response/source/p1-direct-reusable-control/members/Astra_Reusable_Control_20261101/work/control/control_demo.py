#!/usr/bin/env python3
"""Counts-free calibrated-interval emulator and exact LP-dual certificates.

The source supplies only rational scalar intervals to the learner. A floating
LP/SLSQP solver proposes fits/actions/duals; Fraction arithmetic validates every
reported bound. This is an emulated apparatus, not physical measurements.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
from pathlib import Path
import json, time, argparse
import numpy as np
from scipy.optimize import linprog, minimize

HERE=Path(__file__).resolve().parent
OUT=HERE/'results'
OUT.mkdir(exist_ok=True)
ZERO=Q(0); ONE=Q(1)

def dot(a,b): return sum((x*y for x,y in zip(a,b)),ZERO)
def det(A):
    A=[list(map(Q,row)) for row in A]; n=len(A); out=ONE
    for j in range(n):
        p=next((p for p in range(j,n) if A[p][j]),None)
        if p is None: return ZERO
        if p!=j: A[p],A[j]=A[j],A[p]; out=-out
        v=A[j][j]; out*=v
        for i in range(j+1,n):
            t=A[i][j]/v
            for k in range(j+1,n): A[i][k]-=t*A[j][k]
    return out

def subsets(n,r):
    return [s for j in range(1,min(n,r)+1) for s in combinations(range(n),j)]
def mons(x,ss):
    return [np.prod([x[i] for i in s]) if not isinstance(x[0],Q)
            else prodq([x[i] for i in s]) for s in ss]
def prodq(vals):
    z=ONE
    for v in vals: z*=v
    return z
def dmons(x,ss,i):
    return [prodq([x[j] for j in s if j!=i]) if i in s else ZERO for s in ss]
def compositions(k,n):
    if n==1:
        yield (k,); return
    for j in range(k+1):
        for rest in compositions(k-j,n-1): yield (j,)+rest
def lattice(n,k):
    return [tuple(Q(a,k) for a in c[1:]) for c in compositions(k,n+1)]
def coeffs(B,g,ss):
    d=[]; b=[]
    for s in ss:
        C=[[B[i][j] for j in s] for i in s]
        d.append(det(C))
        b.append(det([[B[i][j]+g[i]*g[j] for j in s] for i in s])-d[-1])
    return d,b
def response(x,d,b,ss):
    m=mons(x,ss); return dot(m,b)/(ONE+dot(m,d))
def qr(x,den=10**12): return Q(int(round(float(x)*den)),den)
def recordq(x):
    if isinstance(x,Q): return {'fraction':str(x),'float':float(x)}
    if isinstance(x,dict): return {k:recordq(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [recordq(v) for v in x]
    if isinstance(x,np.generic): return x.item()
    return x

class IntervalLearner:
    def __init__(self,n,r,q,records):
        self.n=n; self.ss=subsets(n,r); self.p=len(self.ss)
        self.ub=[q**len(s) for s in self.ss]+[len(s)**2*q**(len(s)-1) for s in self.ss]
        self.A=[]; self.b=[]
        for x,y,eta in records:
            m=mons(x,self.ss); lo=y-eta; hi=y+eta
            self.A.append([lo*v for v in m]+[-v for v in m]); self.b.append(-lo)
            self.A.append([-hi*v for v in m]+[v for v in m]); self.b.append(hi)
        self.Af=np.array(self.A,float); self.bf=np.array(self.b,float)
        sol=linprog(np.zeros(2*self.p),A_ub=self.Af,b_ub=self.bf,
                    bounds=[(0,float(v)) for v in self.ub],method='highs',
                    options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
        if not sol.success: raise RuntimeError(sol.message)
        self.fit=sol.x; self.dual_records=[]

    def propose_value(self,x):
        m=np.array(mons(np.array(x,float),self.ss),float)
        return float(m@self.fit[self.p:]/(1+m@self.fit[:self.p]))

    def certify_ratio(self,x,cnum,c0=ZERO):
        """Upper bound max (c0+cnum.theta)/(1+m.d), exact dual residual repair."""
        m=mons(x,self.ss); v=2*self.p
        A=[row+[-rhs] for row,rhs in zip(self.A,self.b)]
        b=[ZERO]*len(A)
        # z_j <= upper_j t. Also explicit finite coordinate bounds, used below.
        for j,U in enumerate(self.ub):
            row=[ZERO]*(v+1); row[j]=ONE; row[-1]=-U; A.append(row); b.append(ZERO)
        eq=m+[ZERO]*self.p+[ONE]; c=list(cnum)+[c0]
        upper=self.ub+[ONE]
        sol=linprog(-np.array(c,float),A_ub=np.array(A,float),b_ub=np.zeros(len(A)),
                    A_eq=np.array([eq],float),b_eq=[1.],bounds=[(0,float(U)) for U in upper],
                    method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
        if not sol.success: raise RuntimeError(sol.message)
        lam=[max(ZERO,qr(-t)) for t in sol.ineqlin.marginals]
        nu=qr(-sol.eqlin.marginals[0])
        residual=[c[j]-sum((lam[i]*A[i][j] for i in range(len(A))),ZERO)-nu*eq[j] for j in range(v+1)]
        bound=nu+dot(lam,b)+sum((max(ZERO,z)*U for z,U in zip(residual,upper)),ZERO)
        # This exact algebraic certificate is valid for all feasible coefficients.
        proof={'kind':'linear_fractional_upper','x':[str(t) for t in x],
               'objective':[str(t) for t in cnum],'constant':str(c0),
               'dual_nonzero':[[i,str(t)] for i,t in enumerate(lam) if t],
               'equality_dual':str(nu),'residual_box_repair':str(sum((max(ZERO,z)*U for z,U in zip(residual,upper)),ZERO)),
               'upper_bound':str(bound),'solver_proposal':-float(sol.fun)}
        self.dual_records.append(proof)
        return bound

    def interval(self,x):
        m=mons(x,self.ss); c=[ZERO]*self.p+m
        hi=self.certify_ratio(x,c); lo=-self.certify_ratio(x,[-z for z in c])
        return max(ZERO,lo),min(ONE,hi)

    def gradients(self,x,lo,hi):
        lows=[]; highs=[]
        for i in range(self.n):
            dm=dmons(x,self.ss,i)
            # N_i - f D_i, with nonnegative D_i.
            high=self.certify_ratio(x,[-lo*t for t in dm]+dm)
            low=-self.certify_ratio(x,[hi*t for t in dm]+[-t for t in dm])
            lows.append(max(ZERO,low)); highs.append(max(ZERO,high))
        return lows,highs

def run(fixture='gram'):
    global OUT
    OUT=HERE/('results' if fixture=='gram' else 'network_results')
    OUT.mkdir(exist_ok=True)
    started=time.time(); n=3; q=Q(4); r=3; k=6
    if fixture=='gram':
        B=[[Q(4),Q(2),Q(2)],[Q(2),Q(4),Q(-2)],[Q(2),Q(-2),Q(4)]]
        g=[ONE,ZERO,ZERO]
    else:
        # Actual ideal resistor network: four hidden nodes with rail-set
        # baseline potentials (0,1/2,1/2,1), total anchor conductance1/2
        # each, and three controllable adjacent-node conductances. Normalize
        # physical gain by L=delta*G^2=1/4; hence normalized g=(1,0,1).
        B=[[Q(4),Q(-2),ZERO],[Q(-2),Q(4),Q(-2)],[ZERO,Q(-2),Q(4)]]
        g=[ONE,ZERO,ONE]
    ss=subsets(n,r); d,b=coeffs(B,g,ss)
    assert all(det([[B[i][j] for j in s] for i in s])>=0 for s in ss)
    nodes=lattice(n,k); eta=Q(1,10**6)
    rng=np.random.default_rng(410271)
    records=[]; raw_records=[]
    physical_scale=Q(1,4) if fixture=='network' else ONE
    baseline_current=Q(1,4) if fixture=='network' else ZERO
    current_radius=eta*physical_scale/2
    baseline_error=Q(int(rng.integers(-1000,1001)),1000)*current_radius if fixture=='network' else ZERO
    observed_baseline=baseline_current+baseline_error
    for x in nodes:
        exact=response(x,d,b,ss)
        if fixture=='network':
            raw_error=Q(int(rng.integers(-1000,1001)),1000)*current_radius if any(x) else baseline_error
            raw=baseline_current+physical_scale*exact+raw_error
            y=(raw-observed_baseline)/physical_scale
            raw_records.append({'x':list(map(str,x)),'raw_current':str(raw),'absolute_radius':str(current_radius)})
        else:
            noise=Q(int(rng.integers(-1000,1001)),1000)*eta
            y=exact+noise
        records.append((x,y,eta))
    learner=IntervalLearner(n,r,q,records)
    theta=d+b
    assert all(dot(row,theta)<=rhs for row,rhs in zip(learner.A,learner.b))
    tasks=[('all_controls',[ZERO]*n,[ONE]*n,ONE),
           ('price_change',[Q(1,20),ZERO,Q(1,5)],[ONE]*n,ONE),
           ('actuator_2_unavailable',[ZERO]*n,[ONE,ZERO,ONE],ONE),
           ('half_budget',[ZERO]*n,[ONE]*n,Q(1,2))]
    outputs=[]
    for name,cost,caps,budget in tasks:
        cf=np.array(cost,float); capf=np.array(caps,float); bf=float(budget)
        constraints=[{'type':'ineq','fun':lambda x,bf=bf:bf-np.sum(x)}]
        start=np.minimum(capf,bf/(n+1))
        proposal=minimize(lambda x: -learner.propose_value(x)+cf@x,start,
                          method='SLSQP',bounds=[(0,float(v)) for v in caps],constraints=constraints,
                          options={'ftol':1e-13,'maxiter':500})
        if not proposal.success: raise RuntimeError(proposal.message)
        # Rational feasible action. Flooring keeps every budget/cap constraint.
        x=tuple(Q(max(0,int(np.floor(float(t)*10**7))),10**7) for t in proposal.x)
        assert sum(x)<=budget and all(xi<=cap for xi,cap in zip(x,caps))
        lo,hi=learner.interval(x); gl,gu=learner.gradients(x,lo,hi)
        # Linear maximization over a box-constrained simplex, exact greedy.
        left=budget; linearmax=ZERO
        for i in sorted(range(n),key=lambda i:gu[i]-cost[i],reverse=True):
            if gu[i]<=cost[i]: continue
            z=min(left,caps[i]); linearmax+=(gu[i]-cost[i])*z; left-=z
        regret=max(ZERO,linearmax-dot([gl[i]-cost[i] for i in range(n)],x))
        actual=response(x,d,b,ss)-dot(cost,x)
        def trueval(z):
            m=np.array(mons(np.array(z,float),ss),float)
            return float(m@np.array(b,float)/(1+m@np.array(d,float))-cf@z)
        oracle=minimize(lambda z:-trueval(z),start,method='SLSQP',bounds=[(0,float(v)) for v in caps],
                        constraints=constraints,options={'ftol':1e-14,'maxiter':500})
        truth_gradient=[]
        D=ONE+dot(mons(x,ss),d); F=response(x,d,b,ss)
        for i in range(n): truth_gradient.append((dot(dmons(x,ss,i),b)-F*dot(dmons(x,ss,i),d))/D)
        assert lo<=response(x,d,b,ss)<=hi
        assert all(a<=t<=b1 for a,t,b1 in zip(gl,truth_gradient,gu))
        assert max(0,-float(oracle.fun)-float(actual))<=float(regret)+1e-10
        outputs.append({'task':name,'action':x,'response_interval':[lo,hi],
                        'reward_interval':[lo-dot(cost,x),hi-dot(cost,x)],
                        'gradient_lower':gl,'gradient_upper':gu,
                        'certified_global_regret':regret,
                        'emulator_true_reward':actual,
                        'known_source_optimizer_diagnostic':-float(oracle.fun),
                        'known_source_regret_diagnostic':max(0,-float(oracle.fun)-float(actual)),
                        'additional_source_calls':0})
    # Readout-only diagnostic on a held-out grid, not the basis of the certificate.
    hold=lattice(n,31)
    errs=[abs(learner.propose_value(x)-float(response(x,d,b,ss))) for x in hold]
    report={'source_contract':'fixed affine PSD rank-one intervention; exact rational interval emulator',
            'fixture':fixture,'physical_gain_scale':Q(1,4) if fixture=='network' else ONE,
            'baseline_subtraction':fixture=='network','baseline_included_in_settings':True,
            'n':n,'r':r,'k':k,'q':q,'normalized_reward_bound':1,
            'settings':len(nodes),'coefficient_variables':2*len(ss),
            'calibrated_error_per_setting':eta,
            'sensor_model':'deterministic absolute-error cap, simulated rational errors; no physical apparatus or Bernoulli count claim',
            'active_setting_writes':sum(sum(t>0 for t in x) for x in nodes),
            'reset_operations':len(nodes),'heldout_grid_points':len(hold),
            'heldout_max_float_error':max(errs),'tasks':outputs,
            'dual_certificate_count':len(learner.dual_records),
            'seconds':time.time()-started}
    (OUT/'demo_results.json').write_text(json.dumps(recordq(report),indent=2))
    (OUT/'dual_certificates.json').write_text(json.dumps(learner.dual_records,indent=2))
    (OUT/'scalar_records.json').write_text(json.dumps([{'x':list(map(str,x)),'y':str(y),'eta':str(e)} for x,y,e in records],indent=2))
    if fixture=='network':
        (OUT/'raw_current_records.json').write_text(json.dumps({'physical_gain_scale':str(physical_scale),
            'observed_zero_current':str(observed_baseline),'zero_current_radius':str(current_radius),
            'records':raw_records},indent=2))
    print(json.dumps(recordq(report),indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--fixture',choices=['gram','network'],default='gram')
    run(parser.parse_args().fixture)
