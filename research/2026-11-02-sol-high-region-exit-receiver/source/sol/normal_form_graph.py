#!/usr/bin/env python3
"""Finite overapproximation of maximal-source normalization motifs.

Core transfers preserve the pair difference and the parity of its minority.
Positive edges found here require actual-state reconciliation; graph identity
alone does not prove global recurrence or pay the physical clock.
"""
from collections import deque
from pathlib import Path
import json

P=Path(__file__).resolve().parent
# anchor 0,1,2, H0,H1,H2; minority 0,1,even>=2,odd>=3.
def increment_a(a):return {0:1,1:2,2:3,3:4,4:5,5:3}[a]
def terminal_a(a):return ((a-3),a) if a>=3 else ()
def inc_t(t):return {0:1,1:2,2:3,3:2}[t]
def plus2(t):return {0:2,1:3,2:2,3:3}[t]
def minus2(t):return {2:(0,2),3:(1,3)}.get(t,())
def odd(t):return int(t in (1,3))

def edges(v):
    a,r,t=v
    if a>=3 and t>=2:j=3
    elif a>=2 and t>=1:j=2
    elif a>=1 and (t>=1 or r>0):j=1
    else:j=0
    if j==3:
        for aa in terminal_a(a):
            for tt in minus2(t):yield (aa,r,tt),0,'max_terminal'
    else:
        rr=r+int(j==0)-int(j==1)
        dt=int(j==2 or (j==0 and r<0) or (j==1 and r>0))
        tt=inc_t(t) if dt else t
        # Twice Delta F; F=A-|r|-3t/2-odd(t)/2.
        delta2=2-2*(abs(rr)-abs(r))-3*dt-(odd(tt)-odd(t))
        yield (increment_a(a),rr,tt),delta2,'max_growth_'+str(j)
    if a>=1:
        yield (a,r,plus2(t)),0,'core_received_pair'
        for tt in minus2(t):yield (a,r,tt),0,'core_sent_pair'

def main():
    starts=[(a,0,0) for a in range(6)];back={v:None for v in starts};todo=deque(starts)
    positive=[];negative=[];escaped=[];checked=0
    while todo:
        v=todo.popleft()
        for u,delta,label in edges(v):
            checked+=1
            if delta>0:positive.append((v,u,delta,label))
            if delta<0:negative.append((v,u,delta,label))
            if abs(u[1])>8:escaped.append((v,u,label));continue
            if u not in back:back[u]=(v,label,delta);todo.append(u)
    def trace(v):
        out=[]
        while back[v] is not None:
            prev,label,delta=back[v];out.append({'from':prev,'to':v,'channel':label,'twice_delta_F':delta});v=prev
        return out[::-1]
    result={'overapproximation_states':len(back),'edges':checked,'residual_difference_range':[min(v[1] for v in back),max(v[1] for v in back)],
            'positive_edges':len(positive),'negative_edges':len(negative),'escape_edges':escaped,
            'first_positive_witness':None if not positive else trace(positive[0][0])+[{'from':positive[0][0],'to':positive[0][1],'channel':positive[0][3],'twice_delta_F':positive[0][2]}],
            'reachable_states':sorted(back),
            'scope':'Finite raw motif overapproximation; unconstrained peer supplies can introduce spurious paths. No physical-clock or recurrence claim.'}
    (P/'results').mkdir(exist_ok=True);(P/'results/normal_form_graph.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='reachable_states'},indent=2))

if __name__=='__main__':main()
