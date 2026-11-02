#!/usr/bin/env python3
"""Complete actual four-noncore-event kernel on the joint anchor axes.

Every core path is summed by an exact finite physical Green solve. Coefficients
of eta_1 and eta_2 are rational; eta_2/eta_1 is an algebraic cube root.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
import json
import mpmath as mp
from verify_high_anchor_work import ff,psi,constants,proper_constants,Y

P=Path(__file__).resolve().parent
mp.mp.dps=100

def mv(x):return mp.mpf(x.numerator)/x.denominator
def exact_cubic_sign(A,B,R):
    """Sign of A+B*R^(1/3), using rational comparisons only."""
    A,B,R=F(A),F(B),F(R);assert R>0
    sg=lambda z:int(z>0)-int(z<0)
    if B==0:return sg(A)
    if B>0:return 1 if A>=0 else sg(R-(-A/B)**3)
    return -1 if A<=0 else sg((A/(-B))**3-R)
def raw_list(alpha,beta,kf,kb):
    raw=[]
    for port,rates in enumerate((alpha,beta)):
        for j in range(4):
            s=[0]*6;u=[0]*6;s[3*port:3*port+3]=Y[j];u[3*port:3*port+3]=Y[(j+1)%4]
            raw.append((tuple(s),tuple(u),rates[j]))
    return raw+[((1,2,2,1,0,0),(1,0,0,1,2,2),kf),((1,0,0,1,2,2),(1,2,2,1,0,0),kb)]

def green(x,raw):
    lo=-(min(x[4:6])//2);hi=min(x[1:3])//2
    states=[(x[0],x[1]-2*k,x[2]-2*k,x[3],x[4]+2*k,x[5]+2*k) for k in range(lo,hi+1)]
    n=len(states);assert n<=2
    h=[[v*ff(z,s) for s,u,v in raw[:8]] for z in states];kill=[sum(row) for row in h]
    start=-lo
    if n==1:occ=[1/kill[0]]
    else:
        f=raw[8][2]*ff(states[0],raw[8][0]);b=raw[9][2]*ff(states[1],raw[9][0])
        det=kill[0]*kill[1]+kill[0]*b+f*kill[1]
        occ=[(kill[1]+b)/det,f/det] if start==0 else [b/det,(kill[0]+f)/det]
        assert occ[0]*(kill[0]+f)-occ[1]*b==int(start==0)
        assert occ[1]*(kill[1]+b)-occ[0]*f==int(start==1)
    outputs=defaultdict(F)
    for z,occupation,row in zip(states,occ,h):
        for j,rate in enumerate(row):
            if rate:
                s,u,_=raw[j];after=tuple(a-b+c for a,b,c in zip(z,s,u))
                outputs[after]+=occupation*rate
    assert sum(outputs.values())==1 and min(outputs.values())>0
    return outputs,sum(occ),n

def f_values(x):
    ans=[]
    for q in (0,3):
        A,B,C=x[q:q+3];t=min(B,C);h=abs(B-C)+(3*t+t%2)//2
        ans.append(A-h)
    return ans

def plus_probability(a,rates,B0):
    r0,r1,r2,r3=rates;A1=a+1;A2=a+2;A3=a+3
    t1=r1*A1+B0;t00=2*r1*A2+B0;t01=r2*A2*(A2-1)+r1*A2+B0
    t001=2*r2*A3*(A3-1)+2*r1*A3+B0;t011=2*r2*A3*(A3-1)+r1*A3+B0
    return r0/B0*(r0/t1*(2*r1*A2/t00)*(2*r1*A3/t001)
            +(r1*A1/t1)*(r0/t01)*(2*r1*A3/t001)
            +(r1*A1/t1)*(r1*A2/t01)*(r0/t011))

def clean_formula(a,d,alpha,beta,kf,kb):
    B0=alpha[0]+beta[0]
    p=alpha[0]/B0*alpha[1]*(a+1)/(alpha[1]*(a+1)+B0)
    p*=alpha[2]*(a+2)*(a+1)/(alpha[2]*(a+2)*(a+1)+alpha[1]*(a+2)+B0)
    own2=4*alpha[2]*(a+3)*(a+2)
    rec2=4*beta[2]*d*(d-1)
    k0=4*alpha[3]*(a+3)*(a+2)*(a+1)+own2+2*alpha[1]*(a+3)+B0
    k1=4*beta[3]*d*(d-1)*(d-2)+rec2+2*beta[1]*d+B0
    fw=4*kf*(a+3)*d;bw=4*kb*(a+3)*d;det=k0*k1+k0*bw+fw*k1
    o0=(k1+bw)/det;o1=fw/det
    # Own coordinate coefficient and other coordinate coefficient.
    own=p*(o0*own2*(-2*a+1)+o1*k1*(6*a+9))
    other=p*o1*(k1*(-6*d+9)+rec2*(-2*(d-3)+1))
    return own,other,p*o1*k1,p

def run(a,d,alpha=(1,1,1,1),beta=(1,1,1,1),kf=2,kb=1,save_law=False):
    assert min(a,d)>=8
    alpha=tuple(map(F,alpha));beta=tuple(map(F,beta));kf,kb=F(kf),F(kb)
    c=constants((alpha,beta));ratio=alpha[0]*kf*beta[3]/(beta[0]*kb*alpha[3])
    lower=upper=F(1)
    while lower**3>ratio:lower/=2
    while upper**3<ratio:upper*=2
    H=max(F(1),upper);h=min(F(1),lower)
    # Safe rational constants for all eta in [h,H].
    core=54*H*(2*H/h+1)*max(kf/alpha[3],kb/beta[3]);block=3*H*c['D']
    pc={'c0':8*(c['a']+1)**2,'C':8*(core+block+1/c['B0'])}
    raw=raw_list(alpha,beta,kf,kb);root=(a,0,0,d,0,0);law={root:F(1)};clock=F(0);sizes=[]
    for depth in range(4):
        nxt=defaultdict(F);largest=0
        for x,p in law.items():
            outputs,t,n=green(x,raw);clock+=p*t;largest=max(largest,n)
            for z,v in outputs.items():nxt[z]+=p*v
        law=dict(nxt);assert sum(law.values())==1;sizes.append({'noncore_depth':depth+1,'output_states':len(law),'largest_core_fiber':largest})
    qa=qd=work=F(0);axis_prob=F(0)
    for x,p in law.items():
        fa,fd=f_values(x);assert min(fa,fd)>=0
        qa+=p*(fa*fa-a*a);qd+=p*(fd*fd-d*d)
        w=psi(x,c['a']);work+=p*pc['C']*(2*pc['c0']*w+w*w)
        if x[1]==x[2]==x[4]==x[5]==0:axis_prob+=p
    ia,id_,ti,pi=clean_formula(a,d,alpha,beta,kf,kb)
    jd,ja,tj,pj=clean_formula(d,a,beta,alpha,kb,kf)
    plusi=plus_probability(a,alpha,c['B0']);plusj=plus_probability(d,beta,c['B0'])
    assert qa==ia+ja+(2*a+1)*plusi
    assert qd==id_+jd+(2*d+1)*plusj
    B0=c['B0'];Da=c['D']+B0/min(alpha[3],beta[3])
    Ki=alpha[0]/B0*(B0/alpha[1]+(alpha[1]+B0)/alpha[2])
    Kj=beta[0]/B0*(B0/beta[1]+(beta[1]+B0)/beta[2])
    plus_bound=lambda r:r[0]**2/(B0*r[2])+F(3,2)*r[0]**2*r[1]/(B0*r[2]**2)
    assert plusi<=plus_bound(alpha)/a**2 and plusj<=plus_bound(beta)/d**2
    prob_bound=(Ki+Da)/a+(Kj+Da)/d
    work_bound=pc['C']*((pc['c0']+8*c['a'])**2-pc['c0']**2)*prob_bound
    assert 1-axis_prob<=prob_bound and work<=work_bound and clock<=4/B0
    eta=mp.root(mv(ratio),3);delta=mv(qa)+eta*mv(qd)+mv(work);total=delta+mv(clock)
    out={'input':list(map(str,root)),'alpha':[str(v) for v in alpha],'beta':[str(v) for v in beta],
         'core_rates':[str(kf),str(kb)],'eta_ratio_cube_exact':str(ratio),'eta_ratio':mp.nstr(eta,40),
         'proper_constants':{k:str(v) for k,v in pc.items()},'frontier_constants':{k:str(v) for k,v in c.items()},
         'physical_mean_exact':str(clock),'Q_eta1_coefficient_exact':str(qa),'Q_eta2_coefficient_exact':str(qd),
         'work_receiving_increment_exact':str(work),'axis_output_probability_exact':str(axis_prob),
         'first_clean_probabilities':[str(pi),str(pj)],'transferred_exit_probabilities':[str(ti),str(tj)],
         'complete_positive_word_and_unfinished_work_bounds_replayed':True,
         'exact_complete_Q_formula_replayed':True,'costs':sizes,
         'physical_mean':mp.nstr(mv(clock),30),'mean_U_increment':mp.nstr(delta,30),
         'mean_physical_time_plus_U_increment':mp.nstr(total,30),
         'exact_sign_mean_U_increment':exact_cubic_sign(qa+work,qd,ratio),
         'exact_sign_mean_physical_time_plus_U_increment':exact_cubic_sign(clock+qa+work,qd,ratio),
         'scope':'Exact complete four-noncore actual kernel, rational receiver coefficients and exact cubic-field signs; multiprecision decimals are for display. A finite fixture sign is not the all-axes proof or global recurrence.'}
    if save_law:out['complete_actual_output_law']=[{'state':list(map(str,x)),'probability_exact':str(p)} for x,p in sorted(law.items())]
    return out

def main():
    N=10**12
    fixtures=((10,10),(1000,1000),(10**6,10**6),(N,N),(1259921049895,N),
              (N,2*N),(2*N,N),(N,100*N),(100*N,N),(N,N*N),(N,N**3),(N**3,N))
    rows=[]
    for a,d in fixtures:
        row=run(a,d,save_law=(a==N and d==N));rows.append(row)
        print(json.dumps({'axes':[str(a),str(d)],'mean_time':row['physical_mean'],
              'mean_U_increment':row['mean_U_increment'],'time_plus_U_increment':row['mean_physical_time_plus_U_increment'],
              'exact_Q_formula_replayed':True}),flush=True)
    out={'fixtures':rows,'scope':'Complete exact source kernels and finite diagnostics, separate from quantified high-axis theorem.'}
    (P/'results/four_nc_axis_checks.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
