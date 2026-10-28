"""Exact rational enclosure of actual fixed-time CTMC active probabilities.

Normalized finite uniformization sums are stochastic rational kernels;
a positive-series tail certifies distance from exp(tQ). No floating
exponential or experimental data are trusted.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time,math
START=time.monotonic()
from model import make_family,tilt,mm,mv,controlled_word,labels,x,u,v
OUT=Path(__file__).resolve().parent
a=F(1);b=F(33,100);c=F(1,3);gamma=F(11,200);d=F(5,2)
Q=make_family(a,b,c,gamma);S=make_family(a,b,c,F(0))
N=6;I=[[F(i==j) for j in range(N)] for i in range(N)]
def trans(A):return list(map(list,zip(*A)))
def inverse(A):
    T=[list(r)+I[i] for i,r in enumerate(A)]
    for k in range(N):
        p=next(j for j in range(k,N) if T[j][k]);T[k],T[p]=T[p],T[k]
        den=T[k][k];T[k]=[z/den for z in T[k]]
        for j in range(N):
            if j!=k:
                f=T[j][k];T[j]=[z-f*w for z,w in zip(T[j],T[k])]
    return [r[N:] for r in T]
H=[[F(1),F(x[i]),F(u[i]),F(v[i]),F(0),F(0)] if i<4 else [F(0)]*4+[F(i==4),F(i==5)] for i in range(N)]
HI=inverse(H)
# Exact baseline invariant subspace and equality with the ordinary control.
for j in [0,1,4,5]:
    col=[r[j] for r in H];assert mv(Q,col)==mv(S,col)
L=mm(mm(HI,Q),H)
assert all(L[i][j]==0 for i in [2,3] for j in [0,1,4,5])

queries={};kernels={};times={};tails={}
def normalized_uniformization(A,t,degree=48):
    rate=F(6);P=[[F(i==j)+A[i][j]/rate for j in range(N)] for i in range(N)]
    assert min(z for row in P for z in row)>=0 and all(sum(r)==1 for r in P)
    z=rate*t;power=I;coef=F(1);E=F(1);total=[r[:] for r in I]
    for k in range(1,degree+1):
        power=mm(power,P);coef=coef*z/k;E+=coef
        total=[[old+coef*w for old,w in zip(r,p)] for r,p in zip(total,power)]
    nextcoef=coef*z/(degree+1)
    assert z<degree+2
    U=nextcoef/(1-z/(degree+2))
    result=[[w/E for w in row] for row in total]
    assert all(sum(row)==1 for row in result)
    return result,U/(E+U)

for name,A in [('target',Q),('ordinary',S)]:
    start=time.monotonic()
    for field in [F(1),d]:
        Af,pi=tilt(A,field)
        assert all(sum(pi[i]*Af[i][j] for i in range(N))==0 for j in range(N))
        # Full static bilinear symmetrizer, generally indefinite.
        rho=20*(3*b*(field-1)+20*(gamma if name=='target' else 0))/(3*b*(field-1)-20*(gamma if name=='target' else 0)) if (name=='target' or field!=1) else F(20)
        M=[F(4),F(20),F(4),rho,field*field,F(1)]
        Lf=mm(mm(HI,Af),H)
        assert all(M[i]*Lf[i][j]==M[j]*Lf[j][i] for i in range(N) for j in range(N))
        # Full multichannel Kubo identity at the generator level.
        for letter in range(3):
            g=[F(y==letter) for y in labels]
            B=[[Af[i][j]*(g[j]-g[i])/2 if i!=j else F(0) for j in range(N)] for i in range(N)]
            for i in range(N):B[i][i]=-sum(B[i])
            assert [sum(pi[i]*B[i][j] for i in range(N)) for j in range(N)]==[-sum(pi[i]*g[i]*Af[i][j] for i in range(N)) for j in range(N)]
        for duration in ([F(1,4),F(1,2)] if field==d else [F(1,4)]):
            key=f'{name}:{field}:{duration}';P,err=normalized_uniformization(Af,duration)
            kernels[key]=P;tails[key]=err
            queries[key]={'field':str(field),'duration':str(duration),'row_TV_error_bound':str(err),
                          'kernel':[[str(z) for z in r] for r in P]}
    times[name]=time.monotonic()-start

fields=[F(1),d,F(1),d,F(1)];durations=[F(1,4)]*3+[F(1,2),F(1,4)]
word=[1,0,0,0,0,2];pi=[F(1,6)]*6;outcomes={}
for name in ['target','ordinary']:
    keys=[f'{name}:{field}:{duration}' for field,duration in zip(fields,durations)]
    matrices=[kernels[k] for k in keys];error=sum(tails[k] for k in keys)
    forward=controlled_word(matrices,pi,word)
    reverse=controlled_word(matrices[::-1],pi,word[::-1]);diff=forward-reverse
    if name=='ordinary':assert diff==0
    lower,upper=diff-2*error,diff+2*error
    if name=='target':
        assert -F(700390315,10**16)<lower<upper<-F(700390314,10**16)
    outcomes[name]={'forward_approximation':str(forward),'reverse_approximation':str(reverse),
                    'individual_probability_error_bound':str(error),'difference_interval':[str(lower),str(upper)],
                    'display_forward':float(forward),'display_reverse':float(reverse),'display_difference':float(diff)}

delta=F(7,10**8)
# A conservative relaxation bound from symmetric generator S alone.
minimum_symmetric_rate=min(S[i][j] for i in range(6) for j in range(6) if i!=j and S[i][j]>0)
assert minimum_symmetric_rate==F(1,100)
# Missing marker-to-marker edge costs at most twice a two-edge route;
# the symmetric spectral gap is at least 2m=1/50.
burnin=1250
assert sum(F(5)**j/math.factorial(j) for j in range(7))>100
prep_error_bound=F(3,2*10**10) # (sqrt5/2)e^(-25) <1.5e-10
assert prep_error_bound<delta/16
per_arm=math.ceil(160/delta**2)

result={'status':'EXACT_FIXED_TIME_CTMC_ACTIVE_SEPARATION','parameters':dict(zip(['a','b','c','gamma','d'],map(str,[a,b,c,gamma,d]))),
        'fields':list(map(str,fields)),'durations':list(map(str,durations)),'word':word,
        'continuous_time':True,'degree':48,'uniformization_rate':'6','kernel_queries':queries,
        'outcomes':outcomes,'Q':[[str(z) for z in row] for row in Q],'S':[[str(z) for z in row] for row in S],
        'cost':{'preparation_model_time_units':burnin,'preparation_TV_bound':str(prep_error_bound),
                'signal_abs_floor':str(delta),'hypothetical_Hoeffding_cycles_per_arm':per_arm,
                'protocol_time_units':'3/2','scope':'Conservative sufficient upper acquisition budget, not a sample lower bound or physical experiment.'},
        'phases_seconds':times,'module_seconds':time.monotonic()-START,
        'scope':'Exact model probability enclosure. Equilibrium inference requires qualified common-reversal energy-control and stationary preparation contracts. No physical calibration, samples or device acquired.'}
(OUT/'CONTINUOUS_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','cost','phases_seconds','module_seconds']},indent=2))
print('target difference',outcomes['target']['display_difference'])
