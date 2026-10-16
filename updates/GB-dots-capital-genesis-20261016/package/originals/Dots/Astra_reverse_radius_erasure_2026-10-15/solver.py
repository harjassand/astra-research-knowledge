#!/usr/bin/env python3
"""Numerically propose, then EXACTLY verify a rational interval for C(T).
Usage: python solver.py channel.json [--denominator 1000000000]
JSON is output-row by input-column; use strings such as "1/3" for exact input.
Only the exact Fraction certificate determines the reported interval.
"""
import argparse,json
from fractions import Fraction as F
import numpy as np
from scipy.optimize import minimize

def solve(T,denominator=10**9):
    T=[[F(x) for x in row] for row in T]
    if not T or not T[0]:raise ValueError('Nonempty matrix required')
    n,m=len(T),len(T[0])
    if any(len(row)!=m for row in T) or any(x<0 for row in T for x in row):raise ValueError('Invalid nonnegative rectangular matrix')
    if any(sum(T[y][i] for y in range(n))!=1 for i in range(m)):raise ValueError('Columns must sum to one exactly')
    J=[y for y in range(n) if all(T[y][i]>0 for i in range(m))]
    if not J:
        return {'lower':'1','upper':'1','gap':'0','p':[str(F(1,m))]*m,'u':['0']*n,'common_rows':J,'numeric_status':'No optimization needed'}
    A=np.array([[float(1/T[y][i]) for i in range(m)] for y in J])
    def fun(p):return np.sum(1/(A@p))
    def jac(p):return -np.sum(A/((A@p)[:,None]**2),axis=0)
    res=minimize(fun,np.ones(m)/m,jac=jac,bounds=[(0,1)]*m,constraints=[{'type':'eq','fun':lambda p:p.sum()-1,'jac':lambda p:np.ones(m)}],method='SLSQP',options={'ftol':1e-14,'maxiter':10000})
    p=[F(max(0,float(x))).limit_denominator(denominator) for x in res.x]
    total=sum(p)
    if not total: p=[F(1,m)]*m
    else:p=[x/total for x in p]
    # The exact minimizer in u for this rational p is itself rational.
    u=[F(0)]*n
    for y in J:u[y]=1/sum(p[i]/T[y][i] for i in range(m))
    lo=1-sum(u)
    hi=max(1-2*sum(u)+sum(u[y]**2/T[y][i] for y in J) for i in range(m))
    assert F(0)<=lo<=hi
    return {'lower':str(lo),'upper':str(hi),'gap':str(hi-lo),'lower_float':float(lo),'upper_float':float(hi),'p':list(map(str,p)),'u':list(map(str,u)),'common_rows':J,'numeric_status':str(res.message)}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('channel');ap.add_argument('--denominator',type=int,default=10**9);args=ap.parse_args()
    with open(args.channel) as f:T=json.load(f)
    print(json.dumps(solve(T,args.denominator),indent=2))
