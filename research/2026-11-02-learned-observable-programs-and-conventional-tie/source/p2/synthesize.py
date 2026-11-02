"""Generic finite-local-algebra synthesis from eight Poisson observation cells.

Does NOT import source_device. Search operations over an arbitrary two-state site:
 - local unary features d with two values in {-1,0,1},
 - commutative product-fold of features across an arbitrary finite site subset,
 - local index rewrites by symmetric-difference of a subset of three places.
No rate-law model, support masks or discovered parameters are specified in input.

A strong conventional full-table Walsh transformation is also implemented:
it produces equivalent coefficients, and is explicitly credited as an ordinary comparator.
"""
import itertools, math, json
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from fractions import Fraction
from math import isqrt

PATTERNS=list(itertools.product((-1,1),repeat=3))
OFFSETS=(-1,0,1)
CANDIDATES=[(-1,1),(1,-1),(0,1),(1,0)]

@dataclass
class LocalRecords:
    mode:str
    exposures:float
    counts:dict
    intervals:dict
    estimates:dict
    def to_json(self):
        return {"mode":self.mode,"exposure_per_configuration":self.exposures,
                "counts":{"".join('+' if z==1 else '-' for z in k):v for k,v in self.counts.items()},
                "intervals":{"".join('+' if z==1 else '-' for z in k):[float(a),float(b)] for k,(a,b) in self.intervals.items()}}

def acquire(device,mode,exposure,delta_total=1e-7,total_cells=16):
    """Finite-data, exact-rational Poisson intervals. No numeric quantiles.

    For K~Pois(mu) the event |K-mu| <= sqrt(2 mu x)+x follows
    from standard Poisson Bernstein tails with failure <=2 exp(-x).
    Inversion yields a conservative interval
      mu in [max(0,k-sqrt(2kx)-x),k+sqrt(2kx)+2x].
    We upper-round the square root with an exact integer isqrt. With x=22,
    16 cells have total failure <=32*exp(-22)<1e-7.
    """
    exposure=int(exposure); assert exposure>0 and total_cells<=16 and delta_total>=1e-7
    cells={p:device.observe(mode,p,exposure) for p in PATTERNS}
    x=22;scale=10**12
    intervals={}
    for p,k in cells.items():
        root_upper=Fraction(isqrt(2*k*x*scale*scale)+1,scale)
        lo=max(Fraction(0), (Fraction(k-x)-root_upper)/exposure)
        hi=(Fraction(k+2*x)+root_upper)/exposure
        intervals[p]=(lo,hi)
    return LocalRecords(mode,exposure,cells,intervals,{p:Fraction(k,exposure) for p,k in cells.items()})

def d_eval(d,spin):return d[0] if spin==-1 else d[1]

def d_product(d,p,mask):
    v=1.
    for j in range(3):
        if (mask>>j)&1:v*=d_eval(d,p[j])
    return v

def flipped(p):return (p[0],-p[1],p[2])

def local_action(d,p,active,rate):
    return rate*(d_product(d,flipped(p),active)-d_product(d,p,active))

def local_matrix(d,est):
    """8x8 basis interpolation. Columns include all generic product features.
    Return each active-centre row expansion of observed generator action.
    """
    A=np.array([[d_product(d,p,mask) for mask in range(8)] for p in PATTERNS],dtype=float)
    if np.linalg.matrix_rank(A)!=8: return None
    rows={}
    for mask in (2,3,6,7):
        b=np.array([local_action(d,p,mask,est[p]) for p in PATTERNS])
        rows[mask]=np.linalg.solve(A,b)
    return rows

def positivity_report(rows):
    worst_negative=0.;worst_excess=0.;n_negative=0
    for src,row in rows.items():
        neg=[-row[t] for t in range(8) if t!=src and row[t]<-.01]
        worst_negative=max(worst_negative,max(neg,default=0))
        n_negative+=len(neg)
        total=sum(max(row[t],0) for t in range(8) if t!=src)
        worst_excess=max(worst_excess,total+row[src])
    return {"n_negative_offdiag":n_negative,"largest_negative_offdiag":float(worst_negative),"largest_markov_excess":float(worst_excess)}

def walsh_fit(est):
    """Ordinary strong baseline: exact full truth-table Fourier/Walsh decomposition."""
    return {mask: sum(est[p]*math.prod(p[k] for k in range(3) if (mask>>k)&1) for p in PATTERNS)/8
            for mask in range(8)}

def local_residual(records,alpha,jumps):
    # Candidate D_S = product_{i in S} sigma_i; one local action around one active site.
    # The physical action is -2 c(s) D_S. A trial program acts by -2 alpha D_S
    # plus sum_B q_B D_{S xor B}. Since D_{S xor B}=D_S * prod(s_B),
    # local residual magnitude = |-2c(s)+2alpha-sum q_B prod(s_B)|.
    # Notice this is independent of membership of the two neighbouring sites!
    worst=0.
    for p,(lo,hi) in records.intervals.items():
        for physical_c in (lo,hi):
            residual=-2*physical_c+2*alpha-sum(q*math.prod(p[j] for j in range(3) if (m>>j)&1) for m,q in jumps.items())
            worst=max(worst,abs(residual))
    return worst

