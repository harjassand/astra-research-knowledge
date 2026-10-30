"""Exhaustive all-basis-label check of the new I/A/C/B/Q/R machine.
Checks classical predicate identities underpinning operator no-creation;
not a substitute for quantum instruments/probability estimates.
"""
from itertools import product
from collections import Counter, deque
from pathlib import Path
import json
supports=[(0,1),(1,2)]; lengths=[2,1]; gate_targets=[(0,1),(1,)]
base=[]; phases=[]
for h,k in enumerate(map(len,supports)):
    b=[('I',0)]+[('A',i) for i in range(k+1)]+[('C',i) for i in range(lengths[h]+1)]+[('B',j,l) for j in range(lengths[h]+1) for l in range(j+1)]+[('Q',i) for i in range(k+1)]
    base.append(b)
    rr=[('R',p,j) for p in b for j in range(k) if p[0]!='Q' or j<p[1]]
    phases.append(b+rr)
lockoptions=[('f','o0','z0'),('f','o0','z0','o1','z1'),('f','o1','z1')]
def violates(h,p,j,l):
    own={f'o{h}',f'z{h}'}; typ=p[0]
    if typ=='I':return l in own
    if typ=='A':return l!=f'o{h}' if j<p[1] else l in own
    if typ in {'C','B'}:return l!=f'o{h}'
    if typ=='Q':return j<p[1] and l in own
    raise ValueError(p)
def flag(h,p,ls):
    return p[0]=='R' or any(violates(h,p,j,ls[q]) for j,q in enumerate(supports[h]))
def claims(h,p,j):
    return p[0] in {'C','B','R'} or p[0]=='A' and j<p[1]
def compute(p):return p[0] in {'C','B'} or p[0]=='R' and p[1][0] in {'C','B'}
def ch(s,h=None,p=None,q=None,l=None):
    ps=list(s[0]);ls=list(s[1])
    if h is not None:ps[h]=p
    if q is not None:ls[q]=l
    return tuple(ps),tuple(ls)
def trans(s, launches=True):
    ps,ls=s
    for h,p in enumerate(ps):
        k=len(supports[h]); typ=p[0]
        if typ=='I' and launches:yield ch(s,h,('A',0)),'load_reset',False
        if typ=='A':
            i=p[1]
            if i<k and ls[supports[h][i]]=='f':yield ch(s,h,('A',i+1),supports[h][i],f'o{h}'),'acquire',True
            if i>0 and ls[supports[h][i-1]]==f'o{h}':yield ch(s,h,('A',i-1),supports[h][i-1],'f'),'unacquire',True
            if i==k:yield ch(s,h,('C',0)),'commit_reset',False
        if typ=='C':
            t=p[1]
            if t<lengths[h] and ls[gate_targets[h][t]]==f'o{h}':yield ch(s,h,('C',t+1)),'gate',True
            if t>0 and ls[gate_targets[h][t-1]]==f'o{h}':yield ch(s,h,('C',t-1)),'ungate',True
            if t==lengths[h]:yield ch(s,h,('Q',0)),'terminal_reset',False
            yield ch(s,h,('B',t,t)),'watchdog_to_rollback',False
        if typ=='B':
            j,l=p[1:]
            if l>0 and ls[gate_targets[h][l-1]]==f'o{h}':yield ch(s,h,('B',j,l-1)),'rollback_inverse',True
            if l<j and ls[gate_targets[h][l]]==f'o{h}':yield ch(s,h,('B',j,l+1)),'rollback_forward',True
            if l==0:yield ch(s,h,('Q',0)),'rollback_reset',False
        if typ=='Q':
            i=p[1]
            if i<k and ls[supports[h][i]] not in {f'o{h}',f'z{h}'}:yield ch(s,h,('Q',i+1)),'verify',True
            if i>0 and ls[supports[h][i-1]] not in {f'o{h}',f'z{h}'}:yield ch(s,h,('Q',i-1)),'unverify',True
            if i==k:yield ch(s,h,('I',0)),'ready_reset',False
        if typ in {'I','A','Q','R'}:yield ch(s,h,('Q',0)),'watchdog_complete_reset',False
        if typ!='R':
            for j,q in enumerate(supports[h]):
                if violates(h,p,j,ls[q]):yield ch(s,h,('R',p,j)),'abort_drive',True
        else:
            old,j=p[1:];q=supports[h][j]
            if violates(h,old,j,ls[q]):yield ch(s,h,old),'unabort_drive',True
            yield ch(s,h,('Q',0)),'abort_reset',False
    for q,l in enumerate(ls):
        if l=='f':continue
        h=int(l[1]);j=supports[h].index(q);enabled=not claims(h,ps[h],j)
        if l[0]=='o' and enabled:yield ch(s,q=q,l=f'z{h}'),'cleanup_drive',True
        if l[0]=='z':
            if enabled:yield ch(s,q=q,l=f'o{h}'),'uncleanup_drive',True
            yield ch(s,q=q,l='f'),'cleanup_reset',False

