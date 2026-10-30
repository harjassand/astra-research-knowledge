"""Exact rational recognizer for a restricted trace/pool certificate class.
No simulation, rate fitting, or claim of completeness for arbitrary CRNs.
"""
from fractions import Fraction as F
from itertools import product
from collections import deque
import json
import sympy as sp

def vec(d,species): return tuple(d.get(s,0) for s in species)
def partitions(xs):
    if not xs: yield []; return
    x,*tail=xs
    for pp in partitions(tail):
        yield [(x,)]+pp
        for i in range(len(pp)):
            yield pp[:i]+[tuple(sorted((x,)+pp[i]))]+pp[i+1:]
def positive(v): return any(v)
def enabled(y,x): return all(a>=b for a,b in zip(x,y))
def fall(x,k):
    z=1
    for j in range(k): z*=x-j
    return z

def coeffs(expr,variables):
    expr=sp.expand(expr)
    if not variables: return {():F(expr)} if expr else {}
    return {mon:F(co) for mon,co in sp.Poly(expr,*variables).terms() if co}
def domination(num,den,variables):
    p,q=coeffs(num,variables),coeffs(den,variables)
    if any(v<0 for v in p.values()) or any(v<0 for v in q.values()): return None
    if any(q.get(mon,0)<=0 for mon in p): return None
    return max([F(0)]+[co/q[mon] for mon,co in p.items()])

def full_network(coupled=True):
    S=['A','C','E','D','B']; a0=2;q=5;m=4
    out=[]
    def add(y,z,k=1,name=''):
        out.append(dict(name=name,source=y,target=z,rate=str(k)))
    add({},dict(A=1,B=1),name='immigration')
    add(dict(A=1,B=1),dict(A=m,B=q),name='activation')
    add(dict(A=m,B=q),{},name='clearing')
    def fast(y,z,name):
        for t in (y,z): t['A']=t.get('A',0)+a0;t['B']=q
        add(y,z,name=name)
    fast(dict(A=1,D=1),dict(C=1,D=1),'A_to_C')
    fast(dict(C=1,D=1),dict(E=1,D=1),'C_to_E')
    fast(dict(E=1,D=1),dict(A=1,D=1),'E_to_A')
    fast(dict(A=1,D=1),dict(A=2),'A_birth')
    fast(dict(D=2),dict(A=1,D=1),'D_reverse')
    fast(dict(A=2),dict(A=1,D=1),'seed1')
    fast(dict(A=2),dict(D=2),'seed2')
    if coupled:
        fast(dict(C=1,D=1),dict(C=1,E=1),'mixed_forward')
        fast(dict(C=1,E=1),dict(C=1,D=1),'mixed_reverse')
    return dict(species=S,reactions=out)

def weakly_reversible(rs):
    V={r['y'] for r in rs}|{r['z'] for r in rs}
    adj={v:set() for v in V}
    for r in rs: adj[r['y']].add(r['z'])
    for r in rs:
        seen={r['z']};todo=[r['z']]
        while todo:
            for w in adj[todo.pop()]:
                if w not in seen: seen.add(w);todo.append(w)
        if r['y'] not in seen:return False
    return True

def boundary_checks(rs,seeds,rest,A,D,k0,kseed):
    """Cells 0,1,2,3,4+z fix source/output enablement under shifts <=2."""
    k=len(rs[0]['y']); others=[i for i in range(k) if i!=D]
    worst={}; true_bound=F(0); checked=0; failure=[]
    for r in rs:
        nu=tuple(z-y for y,z in zip(r['y'],r['z']))
        if nu[D]>=0: continue
        d=-nu[D]
        if d not in (1,2): return None,'D jump outside binary boundary'
        cmax=F(0);r_true=F(0)
        for cell in product(range(5),repeat=k-1):
            lower=[0]*k;lower[D]=d
            for i,v in zip(others,cell):lower[i]=v
            if not enabled(r['y'],lower):continue
            outlo=[v+w for v,w in zip(lower,nu)]
            if min(outlo)<0:continue
            active_rest=[h for h in rest if enabled(h['y'],outlo)]
            variables=[];x=list(lower)
            for i,v in zip(others,cell):
                if v==4:
                    z=sp.Symbol('z'+str(i),nonnegative=True);variables.append(z);x[i]=4+z
            out=[v+w for v,w in zip(x,nu)]
            num=r['k']
            for v,j in zip(x,r['y']):num*=fall(v,j)
            if not active_rest:
                if outlo[A]<2:
                    return None,dict(reason='true-face output is not active',reaction=r['name'],cell=lower)
                bound=domination(num,1+x[A],variables)
                if bound is None:
                    return None,dict(reason='true-face ingress not bounded by 1+a',reaction=r['name'],cell=lower)
                r_true=max(r_true,bound)
            else:
                den=(k0+kseed)*fall(out[A],2)
                for h in active_rest:
                    term=h['k']
                    for v,j in zip(out,h['y']):term*=fall(v,j)
                    den+=term
                bound=domination(num,den,variables)
                if bound is None:
                    return None,dict(reason='mixed holding domination certificate fails',reaction=r['name'],cell=lower)
                cmax=max(cmax,bound)
            checked+=1
        true_bound+=r_true
        if cmax:worst[r['name']]=str(cmax)
    return dict(boundary_cells_checked=checked,trace_constants=worst,
                trace_total=str(sum(map(F,worst.values()),F(0))),
                true_face_ingress_constant=str(true_bound)),None

