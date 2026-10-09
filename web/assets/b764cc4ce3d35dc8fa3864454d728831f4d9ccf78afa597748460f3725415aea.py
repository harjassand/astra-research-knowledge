#!/usr/bin/env python3
"""One exact complex repeated-spectrum control at r=1/4 and 3/4.

Gaussian rational arithmetic only, with rational matrix powers constructed
from a specified exact unitary. No scan or floating spectral calculation.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import runpy
import sys


def run():
    helper=Path(__file__).resolve().parent.parent/'cycle09_lp_review'/'verify_exposed_p4_exact.py'
    assert hashlib.sha256(helper.read_bytes()).hexdigest()=='aee20be2e4228bdd9d4c349ed7a9d338ebb0efb3042e7ed86880e0cd5fce896b'
    ns=runpy.run_path(str(helper),run_name='readonly_exact_helper')
    C,diag,add,scale,mul,adj,tr=[ns[k] for k in ['C','diag','add','scale','mul','adj','tr']]
    sv=[F(1),F(1),F(16)]
    S=diag(sv)
    B1=[[C(1),C(2,1),C(-1)],[C(0,1),C(-2),C(3,-1)],[C(2),C(1,2),C(F(1,2))]]
    vv=[C(1),C(1),C(0,1)]
    noises=[B1,adj(B1),[[vv[i] for _ in range(3)] for i in range(3)]]
    Y,Z=diag([0,0,0]),diag([0,0,0])
    for B in noises:
        Y=add(Y,mul(mul(adj(B),S),B))
        Z=add(Z,mul(mul(B,S),adj(B)))
    D=[]
    for i in range(3):
        row=[]
        for j in range(3):
            if sv[i]==sv[j]:
                assert Y[i][j]==Z[i][j]
                row.append(Y[i][j]/sv[i])
            else:row.append(2*(sv[i]*Y[i][j]-sv[j]*Z[i][j])/(sv[i]**2-sv[j]**2))
        D.append(row)
    assert D!=adj(D)

    def H(X):
        out=scale(add(mul(adj(D),X),mul(X,D)),F(1,2))
        for B in noises:out=add(out,scale(mul(mul(adj(B),X),B),-1))
        return out

    def Hstar(X):
        out=scale(add(mul(D,X),mul(X,adj(D))),F(1,2))
        for B in noises:out=add(out,scale(mul(mul(B,X),adj(B)),-1))
        return out

    assert H(S)==Hstar(S)==diag([0,0,0])
    rootS,invrootS=diag([1,1,4]),diag([1,1,F(1,4)])
    Cphys=mul(mul(rootS,D),invrootS)
    KKs=diag([0,0,0])
    for B in noises:
        K=mul(mul(rootS,B),invrootS)
        KKs=add(KKs,mul(adj(K),K))
    assert add(Cphys,adj(Cphys))==scale(KKs,2)
    ve=[F(1),F(2),F(3)]
    O=[[C((1 if i==j else 0)-ve[i]*ve[j]/7) for j in range(3)] for i in range(3)]
    phase=[C(1),C(0,1),C(F(3,5),F(4,5))]
    U=[[phase[i]*O[i][j] for j in range(3)] for i in range(3)]
    assert mul(adj(U),U)==diag([1,1,1])

    def spectral(xs):return mul(mul(U,diag(xs)),adj(U))
    qs=[F(1),F(4),F(9)]
    rootqs=[F(1),F(2),F(3)]
    q=spectral(qs)
    assert ns['comm'](q,S)!=diag([0,0,0])
    sq,siq=diag([1,1,2]),diag([1,1,F(1,2)])
    g=mul(mul(siq,spectral([1,8,27])),siq)
    h=mul(mul(sq,spectral([1,2,3])),sq)
    direct={F(1,4):tr(mul(g,H(h))),F(3,4):tr(mul(h,H(g)))}
    energy=tr(mul(q,scale(add(H(q),Hstar(q)),F(1,2))))
    assert all(x.i==0 for x in [*direct.values(),energy])
    assert direct[F(1,4)]!=direct[F(3,4)]
    grams={F(1,4):C(),F(3,4):C()}
    gram_E=C()
    pos=[0,0,1]
    for B in noises:
        parts={}
        for n in [-1,0,1]:
            Bn=[[B[i][j] if pos[i]-pos[j]==n else C() for j in range(3)] for i in range(3)]
            parts[n]=mul(mul(adj(U),Bn),U)
        for i in range(3):
            for k in range(3):
                for n in parts:
                    for m in parts:
                        ez=(qs[i]/qs[k])/(F(4)**(n+m))
                        root_ez=(rootqs[i]/rootqs[k])/(F(2)**(n+m))
                        dh=m-n
                        if dh:
                            dy=ns['sh'](F(8)**dh)/ns['sh'](F(16)**dh)
                            dz=ns['sh'](F(2)**dh)/ns['sh'](F(16)**dh)
                        else:dy,dz=F(3,4),F(1,4)
                        kr={F(1,4):dy/ez+dz*ez-1/root_ez,F(3,4):dz/ez+dy*ez-root_ez}
                        amp=qs[i]*qs[k]*parts[n][i][k].star()*parts[m][i][k]
                        for r in grams:grams[r]+=amp*kr[r]
                        gram_E+=amp*(ns['ch'](ez)/ns['ch'](F(4)**dh)-1)
    assert grams==direct
    assert gram_E==energy
    scalar_checks=0
    for r in [F(1,4),F(3,4)]:
        alpha=1-r
        for i in range(3):
            for j in range(3):
                R,Uv=F(16)**i,F(16)**j
                v,w=R*R,Uv*Uv
                vp=F(64 if alpha==F(3,4) else 4)**i
                wp=F(64 if alpha==F(3,4) else 4)**j
                if v==w:
                    dd=alpha*(1-alpha)/2 if v==1 else ((vp-1)-alpha*(vp/v)*(v-1))/(v-1)**2
                else:
                    fv=alpha if v==1 else (vp-1)/(v-1)
                    fw=alpha if w==1 else (wp-1)/(w-1)
                    dd=-(fv-fw)/(v-w)
                pref=F(2)**((1 if r==F(3,4) else -1)*(i+j))
                integral_form=pref*(v-1)*(w-1)*dd
                dh=i-j
                ez=F(4)**(i+j)
                if dh:
                    y=ns['sh'](F(8)**dh)/ns['sh'](F(16)**dh)
                    z=ns['sh'](F(2)**dh)/ns['sh'](F(16)**dh)
                else:y,z=F(3,4),F(1,4)
                direct_scalar=y/ez+z*ez-F(2)**(-(i+j)) if r==F(1,4) else z/ez+y*ez-F(2)**(i+j)
                assert integral_form==direct_scalar
                scalar_checks+=1
    return {
        'status':'PASS',
        'arithmetic':'Exact Gaussian rational; specified exact unitary and rational quarter powers',
        'dimension':3,
        'raw_s':['1','1','16'],
        'r_values':['1/4','3/4'],
        'T_1_over_4':str(direct[F(1,4)].r),
        'T_3_over_4':str(direct[F(3,4)].r),
        'E_root':str(energy.r),
        'orientations_distinct':True,
        'full_complex_noncommuting_state':True,
        'summed_degenerate_stationarity':True,
        'physical_legality_exact':True,
        'kernel_matches_both_actual_pairings':True,
        'power_Loewner_checks':scalar_checks,
        'readonly_helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),
        'scan_count':0,
        'scope':'One exact identity diagnostic; analytic proof, not this control, establishes universal lower.'
    }


def main():
    p=Path(__file__).resolve().parent/'BLIND_QUARTER_KERNEL_REPLAY.json'
    result=run()
    if sys.argv[1:]==['--verify']:
        assert json.loads(p.read_text())==result
        print('PASS: exact blind quarter-power kernel replay reproduced.')
    elif not sys.argv[1:]:
        with p.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
        print('PASS: wrote exact blind quarter-power kernel replay.')
    else:raise SystemExit('Usage: verify_blind_quarter_kernel.py [--verify]')
    print('sha256',hashlib.sha256(p.read_bytes()).hexdigest())


if __name__=='__main__':main()
