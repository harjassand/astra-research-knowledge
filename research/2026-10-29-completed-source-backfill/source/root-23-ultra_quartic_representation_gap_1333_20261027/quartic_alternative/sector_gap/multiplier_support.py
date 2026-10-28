"""Ordinary SOS multiplier search; positivity still needs exact checking.

If |X|² times the Bregman support residual is SOS, the residual is
nonnegative for X!=0 and vanishes at X=0. This is a PC support certificate,
but is not the primary paper's unmultiplied SOS-polyconvex support.
"""
import json,time,sys,itertools
from pathlib import Path
import numpy as np
import sympy as s
import scipy.sparse as sparse
import cvxpy as cp
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from poly_support import build

def compile_map():
    _,_,_,_,P,multipliers,_=build(['1','1','113/10','-83/10','0','0','4','-4','0'])
    variables=P.gens;a=variables[:4];x=variables[4:]
    norm=sum(t*t for t in x)
    P=s.Poly(P.as_expr()*norm,variables)
    multipliers=[s.Poly(p.as_expr()*norm,variables) for p in multipliers]
    pairs=list(itertools.combinations_with_replacement(range(4),2))
    triples=list(itertools.combinations_with_replacement(range(4),3))
    z=[ai*x[j]*x[k] for ai in a for j,k in pairs]+[x[i]*x[j]*x[k] for i,j,k in triples]
    terms=[(i,j,s.Poly(z[i]*z[j],variables)) for i in range(len(z)) for j in range(i,len(z))]
    monoms=sorted(set(P.monoms()).union(*(set(p.monoms()) for _,_,p in terms),
                                      *(set(p.monoms()) for p in multipliers)))
    rows={e:i for i,e in enumerate(monoms)};rr=[];cc=[];dd=[]
    for c,(i,j,p) in enumerate(terms):
        for e,v in p.terms():rr.append(rows[e]);cc.append(c);dd.append(float(v)*(1 if i==j else 2))
    for j,p in enumerate(multipliers):
        for e,v in p.terms():rr.append(rows[e]);cc.append(len(terms)+j);dd.append(float(v))
    M=sparse.coo_matrix((dd,(rr,cc)),shape=(len(rows),len(terms)+len(multipliers))).tocsr()
    b=np.zeros(len(rows))
    for e,c in P.terms():b[rows[e]]=float(c)
    return M,b,terms,monoms,P,multipliers,z

def main():
    start=time.monotonic();M,b,terms,monoms,P,multipliers,z=compile_map();n=len(z)
    v=cp.Variable(M.shape[1]);rho=cp.Variable()
    rows=[];cols=[];values=[]
    for col,(i,j,_) in enumerate(terms):
        rows.append(i*n+j);cols.append(col);values.append(1)
        if i!=j:rows.append(j*n+i);cols.append(col);values.append(1)
    embed=sparse.coo_matrix((values,(rows,cols)),shape=(n*n,M.shape[1])).tocsr()
    Q=cp.reshape(embed@v,(n,n),order='C')
    weights=np.sqrt(np.asarray(M.multiply(M).sum(axis=1)).ravel())
    row_scale=sparse.diags(1/weights)
    problem=cp.Problem(cp.Maximize(rho),[row_scale@M@v==b/weights,Q-rho*np.eye(n)>>0])
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_feas=1e-8,max_iter=100)
    out={'status':'NUMERICAL_ONLY','solver_status':problem.status,'features':n,'constraints':M.shape[0],
         'margin':None if rho.value is None else float(rho.value),
         'selector':None if v.value is None else v.value[-2:].tolist(),
         'affine_residual':None if v.value is None else float(np.max(np.abs(M@v.value-b))),
         'gram':None if Q.value is None else Q.value.tolist(),'wall_seconds':time.monotonic()-start,
         'PC':'NOT_CLAIMED_BEFORE_EXACT_RECONSTRUCTION'}
    Path('multiplier_support_search.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='gram'},indent=2))

if __name__=='__main__':main()
