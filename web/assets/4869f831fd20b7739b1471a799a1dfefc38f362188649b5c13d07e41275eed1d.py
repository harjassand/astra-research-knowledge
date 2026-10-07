from paired_phase_estimator import *
from itertools import product,combinations
from pathlib import Path
import json,time,random
start=time.perf_counter();rng=random.Random(52021)

def direct_volume(U,V,k,lam):
    d=len(U[0]);answer=Q(0)
    for chosen in combinations(range(len(U)),k):
        scalar=Q(1)
        for a in chosen:scalar*=lam[a]
        columns=[vec for a in chosen for vec in (U[a],V[a])]
        for rows in combinations(range(d),2*k):
            answer+=scalar*determinant([[vec[i] for vec in columns] for i in rows]).norm()
    return answer

def phase_distribution(var):
    a,b=var.numerator,var.denominator;sa,sb=isqrt(a),isqrt(b)
    if sa*sa==a and sb*sb==b:R=Q(sa,sb)
    else:
        t=isqrt(16*a*b);R=Q(t+int(t*t<16*a*b),4*b)
    p=var/(R*R)
    return [(G(),1-p)]+[(z*R,p/4) for z in [G(1),G(-1),G(0,1),G(0,-1)]]

U=[[G(rng.randrange(-1,2),rng.randrange(-1,2)) for _ in range(4)] for _ in range(3)]
V=[[G(rng.randrange(-1,2),rng.randrange(-1,2)) for _ in range(4)] for _ in range(3)]
lam=[Q(1,2),Q(2,3),Q(4)];weighted=[]
for k,mode in [(1,'direct'),(2,'complement')]:
    expected=direct_volume(U,V,k,lam);mean=Q(0);second=Q(0);states=0;zero_phase_states=0
    distributions=[phase_distribution(w if mode=='direct' else 1/w) for w in lam]
    for drawn in product(*distributions):
        probability=Q(1)
        for _,p in drawn:probability*=p
        if not probability:continue
        z=[a for a,_ in drawn]
        value=evaluate_direct(U,V,k,z,4) if mode=='direct' else evaluate_complement(U,V,k,z,lam,4)
        assert value>=0
        mean+=probability*value;second+=probability*value*value;states+=1
        zero_phase_states+=int(any(not a for a in z))
    degree=k if mode=='direct' else len(U)-k
    assert mean==expected and second<=comb(2*degree,degree)*expected*expected
    weighted.append({'k':k,'mode':mode,'target':str(expected),'mean':str(mean),
                     'second_moment_ratio':str(second/(expected*expected)),
                     'exact_states':states,'states_with_zero_phase':zero_phase_states})

# Complete paired-volume sector with nonsquare activities: complement degree0
# yields the same exact value on every activated-phase sample, including zeros.
for t in range(8):
    value,meta=sample_value(U[:2],V[:2],2,lam[:2],rng.getrandbits)
    assert value==direct_volume(U[:2],V[:2],2,lam[:2]) and meta['effective_degree']==0

def magic(x):
    B=[[G() for _ in range(4)] for _ in range(4)]
    entries={(0,1):x[0]+G(0,1)*x[1],(2,3):x[0]-G(0,1)*x[1],
             (0,2):x[2]+G(0,1)*x[3],(1,3):-x[2]+G(0,1)*x[3],
             (0,3):x[4]+G(0,1)*x[5],(1,2):x[4]-G(0,1)*x[5]}
    for (i,j),v in entries.items():B[i][j]=v;B[j][i]=-v
    return B
forms=[];baseU=[];baseV=[]
for a in range(1,6):
    for sign in (-1,1):
        x=[G(1)]+[G() for _ in range(5)];x[a]=G(0,sign);B=magic(x)
        assert B[0][1]*B[2][3]-B[0][2]*B[1][3]+B[0][3]*B[1][2]==G()
        i,j=next((i,j) for i in range(4) for j in range(i+1,4) if B[i][j])
        u=[B[t][i] for t in range(4)];v=[B[t][j]/B[i][j] for t in range(4)]
        assert all(u[s]*v[t]-v[s]*u[t]==B[s][t] for s in range(4) for t in range(4))
        forms.append((a,sign));baseU.append(u);baseV.append(v)
sharp=[]
for copies in (1,2):
    Uc=baseU*copies;Vc=baseV*copies;labels=forms*copies;m=len(labels);coeff={}
    for i,j in combinations(range(m),2):
        value=determinant([[vec[t] for vec in (Uc[i],Vc[i],Uc[j],Vc[j])] for t in range(4)])
        expected=4 if labels[i][0]==labels[j][0] and labels[i][1]!=labels[j][1] else 2 if labels[i][0]!=labels[j][0] else 0
        assert value==G(expected)
        if value:coeff[(i,j)]=value
    square={}
    for A,a in coeff.items():
        for B,b in coeff.items():
            alpha=tuple(int(i in A)+int(i in B) for i in range(m))
            square[alpha]=square.get(alpha,G())+a*b
    Z=sum((v.norm() for v in coeff.values()),Q(0))
    phase_fourth=sum((v.norm() for v in square.values()),Q(0))
    gaussian_fourth=sum((v.norm()*2**sum(e==2 for e in alpha) for alpha,v in square.items()),Q(0))
    phase_ratio=Q(24,5)-Q(4,5*copies)+Q(1,30*copies*copies)
    assert Z==240*copies*copies and phase_fourth/(Z*Z)==phase_ratio and gaussian_fourth/(Z*Z)==Q(24,5)
    assert phase_ratio>4
    if copies==1:
        for _ in range(4):
            z=[G(1),G(-1),G(0,1),G(0,-1)]
            drawn=[rng.choice(z) for _ in range(m)]
            p=sum((a*drawn[i]*drawn[j] for (i,j),a in coeff.items()),G())
            assert evaluate_direct(Uc,Vc,2,drawn,4)==p.norm()
    sharp.append({'copies':copies,'pair_labels':m,'target':str(Z),'phase_second_moment_ratio':str(phase_ratio),
                  'gaussian_second_moment_ratio':str(gaussian_fourth/(Z*Z)),
                  'two_power_upper_bound_refuted':True})
assert approximate(U,V,0,lam)[0]==1
assert sample_value([[G(1),G()]],[[G(1),G()]],1)[0]==0
full,full_meta=approximate(U[:2],V[:2],2,lam[:2])
assert full==direct_volume(U[:2],V[:2],2,lam[:2]) and full_meta['samples']==0
estimate,estimate_meta=approximate(U,V,2,lam,epsilon=Q(1,2),delta=Q(1,2),randbits=rng.getrandbits)
assert abs(estimate-Q(718,3))<=Q(718,6)
res={'status':'PASS','weighted_exact_enumeration':weighted,'sharp_two_pair_fixtures':sharp,
     'weighted_low_complement_fpras_smoke':{'target':'718/3','estimate':str(estimate),'metadata':estimate_meta,
                                          'scope':'one seeded bounded call; not empirical confidence calibration'},
     'scope':'Exact finite activated-phase moment identities, zero-variable complement projection, polynomial trace coefficient, rational simple-bivector construction and phase/Gaussian moment fibers. Universal bounds proved separately; no frequency-based confidence audit.',
     'elapsed_seconds':time.perf_counter()-start}
Path('work/cycle6/c02_s01/revisions/PAIRED_PHASE_CHECKS.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
