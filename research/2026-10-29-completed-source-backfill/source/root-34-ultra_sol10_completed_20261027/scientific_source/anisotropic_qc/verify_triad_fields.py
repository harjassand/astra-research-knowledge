#!/usr/bin/env python3
"""Exact Laurent replay of three acquired smooth periodic gradient rays.

It proves only that these three rounded fields do not violate Jensen for
any overall amplitude. It does not prove QC or bound the searched family.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,time,math
HERE=Path(__file__).resolve().parent
ZERO=(0,0)

def plus(a,b):
    out=dict(a)
    for k,v in b.items():out[k]=out.get(k,Q(0))+v
    return {k:v for k,v in out.items() if v}
def scale(a,t):return {k:t*v for k,v in a.items() if t*v}
def times(a,b):
    out={}
    for k,v in a.items():
        for l,w in b.items():
            n=(k[0]+l[0],k[1]+l[1]);out[n]=out.get(n,Q(0))+v*w
    return {k:v for k,v in out.items() if v}
def const(x):return {ZERO:Q(x)} if x else {}
def mean(a):return a.get(ZERO,Q(0))

def run():
    start=time.perf_counter();saved=json.loads((HERE/'TRIAD_SEARCH.json').read_text());rows=[]
    for rec in saved['records']:
        z=rec['parameters'];phi,angle,logr=z[6:]
        k1=[math.cos(phi),math.sin(phi)]
        k2=[math.exp(logr)*math.cos(phi+angle),math.exp(logr)*math.sin(phi+angle)]
        wave=[[Q(round(x*10**6),10**6) for x in k] for k in [k1,k2]]
        wave.append([wave[0][j]+wave[1][j] for j in range(2)])
        polar=[[Q(round(z[2*i+j]*10**6),10**6) for j in range(2)] for i in range(3)]
        assert wave[0][0]*wave[1][1]-wave[0][1]*wave[1][0]!=0
        G=[{} for _ in range(4)]
        for mode,k,u in zip([(1,0),(0,1),(1,1)],wave,polar):
            for i in range(2):
                for j in range(2):
                    coeff=u[i]*k[j]/2;idx=2*i+j
                    G[idx]=plus(G[idx],{mode:coeff,(-mode[0],-mode[1]):coeff})
        assert all(mean(x)==0 for x in G)
        if rec['label']=='main99':A=list(map(Q,[36,0,0,35]))
        else:A=list(map(Q,[1,0,0,1]))
        if rec['label']=='norm4':kap=Q(0);L=Q(0)
        elif rec['label']=='main99':kap=Q(252,25);L=Q(99,25)
        else:kap=Q(12);L=4*Q(197**2-1,197**2+1)
        a,b,c,d=G;aa,bb,cc,dd=A
        TA=sum(x*x for x in A);qA=aa*dd-bb*cc;xA=aa*aa+cc*cc-bb*bb-dd*dd
        Tl=scale(plus(plus(scale(a,aa),scale(b,bb)),plus(scale(c,cc),scale(d,dd))),2)
        Tg=plus(plus(times(a,a),times(b,b)),plus(times(c,c),times(d,d)))
        ql=plus(plus(scale(a,dd),scale(b,-cc)),plus(scale(c,-bb),scale(d,aa)))
        qg=plus(times(a,d),scale(times(b,c),-1))
        assert mean(qg)==0
        xl=scale(plus(plus(scale(a,aa),scale(c,cc)),plus(scale(b,-bb),scale(d,-dd))),2)
        xg=plus(plus(times(a,a),times(c,c)),scale(plus(times(b,b),times(d,d)),-1))
        P2=mean(plus(plus(times(Tl,Tl),scale(Tg,2*TA)),
            plus(scale(plus(times(ql,ql),scale(qg,2*qA)),kap),
                 scale(plus(plus(scale(xg,qA),times(ql,xl)),scale(qg,xA)),L))))
        P3=mean(plus(plus(scale(times(Tl,Tg),2),scale(times(ql,qg),2*kap)),
                      scale(plus(times(ql,xg),times(qg,xl)),L)))
        P4=mean(plus(plus(times(Tg,Tg),scale(times(qg,qg),kap)),scale(times(qg,xg),L)))
        assert P2>0 and P4>0 and P3*P3<4*P2*P4
        ratio=P3*P3/(4*P2*P4)
        assert abs(float(ratio)-rec['best_ratio'])<1e-5
        rows.append({'label':rec['label'],'physical_background':list(map(str,A)),
                     'rational_waves':[[str(x) for x in k] for k in wave],
                     'rational_polarizations':[[str(x) for x in u] for u in polar],
                     'P2':str(P2),'P3':str(P3),'P4':str(P4),'ratio_exact':str(ratio),
                     'ratio_float_diagnostic':float(ratio),'mean_gradient_and_determinant_zero':True,
                     'no_negative_Jensen_for_any_amplitude_on_this_ray':True})
    out={'status':'EXACT_THREE_FIELD_REPLAY_PASS','scope':'only the three rounded acquired gradient rays; not a family-wide or QC assertion',
         'rows':rows,'seconds':time.perf_counter()-start}
    (HERE/'TRIAD_EXACT_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'ratios':[r['ratio_float_diagnostic'] for r in rows],'seconds':out['seconds']},indent=2))

if __name__=='__main__':run()
