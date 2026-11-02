#!/usr/bin/env python3
"""Exact two-state reversible sulfur chemistry and cumulative challenge audit.
All numeric rates are hypothetical, NOT experimental. Standard library only.
"""
from fractions import Fraction as F
from math import exp,log

def chemistry(a,h,e,b,k,w):
    # U->T(a), hydrolysis(h), wrong(e); T->U(b), correct(k), wrong(w).
    U=a+h+e;T=b+k+w;det=U*T-a*b
    c=a*k/det; wrong=(e*T+a*w)/det;hydro=h*T/det
    assert c+wrong+hydro==1
    assert wrong/c==w/k+(e/a)*(T/k)
    return {"P_correct":c,"P_wrong":wrong,"P_hydrolysis":hydro,
            "E_reaction_time":(T+a)/det,"wrong_to_correct":wrong/c}

def exposure_counts(n):
    assert n>0 and n&(n-1)==0
    L=n.bit_length()-1
    serial=n*(n-1)//2
    tree=sum(n-n//(1<<level) for level in range(1,L+1))
    assert tree==n*L-(n-1)
    return serial,tree

def challenge(n,eps_transient,eps_amide,k_cut,k_amide,p_transient):
    t=log(n*p_transient/eps_transient)/k_cut
    Bserial,Btree=exposure_counts(n)
    assert abs(n*p_transient*exp(-k_cut*t)-eps_transient)<1e-12
    return {
        "time_s":t,"serial_bond_exposures":Bserial,"tree_bond_exposures":Btree,
        "serial_correct_survival_lower":exp(-k_amide*t*Bserial),
        "tree_correct_survival_lower":exp(-k_amide*t*Btree),
        "max_k_amide_serial":-log(1-eps_amide)/(t*Bserial),
        "max_k_amide_tree":-log(1-eps_amide)/(t*Btree),
        "exposure_ratio":Bserial/Btree}

def tree_restarts(n,q,leaf_cost=1,join_cost=1):
    assert n>0 and n&(n-1)==0 and 0<q<=1
    C=float(leaf_cost)
    while n>1:
        C=(2*C+join_cost)/q;n//=2
    return C

def main():
    rates=chemistry(F(3,10),F(1,10),F(1,1000000),
                    F(1,5),F(1,2),F(1,10000000))
    for k,v in rates.items():print(k,str(v),float(v))
    for n in (64,256,1024):
        print("REQUIRED terminal bad/good ratio",n,.99**(-1/(n-1))-1)
        print("CHALLENGE",n,challenge(n,.005,.005,.1,5e-9,.15))
        print("EXPECTED WORK 0.87/0.99",n,tree_restarts(n,.87),tree_restarts(n,.99))
    print("Wrong durable amide is topologically identical to correct durable amide.")
if __name__=="__main__":main()
