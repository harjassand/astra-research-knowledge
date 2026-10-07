from low_rank_parity import *
import random,time,json,pathlib
rng=random.Random(19027);start=time.perf_counter();cases=[]
for n,r in [(5,2),(6,2),(7,3)]:
    U=[[G(rng.randrange(-1,2),rng.randrange(-1,2)) for _ in range(r)] for _ in range(n)]
    V=[[G(rng.randrange(-1,2),rng.randrange(-1,2)) for _ in range(r)] for _ in range(n)]
    F=[[sum((U[i][a]*V[j][a] for a in range(r)),G()) for j in range(n)] for i in range(n)]
    acquired=factorize(F);coeff,_=count_uv(*acquired);_,law=enumerate_count(F)
    fixtures=[]
    for k,w in enumerate(coeff):
        if w:
            word,stats=sample_uv_cached(*acquired,k,randbits=rng.getrandbits)
            assert word in law and word.count('R')==word.count('C')==k
            fixtures.append({'k':k,'word':word,'stats':stats})
    # Two-site conditioning uses the acquired dual suffix law, with every exact
    # branch mass and its partition sum asserted in sample_uv_cached.
    allowed=[set('ERC') for _ in range(n)];allowed[0]={'R'};allowed[2]={'E','C'}
    constrained,_=enumerate_count(F,allowed)
    if sum(constrained):
        word,stats=sample_uv_cached(*acquired,allowed=allowed,randbits=rng.getrandbits)
        assert word[0]=='R' and word[2] in 'EC' and word in law
        fixtures.append({'k':'grandconditional','word':word,'stats':stats})
    cases.append({'n':n,'rank_bound':r,'fixtures':fixtures})
F0=[[G(int(i!=j)) for j in range(4)] for i in range(4)]
word,meta=sample(F0,1,randbits=rng.getrandbits);assert meta['rank_used']==1 and word.count('R')==word.count('C')==1
zeroF=[[G() for _ in range(3)] for _ in range(3)]
word,meta0=sample(zeroF,0,randbits=rng.getrandbits);assert word=='EEE' and meta0['rank_used']==0
res={'status':'PASS','scope':'exact total and branch partition identities in cached dual sampler; small support/sector checks do not empirically certify distribution','seed':19027,'cases':cases,'matrix_wrapper_F0':meta,'zero_rank':meta0,'elapsed_seconds':time.perf_counter()-start}
pathlib.Path('work/cycle6/c02_s01/cached_sampler_checks.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'status':res['status'],'sample_fixture_count':sum(len(c['fixtures']) for c in cases),'elapsed_seconds':res['elapsed_seconds']},indent=2))
