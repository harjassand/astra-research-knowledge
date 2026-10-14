#!/usr/bin/env python3
"""Exact acoustic and non-polyconvexity checks for F_11=Fstar-(11/100)q^2."""
from pathlib import Path
import hashlib, json
import sympy as S

ROOT=Path(__file__).resolve().parent
a,b,c,d,s,t=S.symbols('a b c d s t', real=True)
x=S.Matrix([a,b,c,d]); u=a*a+c*c; v=b*b+d*d; w=a*b+c*d; q=a*d-b*c
Fstar=u*u+v*v+4*w*w+S.Rational(7,2)*q*q-S.Rational(29,10)*q*(u+v)
F=S.expand(Fstar-S.Rational(11,100)*q*q)
F_basis=u*u+v*v+4*w*w+S.Rational(339,100)*q*q-S.Rational(29,10)*q*(u+v)
assert S.expand(F-F_basis)==0

ac=S.expand(s*s*S.diff(F,a,2)+2*s*t*S.diff(F,a,b)+t*t*S.diff(F,b,2))
M11=S.hessian(ac.coeff(s,2).coeff(t,0),x)/2
M12=S.hessian(ac.coeff(s,1).coeff(t,1),x)/4
M22=S.hessian(ac.coeff(s,0).coeff(t,2),x)/2
pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
ks=[S.Rational(288041,10**6),S.Rational(1391905,10**6),0,0,S.Rational(1391905,10**6),S.Rational(2151711,10**6)]
K=S.zeros(4)
for (i,j),v0 in zip(pairs,ks): K[i,j]=v0; K[j,i]=-v0
Q=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
z=(s*x).col_join(t*x)
assert S.expand((z.T*Q*z)[0]-ac)==0
minors=[S.factor(Q[:i,:i].det()) for i in range(1,9)]
assert all(vv>0 for vv in minors)
L,D=Q.LDLdecomposition(hermitian=False)
assert L*D*L.T==Q and all(vv>0 for vv in D.diagonal())

# Symmetric pairs at +/-7I and +/-diag(1,-1) give mean A=0; the
# determinant mean also vanishes. This is a polyconvexity witness only.
I={a:7,b:0,c:0,d:7}; J={a:1,b:0,c:0,d:-1}
law=S.Rational(1,50)*F.subs(I)+S.Rational(49,50)*F.subs(J)
assert law==S.Rational(-4361,500)
assert S.Rational(1,50)*49-S.Rational(49,50)==0

pins={}
for rel in [
    'work/FM-sources/resonant/PROFILE_CIRCULATION.md',
    'work/FM-sources/resonant/certify_profile_graph.py',
    'work/FM-sources/resonant/profile_algebra.py',
    'work/astra-capital/updates/FE/synthesis/quartic/QUARTIC_AUDIT_AND_PROOF.md',
    'work/astra-capital/updates/FE/synthesis/quartic/checks/FSTAR_CLOSED_HEAT_CERTIFICATE.json',
]:
    pins[rel]=hashlib.sha256((ROOT.parents[1]/rel).read_bytes()).hexdigest()

out={
  'status':'EXACT PASS',
  'scope':'homogeneous planar left-SO(2) quartic F_11; sufficient exact acoustic Gram and scoped non-polyconvexity witness',
  'basis':'u^2,v^2,uv,w^2,uw,vw,qu,qv,qw',
  'Fstar_coefficients':['1','1','7/2','1/2','0','0','-29/10','-29/10','0'],
  'F_11_coefficients':['1','1','339/100','61/100','0','0','-29/10','-29/10','0'],
  'identity':'F_11=Fstar-(11/100)q^2',
  'acoustic_K_upper_skew_entries':[str(vv) for vv in ks],
  'acoustic_gram':[[str(Q[i,j]) for j in range(8)] for i in range(8)],
  'leading_principal_minors':[str(vv) for vv in minors],
  'ldl_diagonal':[str(vv) for vv in D.diagonal()],
  'nonpolyconvexity_balanced_law_value':str(law),
  'law_symmetric_pairs':['mass 1/100 at each of +7I and -7I','mass 49/100 at each of +diag(1,-1) and -diag(1,-1)'],
  'law_mean_A':['0','0','0','0'],'law_mean_determinant':'0','law_is_compatible_gradient':False,
  'source_sha256':pins,
  'limitations':['The negative atomic-law mean proves non-polyconvexity only; it is not a compatible Jensen counterexample.',
                 'F_11 is outside N794s explicit 1/82000 coefficient cube and exceeds its listed 83/1000 determinant-square subtraction.',
                 'No quasiconvexity conclusion or historical novelty claim follows; external proof review is UNKNOWN.']
}
(ROOT/'acoustic_certificate_11_100.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('acoustic_gram','source_sha256')},indent=2))
