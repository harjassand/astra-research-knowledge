"""Independently verify an exact hitting-time variance formula for finite-temperature collective spin birth-death chains.
Solves killed-chain linear equations, independently from closed-form passage-time derivation.
"""
import numpy as np
from math import log

def check(M,nu):
 q=nu/(nu+1)
 i=np.arange(M+1,dtype=float)
 down=(nu+1)*i*(M-i+1)
 up=nu*(M-i)*(i+1)
 Q=np.diag(-(down+up))
 for k in range(M):Q[k+1,k]=up[k];Q[k,k+1]=down[k+1]
 # Q acts on probability COLUMNS, Q.T acts on functions. Kill at 0.
 A= -Q.T[1:,1:]
 h=np.linalg.solve(A,np.ones(M))
 g=np.linalg.solve(A,2*h)
 v=g-h*h
 aa=np.zeros(M+1)
 for k in range(1,M+1):
  aa[k]=(1-q**(M-k+1))/(k*(M-k+1))
 computed=np.zeros(M+1)
 for k in range(1,M+1):
  extra=sum(q**(l-k)*(1-q**(M-l+1))*aa[l] for l in range(k+1,M+1))
  computed[k]=aa[k]*aa[k]+2*extra/(k*(M-k+1))
 hp=np.cumsum(aa[1:])
 vp=np.cumsum(computed[1:])
 diff_h=np.max(np.abs(h-hp))
 diff_v=np.max(np.abs(v-vp))
 assert diff_h<1e-6 and diff_v<1e-5,(M,nu,diff_h,diff_v)
 return diff_h,diff_v,h[-1],v[-1]

for nu in [0,.01,.2,1,10]:
 for M in [1,2,3,4,8,16,32,64]:
  a,b,hm,vm=check(M,nu)
 print('ν',nu,'max M=64 fully matches second-moment recurrence; h64,v64:',hm,vm)

for nu in [.2,1.]:
 for M in [100,300,1000,3000]:
  q=nu/(nu+1)
  x=M//2
  a=np.array([(1-q**(M-k+1))/(k*(M-k+1)) for k in range(1,M+1)])
  v=0.
  for k in range(1,x+1):
   # truncated geometric nested sum for speed (l-k <=80; any omitted q^80 negligible)
   cross=0.
   for l in range(k+1,min(M,k+120)+1):
    cross+=q**(l-k)*(1-q**(M-l+1))*a[l-1]
   v+=a[k-1]**2+2*cross/(k*(M-k+1))
  h=a[:x].sum()
  print('ν',nu,'M',M,'M*h/logM',h*M/log(M),'M*sd',np.sqrt(v)*M,'sd/h',np.sqrt(v)/h)
print('PASS all exact/linear algebra hitting-moment cross-checks')
