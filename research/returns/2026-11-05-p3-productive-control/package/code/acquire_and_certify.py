#!/usr/bin/env python3
"""Synthetic acquisition, rational all-depth certificate, independent checks.
No physical experiment is claimed. Compiler sees counts, rewards and budgets only.
"""
import itertools,json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp
OUT=Path(__file__).resolve().parents[1]/'results'
OUT.mkdir(parents=True,exist_ok=True)
def save(name,x):
    (OUT/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def generate(seed,swap=False):
    rng=np.random.default_rng(seed);m=371368
    src={'A':(.1,.2),'B':(.2,.7)}
    if swap:src={'A':src['B'],'B':src['A']}
    counts={a:dict(zip(('up','down','hold'),map(int,rng.multinomial(m,[p,q,1-p-q])))) for a,(p,q) in src.items()}
    return {'synthetic':True,'seed':seed,'samples_per_action':m,'counts':counts,
            'rewards':{'A':'3','B':'2'},'statistical_radius':'3/1000',
            'systematic_allowance':'1/1000','total_radius':'1/250','delta':'1/100',
            'sampling_state':1,'transfer_premise':'homogeneous rows or independently justified uniform envelope'}
def compile_certificate(data):
    m=data['samples_per_action'];z=F(data['total_radius']);boxes={};c={}
    for a,x in data['counts'].items():
        assert sum(x.values())==m
        p,q,r=F(x['up'],m),F(x['down'],m),F(data['rewards'][a])
        b={'pL':p-z,'pU':p+z,'qL':q-z,'qU':q+z,'rL':r,'rU':r}
        assert b['pL']>0 and b['qL']>=0 and b['pU']+b['qU']<1
        boxes[a]=b
        c[a]={'cL':r/b['pU'],'cU':r/b['pL'],'sL':b['qL']/b['pU'],'sU':b['qU']/b['pL']}
    starts=[a for a in c if all(c[a]['cL']>c[b]['cU'] for b in c if b!=a)]
    assert len(starts)==1,'ABSTAIN: unresolved initial action'
    start=starts[0];L,U=c[start]['cL'],c[start]['cU'];tails=[]
    for a in c:
        if c[a]['sL']<=1 or any(c[a]['sL']<=c[b]['sU'] for b in c if b!=a):continue
        D=max([F(0)]+[max(F(0),c[b]['cU']-c[a]['cL'])/(c[a]['sL']-c[b]['sU']) for b in c if b!=a])
        if L>D:tails.append((a,D))
    assert len(tails)==1,'ABSTAIN: unresolved infinite tail'
    tail,D=tails[0]
    return {'status':'CERTIFIED','prefix':[start],'tail':tail,'boxes':boxes,'coefficient_bounds':c,
            'd0_lower':L,'d0_upper':U,'tail_threshold':D,
            'tail_margin_at_d0_lower':min(c[tail]['cL']-c[b]['cU']+(c[tail]['sL']-c[b]['sU'])*L for b in c if b!=tail),
            'tail_survival_ratio_lower':c[tail]['sL'],'startup_up_upper':boxes[start]['pU'],
            'scope':'Exact optimum for every N and every fixed nearest-neighbor row model in boxes; acquisition transfer separately required'}
def direct_solve(rows,policy):
    # Full rational absorbing-chain matrix solve, independent of the compiler.
    n=len(policy);M=sp.zeros(n);reward=sp.zeros(n,1)
    for i,a in enumerate(policy):
        p,q,r=[sp.Rational(v.numerator,v.denominator) for v in rows[i][a]]
        M[i,i]=p+(q if i else 0);reward[i]=r
        if i:M[i,i-1]=-q
        if i+1<n:M[i,i+1]=-p
    return M.inv()*reward
def check_bellman(rows,policy,v):
    n=len(policy);slacks=[]
    for i in range(n):
        for a,row in rows[i].items():
            p,q,r=[sp.Rational(x.numerator,x.denominator) for x in row]
            future=(1-p-q)*v[i]+q*(v[i-1] if i else v[i])+p*(v[i+1] if i+1<n else 0)
            s=sp.factor(v[i]-r-future);assert s>=0,(i,a,s)
            if a==policy[i]:assert s==0
            else:slacks.append(s)
    return min(slacks)
def value(p0,r0,p,q,r,n):
    d=r0/p0;s=d
    for i in range(1,n):d=(r+q*d)/p;s+=d
    return s
def log10(x):return math.log10(x.numerator)-math.log10(x.denominator)
def main():
    data=generate(2026110501);data2=generate(2026110502,True)
    save('calibration_counts.json',data);save('calibration_counts_swapped.json',data2)
    cert=compile_certificate(data);cert2=compile_certificate(data2)
    save('policy_certificate.json',cert);save('policy_certificate_swapped.json',cert2)
    assert(cert['prefix'],cert['tail'])==(['A'],'B')
    assert(cert2['prefix'],cert2['tail'])==(['B'],'A')
    nominal={'A':(F(1,10),F(1,5),F(3)),'B':(F(1,5),F(7,10),F(2))}
    exhaustive=[]
    for n in range(2,8):
        rows=[nominal]*n;policy=['A']+['B']*(n-1);opt=direct_solve(rows,policy)
        check_bellman(rows,policy,opt)
        for other in itertools.product(('A','B'),repeat=n):
            v=direct_solve(rows,other);assert all(opt[i]>=v[i] for i in range(n))
        f=F(68,5)*(F(7,2)**n-1)-4*n
        assert opt[0]==sp.Rational(f.numerator,f.denominator)
        exhaustive.append({'N':n,'policies':2**n,'all_starts':True})
    rng=np.random.default_rng(2026110503);hetero=[]
    for n in (4,8,12):
        for trial in range(6):
            rows=[]
            for i in range(n):
                row={}
                for a,b in cert['boxes'].items():
                    row[a]=(b['pL'] if rng.integers(2) else b['pU'],b['qL'] if rng.integers(2) else b['qU'],b['rL'])
                rows.append(row)
            policy=['A']+['B']*(n-1);v=direct_solve(rows,policy)
            gap=check_bellman(rows,policy,v)
            hetero.append({'N':n,'trial':trial,'minimum_exact_alternative_slack':str(gap)})
    family=[];A=cert['boxes']['A'];B=cert['boxes']['B']
    for n in (4,8,16,32,64,128,256):
        opt=F(68,5)*(F(7,2)**n-1)-4*n
        va=60*(F(2)**n-1)-30*n;vb=F(28,5)*(F(7,2)**n-1)-4*n
        lo=value(A['pU'],A['rL'],B['pU'],B['qL'],B['rL'],n)
        hi=value(A['pL'],A['rU'],B['pL'],B['qU'],B['rU'],n);assert lo<=opt<=hi
        family.append({'N':n,'log10_optimal_work':log10(opt),'optimal_work':str(opt),
                       'optimal_over_always_A':float(opt/va),'optimal_over_always_B':float(opt/vb),
                       'log10_certified_value_lower':log10(lo),'log10_certified_value_upper':log10(hi),
                       'certified_value_upper_over_lower':float(hi/lo)})
    survival=[]
    for n in (4,8,12,16):
        P=np.zeros((n,n))
        for i in range(n):
            p,q,r=map(float,nominal['A' if i==0 else 'B']);P[i,i]=1-p-q
            if i:P[i,i-1]=q
            else:P[i,i]+=q
            if i+1<n:P[i,i+1]=p
        R=cert['tail_survival_ratio_lower'];H=(R**n-1)/(R-1)
        for t in (10,100,1000):
            prob=max(0.,min(1.,1-float(np.linalg.matrix_power(P,t)[0].sum())))
            bound=min(1.,float(t*cert['startup_up_upper']/H));assert prob<=bound+1e-10
            survival.append({'N':n,'cycles':t,'guaranteed_work_if_survives':2*t,
                             'floating_source_failure_probability':prob,'exact_certificate_bound_float':bound})
    info=[];eps=F(1,10)
    for n in (32,64,128,256):
        t0=F(69,100);d=4*eps/n;t1=t0+d
        v0=value(F(1,10),F(3),F(1,5),t0,F(2),n);v1=value(F(1,10),F(3),F(1,5),t1,F(2),n)
        sep=math.log(float(v1/v0))
        kl=float(t0)*math.log(float(t0/t1))+float(F(4,5)-t0)*math.log(float((F(4,5)-t0)/(F(4,5)-t1)))
        assert sep>=4*float(eps) and kl<=13*float(d*d)
        info.append({'N':n,'epsilon':str(eps),'theta0':str(t0),'theta1':str(t1),
                     'log_value_separation':sep,'KL_per_tail_cycle':kl,'KL_upper':13*float(d*d)})
    m=data['samples_per_action']
    receipt={'status':'PASS','synthetic_data_only':True,'samples_per_action':m,'total_trials':2*m,
             'total_resets':2*m,'raw_two_bit_category_payload':4*m,
             'joint_Hoeffding_failure_bound':8*math.exp(-2*m*.003**2),
             'exhaustive_policy_checks':exhaustive,'total_policies_compared':sum(x['policies'] for x in exhaustive),
             'heterogeneous_corner_models':hetero,'survival_checks':survival,'prediction_hard_pairs':info,
             'physical_contract_verified':False,'historical_priority_established':False}
    save('growing_family.json',family);save('verification_receipt.json',receipt)
    print(json.dumps({'status':'PASS','total_trials':2*m,'policies_compared':receipt['total_policies_compared'],
                      'heterogeneous_models':len(hetero),'d0_lower':float(cert['d0_lower']),
                      'tail_threshold':float(cert['tail_threshold']),
                      'tail_survival_ratio_lower':float(cert['tail_survival_ratio_lower']),
                      'family':[{k:v for k,v in x.items() if k!='optimal_work'} for x in family]},indent=2))
if __name__=='__main__':main()