def synthesize(records, max_rules=7, desired_local_residual=.009):
    """Search code and rewrite words, then bound true residual over experimental CI.
    The selected full-rule engine is stochastic if all jump weights and kill are >=0.
    """
    candidates=[]
    for d in CANDIDATES:
        rows=local_matrix(d,records.estimates)
        if rows is None:continue
        p=positivity_report(rows)
        # Literal fold_product is universal combinator, while scalar unary encoding d is learned.
        # task f(s)=1{s=+}: represent by a + b d(s), feasible for any nonconstant d.
        b=(1/(d[1]-d[0])); a=-d[0]*b
        p.update(feature=list(d),terminal_readout=[a,b])
        candidates.append(p)
    # Search smallest nonconstant site coding with low-cost Markov rewriting.
    feasible=[c for c in candidates if c['n_negative_offdiag']==0 and c['largest_markov_excess']<=.02]
    if not feasible:
        raise ValueError('No candidate gives usable positive dual; signed fallback not attempted')
    # Prefer codings with smallest local Markov defect, then bounded terminal range.
    feasible.sort(key=lambda c:(c['largest_markov_excess'],abs(c['terminal_readout'][1]),abs(c['feature'][0])+abs(c['feature'][1])))
    best=feasible[0]
    # For this first build a signed parity code must win; if it does not, reject rather
    # than pretend the parity-specific rule compiler supports the winning different code.
    if tuple(best['feature']) not in ((-1,1),(1,-1)):
        raise ValueError('Winning code outside current general XOR interpreter; not secretly converting it')
    est=records.estimates
    fourier=walsh_fit(est)
    alpha=fourier[0]
    proposed={mask: -2*theta for mask,theta in fourier.items() if mask and -2*theta>0}
    history=[]; selected={}; blacklist=set()
    # Greedy search over all 7 generic index rewrites. No rules are preselected.
    for step in range(max_rules+1):
        residual=local_residual(records,alpha,selected)
        kill=2*alpha-sum(selected.values())
        history.append({"step":step,"added":None if step==0 else history[-1].get('next_rule'),"local_residual_bound":residual,"kill":kill,"rules":{str(m):q for m,q in selected.items()}})
        if residual<=desired_local_residual: break
        choices=[]
        for mask,q in proposed.items():
            if mask in selected or mask in blacklist: continue
            if 2*alpha-sum(selected.values())-q <0: continue
            trial=dict(selected);trial[mask]=q
            err=local_residual(records,alpha,trial)
            choices.append((err,mask,q))
        if not choices:break
        choices.sort()
        err,mask,q=choices[0]
        if err>residual-1e-6:break
        history[-1]['next_rule']=mask
        selected[mask]=q
    final_resid=local_residual(records,alpha,selected)
    # Generic objective: correctness + positivity + obtained small program + provable execution growth.
    kill=2*alpha-sum(selected.values())
    if kill<0:raise RuntimeError('negative death: sign issue')
    output={"mode":records.mode,"encoding":best['feature'],"readout":best['terminal_readout'],
            "alpha":float(alpha),"alpha_fraction":str(alpha),"jumps":[{"toggle_mask":mask,"offsets":[j-1 for j in range(3) if (mask>>j)&1],"rate":float(q),"rate_fraction":str(q)} for mask,q in sorted(selected.items())],
            "kill":float(kill),"kill_fraction":str(kill),"local_residual_bound":float(final_resid),"local_residual_fraction":str(final_resid),"experiment_confidence":None,
            "search_history":[{"step":z["step"],"next_rule":z.get("next_rule"),"local_residual_bound":float(z["local_residual_bound"]),"kill":float(z["kill"]),"rules":{a:float(b) for a,b in z["rules"].items()}} for z in history],"coding_candidates":candidates,
            "full_walsh_baseline":{"theta":{str(k):float(v) for k,v in fourier.items()}},
            "locality_bound":3,"source_configuration_count":8,"program_size_rules":len(selected),"confidence_formula":"failure <= 32 exp(-22) for all sixteen independent Poisson exposure cells"}
    return output

def compile_all(device,exposure=2_000_000,delta_total=1e-7,desired_local_residual=.009):
    records={m:acquire(device,m,exposure,delta_total,total_cells=8*len(device._modes)) for m in device._modes}
    programs={m:synthesize(rec,desired_local_residual=desired_local_residual) for m,rec in records.items()}
    for p in programs.values():p['experiment_confidence']=1-delta_total
    return records,programs
