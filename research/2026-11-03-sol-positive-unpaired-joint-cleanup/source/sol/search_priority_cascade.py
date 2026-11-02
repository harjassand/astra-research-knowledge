#!/usr/bin/env python3
"""Finite adversarial search of a proposed service-priority cleanup.

Hot majorities are taken large enough for all explored steps. This is
a combinatorial diagnostic; probabilities and physical time are separate.
Both growth sources remain in the actual model. For maximising mass,
source2 dominates source1 whenever enabled: they have the SAME anchor/
minority output, and source2 adds one more hot molecule.
"""
from collections import deque
from pathlib import Path
import json

P=Path(__file__).resolve().parent

def service(a,d,c,f):
    if a and d:return max(a,d)>=3 and c//2+f//2>0
    return (a>=3 and c>=2) or (d>=3 and f>=2)

def search(c0,f0,birth_cap=3,anchor_cap=15,cold_cap=15,depth_cap=80):
    # key=(a,d,c,f,N0). value=(mass reward N2-T, path, noncore depth)
    root=(1,0,c0,f0,1)
    best={root:(0,('I0',),1)};todo=deque([root]);exits=[];cut=False
    while todo:
        key=todo.popleft();reward,path,depth=best[key]
        a,d,c,f,n0=key
        if depth>=depth_cap:cut=True;continue
        transitions=[]
        if a and d:
            if c>=2:transitions.append(((a,d,c-2,f+2,n0),0,'COREf',0))
            if f>=2:transitions.append(((a,d,c+2,f-2,n0),0,'COREb',0))
        if service(a,d,c,f):
            if a>=3 and c>=2:transitions.append(((a-3,d,c-2,f,n0),-1,'I3',1))
            if d>=3 and f>=2:transitions.append(((a,d-3,c,f-2,n0),-1,'II3',1))
        else:
            for port,(anchor,cold) in enumerate(((a,c),(d,f))):
                out=[a,d,c,f,n0]
                if anchor:
                    s=2 if anchor>=2 and cold else 1
                    out[port]+=1;out[port+2]+=1
                    transitions.append((tuple(out),int(s==2),('I' if port==0 else 'II')+str(s),1))
                elif n0<birth_cap:
                    out[port]=1;out[4]+=1
                    transitions.append((tuple(out),0,('I' if port==0 else 'II')+'0',1))
        for nxt,inc,label,dt in transitions:
            nr=reward+inc;np=path+(label,);nd=depth+dt
            if nxt[0]==nxt[1]==0:
                exits.append({'initial_cold':[c0,f0],'reward_N2_minus_T':nr,
                              'final_cold':nxt[2:4],'births':nxt[4],'word':np})
                if nr>0:return exits[-1],len(best),cut
                continue
            if max(nxt[:2])>anchor_cap or max(nxt[2:4])>cold_cap:
                cut=True;continue
            old=best.get(nxt)
            if old is None or nr>old[0] or (nr==old[0] and nd<old[2]):
                best[nxt]=(nr,np,nd);todo.append(nxt)
    return max(exits,key=lambda v:v['reward_N2_minus_T']) if exits else None,len(best),cut

def main():
    out=[]
    for c in range(8):
        for f in range(8):
            witness,size,cut=search(c,f)
            out.append({'case':[c,f],'states':size,'capped_search':cut,'best_exit':witness})
            if witness and witness['reward_N2_minus_T']>0:
                print(json.dumps(out[-1],indent=2))
                (P/'results/priority_cascade_search.json').write_text(json.dumps(out,indent=2)+'\n')
                return
    (P/'results/priority_cascade_search.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'cases':len(out),'max_reward':max(v['best_exit']['reward_N2_minus_T'] for v in out if v['best_exit']),
                      'states':sum(v['states'] for v in out),'capped_cases':sum(v['capped_search'] for v in out)},indent=2))

if __name__=='__main__':main()
