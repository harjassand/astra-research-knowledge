#!/usr/bin/env python3
"""Finite actual resource trace. Numeric output is diagnostic only.

All continuing states are acquired by BFS from the raw policy, with the
proved population cap checked. No unobserved incoming law is substituted.
"""
from collections import deque
from pathlib import Path
import sys
import json
import numpy as np
from check_joint_resource_cap import continuing,resources,Y

P=Path(__file__).resolve().parent

def ff(x,y):
    out=1
    for a,s in zip(x,y):
        if a<s:return 0
        for j in range(s):out*=a-j
    return out

def events(x):
    a,b,c,d,e,f=x
    for block in range(2):
        o=3*block
        for s in range(4):
            rate=ff(x[o:o+3],Y[s])
            if not rate:continue
            out=list(x)
            for j in range(3):out[o+j]+=Y[(s+1)%4][j]-Y[s][j]
            success=out[0]==out[3]==0
            cont=continuing(x[o],x[o+1],s) and not success
            yield tuple(out),rate,cont,'success' if success else ('normal' if cont else 'failure'),('block',block,s)
    for donor,k in ((0,2),(1,1)):
        o=3*donor;t=3*(1-donor)
        rate=k*a*d*ff(x[o+1:o+3],(2,2))
        if not rate:continue
        out=list(x);out[o+1]-=2;out[o+2]-=2;out[t+1]+=2;out[t+2]+=2
        cont=x[o]<=2
        yield tuple(out),rate,cont,'normal' if cont else 'failure',('core',donor)

def graph(root,cap=300000):
    ind={root:0};xs=[root];rows=[];todo=deque([root]);H=max(root[0],root[3]);mcap=sum(root)+20*(H+5)
    r0=resources(root)
    while todo:
        x=todo.popleft();row=[]
        assert resources(x)[0]<=r0[0] and resources(x)[1]<=r0[1]
        for out,rate,cont,kind,label in events(x):
            assert sum(out)<=mcap
            if cont:
                if out not in ind:
                    if len(xs)>=cap:return None,len(xs)
                    ind[out]=len(xs);xs.append(out);todo.append(out)
                row.append((ind[out],rate,None,kind,label))
            else:row.append((None,rate,out,kind,label))
        rows.append(row)
    assert len(xs)==len(rows)
    return (xs,rows),len(xs)

def z(x):
    mm=lambda a:(0,2,4)[a] if a<3 else 7
    return 15+sum(x)-mm(x[0])-mm(x[3])

def solve_probe(root,cap=300000,iterations=200000):
    result,size=graph(root,cap)
    if result is None:return {'root':root,'states':size,'status':'STATE_CAP_NOT_SOLVED'}
    xs,rows=result
    # Gauss--Seidel on actual normalized complete trace. State output
    # moments and time are solved together; no generator truncation.
    q=np.array([sum(e[1] for e in row) for row in rows],float)
    rhs=np.zeros((size,5));trans=[]
    zin=z(root)
    for i,row in enumerate(rows):
        tr=[];rhs[i,0]=1/q[i]
        for j,rate,out,kind,label in row:
            prob=rate/q[i]
            if j is None:
                delta=z(out)-zin
                rhs[i,1]+=prob*delta;rhs[i,2]+=prob*delta**2
                rhs[i,3]+=prob;rhs[i,4]+=prob*(kind=='success')
            else:tr.append((j,prob))
        trans.append(tr)
    values=np.zeros_like(rhs);residual=float('inf')
    for it in range(iterations):
        err=0.
        for i,tr in enumerate(trans):
            val=rhs[i].copy()
            for j,p in tr:val+=p*values[j]
            err=max(err,float(np.max(np.abs(val-values[i]))));values[i]=val
        if err<1e-11:
            residual=err;break
    else:return {'root':root,'states':size,'status':'ITERATION_LIMIT_NOT_SOLVED','iterations':iterations,'update_residual':err}
    t,d,d2,p,s=values[0]
    return {'root':root,'states':size,'status':'FINITE_NUMERIC_DIAGNOSTIC','iterations':it+1,
            'max_update_residual':residual,'absorption_probability':p,'success_probability':s,
            'physical_time':t,'mean_delta_Z':d,'second_delta_Z':d2,
            'quadratic_receiving_change_plus_time':2*zin*d+d2+t}

def main():
    if '--sizes' in sys.argv:
        for n in (3,10,30,100):
            result,size=graph((1,0,n,1,2,n),cap=100000)
            print(json.dumps({'n':n,'size':size,'complete':result is not None}))
        return
    out=[]
    for n in (3,10,30):
        for root in ((1,0,n,1,2,n),(3,1,n,0,0,n),(2,0,n,2,0,n)):
            out.append(solve_probe(root,cap=20000,iterations=20000))
            print(json.dumps(out[-1]),flush=True)
    (P/'results/resource_trace_probes.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