def mixed_growth_check(rs,rest,A,D,k0,kseed):
    k=len(rs[0]['y']);others=[i for i in range(k) if i!=D];worst=F(0);checked=0
    for cell in product(range(5),repeat=k-1):
        lower=[0]*k
        for i,v in zip(others,cell):lower[i]=v
        active=[r for r in rest if enabled(r['y'],lower)]
        if not active:continue
        variables=[];x=list(lower)
        for i,v in zip(others,cell):
            if v==4:
                z=sp.Symbol('z'+str(i),nonnegative=True);variables.append(z);x[i]=4+z
        den=(k0+kseed)*fall(x[A],2)
        for r in active:
            term=r['k']
            for v,j in zip(x,r['y']):term*=fall(v,j)
            den+=term
        bound=domination(1+sum(x),den,variables)
        if bound is None:return None,dict(reason='initial mixed face has no linear population clock certificate',cell=lower)
        worst=max(worst,bound);checked+=1
    return dict(cells_checked=checked,population_over_hazard_constant=str(worst)),None

def pooled_check(rs,seeds,rest,A,D,pp):
    k=len(rs[0]['y']); p=len(pp); loc={i:j for j,b in enumerate(pp) for i in b}; ar=loc[A];dr=loc[D]
    def change(r):return tuple(sum(r['z'][i]-r['y'][i] for i in b) for b in pp)
    if any(any(change(r)) for r in rest):return None,'restoring edge not pool-neutral'
    agg={}
    for r in rs:
        if r in seeds:continue
        delta=change(r)
        if not any(delta):continue
        neg=[i for i,v in enumerate(delta) if v==-1];pos=[i for i,v in enumerate(delta) if v==1]
        if len(neg)!=1 or len(pos)!=1 or sum(abs(v) for v in delta)!=2:return None,'nonunit pooled move'
        if not r['y'][D]:return None,'nonsilent D-free move'
        co=[F(0)]*(k+1)
        if r['y'][D]==2:co[D]=r['k'];co[-1]=-r['k']
        elif r['y'][D]==1:
            other=[i for i,v in enumerate(r['y']) if i!=D and v]
            if len(other)!=1:return None,'bad binary source'
            co[other[0]]=r['k']
        else:return None,'bad D degree'
        key=(neg[0],pos[0]);old=agg.setdefault(key,[F(0)]*(k+1))
        for i in range(k+1):old[i]+=co[i]
    edges=[]; extras=[]
    for (i,j),co in agg.items():
        if j!=ar:
            val=co[pp[i][0]]
            target=[val if h in pp[i] else F(0) for h in range(k)]+[-val if i==dr else F(0)]
            if co!=target or val<=0:return None,'non-A-target excess cannot be certified'
        else:
            # substitute D=1+u_D. All residual coefficients must be nonnegative.
            if min(co[:-1])<0 or co[-1]+co[D]<0:return None,'negative baseline remainder'
            val=min(co[h] for h in pp[i])
            extras.append(dict(source_pool=i,affine_rate=list(map(str,co)),baseline=str(val)))
        if val>0:edges.append((i,j,val))
    rev={i:[] for i in range(p)}
    for i,j,q in edges:rev[j].append(i)
    dist={ar:0};queue=deque([ar])
    while queue:
        j=queue.popleft()
        for i in rev[j]:
            if i not in dist:dist[i]=dist[j]+1;queue.append(i)
    if len(dist)!=p:return None,'some pooled type has no baseline path to A'
    return dict(pools=[list(b) for b in pp],protected_pool=dr,
                baseline_edges=[dict(source=i,target=j,rate=str(q)) for i,j,q in edges],
                extras_to_A=extras,distances=dist,L=max(1,max(dist.values()))),None

