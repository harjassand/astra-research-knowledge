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
 degrees=degrees or [p.total_degree() for p in pp]
 assert all(all(sum(e)==d for e,c in p.terms()) for p,d in zip(pp,degrees))
 rho=sum(degrees)-n+1;mons=list(compositions(rho,n));ix={e:i for i,e in enumerate(mons)};M=s.zeros(len(mons));nonred=[]
 for row,e in enumerate(mons):
  choices=[i for i in range(n) if e[i]>=degrees[i]];assert choices
  if len(choices)>=2:nonred.append(row)
  i=choices[0];offset=list(e);offset[i]-=degrees[i]
  for a,c in pp[i].terms():M[row,ix[tuple(a[j]+offset[j] for j in range(n))]]=c
 E=M.extract(nonred,nonred)
 return M,E

def resultant(polynomials,variables,degrees=None):
 M,E=matrices(polynomials,variables,degrees)
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
 out=dict(four_cubic_matrix_dimension=220,extraneous_minor_dimension=112,diagonal_cubic_exact_check=True,linear_four_variable_check=True,binary_quadratic_sylvester_check=True,seconds=time.time()-st,scope='Explicit matrix recipe and small/structured exact tests only. Generic four-cubic determinant/derivatives not executed.')
 Path(__file__).with_name('macaulay_template_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
