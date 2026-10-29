"""Fail-closed exact candidates before the v2 numerical proposal.
Does not change frozen v2. In particular, feasible centers need no optimizer.
"""
from certified_projection_v2 import *
from certified_projection_v2 import project_certified as _v2

def _exact_candidate(Y,mult,E,xi,bits,route):
 w=[F(1,int(k)) for k in mult];L=[F(0)]*4
 assert all(psd_exact(e) for e in E)
 assert [sum(e[j] for e in E) for j in range(4)]==[1,0,0,0]
 prec=max(192,max(mult).bit_length()+128)
 primal=objective(E,Y,w);dual=dual_lower(L,Y,w,prec);gap=primal-dual
 assert gap>=0
 rec={'proposal':route,'iterations':0,'primal':str(primal),'dual_lower':str(dual),'gap':str(gap),'gap_float':float(gap),'xi':str(xi),'certified':gap<=xi,'interval_bits':prec,'round_bits':bits,'input_Y':[[str(x) for x in y] for y in Y],'multiplicities':[str(k) for k in mult],'output_E':[[str(x) for x in e] for e in E],'dual_L':[str(x) for x in L]}
 return E,rec

def project_certified(Y,mult,xi=F(1,10**9),bits=96):
 assert len(Y)==len(mult)>0 and all(isinstance(k,int) and k>0 for k in mult)
 assert all(len(y)==4 and all(isinstance(a,F) for a in y) for y in Y)
 if all(psd_exact(y) for y in Y) and [sum(y[j] for y in Y) for j in range(4)]==[1,0,0,0]:
  E,c=_exact_candidate(Y,mult,[y[:] for y in Y],xi,bits,'already_feasible_centers')
  if c['certified']:return E,c
 if len(Y)>1 and mult[-1]>10**12 and all(k==1 for k in mult[:-1]) and all(psd_exact(y) for y in Y[:-1]):
  residual=sub([F(1),F(0),F(0),F(0)],[sum(y[j] for y in Y[:-1]) for j in range(4)])
  if psd_exact(residual):
   E,c=_exact_candidate(Y,mult,[y[:] for y in Y[:-1]]+[residual],xi,bits,'underloaded_seen_zero_dual')
   if c['certified']:return E,c
 return _v2(Y,mult,xi,bits)
