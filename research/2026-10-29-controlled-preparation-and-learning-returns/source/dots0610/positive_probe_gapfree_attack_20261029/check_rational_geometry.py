import sympy as s,itertools,json
from pathlib import Path
p=Path(__file__).parent
pairs=[(i,j) for i in range(9) for j in range(i,9)]
def rot(u):
 r=sum(x*x for x in u);v=s.Matrix([2*x/(1+r) for x in u]);w=(1-r)/(1+r);X=s.Matrix([[0,-v[2],v[1]],[v[2],0,-v[0]],[-v[1],v[0],0]])
 return (w*w-(v.T*v)[0])*s.eye(3)+2*v*v.T+2*w*X
vals=[s.Rational(-1),s.Rational(-1,2),s.Rational(0),s.Rational(1,2),s.Rational(1)]
rows=[];grids=[]
for u in itertools.product(vals,repeat=3):
 R=rot(u);assert R.T*R==s.eye(3) and R.det()==1
 x=list(R);rows.append([x[i]*x[j] for i,j in pairs]);grids.append(u)
F=s.Matrix(rows);_,cols=F.rref();assert len(cols)==35
G=F[:,list(cols)];_,rr=G.T.rref();assert len(rr)==35
minor=G[list(rr),:];det=minor.det(method='domain-ge');assert det!=0
# Radial endpoint provides the missing affine direction.
A=G[list(rr),:];thick=A.col_join(A[:1,:]/2);aug=s.ones(36,1).row_join(thick);ad=aug.det(method='domain-ge');assert ad!=0
out={'rational_rotation_grid_points':len(rows),'exact_feature_linear_rank':len(cols),'exact_radially_thickened_affine_dimension':35,'independent_feature_columns':list(cols),'independent_grid_row_indices':list(rr),'nonzero_linear_minor_determinant':str(det),'nonzero_augmented_radial_minor_determinant':str(ad),'selected_rational_grid_points':[[str(x) for x in grids[i]] for i in rr],'scope':'Exact finite rational action geometry and full-dimensional radial body certificate, not a convex-body sampler implementation.'}
(p/'rational_geometry_checks.json').write_text(json.dumps(out,indent=2)+'\n');print('exact rank35 and radial affine35 passed')
