"""Independent exact closest-constant Bell bound and odd-dimensional counterexample."""
from pathlib import Path
import sympy as s,json,hashlib
D=Path(__file__).parent;A=D.parent;Q=A.parent
# Algebraic identity |x+r|/2+|x-r|/2=max(|x|,r), r>=0.
for x in [s.Rational(j,7) for j in range(-14,15)]:
 for r in [s.Rational(j,9) for j in range(10)]:assert (abs(x+r)+abs(x-r))/2==max(abs(x),r)
rows=[]
for d in [3,5,7]:
 I=s.eye(d);ks=[]
 for i in range(d):
  for j in range(i+1,d):
   k=s.zeros(d);k[i,j]=1/s.sqrt(d-1);k[j,i]=-1/s.sqrt(d-1);ks.append(k)
 assert sum((k.H*k for k in ks),s.zeros(d))==I
 assert sum((k*k.H for k in ks),s.zeros(d))==I
 for i in range(d):
  for j in range(d):
   e=s.zeros(d);e[i,j]=1;n=sum((k*e*k.H for k in ks),s.zeros(d));assert n==(s.trace(e)*I-e.T)/(d-1)
   nn=sum((k*n*k.H for k in ks),s.zeros(d));assert nn==((d-2)*s.trace(e)*I+e)/(d-1)**2
 # Independent Kraus trace evaluation of the actual composed recovery.
 fe=sum(abs(s.trace(a*b))**2 for a in ks for b in ks)/d**2;assert fe==s.Rational(2,d*(d-1))
 U=s.zeros(d);U[0,0]=1
 for j in range(1,d,2):U[j,j+1]=1;U[j+1,j]=-1
 assert U.H*U==I and s.trace(U*U.conjugate())==2-d
 unit=sum(abs(s.trace(U*k))**2 for k in ks)/d**2;assert unit==s.Rational(2,d*d)<fe
 rows.append({'d':d,'explicit_CPTP_receiver_Fe':str(fe),'max_unitary_Fe':str(unit),'gap':str(fe-unit),'basis_operators_checked':d*d})
files=[A/'CLOSEST_CONSTANT_RECORD_ADDENDUM_v1.md',A/'HIGHER_DIMENSION_BOUNDARY_v1.md',A/'AUTHOR_ADDENDUM_MANIFEST_v1.json',Path(__file__)]
out={'status':'PASS_EXACT_ADDENDA_SCOPE','rows':rows,'new_acquisition_draws':0,'sha256':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(D/'check_addenda_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
