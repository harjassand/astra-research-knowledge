#!/usr/bin/env python3
"""Independent replay/orientation checks; all acceptance tests exact rational."""
import importlib.util,json
from pathlib import Path
from fractions import Fraction as F
import numpy as np
p=Path(__file__).with_name('certify_same_apparatus_window.py')
spec=importlib.util.spec_from_file_location('cert',p);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
A,Ae=c.build(); I=c.eye(2);Z=np.diag([1,-1]).astype(object);sm=np.array([[0,1],[0,0]],dtype=object)
e10=c.zeros(3);e10[1,0]=1;e20=c.zeros(3);e20[2,0]=1
K=np.kron(e10,sm)+F(1,2)*np.kron(e20,sm.T);K+=K.T
H=np.kron(c.eye(3),F(1,3)*Z)+1000*K
L=c.zeros(3);L[0,1]=L[2,1]=1; L=np.kron(L,I)
M=c.zeros(3);M[0,2]=1;M=np.kron(M,I)
for col in range(36):
 rho=c.zeros(6);rho[col%6,col//6]=1
 real=c.zeros(6)
 for J,w in [(L,1),(M,2)]:
  B=J.T@J;real+=10**6*w*(J@rho@J.T-(B@rho+rho@B)/F(2))
 imag=-(H@rho-rho@H)
 assert all(F(x)==F(y,12) for x,y in zip(real.reshape(36,order='F'),A[0][:,col]))
 assert all(F(x)==F(y,12) for x,y in zip(imag.reshape(36,order='F'),A[1][:,col]))
U=np.kron(c.eye(3),Z)
assert np.array_equal(U@K@U,-K)
assert np.array_equal(U@np.kron(c.eye(3),Z)@U,np.kron(c.eye(3),Z))
assert np.array_equal(K@K,np.diag([F(1,4),1,1,0,0,F(1,4)]))
lo,elo,_=c.exp_cert(A,F(8002002),6)
oldscale=c.SCALE
c.BITS=160;c.SCALE=1<<160;c.DEGREE=52
hi,ehi,_=c.exp_cert(A,F(8002002),6)
frob2=sum((F(int(x),oldscale)-F(int(y),c.SCALE))**2 for a,b in zip(lo,hi) for x,y in zip(a.flat,b.flat))
# Unnormalized Choi is 36x36; sqrt(rank)<=6.
assert 6*c.sqrt_upper(frob2)<=elo+ehi
report=json.loads(Path(__file__).with_name('same_apparatus_certified_window.json').read_text())
assert F(report['witness']['certified_absolute_expectation_lower'])>F(1,10000)
assert F(report['paired_complete_channel']['certified_diamond_upper'])<F(1,10000)
assert report['witness']['input']=='(I+(-1)Z)/2' and report['witness']['observable']=='Y'
print('PASS: 36 direct column-orientation checks; exact Z conjugacy and K norm; independent160-bit/52-degree replay; rational PASS/FAIL inequalities.')
