#!/usr/bin/env python3
"""Ideal atomic SSF stress diagnostic; Python standard library only."""
import argparse,collections,itertools,json,math,random,time
from pathlib import Path

def syndrome(e, checks):
    return sum(((e & c).bit_count()&1)<<i for i,c in enumerate(checks))
def basis(rows):
    b={}
    for v in rows:
        while v:
            p=v.bit_length()-1
            if p in b:v^=b[p]
            else:b[p]=v;break
    return b
def reduce(v,b):
    for p in sorted(b,reverse=True):
        if v>>p&1:v^=b[p]
    return v

def make_code(L):
    # H is binary cycle incidence: row i has columns i and i+1 mod L.
    H=[[int(j in (i,(i+1)%L)) for j in range(L)] for i in range(L)]
    # HX=[H tensor I_n | I_m tensor H^T], HZ=[I_n tensor H | H^T tensor I_m].
    HX=[];HZ=[];N=2*L*L
    for a in range(L):
        for b in range(L):
            HX.append(sum(H[a][j]<<(j*L+b) for j in range(L)) | sum(H[j][b]<<(L*L+a*L+j) for j in range(L)))
            HZ.append(sum(H[b][j]<<(a*L+j) for j in range(L)) | sum(H[j][a]<<(L*L+j*L+b) for j in range(L)))
    assert all((x&z).bit_count()%2==0 for x in HX for z in HZ)
    sectors=[]
    for checks,stabs in [(HZ,HX),(HX,HZ)]:
        cols=[syndrome(1<<q,checks) for q in range(N)]
        # BFS of syndrome graph gives exact minimum Hamming-weight representative.
        reps={0:0};dist={0:0};queue=collections.deque([0])
        while queue:
            s=queue.popleft()
            for q,c in enumerate(cols):
                t=s^c
                if t not in reps:
                    reps[t]=reps[s]^(1<<q);dist[t]=dist[s]+1;queue.append(t)
        assert len(reps)==1<<len(basis(checks))
        assert all(syndrome(e,checks)==s and e.bit_count()==dist[s] for s,e in reps.items())
        families=[]
        for g in stabs:
            support=[q for q in range(N) if g>>q&1];family=[]
            for bits in range(1,1<<len(support)):
                f=sum(1<<q for j,q in enumerate(support) if bits>>j&1)
                sf=syndrome(f,checks)
                # FGL eq (5): |sigma(F)| >= d_A |F|/2, d_A=2.
                if sf and sf.bit_count()>=f.bit_count():family.append((f,sf,sf.bit_count()))
            assert len(family)==len(set(f for f,_,_ in family))
            families.append(family)
        sectors.append(dict(checks=checks,stabs=stabs,cols=cols,reps=reps,dist=dist,basis=basis(stabs),families=families))
    assert N-len(basis(HX))-len(basis(HZ))==2
    code=dict(L=L,N=N,H=H,HX=HX,HZ=HZ,sectors=sectors)
    return code

def choose(s,family):
    # beta=1/2, maximize decrease, then minimize support, then numeric mask.
    best=None;key=None
    for f,sf,w in family:
        decrease=2*(s&sf).bit_count()-w
        if 2*decrease>=w:
            k=(decrease,-f.bit_count(),-f)
            if key is None or k>key:key=k;best=(f,sf,decrease)
    return best

def decoded_failure(errors,syndromes,code):
    return any(reduce(e^sec['reps'][s],sec['basis']) for e,s,sec in zip(errors,syndromes,code['sectors']))

def selftest(code):
    N=code['N'];rng=random.Random(912+N);checks=0
    for sec in code['sectors']:
        # Every syndrome and candidate: direct vs incremental syndrome and descent.
        for s in sec['reps']:
            e=sec['reps'][s]
            for family in sec['families']:
                for f,sf,w in family:
                    assert syndrome(e^f,sec['checks'])==s^sf;checks+=1
                move=choose(s,family)
                if move:assert s.bit_count()-(s^move[1]).bit_count()==move[2]>0
        # Exact logical classification: all stabilizers trivial; sampled kernel elements checked.
        b=list(sec['basis'].values())
        for subset in range(1<<len(b)):
            stab=0
            for j,v in enumerate(b):
                if subset>>j&1:stab^=v
            assert syndrome(stab,sec['checks'])==0 and reduce(stab,sec['basis'])==0
        for _ in range(1000):
            e=rng.getrandbits(N);s=syndrome(e,sec['checks']);r=sec['reps'][s]
            assert syndrome(e^r,sec['checks'])==0
            assert sec['dist'][s]<=e.bit_count()
        # Exact code distance by increasing weight, stopping at first nontrivial kernel member.
        distance=None
        for w in range(1,code['L']+1):
            for qs in itertools.combinations(range(N),w):
                e=sum(1<<q for q in qs)
                if not syndrome(e,sec['checks']) and reduce(e,sec['basis']):distance=w;break
            if distance:break
        assert distance==code['L']
    return dict(candidate_update_assertions=checks,distance_X=code['L'],distance_Z=code['L'],rank_X=len(basis(code['HX'])),rank_Z=len(basis(code['HZ'])),k=2,syndromes_per_sector=[len(s['reps']) for s in code['sectors']],candidates_per_hub=[len(f) for f in code['sectors'][0]['families']])

