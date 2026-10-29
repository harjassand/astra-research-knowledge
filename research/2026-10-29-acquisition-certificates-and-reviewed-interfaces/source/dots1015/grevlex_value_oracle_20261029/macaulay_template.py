"""Explicit Macaulay matrices; no generic fast determinant claim.
Rows/columns share degree-rho monomials, row assigned first divisible power.
Delete reduced rows/columns (exactly one distinguished power divides) for denominator.
"""
import itertools,sympy as s,json,time
from pathlib import Path

def compositions(total,n):
 if n==1:yield (total,);return
 for a in range(total+1):
  for r in compositions(total-a,n-1):yield (a,)+r

def matrices(polynomials,variables,degrees=None):
 n=len(variables);assert len(polynomials)==n
 pp=[s.Poly(f,*variables) for f in polynomials]
 if degrees is None:
  if any(p.is_zero for p in pp):raise ValueError('zero forms require explicit positive homogeneous degrees')
  degrees=[p.total_degree() for p in pp]
 if len(degrees)!=n or any(not isinstance(d,int) or isinstance(d,bool) or d<1 for d in degrees):raise ValueError('one positive integer degree required per form')
 if not all(all(c==0 or sum(e)==d for e,c in p.terms()) for p,d in zip(pp,degrees)):raise ValueError('forms must be homogeneous at declared degrees')
 rho=sum(degrees)-n+1;mons=list(compositions(rho,n));ix={e:i for i,e in enumerate(mons)};M=s.zeros(len(mons));nonred=[]
 for row,e in enumerate(mons):
  choices=[i for i in range(n) if e[i]>=degrees[i]];assert choices
  if len(choices)>=2:nonred.append(row)
  i=choices[0];offset=list(e);offset[i]-=degrees[i]
  for a,c in pp[i].terms():
   if c!=0:M[row,ix[tuple(a[j]+offset[j] for j in range(n))]]=c
 E=M.extract(nonred,nonred)
 return M,E

def resultant(polynomials,variables,degrees=None):
 M,E=matrices(polynomials,variables,degrees)
 if any(s.Poly(f,*variables).is_zero for f in polynomials):return s.Integer(0)
 den=E.det(method='domain-ge');assert den!=0,'specialized denominator zero: use auxiliary diagonal shift before quotient'
 return s.cancel(M.det(method='domain-ge')/den)

if __name__=='__main__':
 st=time.time();q=s.symbols('q0:4');a=[s.Integer(i) for i in [2,3,5,7]]
 M,E=matrices([a[i]*q[i]**3 for i in range(4)],q);assert M.shape==(220,220) and E.shape==(112,112)
 # Matrices are diagonal in this test; multiplication is independently transparent.
 assert M.is_diagonal() and E.is_diagonal();r=s.prod(M[i,i] for i in range(220))/s.prod(E[i,i] for i in range(112));assert r==s.prod(a)**27
 A=s.Matrix([[2,3,0,1],[1,4,2,0],[0,1,5,3],[2,0,1,7]])
 rr=resultant(list(A*s.Matrix(q)),q);assert rr==A.det()
 x,y=s.symbols('x y');f=x*x+2*x*y+3*y*y;g=2*x*x-x*y+5*y*y
 rr2=resultant([f,g],[x,y]);assert rr2==s.resultant(f.subs(y,1),g.subs(y,1),x)
 zero_forms=[0,q[1]**3,q[2]**3,q[3]**3]
 assert matrices(zero_forms,q,[3]*4)[0].shape==(220,220) and resultant(zero_forms,q,[3]*4)==0
 try:matrices(zero_forms,q)
 except ValueError:pass
 else:raise AssertionError('zero form missing explicit degree accepted')
 out=dict(explicit_zero_form_check=True,missing_zero_degree_rejected=True,four_cubic_matrix_dimension=220,extraneous_minor_dimension=112,diagonal_cubic_exact_check=True,linear_four_variable_check=True,binary_quadratic_sylvester_check=True,seconds=time.time()-st,scope='Explicit matrix recipe and small/structured exact tests only. Generic four-cubic determinant/derivatives not executed.')
 Path(__file__).with_name('macaulay_template_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
