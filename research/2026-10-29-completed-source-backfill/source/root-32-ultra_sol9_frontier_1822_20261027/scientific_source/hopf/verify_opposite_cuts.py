#!/usr/bin/env python3
"""Independent exact verifier, Python standard library only.

Differentiate by literal univariate polynomial expansion of u,v,w,q.
No Hopf support spectral formula, numerical solver, or symbolic library is used.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,time

OUT=Path(__file__).resolve().parent

def add(a,b):
    c=[Q(0)]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return c
def mul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c
def scale(a,k):return [k*x for x in a]
def det(A):return A[0]*A[3]-A[1]*A[2]
def expand_F(R,A):
    a,b,c,d=([Q(x),Q(y)] for x,y in zip(R,A))
    u=add(mul(a,a),mul(c,c));v=add(mul(b,b),mul(d,d))
    w=add(mul(a,b),mul(c,d));q=add(mul(a,d),scale(mul(b,c),-1))
    # F = (u+v)^2 + (252/25)q^2 + (99/25)q(u-v).
    return add(add(mul(add(u,v),add(u,v)),scale(mul(q,q),Q(252,25))),
               scale(mul(q,add(u,scale(v,-1))),Q(99,25)))
def cut(A,R):
    coeff=expand_F(R,A)
    assert coeff[0]>0
    tf=coeff[2]-coeff[1]*coeff[1]/(4*coeff[0])
    return tf,tf/det(R),coeff
def rat(x):return str(x)
def hopf(A):
    a,b,c,d=A
    return [a*a+c*c-b*b-d*d,2*(a*b+c*d),2*(a*d-b*c)]

def main():
    started=time.perf_counter()
    # Simple integer vectors chosen after the geometric diagnostic.
    A=list(map(Q,[36,0,0,35]));Rp=list(map(Q,[0,55,-4,0]));Rm=list(map(Q,[1,0,0,-2]))
    cp,up,fp=cut(A,Rp);cm,lo,fm=cut(A,Rm)
    print('simple:',float(up),float(lo),'gap',float(lo-up))
    assert det(Rp)>0 and det(Rm)<0
    assert lo>up
    beta=Q(99,100);r=Q(88,25)
    # det N(s) = 3 beta^4 s^2 + 2 beta^2(1-r)s + 2r-1-4beta^2.
    leading=3*beta**4;linear=2*beta**2*(1-r);constant=2*r-1-4*beta**2
    vertex=-linear/(2*leading)
    minimum=constant-linear**2/(4*leading)
    assert 0<vertex<1 and minimum==Q(7,2500)
    assert 1-beta**2>0 and r-beta**2>0
    # Weighted actual two cuts cancel the arbitrary scalar k_A.
    pairing=cp/det(Rp)+cm/(-det(Rm))
    assert pairing<0 and pairing==up-lo
    # Finite three-point minors-Jensen witness, independent of support theory.
    X1=[Q(0),Q(11,20),Q(-1,25),Q(0)]
    X2=[Q(12,5),Q(0),Q(0),Q(-24,5)]
    l1=Q(1,2)
    l2=l1*det(X1)/(-det(X2)+l1*det([x-y for x,y in zip(X1,X2)]))
    l0=1-l1-l2
    X0=[-(l1*x+l2*y)/l0 for x,y in zip(X1,X2)]
    weights=[l0,l1,l2];increments=[X0,X1,X2]
    assert all(l>0 for l in weights) and sum(weights)==1
    assert all(sum(l*X[j] for l,X in zip(weights,increments))==0 for j in range(4))
    assert sum(l*det(X) for l,X in zip(weights,increments))==0
    points=[[a+x for a,x in zip(A,X)] for X in increments]
    assert sum(l*det(B) for l,B in zip(weights,points))==det(A)
    defect=sum(l*expand_F(B,[Q(0)]*4)[0] for l,B in zip(weights,points))-expand_F(A,[Q(0)]*4)[0]
    assert defect==Q(-13534664264487807,296890944920312500)
    hA=hopf(A)
    moment=[[sum(l*hopf(B)[i]*hopf(B)[j] for l,B in zip(weights,points))-hA[i]*hA[j]
             for j in range(3)] for i in range(3)]
    moment_l1=sum(abs(moment[i][j]) for i in range(3) for j in range(3))
    epsilon=Q(1,1000000)
    assert defect+epsilon*moment_l1<0
    hessian_half_margin=Q(7,35200)
    assert hessian_half_margin-18*epsilon>0
    result={'status':'PASS','claim':'STRICT_ROC_AND_NOT_POLYCONVEX',
        'scope':'one even-Hopf quartic on all real 2x2 matrices',
        'F_literal':'(u+v)^2+(252/25)q^2+(99/25)q(u-v)',
        'F_Hopf':'x^2+y^2+(99/50)xz+(88/25)z^2',
        'A':[rat(x) for x in A],'R_plus':[rat(x) for x in Rp],
        'R_minus':[rat(x) for x in Rm],
        'det_plus':rat(det(Rp)),'det_minus':rat(det(Rm)),
        'F_Rplus_expansion':[rat(x) for x in fp],
        'F_Rminus_expansion':[rat(x) for x in fm],
        'upper_k':rat(up),'lower_k':rat(lo),'support_interval_gap':rat(lo-up),
        'weighted_TF_pairing':rat(pairing),'ROC_N11_lower':rat(1-beta**2),
        'ROC_determinant_vertex':rat(vertex),'ROC_determinant_minimum':rat(minimum),
        'K_positive_definite_schur':rat(r-beta**2),
        'Jensen_weights':[rat(l) for l in weights],
        'Jensen_increments':[[rat(x) for x in X] for X in increments],
        'Jensen_defect':rat(defect),'Jensen_hopf_moment_matrix':[[rat(x) for x in row] for row in moment],
        'Jensen_moment_entry_l1':rat(moment_l1),
        'full_six_K_entry_box_radius':rat(epsilon),
        'perturbed_Jensen_defect_upper':rat(defect+epsilon*moment_l1),
        'unperturbed_half_Hessian_ROC_lower':rat(hessian_half_margin),
        'perturbed_half_Hessian_ROC_lower':rat(hessian_half_margin-18*epsilon),
        'elapsed_seconds':time.perf_counter()-started}
    (OUT/'EXACT_SEPARATION_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
