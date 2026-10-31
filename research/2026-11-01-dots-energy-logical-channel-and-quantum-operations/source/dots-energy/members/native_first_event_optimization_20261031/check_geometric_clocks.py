#!/usr/bin/env python3
"""Finite checks of acquired product laws/polynomial, not a gate backend."""
import math,json,numpy as np,mpmath as mp
mp.mp.dps=100
rows=[]
for B in [0,1,3,6,10]:
 M=2**B
 for qh in [1e-12,.001,.1,1,100]:
  p=[]
  for j in range(B):
   z=np.exp(-qh*2**j);p.append(z/(1+z))
  weights=np.ones(M)
  for j,prob in enumerate(p):weights*=np.where((np.arange(M)>>j)&1,prob,1-prob)
  exact=np.exp(-qh*np.arange(M));exact/=exact.sum()
  err=float(np.max(np.abs(weights-exact)));assert err<2e-14
  Ns=sorted(set([max(1,M//2+1),max(1,M-1),M]))
  for N in Ns:
   acc=float(weights[:N].sum());assert acc>=.5-1e-13
   cond=weights[:N]/acc;target=np.exp(-qh*np.arange(N));target/=target.sum()
   assert np.max(np.abs(cond-target))<2e-14
   rows.append(dict(B=B,qh=qh,N=N,success=acc,max_product_error=err))
poly=[]
for m in [1,4,10,30,100]:
 for x in [mp.mpf(0),mp.mpf('.1'),mp.mpf('.5'),1/mp.sqrt(2),mp.mpf('.9'),mp.mpf(1)]:
  ck=mp.mpf(1);p=mp.mpf(0)
  for k in range(m+1):
   if k:ck*=mp.mpf(2*k-1)/(2*k)
   p+=x*ck*(1-x*x)**k
  assert -mp.mpf('1e-90')<=p<=1+mp.mpf('1e-90')
  if x>=1/mp.sqrt(2):assert 1-p<=mp.power(2,-m)+mp.mpf('1e-90')
  poly.append(dict(m=m,x=str(x),p=str(p),error=str(1-p)))
json.dump({'scope':'Finite diagnostic only. No polynomial phase sequence, rotations, gate synthesis or whole simulator executed.', 'product_cases':rows,'polynomial_cases':poly},open('native_first_event_optimization_20261031/geometric_clock_checks.json','w'),indent=2)
print(len(rows),'product/conditional cases,',len(poly),'polynomial cases; minimum success',min(x['success'] for x in rows))
