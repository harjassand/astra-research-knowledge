#!/usr/bin/env python3
"""Exact topology and synthetic resource controls for candidate covalent handoff.
All numbers are illustrative, not physical measurements; stdlib only.
"""
from math import log, exp, log1p

def connected(edges,x,y):
    d={x}; changed=True
    while changed:
        changed=False
        for a,b in edges:
            if (a in d)!=(b in d):
                d.add(a);d.add(b);changed=True
    return y in d

def structural_check():
    for joined in (False,True):
        es=[('D','N')]
        if joined:es.append(('R','D'))
        assert connected(es,'R','N')==joined
    # An unintended stable R-D bridge is indistinguishable from a good bond.
    assert connected([('R','D'),('D','N')],'R','N')
    print('PASS ideal topological connectivity; WRONG stable R-D also passes.')

def rooted_yield(n,p,d):return (p/(p+d))**(n-1)

def tree_cost(n,q,join_cost=1,leaf_cost=1):
    assert n>0 and n&(n-1)==0 and 0<q<=1
    C=float(leaf_cost)
    while n>1:
        C=(2*C+join_cost)/q;n//=2
    return C

def geometric_max_rounds(n,p):
    ans=0.
    for k in range(200000):
        t=1-exp(n*log1p(-(1-p)**k)) if k>0 else 1.
        ans+=t
        if t<1e-12:break
    return ans

def capture_window(n,epsilon,delta_c,E_M,C_M,k_on=1e6):
    low=log(1/delta_c)/(k_on*E_M)
    high=epsilon/(n*k_on*C_M)
    return low,high,E_M/C_M,low<=high

def main():
    structural_check()
    for n in (16,64,256,1024):
        print('ROOT',n,rooted_yield(n,.87,.01))
    for q in (.5,.87,.99):
        for n in (16,64,256,1024):
            print('TREE',q,n,tree_cost(n,q))
    for n in (16,64,256,1024):
        print('RETAINED PARALLEL ROUNDS',n,geometric_max_rounds(n,.87))
    for E,C in ((.000735,1e-9),(.000735,1e-8),(.00000735,1e-9)):
        print('CAPTURE E, C, range',E,C,capture_window(1000,.01,.01,E,C))
    for n in (16,64,1024):
        print('GLOBAL CLEANUP N',n,'kt>=',log(n/.01))
if __name__=='__main__':main()
