import sympy as s,json
from pathlib import Path
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);pa=[X,Y,Z];U=[(I-s.I*p)/s.sqrt(2) for p in [X,Y]];K=[s.kronecker_product(u,u)/s.sqrt(2) for u in U];P=[s.kronecker_product(a,b) for a in pa for b in pa];D=4
H=s.zeros(9)
for i in range(9):
 for j in range(9):H[i,j]=s.simplify(sum(((k*P[i]-P[i]*k).conjugate().T*(k*P[j]-P[j]*k)).trace() for k in K)/(2*D))
ev=H.eigenvals();assert ev.get(s.Integer(0))==1;prod=s.prod(x**m for x,m in ev.items() if x!=0);joint=s.simplify(prod/18**8);pminus=s.trace(H)/18;c=s.Matrix([1,0,0,0,1,0,0,0,1]);assert H*c==s.zeros(9,1)
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(H=[[str(v) for v in row] for row in H.tolist()],eigenvalues={str(x):m for x,m in ev.items()},minus_probability=str(pminus),eight_call_joint_program_probability=str(joint),normalized_eight_record_probability=str(s.simplify(joint/pminus**8)),two_fixed_batches_plus_transduction_and_one_gate_probability=str(s.simplify(joint**2/36)),scope='Exact memoryless collective two-axis example; arbitrary unknown local twist rotates kernel without changing spectrum. Not a guarantee for causal-memory sources.'),indent=2)+'\n');print(ev,pminus,joint,float(joint))
