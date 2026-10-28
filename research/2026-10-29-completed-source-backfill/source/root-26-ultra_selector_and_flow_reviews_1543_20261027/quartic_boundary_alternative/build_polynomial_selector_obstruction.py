#!/usr/bin/env python3
"""Build an exact positive atomic obstruction to polynomial PC selectors.

All values are evaluated on actual rational matrices, rather than on a formal
moment pseudo-distribution. Scientific scope: no polynomial globally
nonnegative minor support exists. This alone does not disprove polyconvexity.
"""
from pathlib import Path
import json,hashlib,time
import sympy as S

HERE=Path(__file__).resolve().parent

def main():
 started=time.perf_counter()
 source=HERE.parent/'common_cone_review/EXACT_SYMMETRIC_TARGET.json'
 source_bytes=source.read_bytes()
 data=json.loads(source_bytes)
 p=list(map(S.Rational,data['coefficients']))
 numerical=json.loads((HERE/'QUADRATIC_SUPPORT_GEOMETRY.json').read_text())
 assert len(numerical['active_cuts'])==3
 av=S.symbols('a b c d',real=True)
 a,b,c,d=av
 u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
 basis=(u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w)
 F=S.expand(sum(v*p for v,p in zip(basis,p)))
 grad=S.Matrix([S.diff(F,z) for z in av]);hess=S.hessian(F,av)
 def evaluate(poly,point): return poly.subs(dict(zip(av,point)),simultaneous=True)
 def h(point):
  aa,bb,cc,dd=point
  return S.Matrix([aa*aa+cc*cc-bb*bb-dd*dd,2*(aa*bb+cc*dd),2*(aa*dd-bb*cc)])
 def determinant(point):return point[0]*point[3]-point[1]*point[2]
 found=None
 for denominator in (1000,10000,100000):
  cuts=[]
  for num in numerical['active_cuts']:
   R=S.Matrix([S.Rational(round(z*denominator),denominator) for z in num['R']])
   A=S.Matrix([S.Rational(round(z*denominator),denominator) for z in num['A']])
   fr=evaluate(F,R);gr=evaluate(grad,R);hr=evaluate(hess,R)
   T=hr/2-gr*gr.T/(4*fr)
   co=determinant(R)*h(A)
   constant=(A.T*T*A)[0]
   scale=-(gr.T*A)[0]/(2*fr)
   assert scale!=0 and fr>0
   cuts.append({'R':R,'A':A,'a':co[0],'b':co[2],'c':constant,'s':scale})
  W=S.Matrix([[z['a'] for z in cuts],[z['b'] for z in cuts],[1,1,1]])
  weights=W.inv()*S.Matrix([0,0,1])
  energy=sum(weights[i]*cuts[i]['c'] for i in range(3))
  if min(weights)>0 and energy<0:
   found=(denominator,cuts,weights,energy);break
 assert found is not None
 denominator,cuts,weights,energy=found

 # Exact symmetry projection of all ten unrestricted quadratic selectors.
 # L is a left rotation, J the antiunitary spin flip, S a column swap.
 L=S.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
 J=S.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,1],[0,0,-1,0]])
 C=S.Matrix([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]])
 group=[L**e*J**f*C**g for e in range(2) for f in range(2) for g in range(2)]
 I=S.eye(4)
 for G in group:
  assert G.T*G==I
  assert S.expand(evaluate(F,G*S.Matrix(av))-F)==0
 atoms=[]
 annihilators={(i,j):S.Rational(0) for i in range(4) for j in range(i,4)}
 total=S.Rational(0)
 for cut,weight in zip(cuts,weights):
  for G in group:
   A=G*cut['A'];R=G*cut['R'];X=cut['s']*R
   subX=dict(zip(av,A+X));subA=dict(zip(av,A))
   B=S.expand(F.subs(subX,simultaneous=True)-F.subs(subA,simultaneous=True)-
              (evaluate(grad,A).T*X)[0])
   atomweight=weight/(8*cut['s']**2)
   total+=atomweight*B
   for i,j in annihilators:
    annihilators[i,j]+=atomweight*A[i]*A[j]*determinant(X)
   atoms.append({'A':list(map(str,A)),'X':list(map(str,X)),
                 'weight':str(atomweight)})
 assert all(z==0 for z in annihilators.values())
 assert total==energy<0
 out={
  'status':'EXACT_ALL_POLYNOMIAL_GLOBAL_SUPPORT_SELECTOR_OBSTRUCTION',
  'not_claimed':'This does not rule out a nonlinear homogeneous selector or true PC.',
  'source_sha256':hashlib.sha256(source_bytes).hexdigest(),
  'coefficients':list(map(str,p)),
  'rounding_denominator':denominator,
  'three_cuts':[{'R':list(map(str,z['R'])),'A':list(map(str,z['A'])),
                 'alpha_coefficient':str(z['a']),'beta_coefficient':str(z['b']),
                 'constant':str(z['c']),'optimal_scale':str(z['s']),
                 'positive_weight':str(weight)} for z,weight in zip(cuts,weights)],
  'atomic_count':len(atoms),'atoms':atoms,
  'ten_annihilators':{f'{i},{j}':str(v) for (i,j),v in annihilators.items()},
  'negative_Bregman_pairing':str(energy),
  'negative_Bregman_pairing_float':float(energy),
  'elapsed_seconds':time.perf_counter()-started,
 }
 (HERE/'EXACT_POLYNOMIAL_SELECTOR_OBSTRUCTION.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ['atoms','three_cuts','ten_annihilators']},indent=2))
 print('weights',list(map(str,weights)))

if __name__=='__main__':main()
