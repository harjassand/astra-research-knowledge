#!/usr/bin/env python3
"""Exact finite legal repair prefix under the literal local VII.1 rule; not a paper counterexample."""
import json

def close(a,b,q): return (a-b)%q in (0,1,q-1)
def run(n):
 q=8*n; s={(x,y):x+y for x in range(n) for y in range(n)}; initial=dict(s); r=n-2
 s[r,r]+=2; events=[]
 for x,y in sorted(((x,y) for x in range(1,r+1) for y in range(1,r+1) if (x,y)!=(r,r)),key=lambda p:-(p[0]+p[1])):
  old=s[x,y]; c=old; ne=[s[x+1,y],s[x,y+1]]
  for _ in range(2):
   if not all(close(c,z,q) for z in ne):
    cand=[v for v in range(q) if all(close(v,z,q) for z in ne)]
    c=max(cand) if cand else 0
  mx=max(c,s[x-1,y],s[x,y-1]); c=mx if not close(c,mx,q) else c
  s[x,y]=c
  assert c-initial[x,y]==2*(1+min(r-x,r-y)),(n,x,y,old,c,ne)
  events.append([x,y,old,c])
 return {'n':n,'q':q,'root':[r,r],'changed_sites_including_root':sum(s[p]!=initial[p] for p in s),
         'expected_changed':r*r,'max_phase_shift':max(s[p]-initial[p] for p in s),
         'total_unperformed_clock_increments':sum(s[p]-initial[p] for p in s),
         'repair_events':events if n==6 else len(events)}
print(json.dumps({'scope':'Exact finite repair-only prefix from a valid sloped absolute clock field. No probabilistic or full-QCA theorem inferred.', 'cases':[run(n) for n in [6,10,20,40]]},indent=2))