def acquire(raw):
    S=raw['species'];rr=[]
    if len(set(S))!=len(S):return dict(status='INVALID_INPUT',reason='duplicate species')
    ids=[r['name'] for r in raw['reactions']]
    if len(ids)!=len(set(ids)):return dict(status='INVALID_INPUT',reason='reaction IDs must be unique')
    for r in raw['reactions']:
        if F(r['rate'])<0:return dict(status='INVALID_INPUT',reason='negative rate')
        for y in (r['source'],r['target']):
            if any(i not in S or not isinstance(v,int) or v<0 for i,v in y.items()):
                return dict(status='INVALID_INPUT',reason='invalid complex')
    for r in raw['reactions']:
        if F(r['rate'])<=0:continue
        rr.append(dict(name=r['name'],y=vec(r['source'],S),z=vec(r['target'],S),k=F(r['rate'])))
    zero=(0,)*len(S);attempts=[]
    for imm in rr:
        if imm['y']!=zero or sum(imm['z'])!=2:continue
        pair=[i for i,v in enumerate(imm['z']) if v==1]
        if len(pair)!=2:continue
        for A0,B0 in (pair,pair[::-1]):
            for act in rr:
                if act['y']!=imm['z']:continue
                m,q=act['z'][A0],act['z'][B0]
                if m<4 or q<=m or sum(act['z'])!=m+q:continue
                clears=[r for r in rr if r['y']==act['z'] and r['z']==zero]
                if not clears:continue
                clear=clears[0];a0=m-2;off=[0]*len(S);off[A0]=a0;off[B0]=q
                inds=[i for i in range(len(S)) if i!=B0];names=[S[i] for i in inds];A=inds.index(A0)
                fast=[];ok=True
                for r in rr:
                    if r in (imm,act,clear):continue
                    y=[r['y'][i]-off[i] for i in range(len(S))];z=[r['z'][i]-off[i] for i in range(len(S))]
                    if min(y+z)<0 or y[B0] or z[B0] or sum(y)!=2 or sum(z)!=2:ok=False;break
                    fast.append(dict(name=r['name'],y=tuple(y[i] for i in inds),z=tuple(z[i] for i in inds),k=r['k']))
                if not ok:continue
                seeds=[r for r in fast if r['y'][A]==2]
                if not seeds:continue
                for D in range(len(inds)):
                    if D==A or any(r['z'][D]<1 for r in seeds):continue
                    ab=[0]*len(inds);ab[A]=1;ab[D]=1;aa=[0]*len(inds);aa[A]=2
                    if not any(r['y']==tuple(ab) and r['z']==tuple(aa) for r in fast):continue
                    rest=[r for r in fast if r not in seeds and r['y'][D]==0]
                    if any(r['z'][D]<1 or r['y'][A] or r['z'][A] for r in rest):
                        attempts.append('D-free face is not one-hold A-neutral restoring');continue
                    bc,err=boundary_checks(fast,seeds,rest,A,D,clear['k'],sum(r['k'] for r in seeds))
                    if err:attempts.append(err);continue
                    growth,err=mixed_growth_check(fast,rest,A,D,clear['k'],sum(r['k'] for r in seeds))
                    # Growth failure remains diagnostic; carried launch has no reset claim.
                    growth_diagnostic=err
                    candidates=sorted(partitions([i for i in range(len(inds)) if i!=A]),key=lambda p:-len(p))
                    for pp0 in candidates:
                        pp=[(A,)]+pp0
                        pool,err=pooled_check(fast,seeds,rest,A,D,pp)
                        if err:continue
                        if not weakly_reversible(rr):attempts.append('global reaction graph is not weakly reversible');continue
                        pool['pool_species']=[[names[i] for i in b] for b in pool['pools']]
                        L=pool['L']
                        return dict(status='CARRIED_FACE_CANDIDATE_FOUND',connector=dict(A=S[A0],B=S[B0],a0=a0,m=m,q=q),
                            pivot=names[D],residual_species=names,
                            true_face=dict(D_equals=0,disabled_sources=[{names[i]:v for i,v in enumerate(r['y']) if v} for r in rest]),
                            trace_certificate=bc,initial_mixed_clock=growth,initial_mixed_clock_failure=growth_diagnostic,
                            launch_mode='D=0 at connector starts; mixed holds internal during positive-D trace',
                            reset_scope='positive-D-start traced row ONLY',pool_certificate=pool,
                            exponents=dict(return_probability=str(F(1,2*L+1)),weighted_return=str(F(1,4*L+2)),
                                           reset_fm=str(F(m,L*m+2*L+1))),
                            scope='UNREVIEWED carried-face candidate; reset exponents apply only to positive-D starts; launch row has bounded non-small Green.')
    return dict(status='NO_CERTIFICATE_IN_THIS_CLASS',attempts=attempts)

if __name__=='__main__':
    good=full_network(True);old=full_network(False)
    bad=json.loads(json.dumps(good))
    # No restoration: exact old non-small face becomes genuinely dormant.
    bad['reactions']=[r for r in bad['reactions'] if r['name']!='mixed_reverse']
    hidden=json.loads(json.dumps(good));hidden['species'].insert(-1,'X')
    hidden['reactions'] += [
        dict(name='A_to_X',source=dict(A=3,D=1,B=5),target=dict(A=2,X=1,D=1,B=5),rate='1'),
        dict(name='X_to_A',source=dict(A=2,X=1,D=1,B=5),target=dict(A=3,D=1,B=5),rate='1')]
    results={name:acquire(net) for name,net in [('coupled_raw',good),('original_cycle_raw',old),('missing_reverse_rejected',bad),('hidden_clock_carried_candidate',hidden)]}
    print(json.dumps(results,indent=2));open(__file__.replace('.py','_results.json'),'w').write(json.dumps(results,indent=2)+'\n')
    open(__file__.replace('acquire_carried.py','raw_inputs.json'),'w').write(json.dumps(dict(coupled=good,original=old,missing_reverse=bad,hidden_clock=hidden),indent=2)+'\n')