from functools import lru_cache
@lru_cache(None)
def edges(s):return frozenset((ss,kind) for ss,kind,coh in trans(s,True))
stepcount=0
maxclear=0

def step(s,ss,kind):
 global stepcount
 assert (ss,kind) in edges(s),(s,ss,kind)
 stepcount+=1
 return ss

def clear(s,h):
 global maxclear
 start=stepcount;p=s[0][h]
 if p[0]=='C':s=step(s,ch(s,h,('B',p[1],p[1])),'watchdog_to_rollback');p=s[0][h]
 if p[0]=='B':
  failed=[j for j,r in enumerate(supports[h]) if violates(h,p,j,s[1][r])]
  if failed:
   s=step(s,ch(s,h,('R',p,failed[0])),'abort_drive')
   s=step(s,ch(s,h,('Q',0)),'abort_reset')
  else:
   while s[0][h][2]>0:
    p=s[0][h];s=step(s,ch(s,h,('B',p[1],p[2]-1)),'rollback_inverse')
   s=step(s,ch(s,h,('Q',0)),'rollback_reset')
 else:s=step(s,ch(s,h,('Q',0)),'watchdog_complete_reset')
 for r in supports[h]:
  if s[1][r]==f'o{h}':s=step(s,ch(s,q=r,l=f'z{h}'),'cleanup_drive')
  if s[1][r]==f'z{h}':s=step(s,ch(s,q=r,l='f'),'cleanup_reset')
 for j in range(len(supports[h])):s=step(s,ch(s,h,('Q',j+1)),'verify')
 s=step(s,ch(s,h,('I',0)),'ready_reset')
 used=stepcount-start;maxclear=max(maxclear,used)
 assert used<=max(lengths)+3*max(map(len,supports))+4
 return s

def success(s,h):
 assert s[0][h]==('I',0)
 assert all(s[1][r]=='f' for r in supports[h])
 s=step(s,ch(s,h,('A',0)),'load_reset')
 for j,r in enumerate(supports[h]):s=step(s,ch(s,h,('A',j+1),r,f'o{h}'),'acquire')
 s=step(s,ch(s,h,('C',0)),'commit_reset')
 for j in range(lengths[h]):s=step(s,ch(s,h,('C',j+1)),'gate')
 return step(s,ch(s,h,('Q',0)),'terminal_reset')

num=0;maxone=0;maxtwo=0
for ps in product(*phases):
 for ls in product(*lockoptions):
  init=(ps,ls)
  for h in range(2):
   start=stepcount;s=clear(init,h)
   competitors=[g for g in range(2) if g!=h and set(supports[g])&set(supports[h])]
   for g in competitors:s=clear(s,g)
   s=success(s,h);one=stepcount-start;maxone=max(maxone,one)
   s=clear(s,h);s=success(s,h);two=stepcount-start;maxtwo=max(maxtwo,two)
   k=max(map(len,supports));L=max(lengths);nc=1+len(competitors);M=L+3*k+4
   assert one<=nc*M+k+L+3
   assert two<=(nc+1)*M+2*(k+L+3)
   num+=1
out={'scope':'All-basis-label legal path diagnostic only; no workspace quantum probability or QCA semantics simulation',
     'initial_configurations':num//2,'owner_paths':num,'selected_legal_transitions':stepcount,
     'max_clear_steps':maxclear,'max_one_success_steps':maxone,'max_two_success_steps':maxtwo,
     'all_clear_paths_acquisition_free':True,'new_LOAD_unconditional':True,
     'target_and_competitors_parked_by_record_selection':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
