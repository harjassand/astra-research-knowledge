"""Acquire and exactly check an acoustic Gram at tau=113/10."""
from fractions import Fraction as F
import json,time
from pathlib import Path
import numpy as np
import cvxpy as cp

def exact_ldl(Q):
    n=len(Q);L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        p=Q[j][j]-sum(L[j][k]**2*D[k] for k in range(j));assert p>0,(j,p)
        D.append(p)
        for i in range(j+1,n):L[i][j]=(Q[i][j]-sum(L[i][k]*L[j][k]*D[k] for k in range(j)))/p
    assert all(Q[i][j]==sum(L[i][k]*D[k]*L[j][k] for k in range(n)) for i in range(n) for j in range(n))
    return D

def main():
    start=time.monotonic();tau=F(113,10);t=float(tau);r=1.5;ell=4
    M11=np.array([[12,0,0,12],[0,6,-4,0],[0,-4,4,0],[12,0,0,2*t]])
    M12=np.array([[0,6,-4,0],[6,0,0,-4],[-4,0,0,3-t],[0,-4,3-t,0]])
    M22=np.array([[6,0,0,-4],[0,12,12,0],[0,12,2*t,0],[-4,0,0,4]])
    K=cp.Variable((4,4));margin=cp.Variable();Q=cp.bmat([[M11,M12+K],[M12-K,M22]])
    problem=cp.Problem(cp.Maximize(margin),[K+K.T==0,Q-margin*np.eye(8)>>0])
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_feas=1e-10,max_iter=100)
    assert margin.value>1e-6
    k=[[F(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(i+1,4):k[i][j]=F(round(K.value[i,j]*10**7),10**7);k[j][i]=-k[i][j]
    m11=[[F(12),0,0,12],[0,6,-4,0],[0,-4,4,0],[12,0,0,2*tau]]
    m12=[[0,6,-4,0],[6,0,0,-4],[-4,0,0,3-tau],[0,-4,3-tau,0]]
    m22=[[F(6),0,0,-4],[0,12,12,0],[0,12,2*tau,0],[-4,0,0,4]]
    q=[[F(0) for _ in range(8)] for _ in range(8)]
    for i in range(4):
        for j in range(4):
            q[i][j]=F(m11[i][j]);q[i+4][j+4]=F(m22[i][j])
            q[i][j+4]=F(m12[i][j])+k[i][j];q[i+4][j]=F(m12[i][j])-k[i][j]
    rho=F(int(margin.value*10**6/2),10**6)
    pivots=exact_ldl([[q[i][j]-(rho if i==j else 0) for j in range(8)] for i in range(8)])
    out={'status':'EXACT_STRICT_RANK_ONE_CONVEXITY_CERTIFICATE','tau':str(tau),
         'coefficient_vector':['1','1',str(tau),str(3-tau),'0','0','4','-4','0'],
         'K':[[str(c) for c in row] for row in k],'Q':[[str(c) for c in row] for row in q],
         'gram_margin':str(rho),'shifted_LDL_pivots':[str(c) for c in pivots],
         'numerical_status':problem.status,'numerical_margin':float(margin.value),
         'wall_seconds':time.monotonic()-start,'QC':'NOT_DETERMINED','PC':'NOT_DETERMINED'}
    Path('EXACT_ACOUSTIC.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['K','Q','shifted_LDL_pivots']},indent=2))

if __name__=='__main__':main()
