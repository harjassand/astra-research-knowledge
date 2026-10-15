"""Exploratory grid LP. NOT a certificate or a tail proof."""
import argparse, json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

def run(h=.02, limit=16.):
    n=round(limit/h); one=round(1/h)
    assert abs(h*one-1)<1e-10
    x=np.arange(n+1)*h
    rows=[]; cols=[]; vals=[]; b=[]
    def add_integral(row, lo, hi, sign=1.):
        if lo==hi: return
        for j in range(lo,hi+1):
            rows.append(row);cols.append(j)
            vals.append(sign*h*(.5 if j in (lo,hi) else 1))
    for j in range(one+1,n+1):
        row=len(b); lo=abs(j-2*one)
        add_integral(row,lo,j)
        rows.append(row);cols.append(j);vals.append(-2*(x[j]-1))
        b.append(0.)
        if j<2*one:
            row=len(b)
            add_integral(row,lo,j,-1)
            rows.append(row);cols.append(lo);vals.append(2*(x[j]-1))
            b.append(0.)
    A=coo_matrix((vals,(rows,cols)),shape=(len(b),n+1)).tocsr()
    trap=np.full(n+1,h);trap[[0,-1]]*=.5
    norm=2*x*trap
    cost=(2/3)*x**3*trap
    res=linprog(cost,A_ub=A,b_ub=np.array(b),A_eq=norm[None,:],b_eq=[1.],bounds=[(0,None)]*(n+1),method='highs')
    out={'grid_h':h,'cutoff':limit,'success':res.success,'message':res.message}
    if res.success:
        out.update(variance=res.fun,min_constraint_slack=float(np.min(-A@res.x)),noise_weight_below_1=float(np.dot(norm[:one],res.x[:one])),peak_location=float(x[np.argmax(res.x)]),nonzero_initial=[(float(x[j]),float(res.x[j])) for j in range(one+1) if res.x[j]>1e-8])
        np.savez(Path(__file__).parent/f'lp_h{h:.4f}.npz',x=x,g=res.x,duals=res.ineqlin.marginals,eq_dual=res.eqlin.marginals)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--h',type=float,default=.02);p.add_argument('--limit',type=float,default=16.)
    a=p.parse_args();print(json.dumps(run(a.h,a.limit),indent=2))
