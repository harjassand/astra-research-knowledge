"""Finite-network counterexample to independent-motif selective arrest.

Four two-arm junctions, distinguishable arms, reversible two-bond exchange,
and perfect non-loop locking. All clocks are declared synthetic diagnostics.
No measured chemistry, microscopic force classifier, or network simulation
with spatially resolved polymer conformations is claimed.
"""
from pathlib import Path
from functools import lru_cache
from fractions import Fraction
import itertools
import json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve,expm_multiply

OUT=Path(__file__).resolve().parent
V=4
canonical=lambda edges:tuple(sorted(tuple(sorted(e)) for e in edges))
INITIAL=((),canonical([(0,1),(2,4),(5,6),(3,7)]))
TYPED_INITIAL=((),canonical([(0,1),(2,5),(4,7),(3,6)]))

def compatible(edge,typed):
    # In the typed model even arms are 3'OH and odd arms are 5'phosphate.
    # Sequence compatibility is universal within these two types.
    return not typed or edge[0]%2!=edge[1]%2

def remaining_degrees(open_edges):
    return tuple(sum(s//2==v for edge in open_edges for s in edge) for v in range(V))

def feasible_loopfree(open_edges):
    d=remaining_degrees(open_edges)
    return 2*max(d,default=0)<=sum(d)

def connected(edges):
    reached={0}
    while True:
        enlarged=reached|{s//2 for a,b in edges for s in (a,b)
                          if a//2 in reached or b//2 in reached}
        if enlarged==reached:return len(reached)==V
        reached=enlarged

@lru_cache(None)
def pairings(stubs):
    if not stubs:return ((),)
    a=stubs[0];out=[]
    for idx,b in enumerate(stubs[1:],1):
        rest=stubs[1:idx]+stubs[idx+1:]
        for m in pairings(rest):out.append(canonical(((a,b),)+m))
    return tuple(out)

@lru_cache(None)
def feasible_connected(locked,stubs,typed=False):
    return any(all(a//2!=b//2 and compatible((a,b),typed) for a,b in m) and connected(locked+m)
               for m in pairings(stubs))

def transitions(state,policy,kappa,nu=1.,typed=False):
    locked,opened=state;events={}
    for k,(a,b) in enumerate(opened):
        if a//2==b//2:continue # perfect loop classifier; no false locks
        newopen=opened[:k]+opened[k+1:]
        newlock=canonical(locked+((a,b),))
        if policy=='stub_guard' and not feasible_loopfree(newopen):continue
        if policy=='connected_guard':
            stubs=tuple(sorted(s for e in newopen for s in e))
            if not feasible_connected(newlock,stubs,typed):continue
        nxt=(newlock,newopen)
        events[nxt]=events.get(nxt,0.)+kappa
    # Every pair of unlocked bonds can undergo either alternative pairing.
    # This intentionally generous mixing assumption cannot remove the jam.
    for i,j in itertools.combinations(range(len(opened)),2):
        a,b=opened[i];c,d=opened[j]
        untouched=tuple(e for z,e in enumerate(opened) if z not in (i,j))
        for alternate in [((a,c),(b,d)),((a,d),(b,c))]:
            if not all(compatible(edge,typed) for edge in alternate):continue
            nxt=(locked,canonical(untouched+alternate))
            if nxt!=state:events[nxt]=events.get(nxt,0.)+(nu if typed else nu/2)
    return events

def topology(state):
    locked,opened=state;edges=locked+opened
    loops=sum(a//2==b//2 for a,b in edges)
    return loops,connected(edges)

def solve(policy,kappa,typed=False):
    initial_state=TYPED_INITIAL if typed else INITIAL
    states=[initial_state];ix={initial_state:0};eventlist=[]
    for state in states:
        assert all(compatible(edge,typed) for edge in state[0]+state[1])
        events=transitions(state,policy,kappa,typed=typed)
        eventlist.append(events)
        for nxt in events:
            if nxt not in ix:ix[nxt]=len(states);states.append(nxt)
    transient=[i for i,e in enumerate(eventlist) if e]
    terminal=[i for i,e in enumerate(eventlist) if not e]
    tx={old:new for new,old in enumerate(transient)}
    rows=[];cols=[];vals=[]
    sinks=np.zeros((len(transient),3))
    for old in transient:
        i=tx[old];ev=eventlist[old]
        rows.append(i);cols.append(i);vals.append(-sum(ev.values()))
        for st,rate in ev.items():
            j=ix[st]
            if j in tx:rows.append(i);cols.append(tx[j]);vals.append(rate)
            else:
                loops,conn=topology(st)
                cat=2 if loops else (0 if conn else 1)
                sinks[i,cat]+=rate
    q=coo_matrix((vals,(rows,cols)),shape=(len(transient),len(transient))).tocsr()
    probs=spsolve(-q,sinks)
    mean=spsolve(-q,np.ones(len(transient)))
    initial=tx[0]
    residual=max(float(np.max(np.abs(q@probs+sinks))),float(np.max(np.abs(q@mean+1))))
    assert residual<1e-8
    assert np.max(np.abs(probs.sum(axis=1)-1))<1e-9
    # Finite-duration unconditional masses, including all unfinished states.
    # Add three absorbing categories to the generator explicitly.
    rr=list(rows);cc=list(cols);vv=list(vals);nt=len(transient)
    for i in range(nt):
        for j in range(3):
            if sinks[i,j]:rr.append(i);cc.append(nt+j);vv.append(sinks[i,j])
    full=coo_matrix((vv,(rr,cc)),shape=(nt+3,nt+3)).tocsr()
    p0=np.zeros(nt+3);p0[initial]=1
    tt=2*mean[initial]
    pt=expm_multiply(full.T*tt,p0)
    k=Fraction(str(kappa));nu=Fraction(1)
    jam_bound=(3*k/(3*k+6*nu))*(2*k/(2*k+3*nu))*(k/(k+nu))
    ans={
        'policy':policy,'arm_chemistry':'opposite_polarity_only' if typed else 'untyped',
        'kappa_over_nu':kappa,'reachable_states':len(states),
        'transient_states':len(transient),'terminal_states':len(terminal),
        'final_connected_loopfree_probability':float(probs[initial,0]),
        'final_disconnected_loopfree_probability':float(probs[initial,1]),
        'final_one_loop_jam_probability':float(probs[initial,2]),
        'mean_absorption_time_in_nu_inverse':float(mean[initial]),
        'linear_equation_max_residual':residual,
        'finite_duration':float(tt),
        'finite_connected_loopfree_mass':float(pt[-3]),
        'finite_disconnected_loopfree_mass':float(pt[-2]),
        'finite_jam_mass':float(pt[-1]),
        'finite_unfinished_mass':float(pt[:-3].sum()),
        'initial_three_locks_first_jam_probability_lower_bound':str(jam_bound) if policy=='unrestricted' else 'not applicable',
    }
    if policy=='unrestricted':assert probs[initial,2]>=float(jam_bound)-1e-10
    if policy=='stub_guard':assert probs[initial,2]<1e-10
    if policy=='connected_guard':assert probs[initial,0]>1-1e-10
    return ans

def main():
    # Exhaustive verification of the pairing feasibility criterion on this
    # finite instance. The general proof is in COLLECTIVE_CAPTURE.txt.
    checked=0
    for mask in range(1<<(2*V)):
        stubs=tuple(s for s in range(2*V) if mask>>s&1)
        if len(stubs)%2:continue
        d=[sum(s//2==v for s in stubs) for v in range(V)]
        condition=2*max(d,default=0)<=sum(d)
        actual=any(all(a//2!=b//2 for a,b in m) for m in pairings(stubs))
        assert condition==actual
        checked+=1
    results=[]
    typed_checked=0
    for mask in range(1<<(2*V)):
        stubs=tuple(s for s in range(2*V) if mask>>s&1)
        if sum(s%2==0 for s in stubs)!=sum(s%2==1 for s in stubs):continue
        d=[sum(s//2==v for s in stubs) for v in range(V)]
        condition=2*max(d,default=0)<=sum(d)
        actual=any(all(a//2!=b//2 and compatible((a,b),True) for a,b in m) for m in pairings(stubs))
        assert condition==actual
        typed_checked+=1
    for typed in [False,True]:
        for policy in ['unrestricted','stub_guard','connected_guard']:
            for k in [.1,1.,10.]:
                r=solve(policy,k,typed);results.append(r);print(json.dumps(r),flush=True)
    payload={'status':'EXACT_FINITE_STATE_MODEL_TO_NUMERICAL_LINEAR_ALGEBRA_TOLERANCE',
             'initial_edges_by_vertex':'A-A, B-C, C-D, D-B',
             'number_of_junctions':V,'arms_per_junction':2,
             'model':'distinguishable-arm pairings; symmetric two-bond exchanges; perfect non-loop lock',
             'rate_provenance':'synthetic diagnostic clocks, not acquired chemical rates',
             'loopfree_feasibility_subsets_exhaustively_checked':checked,
             'typed_balanced_feasibility_subsets_exhaustively_checked':typed_checked,
             'typed_scope':'One OH and one phosphate per vertex; universal sequence compatibility; a unique allowed re-pairing per edge pair at total rate nu. Not an acquired ligation model.',
             'physical_guard_interface':'UNKNOWN; guards explicitly require global network information',
             'retained_stiffness_or_toughness':'NOT INFERRED from primary-loop or connectivity counts',
             'cases':results}
    (OUT/'collective_capture_results.json').write_text(json.dumps(payload,indent=2)+'\n')

if __name__=='__main__':main()
