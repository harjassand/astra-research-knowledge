#!/usr/bin/env python3
"""Independent exact Choi/Bell replay; no draws or deployed twirl."""
from pathlib import Path
import hashlib,json
import sympy as s
D=Path(__file__).parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[I,X,Y,Z]
v=s.Matrix([1,0,0,1]);bell=v*v.H/2
Bs=[s.kronecker_product(I,q)*bell*s.kronecker_product(I,q.H) for q in P]
rows=[]
for N in [4096,16384]:
 f=D/f'exact_channels_N{N}.json';M=s.Matrix([[s.Rational(x) for x in r] for r in json.loads(f.read_text())['logical_PTM']])
 # Normalized Choi with reference first, output second.
 J=sum((M[i,j]*s.kronecker_product(P[j].T,P[i])/4 for i in range(4) for j in range(4)),s.zeros(4))
 assert s.trace(J)==1 and J==J.H
 Jtw=sum((s.kronecker_product(q.T,q)*J*s.kronecker_product(q.conjugate(),q.H) for q in P),s.zeros(4))/4
 probs=[s.trace(B*J) for B in Bs]
 assert all(p>=0 for p in probs) and sum(probs)==1
 assert Jtw==sum((p*B for p,B in zip(probs,Bs)),s.zeros(4))
 assert probs[0]==s.trace(M)/4
 # Bell diagonal error has spectrum p0-1,p1,p2,p3.
 assert (sum(probs[1:])+1-probs[0])/2==1-probs[0]
 rows.append({'N_per_site':N,'Choi_twirl_equals_Bell_diagonal':True,'half_diamond_equals_infidelity_exact':True,'posthoc_half_diamond':float(1-probs[0])})
# Retaining the Pauli label invalidates infidelity-to-distance equality.
U=s.Rational(3,5)*I-s.I*s.Rational(4,5)*Z
ju=s.kronecker_product(I,U)*bell*s.kronecker_product(I,U.H)
assert sorted(ju.__sub__(bell).eigenvals().items(),key=lambda z:float(z[0]))==[(s.Rational(-4,5),1),(s.Integer(0),2),(s.Rational(4,5),1)]
assert s.simplify(s.trace(bell*ju))==s.Rational(9,25)
files=['independent_twirl_review.py','OPTIONAL_LOGICAL_TWIRL_COROLLARY.md','exact_channels_N4096.json','exact_channels_N16384.json']
out={'status':'PASS_EXACT_REDUCED_REFERENCE_COMPLETE_TWIRL_COROLLARY','acquired_draws':0,'deployed_twirl':False,'banks':rows,'retained_key_counterexample':{'reduced_half_diamond':'16/25','retained_key_Bell_input_half_trace_distance':'4/5'},'sha256':{f:hashlib.sha256((D/f).read_bytes()).hexdigest() for f in files}}
(D/'independent_twirl_review.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
