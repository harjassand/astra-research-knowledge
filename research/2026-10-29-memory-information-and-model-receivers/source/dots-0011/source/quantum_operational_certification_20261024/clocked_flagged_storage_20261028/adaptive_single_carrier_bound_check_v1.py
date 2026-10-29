#!/usr/bin/env python3
"""Reproducible algebra and floating stress checks; not certified arithmetic."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import numpy as np, sympy as s, json, hashlib, importlib.util
HERE=Path(__file__).resolve().parent
rng=np.random.default_rng(682018)
I=np.eye(2);Y=np.array([[0,-1j],[1j,0]]);YY=np.kron(Y,Y)
v=np.array([1,0,0,1])/np.sqrt(2);Phi=np.outer(v,v)
def concurrence(r):
 r=(r+r.conj().T)/2
 e,u=np.linalg.eigh(r);root=(u*np.sqrt(np.maximum(e,0)))@u.conj().T
 w=np.linalg.eigvalsh(root@YY@r.conj()@YY@root)
 a=np.sort(np.sqrt(np.maximum(w,0)))[::-1]
 return max(0.,float(a[0]-sum(a[1:])))
def apply(r,ks):
 return sum(np.kron(I,k)@r@np.kron(I,k).conj().T for k in ks)
def random_ks(n=4):
 a=rng.normal(size=(2*n,2))+1j*rng.normal(size=(2*n,2));u=np.linalg.qr(a)[0]
 return [u[2*i:2*i+2] for i in range(n)]
max_contract=max_instrument=max_bell=-1.
for _ in range(500):
 a=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));r=a@a.conj().T;r/=np.trace(r)
 ks=random_ks();out=apply(r,ks)
 max_contract=max(max_contract,concurrence(out)-concurrence(apply(Phi,ks))*concurrence(r))
 max_instrument=max(max_instrument,sum(concurrence(apply(r,[k])) for k in ks)-concurrence(r))
 max_bell=max(max_bell,float(np.trace(Phi@r).real)-(1+concurrence(r))/2)
assert max(max_contract,max_instrument,max_bell)<1e-7
# Exact primitive-channel identities (concurrence characteristic polynomials).
c,q,z=s.symbols('c q z',real=True)
Jad=s.Matrix([[1,0,0,c],[0,0,0,0],[0,0,1-c*c,0],[c,0,0,c*c]])/2
Jd=s.Matrix([[1,0,0,q],[0,0,0,0],[0,0,0,0],[q,0,0,1]])/2
SY=s.kronecker_product(s.Matrix([[0,-s.I],[s.I,0]]),s.Matrix([[0,-s.I],[s.I,0]]))
pad=s.factor((z*s.eye(4)-Jad*SY*Jad.conjugate()*SY).det())
pd=s.factor((z*s.eye(4)-Jd*SY*Jd.conjugate()*SY).det())
assert s.simplify(pad-z**3*(z-c*c))==0
assert s.simplify(pd-z*z*(z-(1+q)**2/4)*(z-(1-q)**2/4))==0
spec=importlib.util.spec_from_file_location('src',HERE.parent/'five_qubit_acquired_frame_pilot_20261028/code_and_channels.py');src=importlib.util.module_from_spec(spec);spec.loader.exec_module(src)
sources=src.generator_sources();rows=[]
for m,x in zip([20,19,18,17,16],sources):
 amplitude=s.Rational(m*m-1,m*m+1);assert s.cancel(amplitude**2-(1-x['gamma']))==0
 rows.append({'m':m,'gamma_exact':str(x['gamma']),'survival_amplitude_exact':str(amplitude),'gamma':float(x['gamma'])})
bestc=399/401
comparisons=[]
paths=sorted(HERE.glob('rate_*_v1.json'))+sorted(HERE.glob('measure_*_v1.json'))+[HERE/'zero_clock_v1.json']
for path in paths:
 data=json.loads(path.read_text());a=data['integrated_background_strength_EC_window']
 for row in data['encoded']:
  T=row['T'];ub=(1+bestc**T*np.exp(-T*a))/2;fe=1-row['entanglement_infidelity']
  comparisons.append({'case':path.name,'T':T,'integrated':a,'encoded_Fe':fe,'adaptive_single_carrier_Fe_upper':float(ub),'encoded_Fe_minus_upper':float(fe-ub),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
out={'status':'author checks; analytic theorem separate; floating stress tests not proof','seed':682018,'primitive_AD_spinflip_characteristic':str(pad),'primitive_dephasing_spinflip_characteristic':str(pd),'rates':rows,'random_checks':500,'max_contraction_excess':max_contract,'max_instrument_excess':max_instrument,'max_Bell_overlap_excess':max_bell,'comparisons':comparisons,'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'native_generator_sha256':hashlib.sha256((HERE.parent/'five_qubit_acquired_frame_pilot_20261028/code_and_channels.py').read_bytes()).hexdigest(),'clock_program_sha256':hashlib.sha256((HERE/'clocked_channel_v1.py').read_bytes()).hexdigest()}
(HERE/'adaptive_single_carrier_bound_check_v1.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps([x for x in comparisons if x['T']==32],indent=2))
