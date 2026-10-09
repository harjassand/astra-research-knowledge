#!/usr/bin/env python3
"""One exact complex control with repeated sigma eigenvalues and summed balance.

Gaussian-rational matrices and rational coefficients of formal log2/log3.
No scan, floating arithmetic or logarithm/spectrum approximation.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import runpy
import sys


def run():
    own=Path(__file__).resolve().parent.parent
    helper=own/'cycle09_lp_review'/'verify_exposed_p4_exact.py'
    assert hashlib.sha256(helper.read_bytes()).hexdigest()=="aee20be2e4228bdd9d4c349ed7a9d338ebb0efb3042e7ed86880e0cd5fce896b"
    ns=runpy.run_path(str(helper),run_name='readonly_exact_helper')
    C,diag,add,scale,mul,adj,tr=[ns[x] for x in ['C','diag','add','scale','mul','adj','tr']]
    sv=[F(1),F(1),F(4)]
    S=diag(sv)
    rootS=diag([1,1,2])
    invrootS=diag([1,1,F(1,2)])
    B1=[[C(1),C(2,1),C(-1)],
        [C(0,1),C(-2),C(3,-1)],
        [C(2),C(1,2),C(F(1,2))]]
    B2=adj(B1)
    vv=[C(1),C(1),C(0,1)]
    B3=[[vv[i] for _ in range(3)] for i in range(3)]
    noises=[B1,B2,B3]
    Ys=[mul(mul(adj(B),S),B) for B in noises]
    Zs=[mul(mul(B,S),adj(B)) for B in noises]
    Y=diag([0,0,0])
    ZZ=diag([0,0,0])
    for y,z in zip(Ys,Zs):Y,ZZ=add(Y,y),add(ZZ,z)
    assert any(Ys[0][i][j]!=Zs[0][i][j] for i in [0,1] for j in [0,1])
    assert all(Y[i][j]==ZZ[i][j] for i in [0,1] for j in [0,1])
    D=[]
    for i in range(3):
        row=[]
        for j in range(3):
            if sv[i]==sv[j]:
                assert Y[i][j]==ZZ[i][j]
                row.append(Y[i][j]/sv[i])
            else:row.append(2*(sv[i]*Y[i][j]-sv[j]*ZZ[i][j])/(sv[i]**2-sv[j]**2))
        D.append(row)
    assert D!=adj(D)
    V=scale(add(D,adj(D)),F(1,2))

    def H(X):
        out=scale(add(mul(adj(D),X),mul(X,D)),F(1,2))
        for B in noises:out=add(out,scale(mul(mul(adj(B),X),B),-1))
        return out

    def Hstar(X):
        out=scale(add(mul(D,X),mul(X,adj(D))),F(1,2))
        for B in noises:out=add(out,scale(mul(mul(B,X),adj(B)),-1))
        return out

    assert H(S)==Hstar(S)==diag([0,0,0])
    Cphys=mul(mul(rootS,D),invrootS)
    Ks=[mul(mul(rootS,B),invrootS) for B in noises]
    KK=diag([0,0,0])
    for K in Ks:KK=add(KK,mul(adj(K),K))
    assert add(Cphys,adj(Cphys))==scale(KK,2)

    def Lstar(X):
        out=scale(add(mul(Cphys,X),mul(X,adj(Cphys))),F(1,2))
        for K in Ks:out=add(out,scale(mul(mul(K,X),adj(K)),-1))
        return out

    assert Lstar(mul(S,S))==diag([0,0,0])
    ve=[F(1),F(2),F(3)]
    O=[[C((1 if i==j else 0)-ve[i]*ve[j]/7) for j in range(3)] for i in range(3)]
    phase=[C(1),C(0,1),C(F(3,5),F(4,5))]
    U=[[phase[i]*O[i][j] for j in range(3)] for i in range(3)]
    assert mul(adj(U),U)==diag([1,1,1])

    def spectral(xs):return mul(mul(U,diag(xs)),adj(U))
    qs=[F(1),F(4),F(9)]
    q=spectral(qs)
    rho=mul(q,q)
    assert ns['comm'](q,S)!=diag([0,0,0])
    Lrho=Lstar(rho)
    direct_J2=tr(mul(Lrho,add(spectral([0,4,0]),scale(diag([0,0,4]),-1))))
    direct_J3=tr(mul(Lrho,spectral([0,0,4])))
    direct_E=tr(mul(q,scale(add(H(q),Hstar(q)),F(1,2))))
    assert direct_J2.i==direct_J3.i==direct_E.i==0
    # Frequency n log4; exponent exp(omega)=4^n, n=-1,0,1.
    pos=[0,0,1]
    bexponents=[(0,0),(2,0),(0,2)]  # log q_i as log2/log3 coefficients
    gram_J0,gram_J2,gram_J3,gram_E=C(),C(),C(),C()
    diagonal_pairs=[]
    for B in noises:
        freqs={}
        for n in [-1,0,1]:
            Bn=[[B[i][j] if pos[i]-pos[j]==n else C() for j in range(3)] for i in range(3)]
            freqs[n]=mul(mul(adj(U),Bn),U)
        for i in range(3):
            for k in range(3):
                pair=[C(),C(),C()]
                for n in freqs:
                    for m in freqs:
                        e_z=(qs[i]/qs[k])/(F(2)**(n+m))
                        z2=bexponents[i][0]-bexponents[k][0]-(n+m)
                        z3=bexponents[i][1]-bexponents[k][1]
                        h2=m-n
                        if h2==0:
                            constant=e_z-1/e_z
                            j2=-2*z2/e_z
                            j3=-2*z3/e_z
                        else:
                            e_2h=F(4)**h2
                            coth=(e_2h+1/e_2h)/(e_2h-1/e_2h)
                            csch=2/(e_2h-1/e_2h)
                            constant=F()
                            j2=-2*(z2+h2*coth)/e_z+2*e_z*h2*csch
                            j3=-2*z3/e_z
                        Lzero=ns['ch'](e_z)/ns['ch'](F(2)**h2)-1
                        amp=qs[i]*qs[k]*freqs[n][i][k].star()*freqs[m][i][k]
                        pair[0]+=amp*constant
                        pair[1]+=amp*j2
                        pair[2]+=amp*j3
                        gram_E+=amp*Lzero
                for v in pair:assert v.i==0
                gram_J0+=pair[0]
                gram_J2+=pair[1]
                gram_J3+=pair[2]
                if i==k:diagonal_pairs.append([str(v.r) for v in pair])
    assert gram_J0==C()
    assert gram_J2==direct_J2
    assert gram_J3==direct_J3
    assert gram_E==direct_E
    assert any(any(x!="0" for x in pair) for pair in diagonal_pairs)

    # Exact scalar Loewner representation algebra at three fixed positive
    # exponential nodes: coefficients in formal log2, allowing zero node x=0.
    rs=[F(1),F(2),F(4)]
    kvals=[0,1,2]
    loewner_checks=0
    for i,r in enumerate(rs):
        for j,t in enumerate(rs):
            if i==j:
                if r==1:continue
                # g'(r^2)=[r^2-1-log(r^2)]/(r^2-1)^2
                loew_const=(r*r-1)/(r*r-1)**2
                loew_log=-2*kvals[i]/(r*r-1)**2
            else:
                def gg(v,k):
                    return (F(1),F()) if v==1 else (F(),v*(2*k)/(v-1))
                gc,gl=gg(r*r,kvals[i]);hc,hl=gg(t*t,kvals[j])
                loew_const=(gc-hc)/(r*r-t*t)
                loew_log=(gl-hl)/(r*r-t*t)
            # sqrt(r*t) may be irrational. Square congruence avoided by
            # multiplying both expressions by sqrt(r*t) before comparison.
            lhs_const=(r*r-1)*(t*t-1)*loew_const
            lhs_log=(r*r-1)*(t*t-1)*loew_log
            zz=F(kvals[i]+kvals[j],2)
            hh=F(kvals[i]-kvals[j],2)
            # Jker*sqrt(rt): exp(-z)*sqrt(rt)=1, exp(z)*sqrt(rt)=rt.
            if hh==0:
                rhs_const=r*t-1
                rhs_log=-2*zz
            else:
                exp2h=r/t
                co=(exp2h+1/exp2h)/(exp2h-1/exp2h)
                cs=2/(exp2h-1/exp2h)
                rhs_const=F()
                rhs_log=-2*(zz+hh*co)+2*r*t*hh*cs
            assert lhs_const==rhs_const and lhs_log==rhs_log
            loewner_checks+=1
    return {
        'status':'PASS',
        'arithmetic':'Gaussian rational and rational coefficients of formal log2/log3; no floats',
        'dimension':3,
        'raw_s':['1','1','4'],
        'sigma_repeated_eigenvalue':True,
        'individual_noise_stationarity_not_assumed':True,
        'summed_degenerate_block_balance':True,
        'non_HS_selfadjoint':True,
        'full_complex_noncommuting_rho':True,
        'physical_J_log2_coefficient':str(direct_J2.r),
        'physical_J_log3_coefficient':str(direct_J3.r),
        'physical_root_E':str(direct_E.r),
        'exact_entropy_Gram_constant_cancellation':True,
        'exact_entropy_Gram_log2_log3_match':True,
        'exact_root_Gram_match':True,
        'nonzero_diagonal_ordered_pairs':True,
        'scalar_Loewner_prefactor_checks':loewner_checks,
        'readonly_helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),
        'scan_count':0,
        'scope':'One exact identity control and scalar-factor diagnostics; not a universal kernel comparison proof.'
    }


def main():
    path=Path(__file__).resolve().parent/'EXACT_GENERAL_GRAM_REPLAY.json'
    result=run()
    if sys.argv[1:]==['--verify']:
        assert json.loads(path.read_text())==result
        print('PASS: exact general forward Gram and summed-degeneracy replay reproduced.')
    elif not sys.argv[1:]:
        with path.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
        print('PASS: wrote exact general forward Gram and summed-degeneracy replay.')
    else:raise SystemExit('Usage: verify_exact_general_gram.py [--verify]')
    print('sha256',hashlib.sha256(path.read_bytes()).hexdigest())


if __name__=='__main__':main()
