import sympy as s,json
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);P0=s.diag(1,0);P1=s.diag(0,1)
k=s.kronecker_product
E=k(s.eye(8),s.Matrix([1,0]))
allP=[];rows=[]
for i,A in [(0,Z),(1,X)]:
 good=k(P0,I,I) if i==0 else k(I,P0,I)
 bad=k(P1,I,I) if i==0 else k(I,P1,I)
 Bp=k(I,I,(I+A)/2);Bm=k(I,I,(I-A)/2)
 ps=[good,bad*Bp,bad*Bm];allP.append(ps)
 U=k(ps[0]+ps[1],I)+k(ps[2],X)
 qs=[k(good,I),k(bad,P0),k(bad,P1)]
 assert U.T*U==s.eye(16)
 for j in range(3):
  assert qs[j]*U*E==U*E*ps[j]
  assert U.T*qs[j]*U*E==E*ps[j]
 rows.append({'coordinate':i,'unitary':True,'all_projector_intertwiners':True,'uncompute':True})
assert allP[0][1]*allP[1][1]!=allP[1][1]*allP[0][1]
r={'exact_rational_checks':rows,'fine_projectors_noncommute':True,'coarse_parities_commute':True,'scope':'interface only, not stochastic theorem or hardware'}
open(__import__('pathlib').Path(__file__).with_name('interface_checks.json'),'w').write(json.dumps(r,indent=2));print(r)
