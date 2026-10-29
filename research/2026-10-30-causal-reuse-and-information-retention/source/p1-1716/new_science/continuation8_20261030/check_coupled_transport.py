#!/usr/bin/env python3
"""Construct a productive cycle and check forced population generators.
No acquired data, apparatus claim, or power lower bound is supplied.
"""
from collections import deque
from pathlib import Path
import hashlib, json, math, platform
import numpy as np
from check_event_memory import build


def base_events(seed):
    states, _, _, rows, _ = build(1., 'opposed', 1.)
    rng = np.random.default_rng(seed)
    factors, out = {}, []
    for i, row in enumerate(rows):
        rr = []
        for j, rate, inc, selected in row:
            channel = int(np.argmax(abs(inc))) if selected else -1
            key = (min(i,j), max(i,j), channel)
            if key not in factors:
                factors[key] = float(10**rng.uniform(-2,2))
            d = tuple(int(x) for x in inc)
            assert d[0]-d[1] == (states[i][1][0]-states[j][1][0])//2
            rr.append((j, rate*factors[key], d, channel))
        out.append(rr)
    for i, row in enumerate(out):
        for j, r, d, ch in row:
            rev = [q for k,q,e,c in out[j] if k==i and c==ch
                   and e==tuple(-x for x in d)]
            assert len(rev)==1 and abs(rev[0]-r)<1e-12
    return states,out


def productive_cycle(states, rows):
    start=(0,0,0); todo=deque([start]); parent={start:None}; end=None
    while todo:
        x=todo.popleft(); i,a,b=x
        if i==0 and a==b and a!=0:
            end=x; break
        for j,_,d,ch in rows[i]:
            y=(j,a+d[0],b+d[1])
            if max(abs(y[1]),abs(y[2]))>3 or y in parent: continue
            parent[y]=(x,d,ch); todo.append(y)
    assert end is not None
    path=[]; x=end
    while parent[x] is not None:
        prev,d,ch=parent[x]
        path.append({'from':prev[0],'to':x[0],'increment':d,'channel':ch})
        x=prev
    path.reverse()
    reachable={0}; queue=deque([0])
    while queue:
        i=queue.popleft()
        for j,_,_,_ in rows[i]:
            if j not in reachable: reachable.add(j); queue.append(j)
    assert len(reachable)==len(states)
    return {'joint_state_count':len(states),'irreducible_support':True,
            'states':[{'occupied_sites':[k for k in range(5) if mask>>k&1],
                       'u':bits[0]} for mask,bits in states],
            'cycle':path,'cycle_current':[end[1],end[2]]}


def forced_case(seed,h):
    states,rows=base_events(seed); n=len(states); L=np.zeros((n,n))
    forced=[]
    for i,row in enumerate(rows):
        rr=[]
        for j,r,d,ch in row:
            q=r*math.exp(float(np.dot(h,d)))
            L[i,j]+=q; L[i,i]-=q; rr.append((j,q,d,ch))
        forced.append(rr)
    mat=L.T.copy(); mat[-1,:]=1
    rhs=np.zeros(n); rhs[-1]=1
    pi=np.linalg.solve(mat,rhs)
    assert min(pi)>0
    currents=sum((pi[i]*q*np.array(d) for i,row in enumerate(forced)
                  for _,q,d,_ in row), start=np.zeros(2))
    entropy=0.
    for i,row in enumerate(forced):
        for j,q,d,ch in row:
            rev=next(v for k,v,e,c in forced[j] if k==i and c==ch
                     and e==tuple(-x for x in d))
            entropy+=pi[i]*q*math.log(pi[i]*q/(pi[j]*rev))
    expected_entropy=2*float(np.dot(h,currents))
    stationarity=float(max(abs(pi@L)))
    stall_residual=None
    if abs(sum(h))<1e-14:
        p=np.array([math.exp(-h[0]*bits[0]) for _,bits in states]); p/=p.sum()
        stall_residual=float(max(abs(p@L)))
        assert stall_residual<1e-11 and max(abs(currents))<1e-11
    else:
        assert sum(h)*currents[0]>0
    assert abs(currents[0]-currents[1])<1e-11
    assert abs(entropy-expected_entropy)<1e-10
    return {'seed':seed,'forces':h,'stationarity_residual':stationarity,
            'currents':currents.tolist(),'entropy_production':entropy,
            'entropy_identity_error':abs(entropy-expected_entropy),
            'stall_law_residual':stall_residual}


def main():
    states,rows=base_events(19)
    out={'scope':'Exact support witness and floating population generators only.',
         'python':platform.python_version(),'numpy':np.__version__,
         'productive_witness':productive_cycle(states,rows),
         'cases':[forced_case(seed,h) for seed in (19,104,2026)
                  for h in ((0.,0.),(.4,-.4),(.7,-.2),(-.3,.6),(-.5,.2))]}
    out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    target=Path(__file__).with_name('COUPLED_TRANSPORT_CHECK.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'cases':len(out['cases']),
                      'productive_cycle_length':len(out['productive_witness']['cycle']),
                      'cycle_current':out['productive_witness']['cycle_current'],
                      'max_entropy_identity_error':max(c['entropy_identity_error'] for c in out['cases']),
                      'output':str(target)},indent=2))


if __name__=='__main__': main()
