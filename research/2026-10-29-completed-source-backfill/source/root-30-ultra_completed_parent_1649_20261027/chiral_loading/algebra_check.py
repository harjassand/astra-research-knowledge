from pathlib import Path
import sympy as s,json
q=s.Matrix([[3,1,0],[1,2,1],[0,1,3]])
g=s.Matrix([[1,2],[0,1],[2,-1]])
eta=s.symbols('eta',real=True)
w=q.inv()*g;l=w.T*w;d=g.T*q.inv()*g
assert sorted(q.eigenvals())==[1,3,4]
assert d*l-l*d!=s.zeros(2)
assert q*(w*w.T)-(w*w.T)*q!=s.zeros(3)
k=(eta*g).row_join(q)
assert s.simplify(k*k.T-eta**2*g*g.T-q*q)==s.zeros(3)
raw=s.eye(2).col_join(s.zeros(3,2)).col_join(-eta*w)
h=s.zeros(8);h[:2,2:5]=eta*g.T;h[2:5,:2]=eta*g;h[2:5,5:]=q;h[5:,2:5]=q
assert h*raw==s.zeros(8,2)
out={'status':'EXACT_SYMBOLIC_NONCOMMUTING_CHIRAL_CORE_PASS',
     'Q_spectrum':[1,3,4],'L':[[str(x) for x in row] for row in l.tolist()],
     'D_L_commutator':[[str(x) for x in row] for row in (d*l-l*d).tolist()],
     'all_eta_kernel_identity':True,'all_eta_gap_factorization':True,
     'scope':'Exact structural fixture and symbolic eta identities. General loading and changed physical contract are derived in OPERATION.txt; no apparatus, passive protection or novelty claimed.'}
(Path(__file__).resolve().parent/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
