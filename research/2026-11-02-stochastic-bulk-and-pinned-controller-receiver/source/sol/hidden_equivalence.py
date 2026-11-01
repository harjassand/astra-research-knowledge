#!/usr/bin/env python3
"""Exact first obstruction for mechanism discovery from one known input/output.

This is an ordinary positive-realization gauge, not a new identifiability result.
It is used to test the consequence and information contract of a research opening.
"""
from pathlib import Path
import json
import sympy as s
P=Path(__file__).resolve().parent
alpha=s.symbols('alpha',positive=True);z=s.symbols('z')
A=s.Matrix([[-5,1,2],[0,-1,1],[1,0,-3]])
T=s.Matrix([[1,0,0],[0,1,0],[0,alpha,1]])
B=s.Matrix([1,0,0]);C=s.Matrix([[1,0,0]])
At=s.simplify(T*A*T.inv());I=s.eye(3)
assert T*B==B and C*T.inv()==C
h=s.factor((C*(z*I-A).inv()*B)[0]);ht=s.factor((C*(z*I-At).inv()*B)[0]);assert s.simplify(h-ht)==0
# Both are positive systems for 0<alpha<1/2. Stable poles are identical.
Ar=At.subs(alpha,s.Rational(1,4))
assert all(Ar[i,j]>=0 for i in range(3) for j in range(3) if i!=j)
w=(s.ones(1,3)*T.inv());assert all(v.subs(alpha,s.Rational(1,4))>0 for v in w)
assert s.simplify(w*At)==s.Matrix([[-4,0,0]])
assert A[2,1]==0 and Ar[2,1]>0
assert s.Matrix.hstack(B,A*B,A*A*B).det()!=0
assert s.Matrix.vstack(C,C*A,C*A*A).det()!=0
out={'scope':'Exact positive stable linear example; supplied known input port and measured output preserved. This refutes universal hidden-graph identification under that information contract, not prediction of the shared output law.',
 'A':str(A),'A_transformed':str(At),'T':str(T),'known_B':str(B),'known_C':str(C),
 'parameter_range':'0<alpha<1/2','transfer_function':str(h),'characteristic_polynomial':str(A.charpoly(z).as_expr()),
 'controllable_and_observable_minimal':True,
 'zero_initial_state_preserved':True,'same_output_for_every_known_input_u':True,'hidden_edge_changes':True,
 'conservation_weight_after_transform':str(w)}
(P/'results').mkdir(exist_ok=True);(P/'results/hidden_equivalence.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
