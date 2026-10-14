#!/usr/bin/env python3
"""Exact all-closed-walk certificate for a finite graph of compatible profiles.
This certifies a specified infinite class of walks, not full quasiconvexity.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import lcm
import json,time
from profile_algebra import averaged,poly_terms,edge_coeffs,edge_value
ROOT=Path(__file__).resolve().parent

def build():
 vertices=[(Q(i,4),Q(j,4)) for i in range(9) for j in range(9)]
 widths=[Q(1,8),Q(1,4),Q(1,2),Q(1),Q(2)];eta=Q(1,4)
 G,N,_,_=averaged(1,-1,False)
 gt=poly_terms(G);nt=poly_terms(N)
 allw=[];minedges=[];negn=0;rawneg=0;minraw=None;den=1
 for i,a in enumerate(vertices):
  for j,b in enumerate(vertices):
   gc=edge_coeffs(gt,a,b);nc=edge_coeffs(nt,a,b)
   best=None
   for k,h in enumerate(widths):
    gv=edge_value(gc,h);nv=edge_value(nc,h);w=gv-eta*nv
    assert nv>=0
    if w<0:negn+=1
    if gv<0:rawneg+=1
    if minraw is None or gv<minraw[0]:minraw=(gv,i,j,k)
    allw.append((i,j,k,w))
    den=lcm(den,w.denominator)
    if best is None or w<best[0]:best=(w,k)
   minedges.append((i,j,best[0]))
 return vertices,widths,eta,allw,minedges,den,negn,rawneg,minraw

def certify(save=True):
 start=time.time(); V,W,eta,edges,minedges,den,negn,rawneg,minraw=build()
 integeredges=[(i,j,int(w*den)) for i,j,w in minedges]
 d=[0]*len(V);iterations=0
 for it in range(len(V)):
  nd=d.copy()
  for i,j,w in integeredges:
   v=d[i]+w
   if v<nd[j]:nd[j]=v
  iterations=it+1
  if nd==d:break
  d=nd
 else:raise AssertionError('Negative cycle or failure to stabilize: no certificate produced.')
 # Independent exact verification of every directed edge and every allowed width.
 tight=0;minslack=None
 for i,j,k,w in edges:
  slack=int(w*den)+d[i]-d[j]
  assert slack>=0,(i,j,k,slack)
  tight+=slack==0
  minslack=slack if minslack is None else min(minslack,slack)
 out={'status':'EXACT PASS','scope':'G, carriers (1,-1), all finite closed walks on the specified profile graph; all affine backgrounds',
      'eta':str(eta),'vertices':[[str(x),str(y)] for x,y in V], 'allowed_widths':[str(x) for x in W],
      'vertex_count':len(V),'directed_edge_width_count':len(edges),'common_denominator':str(den),
      'potential_numerators':[str(x) for x in d], 'bellman_passes':iterations,'tight_constraints':tight,
      'negative_adjusted_edges':negn,'negative_raw_energy_edges':rawneg,
      'most_negative_raw_edge':{'energy':str(minraw[0]),'start':minraw[1],'end':minraw[2],'width_index':minraw[3]},
      'minimum_slack_integer':str(minslack),'elapsed_seconds':time.time()-start}
 if save:(ROOT/'profile_graph_certificate.json').write_text(json.dumps(out,indent=2))
 print('EXACT GRAPH PASS', {k:out[k] for k in ['vertex_count','directed_edge_width_count','bellman_passes','negative_adjusted_edges','negative_raw_energy_edges','tight_constraints','elapsed_seconds']},flush=True)
 print('most negative raw edge',out['most_negative_raw_edge'],flush=True)
 return out
if __name__=='__main__':certify()
