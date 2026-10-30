"""Finite Gram acquisition for the complete six-dimensional Hopf ROC cone.

The Gram equivalence uses the ordinary univariate matrix SOS theorem.
Numerical optimizers are diagnostics; exact structural statements are separate.
"""
from pathlib import Path
import sympy as S,numpy as np,cvxpy as cp,json,time
here=Path(__file__).parent
def main():
    start=time.perf_counter();a,b,c,d,t=S.symbols('a b c d t',real=True)
    v=S.symbols('u l p n q r',real=True);u,l,p,n,q,r=v
    X=a*a+c*c-b*b-d*d;Y=2*(a*b+c*d);Z=2*(a*d-b*c)
    F=u*X*X+2*l*X*Y+2*p*X*Z+n*Y*Y+2*q*Y*Z+r*Z*Z
    H=(S.hessian(F,(a,b,c,d))/4).subs({a:1,b:t,c:0,d:0})
    coeff=[H.applyfunc(lambda x:S.expand(x).coeff(t,i)) for i in range(3)]
    arrays=[np.array([[float(S.diff(x,z)) for z in v] for x in mat],float).reshape(4,4,6) for mat in coeff]
    x=cp.Variable(6);sk=cp.Variable((4,4));Hc=[sum((x[j]*ar[:,:,j] for j in range(6))) for ar in arrays]
    G=cp.bmat([[Hc[0],Hc[1]/2+sk],[Hc[1]/2-sk,Hc[2]]])
    constraints=[sk+sk.T==0,G>>0,x[0]+x[3]+x[5]==1]
    directions=[np.array([0,0,1,0,1,0.]),np.array([1,.23,-.61,-.5,.37,-.2]),
                np.array([.12,.77,.31,-.43,-.52,.2]),np.array([-.3,.1,.73,.2,-.19,-.4])]
    results=[]
    for objective in directions:
        model=cp.Problem(cp.Maximize(objective@x),constraints)
        model.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10,max_iter=180)
        xx=x.value;B=np.array([[xx[0],xx[1]],[xx[1],xx[3]]]);dd=np.array([xx[2],xx[4]])
        eig,V=np.linalg.eigh(B);rot=V.T@dd
        nonalignment=abs(np.linalg.det(np.column_stack((dd,B@dd))))
        results.append({'status':model.status,'K':[[xx[0],xx[1],xx[2]],[xx[1],xx[3],xx[4]],[xx[2],xx[4],xx[5]]],
                        'B_eigenvalues':eig.tolist(),'d_in_B_eigenbasis':rot.tolist(),'nonalignment':nonalignment,
                        'Gram_eigenvalues':np.linalg.eigvalsh(G.value).tolist()})
        print(json.dumps(results[-1]),flush=True)
    out={'H_coefficients':[[[str(x) for x in row] for row in mat.tolist()] for mat in coeff],
         'variables':list(map(str,v)),'diagnostics':results,'seconds':time.perf_counter()-start,
         'scope':'Finite Gram cone acquisition and numerical supporting points; numerical points do not prove extremality or quasiconvexity.'}
    (here/'hopf_cone_geometry.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
