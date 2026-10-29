#!/usr/bin/env python3
from pathlib import Path
import sympy as s,json,hashlib,itertools
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[X,Y,Z];k=s.kronecker_product
errors=[k(I,I),k(X,I),k(Z,I),k(I,X),k(I,Z)];weights=[s.Rational(1,10)]+[s.Rational(9,40)]*4;assert sum(weights)==1
N=lambda M:sum((w*p*M*p.H for w,p in zip(weights,errors)),s.zeros(4))
lambdas=[s.Rational(11,20),s.Rational(1,10),s.Rational(11,20)]
for i,j in itertools.product(range(2),range(3)):
 B=k(P[j],I) if i==0 else k(I,P[j]);assert N(B/4)==lambdas[j]*B/4
fe_identity=sum(w*abs(s.trace(p)/4)**2 for w,p in zip(weights,errors));fe_correct=sum(w*abs(s.trace(k(X,I)*p)/4)**2 for w,p in zip(weights,errors))
assert fe_identity==s.Rational(1,10) and fe_correct==s.Rational(9,40) and fe_correct>fe_identity
out={'status':'PASS_EXACT_STRICT_LOCAL_ORACLE_COLLECTIVE_COUNTEREXAMPLE','source_outcomes':0,'local_Bloch_contractions':[str(x) for x in lambdas],'full_output_local_positive_block_floor':'1/40','collective_identity_entanglement_fidelity':str(fe_identity),'collective_XI_corrected_fidelity':str(fe_correct),'same_global_encoding':True,'scope':'Exact finite Pauli boundary, not collective capacity theorem','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_suffix('.md')]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
