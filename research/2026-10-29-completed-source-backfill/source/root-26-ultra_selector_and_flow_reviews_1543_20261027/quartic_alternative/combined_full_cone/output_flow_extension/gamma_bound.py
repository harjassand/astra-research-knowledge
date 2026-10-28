"""One rational rank-one pair bounds any nonnegative det² removal."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,math
import numpy as np
from scipy.optimize import minimize_scalar
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
import verify_common as P


def evaluate(p,A):
    values=list(A)+[F(0)]*6;ans=F(0)
    for e,c in p.items():
        term=c
        for value,n in zip(values,e):term*=value**n
        ans+=term
    return ans


def main():
    record=json.loads((ROOT/'SYMMETRIC_TARGET.json').read_text());p=list(map(F,record['coefficients']))
    a=[P.var(i) for i in range(4)];f=P.add(*(P.scale(q,c) for q,c in zip(P.bases(a),p)))
    Q=np.array(P.acoustic_matrix(f),float)
    def at(z):return Q[:4,:4]+z*(Q[:4,4:]+Q[4:,:4])+z*z*Q[4:,4:]
    def criterion(z):
        v=np.array([0,0,-z,1.]);A=np.linalg.solve(at(z),v)
        return 1/(2*float(v@A))
    grid=np.linspace(0,1,101);i=int(np.argmin([criterion(z) for z in grid]))
    lo,hi=grid[max(i-1,0)],grid[min(i+1,100)]
    result=minimize_scalar(criterion,bounds=(lo,hi),method='bounded',options={'xatol':1e-13})
    z=float(result.x);v=np.array([0,0,-z,1.]);A=np.linalg.solve(at(z),v);A/=np.linalg.norm(A)
    zz=F(round(z*10**6),10**6);AA=[F(round(x*10**6),10**6) for x in A]
    curve=P.add(P.diff(P.diff(f,0),0),P.scale(P.diff(P.diff(f,0),1),2*zz),P.scale(P.diff(P.diff(f,1),1),zz*zz))
    curvature=evaluate(curve,AA);detprime=AA[3]-zz*AA[2]
    assert curvature>0 and detprime
    bound=curvature/(2*detprime*detprime)
    upper=F((bound.numerator*10**8+bound.denominator-1)//bound.denominator,10**8)
    assert bound<=upper
    out={'status':'EXACT_RANK_ONE_GAMMA_UPPER_BOUND','A':list(map(str,AA)),'eta':['1',str(zz)],
         'H':'e1 tensor eta','F_curvature':str(curvature),'det_derivative':str(detprime),
         'exact_gamma_upper_bound':str(bound),'used_rational_upper_bound':str(upper),
         'scope':'Any hypothetical flow certificate makes F-gamma det² QC and hence ROC; this one exact rankone curvature bounds gamma. Not a sharp global optimum claim.'}
    (ROOT/'GAMMA_BOUND.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
