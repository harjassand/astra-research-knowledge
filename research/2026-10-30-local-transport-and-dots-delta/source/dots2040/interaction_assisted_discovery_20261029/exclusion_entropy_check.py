"""Uniform fixed-k stationary law and exact entropy combinatorial coefficient."""
import json,sympy as s
from finite_boundary_tests import rowgen,exclusion
u,v=s.symbols('u v',positive=True);E={(0,1):1,(1,0):1}
for i in [2,3,4]:
 E[1,i]=E[i,1]=1;E[i,2+(i-2+1)%3]=u;E[i,2+(i-2-1)%3]=v
Q=rowgen(5,E);out=[]
for k in range(1,5):
 st,L=exclusion(Q,k=k);assert s.ones(1,len(st))*L==s.zeros(1,len(st));coefficient=s.Rational(3)*s.binomial(3,k-1)/s.binomial(5,k);assert coefficient==s.Rational(3*k*(5-k),20)
 out.append({'k':k,'stationary':'uniform on k-subsets','cycle_entropy_coefficient':str(coefficient),'column_sum_exact':'ZERO'})
print(json.dumps(out,indent=2))
