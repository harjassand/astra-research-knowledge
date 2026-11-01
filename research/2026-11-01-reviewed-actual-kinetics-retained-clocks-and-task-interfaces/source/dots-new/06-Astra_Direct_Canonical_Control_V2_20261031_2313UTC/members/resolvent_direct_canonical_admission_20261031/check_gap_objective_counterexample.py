"""Independent-review counterexample replay. Zero observations; no file writes in run()."""
from pathlib import Path
import json,time
import sympy as S
import direct as D
C=D.C
ROOT=Path(__file__).resolve().parent

def run():
    checks=0
    def ck(v):
        nonlocal checks
        assert v;checks+=1
    gamma=S.Rational(9,10);A0=S.Matrix([[S.Rational(1,2),S.Rational(1,2),0],[S.Rational(1,4),S.Rational(3,4),0],[0,0,1]]);A1=S.Matrix([[S.Rational(103,144),S.Rational(41,144),0],[S.Rational(49,72),S.Rational(23,72),0],[0,0,1]])
    for A in [A0,A1]:ck(min(A)>=0);ck(A*S.ones(3,1)==S.ones(3,1))
    H=(1-gamma)*(S.eye(3)-gamma*A0).inv();B=(A1-A0)*H;t=gamma/(1-gamma);M=S.Matrix([[S.Rational(3,4),S.Rational(1,4),0],[-S.Rational(1,2),S.Rational(3,2),0],[0,0,1]]);ck(S.eye(3)-t*B==M)
    X=S.Matrix([[S.Rational(4,5),0,0],[-S.Rational(1,5),S.Rational(3,5),0],[0,0,1]]);X2=X.copy();X2[2,2]=S.Rational(4,5);delta=S.Rational(3,5)
    for V in [X,X2]:
        for R in [S.eye(3),M.T]:
            Y=V*R
            for j in range(3):ck(delta<=sum(Y[:,j])<=Y[j,j]<=1);ck(all(Y[i,j]<=0 for i in range(3) if i!=j))
    ck(max(X.diagonal())/delta==S.Rational(5,3));ck(max(X2.diagonal())/delta==S.Rational(4,3))
    # Any feasible witness: delta<=x22 by baseline col2 signs; action1
    # col1 offdiag gives x21<=-x22/3; action1 col2 diagonal then
    # 1>=-x21/2+3*x22/2>=(5/3)x22. Thus delta<=3/5.
    x=S.symbols('x',real=True);ck(-(-x/3)/2+3*x/2==5*x/3);ck(1/(S.Rational(5,3))==delta)
    return dict(status='PASS_GAP_OBJECTIVE_COUNTEREXAMPLE',checks=checks,new_source_calls=0,gamma=str(gamma),A0=C.serial(A0),A1=C.serial(A1),M=C.serial(M),optimal_canonical_gap=str(delta),witnesses=[{'X':C.serial(X),'C_X':'5/3'},{'X':C.serial(X2),'C_X':'4/3'}],scope='Review-supplied exact counterexample to auxiliary optimization equivalence only. Main feasible-witness admission/consumer unchanged; no experiment or practical speedup claim.')
if __name__=='__main__':
    out=run();(ROOT/'gap_objective_counterexample.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