def trial(code,epsilon,seed,horizons):
    N=code['N'];hubs=2*code['L']**2;max_t=max(horizons)
    # Aggregate thinning equals independent Poisson rate-1 clocks per sector hub;
    # the same ticks and noises are replayed to RR, ensuring exact prefix budgets.
    clock=random.Random(seed);noise=random.Random(seed^0x4e4f495345);labels=random.Random(seed^0x485542)
    ev=[];t=0
    while True:
        t+=clock.expovariate(hubs)
        if t>max_t:break
        ev.append((t,1,labels.randrange(hubs)))
    t=0
    while True:
        t+=noise.expovariate(N*epsilon)
        if t>max_t:break
        ev.append((t,0,(noise.randrange(N),noise.randrange(3)))) # 0=X,1=Z,2=Y
    ev.sort();out={}
    for mode in ('async','round_robin'):
        e=[0,0];s=[0,0];attempts=accepted=faults=0;charged=0;first=None;records=[];hi=0
        def snapshot(t):
            return dict(t=t,failure=bool(decoded_failure(e,s,code)),syndrome_weight=sum(v.bit_count() for v in s),physical_pauli_weight=(e[0]|e[1]).bit_count(),minimum_sector_weight=sum(sec['dist'][v] for v,sec in zip(s,code['sectors'])),attempts=attempts,accepted=accepted,fault_events=faults,first_decoded_failure=first)
        for t,kind,payload in ev:
            while hi<len(horizons) and horizons[hi]<t:records.append(snapshot(horizons[hi]));hi+=1
            if kind==0:
                q,p=payload;faults+=1
                for sector in ([0] if p==0 else [1] if p==1 else [0,1]):
                    e[sector]^=1<<q;s[sector]^=code['sectors'][sector]['cols'][q];charged+=2
            else:
                h=payload if mode=='async' else attempts%hubs
                attempts+=1;sector,g=divmod(h,code['L']**2);sec=code['sectors'][sector]
                move=choose(s[sector],sec['families'][g])
                if move:
                    f,sf,d=move;e[sector]^=f;s[sector]^=sf;accepted+=1
                    assert syndrome(e[sector],sec['checks'])==s[sector]
            assert accepted<=charged # finite-work bound from total noise syndrome increments
            if first is None and decoded_failure(e,s,code):first=t
        while hi<len(horizons):records.append(snapshot(horizons[hi]));hi+=1
        out[mode]=records
    assert all(a['attempts']==b['attempts'] and a['fault_events']==b['fault_events'] for a,b in zip(out['async'],out['round_robin']))
    return out

def wilson(f,n):
    z=1.959963984540054;p=f/n;d=1+z*z/n
    m=(p+z*z/(2*n))/d;r=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [m-r,m+r]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=200);ap.add_argument('--out',default=str(Path(__file__).parent));a=ap.parse_args()
    start=time.time();result=dict(seed_base=2026102900,trials=a.trials,beta=0.5,hub_rate=1,noise='independent rate epsilon depolarizing Poisson per data qubit; X,Z,Y equally likely',horizons=[1,10,50,100],rates=[0.002,0.02],codes=[],summary=[],raw=[])
    for L in (3,4):
        code=make_code(L);validation=selftest(code);result['codes'].append(dict(L=L,N=code['N'],H=code['H'],HX=code['HX'],HZ=code['HZ'],validation=validation));print('validated',L,validation,flush=True)
        for epsilon in result['rates']:
            records=[]
            for i in range(a.trials):
                seed=result['seed_base']+100000*L+int(epsilon*1000000)*1000+i
                rec=trial(code,epsilon,seed,result['horizons']);records.append(rec);result['raw'].append(dict(L=L,epsilon=epsilon,seed=seed,records=rec))
            for mode in ('async','round_robin'):
                for j,t in enumerate(result['horizons']):
                    rows=[r[mode][j] for r in records];f=sum(r['failure'] for r in rows)
                    row=dict(L=L,N=code['N'],epsilon=epsilon,mode=mode,t=t,failures=f,n=a.trials,failure_rate=f/a.trials,wilson95=wilson(f,a.trials),ever_failed=sum(r['first_decoded_failure'] is not None for r in rows))
                    for key in ('syndrome_weight','physical_pauli_weight','minimum_sector_weight','attempts','accepted','fault_events'):row['mean_'+key]=sum(r[key] for r in rows)/a.trials
                    result['summary'].append(row)
            print('done',L,epsilon,flush=True)
    result['runtime_seconds']=time.time()-start
    Path(a.out).mkdir(parents=True,exist_ok=True);Path(a.out,'results.json').write_text(json.dumps(result,indent=2))
    print('runtime',result['runtime_seconds'])
if __name__=='__main__':main()
