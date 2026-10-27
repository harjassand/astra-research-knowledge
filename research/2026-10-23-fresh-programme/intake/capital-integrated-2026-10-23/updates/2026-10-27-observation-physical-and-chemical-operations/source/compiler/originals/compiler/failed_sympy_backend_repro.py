"""Retained failed backend receipt; no output from this is accepted as a solution."""
import json
import sympy as s
from sympy.solvers.simplex import linprog
from compiler import constraints,matrix
K=matrix([["1","0"],["0","1"]]);L=matrix([["1","1"]]);A,b,names=constraints(K,L)
A=s.Matrix(A);b=s.Matrix(b);objective,point=linprog(s.Matrix([[0,0,1]]),A,b)
slack=b-A*s.Matrix(point)
print(json.dumps({"backend_version":s.__version__,"objective":str(objective),"point":list(map(str,point)),"constraint_slack":list(map(str,slack)),"feasible":all(v>=0 for v in slack),"accepted_as_solution":False},indent=2))
