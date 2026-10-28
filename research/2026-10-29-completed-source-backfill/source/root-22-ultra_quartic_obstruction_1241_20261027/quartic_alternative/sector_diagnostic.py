"""Short ordinary SDP comparison; no exact/general-cone conclusion."""
import json,time
from pathlib import Path
import numpy as np
import cvxpy as cp
from poly_support import build

def acoustic(r,L):
    lam=cp.Variable();K=cp.Variable((4,4))
    M11=cp.bmat([[12,0,0,3*L],[0,4*r,-L,0],[0,-L,4,0],[3*L,0,0,2*lam]])
    M12=cp.bmat([[0,4*r,-L,0],[4*r,0,0,-L],[-L,0,0,2*r-lam],[0,-L,2*r-lam,0]])
    M22=cp.bmat([[4*r,0,0,-L],[0,12,3*L,0],[0,3*L,2*lam,0],[-L,0,0,4]])
    Q=cp.bmat([[M11,M12+K],[M12-K,M22]])
    problem=cp.Problem(cp.Minimize(lam),[K+K.T==0,Q>>0])
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_feas=1e-8,max_iter=100)
    return {'status':problem.status,'energy_lambda':problem.value,'K':K.value.tolist()}

def poly(r,L):
    def vector(t):return [1,1,t,2*r-t,0,0,L,-L,0]
    M,b0,terms,*_=build(vector(0));M1,b1,*_=build(vector(1));assert np.array_equal(M,M1)
    x=cp.Variable(M.shape[1]);lam=cp.Variable();n=26
    positions={(i,j):k for k,(i,j,_) in enumerate(terms)}
    Q=cp.bmat([[x[positions[min(i,j),max(i,j)]]/(1 if i==j else np.sqrt(2))
                for j in range(n)] for i in range(n)])
    problem=cp.Problem(cp.Minimize(lam),[M@x==b0+lam*(b1-b0),Q>>0])
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_feas=1e-8,max_iter=100)
    return {'status':problem.status,'energy_lambda':problem.value,'selector':None if x.value is None else x.value[-2:].tolist()}

def main():
    start=time.monotonic();records=[]
    for r,L in [(1.5,4.0)]:
        a=acoustic(r,L);p=poly(r,L)
        records.append({'r':r,'L':L,'acoustic':a,'SOS_polyconvex':p})
        print(records[-1],flush=True)
    Path('sector_diagnostic.json').write_text(json.dumps({'status':'NUMERICAL_DIAGNOSTIC_ONLY','records':records,
        'wall_seconds':time.monotonic()-start,'scope':'NO_EXACT_BOUNDARY_OR_GENERAL_INCLUSION_CLAIM'},indent=2)+'\n')

if __name__=='__main__':main()
