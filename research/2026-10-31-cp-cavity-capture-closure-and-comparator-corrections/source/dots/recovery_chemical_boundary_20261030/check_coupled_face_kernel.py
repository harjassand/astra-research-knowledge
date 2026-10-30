"""Finite-shell falsification only; not proof of uniform kernel estimates."""
import json, math, time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu

def run(n):
    st=[(a,c,e,n-a-c-e) for a in range(n+1) for c in range(n-a+1) for e in range(n-a-c+1)
        if n-a-c-e>0 or c*e>0]
    ix={x:i for i,x in enumerate(st)}; nn=len(st)
    rr=[];cc=[];vv=[]; rhs=np.zeros((nn,5))
    for i,(a,c,e,d) in enumerate(st):
        A=a+2; F=A*(A-1); kill=a*(a-1); total=kill
        rhs[i,0]=1/F;rhs[i,1]=A/F
        rhs[i,4]=kill*(1+a-2)**(-4) if kill else 0
        moves=[((-1,1,0,0),a*d),((0,-1,1,0),c*d),((1,0,-1,0),e*d),
               ((1,0,0,-1),a*d+d*(d-1)),((-1,0,0,1),a*(a-1)),
               ((-2,0,0,2),a*(a-1)),((0,0,1,-1),c*d),((0,0,-1,1),c*e)]
        for delta,rate in moves:
            if rate==0: continue
            y=tuple(x+v for x,v in zip((a,c,e,d),delta));total+=rate
            j=ix.get(y)
            if j is None:
                assert y[3]==0 and y[1]*y[2]==0
                rhs[i,2]+=rate;rhs[i,3]+=rate*(1+y[0]+2)**(-4)
                rhs[i,4]+=rate*(1+y[0]+2)**(-4)
            else: rr.append(i);cc.append(j);vv.append(-rate)
        rr.append(i);cc.append(i);vv.append(total)
    mat=coo_matrix((vv,(rr,cc)),shape=(nn,nn)).tocsc();sol=splu(mat).solve(rhs)
    residual=float(np.max(np.abs(mat@sol-rhs)))
    x=np.array([1+a for a,c,e,d in st]);T,U,P,V,O=sol.T
    j=ix[(0,n-1,0,1)]
    return dict(n=n,states=nn,max_F_return=float(P.max()),max_F_return_scaled=float(P.max()*n**.2),
        C_axis_seed_return=float(P[j]),C_axis_seed_T=float(T[j]),
        max_x_T_over_U=float(np.max(x*T/U)),max_x2_V4_over_U=float(np.max(x*x*V/U)),
        max_output_f4=float(O.max()),linear_solve_residual=residual,
        caveat='Unit rates, no connector births, physical common factor A(A-1), (b)_q normalized to1. Finite scan only.')
if __name__=='__main__':
    out=[run(n) for n in (8,16,32)]
    print(json.dumps(out,indent=2))
    open(__file__.replace('.py','.json'),'w').write(json.dumps(out,indent=2)+'\n')
