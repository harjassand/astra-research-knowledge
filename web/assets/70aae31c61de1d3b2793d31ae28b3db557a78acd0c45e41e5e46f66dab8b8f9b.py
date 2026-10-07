from low_rank_parity import *
import random,time,json,pathlib
start=time.perf_counter();rng=random.Random(2706);cases=[]
for n,r in [(3,1),(5,1),(5,2),(6,2),(7,3)]:
    U=[[G(rng.randrange(-2,3),rng.randrange(-1,2)) for _ in range(r)] for i in range(n)]
    V=[[G(rng.randrange(-2,3),rng.randrange(-1,2)) for _ in range(r)] for i in range(n)]
    F=[[sum((U[i][a]*V[j][a] for a in range(r)),G()) for j in range(n)] for i in range(n)]
    rw=[Q(i+2,i+1) for i in range(n)];cw=[Q(i+3,i+2) for i in range(n)]
    ans,meta=count(F,row_weights=rw,col_weights=cw,try_dense_completion=False)
    brute,law=enumerate_count(F,row_weights=rw,col_weights=cw)
    padded=ans+[Q(0)]*(len(brute)-len(ans));assert padded==brute
    # Arbitrary one-site and multi-site conditioning obtains the true coefficients.
    checks=0
    for i in range(n):
        for t in 'ERC':
            allowed=[set('ERC') for _ in range(n)];allowed[i]={t}
            got,_=count(F,allowed,rw,cw,False);exp,_=enumerate_count(F,allowed,rw,cw)
            assert got+[Q(0)]*(len(exp)-len(got))==exp;checks+=1
    acquired=factorize(F)
    # Every sampled word has correct sector/support. Distribution equality is proved
    # by exact branch sums, not claimed from these sample frequencies.
    samples=[]
    for k,w in enumerate(ans):
        if w:
            word=sample_uv(*acquired,k,row_weights=rw,col_weights=cw,randbits=rng.getrandbits)
            assert word in law and word.count('R')==k and word.count('C')==k
            samples.append({'k':k,'word':word})
    cases.append({'n':n,'input_rank_bound':r,'meta':meta,'coefficients':[str(x) for x in ans],'prefix_checks':checks,'samples':samples})
# F0: off-diagonal rank-one completion is actually acquired; diagonal terms irrelevant.
F0=[[G(int(i!=j)) for j in range(4)] for i in range(4)]
ans,meta=count(F0);assert ans==[Q(1),Q(12)] and meta['rank_used']==1
brute,_=enumerate_count(F0);assert brute==[Q(1),Q(12),Q(0)]
# Exact tiny positive canonical sector under rank-two dense non-bipartite perturbation.
d=Q(1,2**24);Fdelta=[[G(int(i!=j)) for j in range(4)] for i in range(4)];Fdelta[0][1]+=d
# Explicit diagonal completion Fdelta+I=J+delta E12 has rank<=2.
Gdelta=[[Fdelta[i][j]+G(int(i==j)) for j in range(4)] for i in range(4)]
ans,meta=count(Gdelta,try_dense_completion=False);assert ans[2]==2*d*d
word=sample_uv(*factorize(Gdelta),2,randbits=rng.getrandbits)
assert word.count('R')==2 and word.count('C')==2
result={'status':'PASS','scope':'exact counting/prefix identities and sampler support; universal DP and sampling law proved separately','random_seed':2706,'cases':cases,'F0':{'coefficients':[str(x) for x in count(F0)[0]],'meta':count(F0)[1]},'tiny_sector':{'delta':str(d),'canonical_k2':str(ans[2]),'meta':meta,'sample':word},'elapsed_seconds':time.perf_counter()-start}
pathlib.Path('work/cycle6/c02_s01/low_rank_parity_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'case_count':len(cases),'prefix_checks':sum(x['prefix_checks'] for x in cases),'F0':result['F0'],'tiny_sector':result['tiny_sector'],'elapsed_seconds':result['elapsed_seconds']},indent=2))
