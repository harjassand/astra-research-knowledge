"""Exact sharpness check: actual unitary channel versus identity positive fit.
No acquisition or solver calls. The actual contrasts need not be positive in the fitted orientation.
"""
import sympy as s,json
from pathlib import Path
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[X,Y,Z]
rows=[]
for m in [2,3,5,10]:
 c=s.Rational(m*m-1,m*m+1);r=s.Rational(2*m,m*m+1);U=s.Matrix([[c,-r],[r,c]])
 assert U.H*U==I
 C=[U*p*U.H/2 for p in P];Ct=[p/2 for p in P];kap=s.Rational(1,2)
 e2=s.simplify(sum(s.trace((a-b).H*(a-b)) for a,b in zip(C,Ct)))
 Fe=s.simplify((1+sum(s.trace(p*q) for p,q in zip(P,C)))/4)
 # Inverse-unitary decoder has fidelity exactly 1; identity extraction has c^2.
 assert Fe==c*c and 1-Fe==e2/(8*kap)
 rows.append({'m':m,'identity_extraction_fidelity':str(Fe),'actual_full_CPTP_oracle':1,'fit_error_squared':str(e2),'bound_equals_actual_regret':True})
out={'status':'PASS_EXACT_SHARPNESS_OUTSIDE_FITTED_ORIENTATION','source_outcomes':0,'rows':rows,'scope':'Four exact unitary-channel examples show same-channel e^2/(8kappa) is sharp; not a finite-shot pilot or future-memory theorem.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
