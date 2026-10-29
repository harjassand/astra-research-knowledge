#!/usr/bin/env python3
"""Independent exact review; no producer import, sampling or raw-data re-audit."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json,time
HERE=Path(__file__).resolve().parent
RUN=HERE.parent/'native_excursions'/'macro_run'

def solve(a,b):
    n=len(b);a=[list(map(F,row))+[F(rhs)] for row,rhs in zip(a,b)]
    for col in range(n):
        pivot=next(i for i in range(col,n) if a[i][col]);a[col],a[pivot]=a[pivot],a[col]
        z=a[col][col];a[col]=[x/z for x in a[col]]
        for i in range(n):
            if i!=col:
                z=a[i][col]
                if z:a[i]=[x-z*y for x,y in zip(a[i],a[col])]
    return [r[-1] for r in a]

def row_extreme(i,R,h,Sl,Su,minimum):
    x=R.index(i);ans=F(0)
    for j in range(len(Sl)):
        if j==i:continue
        diff=h[x]-(h[R.index(j)] if j in R else 0)
        lo,hi=-Sl[i][j],-Su[i][j];assert 0<=lo<=hi
        ans+=min(lo*diff,hi*diff) if minimum else max(lo*diff,hi*diff)
    return ans

def corners(c,h,lo,hi):
    values=[]
    for bits in product([0,1],repeat=len(h)):
        b=[hi[i] if bit else lo[i] for i,bit in enumerate(bits)]
        assert min(b)>=0 and sum(b)>0
        values.append((c+sum(x*y for x,y in zip(b,h)))/sum(b))
    return min(values),max(values),len(values)

def original_model():
    # Independent rational reconstruction of the declared private geometry.
    w=list(map(F,['1','5/4','3/4','3/2','1','9/8']))+[F(1,2)]*12
    L=[[F(0) for _ in range(18)] for _ in range(18)]
    def edge(a,b,c):L[a][a]+=c;L[b][b]+=c;L[a][b]-=c;L[b][a]-=c
    for a,b in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]:edge(a,b,F(1,8))
    for p in range(6):
        c=(w[p]-F(1,4))/2;edge(p,6+2*p,c);edge(p,7+2*p,c)
    modules=[]
    for r in range(3):
        interior=list(range(6+4*r,10+4*r));modules.append([2*r,2*r+1]+interior)
        for a,b in zip(interior,interior[1:]+interior[:1]):edge(a,b,F(1,16))
    assert all(sum(row)==0 for row in L)
    return w,L,modules

def mean(C,A,w,L,modules):
    target={i for r in A for i in modules[r]};source=[i for r in C for i in modules[r]]
    live=[i for i in range(len(w)) if i not in target]
    h=solve([[L[i][j] for j in live] for i in live],[w[i] for i in live])
    return sum(w[i]*h[live.index(i)] for i in source)/sum(w[i] for i in source)

def main():
    start=time.perf_counter()
    # Exact bilinear Loewner failure and its correct rectangular remedy.
    h1=solve([[F(2),F(-1)],[F(-1),F(2)]],[F(1),F(2)])
    h2=solve([[F(3),F(-2)],[F(-2),F(3)]],[F(1),F(2)])
    assert h1==[F(4,3),F(5,3)] and h2==[F(7,5),F(8,5)] and h1[0]<h2[0]
    small_l=[F(5,4),F(3,2)];small_u=[F(3,2),F(7,4)]
    for i in range(2):
        j=1-i
        assert small_l[i]+max(small_l[i]-small_l[j],2*(small_l[i]-small_l[j]))==i+1
        assert small_u[i]+min(small_u[i]-small_u[j],2*(small_u[i]-small_u[j]))==i+1
    names=['NATIVE_EXCURSION_CERTIFICATE.json','BETWEEN_REGION_CERTIFICATE.json','POSITIVE_MEAN_REALIZATION.json']
    hashes={n:hashlib.sha256((RUN/n).read_bytes()).hexdigest() for n in names}
    base,release,rep=[json.loads((RUN/n).read_text()) for n in names]
    groups=base['input_contracts']['module_ports'];assert groups==[[0,1],[2,3],[4,5]]
    Sl=[[F(x) for x in r] for r in base['S_lower']];Su=[[F(x) for x in r] for r in base['S_upper']]
    bl=list(map(F,base['b_lower']));bu=list(map(F,base['b_upper']))
    sl=list(map(F,base['stationary_event_lower']));su=list(map(F,base['stationary_event_upper']))
    vl=list(map(F,base['v_lower']));vu=list(map(F,base['v_upper']))
    for M in [Sl,Su]:
        assert all(sum(r)==0 for r in M)
        assert all(M[i][j]==M[j][i] for i in range(6) for j in range(6))
    vectors={};rows=0
    for d in release['vectors']:
        A=d['target_modules'];R=d['live_ports']
        assert R==[i for r,g in enumerate(groups) if r not in A for i in g]
        lower=list(map(F,d['lower']));upper=list(map(F,d['upper']))
        assert all(0<=l<=u for l,u in zip(lower,upper))
        reached={i for r in A for i in groups[r]}
        while True:
            old=len(reached);reached|={i for i in range(6) if any(Sl[i][j]<0 for j in reached)}
            if len(reached)==old:break
        assert len(reached)==6
        lowres=[];upres=[]
        for i in R:
            lowres.append(row_extreme(i,R,lower,Sl,Su,False)-bl[i])
            upres.append(row_extreme(i,R,upper,Sl,Su,True)-bu[i])
            assert lowres[-1]<=0<=upres[-1];rows+=2
        assert lowres==list(map(F,d['lower_check']['extreme_residual']))
        assert upres==list(map(F,d['upper_check']['extreme_residual']))
        vectors[tuple(A)]=(R,lower,upper)
    queries=[];vertices=0;seen=set();maxfactor=F(1)
    for q in release['queries']:
        A=q['target_modules'];C=q['source_modules']
        assert A and C and not(set(A)&set(C));seen.add((tuple(C),tuple(A)))
        R,lower,upper=vectors[tuple(A)];Cp=[i for r in C for i in groups[r]]
        cl=sum(sl[i]*vl[i] for i in Cp)/2;cu=sum(su[i]*vu[i] for i in Cp)/2
        lo,_,n1=corners(cl,[lower[R.index(i)] for i in Cp],[bl[i] for i in Cp],[bu[i] for i in Cp])
        _,hi,n2=corners(cu,[upper[R.index(i)] for i in Cp],[bl[i] for i in Cp],[bu[i] for i in Cp]);vertices+=n1+n2
        if len(A)+len(C)==3:
            prior=next(x for x in base['macro_queries'] if x['target_modules']==A)
            lo=max(lo,F(prior['lower']));hi=min(hi,F(prior['upper']))
        assert lo==F(q['lower']) and hi==F(q['upper']) and hi/lo==F(q['factor'])
        maxfactor=max(maxfactor,hi/lo)
        queries.append({'source_modules':C,'target_modules':A,'lower_display':float(lo),'upper_display':float(hi),'factor_display':float(hi/lo),'lo':lo,'hi':hi})
    assert len(seen)==len(queries)==12 and len(vectors)==6 and maxfactor<F(1557794,1000000)
    assert F(release['failure_probability_upper'])==F(3,5000) and release['new_source_observations']==0
    # Rebuild private original only after deterministic consumer reconstruction.
    w,L,modules=original_model()
    for q in queries:
        true=mean(q['source_modules'],q['target_modules'],w,L,modules)
        assert q['lo']<=true<=q['hi'];q['original_mean']=str(true);q['original_mean_display']=float(true)
    # Independently reconstruct every public realization coefficient and Schur record.
    rw=list(map(F,rep['weights']));Q=[[F(x) for x in r] for r in rep['generator']]
    Cmat=[[F(x) for x in r] for r in rep['conductances']]
    assert len(rw)==12 and len(Q)==12 and min(rw)>0
    rL=[[-rw[i]*Q[i][j] for j in range(12)] for i in range(12)]
    for i in range(12):
        assert sum(Q[i])==0 and rL[i][i]==sum(Cmat[i])
        for j in range(12):
            assert rw[i]*Q[i][j]==rw[j]*Q[j][i]
            assert Cmat[i][j]==Cmat[j][i]>=0
            if i!=j:assert Q[i][j]>=0 and rL[i][j]==-Cmat[i][j]
    pr=rep['point_record'];S=[[F(x) for x in r] for r in pr['S']]
    b=list(map(F,pr['b']));v=list(map(F,pr['v']));cs=list(map(F,pr['c_by_module']))
    ul=list(map(F,base['u_lower']));uu=list(map(F,base['u_upper']))
    assert rw[:6]==[(a+z)/2 for a,z in zip(sl,su)]==list(map(F,pr['w_B']))
    assert rw[6:]==v==[(sl[i]*ul[i]+su[i]*uu[i])/2 for i in range(6)]
    assert b==[rw[i]+v[i] for i in range(6)]
    assert S==[[(Sl[i][j]+Su[i][j])/2 for j in range(6)] for i in range(6)]
    assert cs==[sum(sl[i]*vl[i]+su[i]*vu[i] for i in g)/4 for g in groups]
    # General block elimination, rather than a leaf-only algebra shortcut.
    II=[[rL[i][j] for j in range(6,12)] for i in range(6,12)]
    solved_load=solve(II,rw[6:])
    reconstructed_b=[rw[i]-sum(rL[i][6+k]*solved_load[k] for k in range(6)) for i in range(6)]
    assert reconstructed_b==b
    for j in range(6):
        column=solve(II,[rL[i][j] for i in range(6,12)])
        assert [rL[i][j]-sum(rL[i][6+k]*column[k] for k in range(6)) for i in range(6)]==[S[i][j] for i in range(6)]
    for k,g in enumerate(groups):
        assert sum(rw[6+i]*solved_load[i] for i in g)==cs[k]
        gamma=sum(v[i] for i in g)/cs[k]
        assert gamma==F(rep['module_leaf_exit_rates'][k])
        for i in g:
            assert Q[6+i][i]==gamma and Q[6+i][6+i]==-gamma
            assert all(Q[6+i][j]==0 for j in range(12) if j not in [i,6+i])
    rmodules=[g+[6+i for i in g] for g in groups]
    for q in queries:
        prepared=mean(q['source_modules'],q['target_modules'],rw,rL,rmodules)
        saved=next(x for x in rep['queries'] if x['source_modules']==q['source_modules'] and x['target_modules']==q['target_modules'])
        assert prepared==F(saved['prepared_mean']) and q['lo']<=prepared<=q['hi']
        assert [q['lo'],q['hi']]==list(map(F,saved['original_source_interval']))
        q['prepared_mean_display']=float(prepared);q['prepared_mean_matches_exactly']=True
        del q['lo'];del q['hi']
    assert rep['input_certificate_sha256']==hashes[names[0]]
    assert rep['new_source_observations']==0 and rep['source_model_reads']==0
    vals=rw+[x for r in Q for x in r]
    nbits=max(x.numerator.bit_length() for x in vals);dbits=max(x.denominator.bit_length() for x in vals)
    assert nbits==rep['max_coefficient_numerator_bits'] and dbits==rep['max_coefficient_denominator_bits']
    out={'status':'PASS','inputs_sha256':hashes,'scope':'Independent deterministic reconstruction, exact release rows, exhaustive fractional-box vertices, original full18-state killed means, and public positive12-state generator plus Schur record and means. Prior acquired confidence event accepted at completed review scope; no raw re-audit or universal-realization theorem re-audit.','source_producer_imported':False,'consumer_imported':False,'new_observations':0,'exact_row_inequalities_checked':rows,'fractional_box_vertices_evaluated':vertices,'query_count':12,'target_vector_count':6,'max_factor_strict_upper':'1.557794','max_factor_display':float(maxfactor),'failure_probability_upper':'3/5000','realization_states':12,'realization_record_equality':True,'max_coefficient_numerator_bits':nbits,'max_coefficient_denominator_bits':dbits,'queries':queries,'wall_seconds':time.perf_counter()-start}
    (HERE/'BETWEEN_REGION_RECORD_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','exact_row_inequalities_checked','fractional_box_vertices_evaluated','query_count','max_factor_display','realization_states','wall_seconds']}))

if __name__=='__main__':main()
