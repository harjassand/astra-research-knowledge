"""Experimental exact joint stationary sampler for noisy UT_d(F_q) word networks.

A group state is an upper-unitriangular dxd matrix, stored as a tuple of
entries above the diagonal ordered by the 'channels' function.
Each site-time independently uses a full Haar reset (rate s>0), residual
specified reset (rate r), or a bounded-length group word in earlier sites.
Local input oracle returns parents and coefficients on demand.

All random code uses PRNG for tests; theorem exactness is ideal random bits.
Expected oracle cost is polynomial in output size, max gate word length,
1/s for FIXED d, independent of network size with random-access inputs.

No historical novelty, external proof verification, or physical significance
is claimed by this research implementation.
"""
from __future__ import annotations
from dataclasses import dataclass
import random
from collections import defaultdict
from heisenberg_quotient_sampler import add_term, const_poly, plus, neg, product, exact_rank_basis_add, span_contains, vec_add_inplace, Oracle


def channels(d):
    return tuple((i,i+level) for level in range(1,d) for i in range(d-level))


def layer(ch):return ch[1]-ch[0]


def group_id(d):return tuple(0 for _ in channels(d))


def group_values_to_dict(x,d):return dict(zip(channels(d),x))


def ut_mul(x,y,d,q):
    a=group_values_to_dict(x,d)
    b=group_values_to_dict(y,d)
    return tuple((a[i,j]+b[i,j]+sum(a[i,k]*b[k,j] for k in range(i+1,j)))%q for i,j in channels(d))


def ut_inv(x,d,q):
    y=group_id(d)
    a=x
    # (I+A)^{-1}=I-A+A^2-... : alternatively group-power via nilpotence
    xinv=tuple((-v)%q for v in x)
    # below triangular recursive calculation: inverse M_{ij}=-M_{ij}-sum M_{ik} inv_{kj}
    av=group_values_to_dict(x,d)
    result={}
    for i,j in channels(d):
        result[i,j]=(-av[i,j]-sum(av[i,k]*result[k,j] for k in range(i+1,j)))%q
    return tuple(result[ch] for ch in channels(d))


def ut_power(x,n,d,q):
    if n<0: x=ut_inv(x,d,q); n=-n
    acc=group_id(d)
    while n:
        if n&1:acc=ut_mul(acc,x,d,q)
        n//=2
        if n:x=ut_mul(x,x,d,q)
    return acc


def ut_word_eval(values,factors,d,q):
    acc=group_id(d)
    for F in factors:
        g=F[1] if F[0]=='c' else ut_power(values[F[1]],F[2],d,q)
        acc=ut_mul(acc,g,d,q)
    return acc


def expr_identity(d):return {ch:{} for ch in channels(d)}


def expr_constant(g,d,q):return {ch:const_poly(g[j],q) for j,ch in enumerate(channels(d))}


def expr_variable(z,d):return {ch:{((z[0],z[1],ch[0],ch[1]),):1} for ch in channels(d)}


def poly_product_any(P,Q,q):
    out={}
    for a,u in P.items():
        for b,v in Q.items():
            mon=tuple(sorted(a+b))
            add_term(out,mon,u*v,q)
    return out


def expr_product(X,Y,d,q):
    return { (i,j):plus(plus(X[i,j],Y[i,j],q),
                        sum_poly([poly_product_any(X[i,k],Y[k,j],q) for k in range(i+1,j)],q),q)
            for i,j in channels(d)}


def sum_poly(ps,q):
    acc={}
    for P in ps: acc=plus(acc,P,q)
    return acc


def expr_inverse(X,d,q):
    result={}
    for i,j in channels(d):
        terms=[neg(X[i,j],q)]
        for k in range(i+1,j):
            terms.append(neg(poly_product_any(X[i,k],result[k,j],q),q))
        result[i,j]=sum_poly(terms,q)
    return result


def expr_power(X,e,d,q):
    if e<0:X=expr_inverse(X,d,q); e=-e
    acc=expr_identity(d)
    while e:
        if e&1:acc=expr_product(acc,X,d,q)
        e//=2
        if e:X=expr_product(X,X,d,q)
    return acc


def expr_gate(model,z):
    d,q=model.d,model.q
    acc=expr_identity(d)
    for F in model.factors(z[0]):
        if F[0]=='c':t=expr_constant(F[1],d,q)
        else:t=expr_power(expr_variable((F[1],z[1]-1),d),F[2],d,q)
        acc=expr_product(acc,t,d,q)
    return acc


def poly_eval(P,values,q):
    out=0
    for mon,coef in P.items():
        t=coef
        for v in mon:t=(t*values[v])%q
        out=(out+t)%q
    return out


@dataclass
class UTModel:
    n:int
    d:int
    q:int
    s:float
    r:float
    gates:object
    residual:object
    def factors(self,i):return self.gates(i) if callable(self.gates) else self.gates[i]
    def reset_value(self,i):return self.residual(i) if callable(self.residual) else self.residual


def layer_gate_data(model,z,level):
    """For every level-l channel: (lower-level polynomial offset, same-channel parent counts).

    The critical triangle property is checked dynamically; this is not
    permitted to silently introduce a nonlinear dependency on level-l states.
    """
    q=model.q
    G=expr_gate(model,z)
    result={}
    for ch in channels(model.d):
        if layer(ch)!=level:continue
        lower={}
        parents={}
        for mon,coef in G[ch].items():
            same=[v for v in mon if (v[3]-v[2])>=level]
            if same:
                if len(mon)!=1 or (mon[0][2],mon[0][3])!=ch or mon[0][3]-mon[0][2]!=level:
                    raise AssertionError('Violates strictly triangular gate condition')
                parent=mon[0][:2]
                parents[parent]=(parents.get(parent,0)+coef)%q
            else:
                # In particular, this includes constants and arbitrary polynomial lower-layer sources.
                add_term(lower,mon,coef,q)
        result[ch]=(lower,{a:b for a,b in parents.items() if b})
    return result


def resolve_layer(model,targets,oracle,level):
    """Conditional representation of requested level-l raw coordinates:
    result = lower_poly_values + Haar(basis), uniformly on the basis span.
    Events are memoized; no sampled Haar coordinate values are revealed.
    """
    q=model.q
    m=len(targets)
    D=[{} for _ in range(m)]
    frontier={}
    for j,(z,ch) in enumerate(targets):
        if z not in frontier:frontier[z]={}
        if ch not in frontier[z]:frontier[z][ch]=[0]*m
        frontier[z][ch][j]=(frontier[z][ch][j]+1)%q
    basis={}
    calls=0
    while frontier:
        z=max(frontier,key=lambda x:(x[1],x[0]))
        cmat=frontier.pop(z)
        cmat={ch:v for ch,v in cmat.items() if any(v) and not span_contains(basis,v,q)}
        if not cmat:continue
        calls+=1
        (kind,value),_=oracle.event(z)
        if kind=='haar':
            for v in cmat.values(): exact_rank_basis_add(basis,v,q)
        elif kind=='residual':
            g=dict(zip(channels(model.d),value))
            for ch,v in cmat.items():
                constv=g[ch]
                if constv:
                    for i,a in enumerate(v):add_term(D[i],(),a*constv,q)
        else:
            gd=layer_gate_data(model,z,level)
            oracle.parent_queries+=sum(abs(F[2]) for F in model.factors(z[0]) if F[0]=='v')
            for ch,v in cmat.items():
                lower,parents=gd[ch]
                for i,a in enumerate(v):
                    if not a:continue
                    for mon,b in lower.items():add_term(D[i],mon,a*b,q)
                for p,co in parents.items():
                    if p not in frontier:frontier[p]={}
                    if ch not in frontier[p]:frontier[p][ch]=[0]*m
                    vec_add_inplace(frontier[p][ch],v,co,q)
            # Remove zero parents to bound memory.
            for p in list(frontier):
                frontier[p]={ch:v for ch,v in frontier[p].items() if any(v)}
                if not frontier[p]: frontier.pop(p)
    assert len(basis)<=m
    required=sorted({v for P in D for mon in P for v in mon})
    assert all(layer((v[2],v[3]))<level for v in required)
    return D,basis,required,calls


def sample_coordinates(model,queries,rng=None,diagnostics=False):
    """Joint exact stationary draw of arbitrary matrix coordinates at arbitrary times.

    queries = [(site,time,i,j), ...] with 0<=i<j<d.
    Site-time past is well-defined using independent stochastic update symbols.
    At level 0 there are no variables. Deliberately shares one oracle across levels.
    """
    rng=rng or random.Random()
    oracle=Oracle(model,rng)
    detail=[]
    q=model.q
    def solve(level,requests):
        if not requests:return []
        if level<=0:raise AssertionError('Unresolved coordinate at level zero')
        top=[(j,(key[0],key[1]),(key[2],key[3])) for j,key in enumerate(requests) if key[3]-key[2]==level]
        rest=[(j,key) for j,key in enumerate(requests) if key[3]-key[2]<level]
        if not top:
            return solve(level-1,requests)
        top_requests=[(z,ch) for _,z,ch in top]
        lower,basis,needed,calls=resolve_layer(model,top_requests,oracle,level)
        lower_requests=[key for _,key in rest]
        for x in needed:
            if x not in lower_requests:lower_requests.append(x)
        values=solve(level-1,lower_requests)
        lower_env=dict(zip(lower_requests,values))
        masked=[poly_eval(P,lower_env,q) for P in lower]
        for basis_vec in basis.values():
            coef=rng.randrange(q)
            for i in range(len(masked)):
                masked[i]=(masked[i]+coef*basis_vec[i])%q
        out=[None]*len(requests)
        for (idx,_,_),v in zip(top,masked):out[idx]=v
        for idx,key in rest:out[idx]=lower_env[key]
        detail.append({'layer':level,'requested':len(top),'rank':len(basis),'needed_lower':len(needed),'event_visits':calls})
        return out
    result=solve(model.d-1,list(queries))
    if diagnostics:return result,{'fresh':oracle.fresh,'parent_queries':oracle.parent_queries,'layers':detail}
    return result


def sample_group_states(model,site_time_keys,rng=None,diagnostics=False):
    site_time_keys=list(site_time_keys)
    cs=channels(model.d)
    requests=[(z[0],z[1],ch[0],ch[1]) for z in site_time_keys for ch in cs]
    vals,stats=sample_coordinates(model,requests,rng,True)
    D={z:tuple(vals[i*len(cs):(i+1)*len(cs)]) for i,z in enumerate(site_time_keys)}
    return (D,stats) if diagnostics else D


def sample_word(model,factors,rng=None,diagnostics=False):
    keys=sorted({(F[1],0) for F in factors if F[0]=='v'})
    states,stats=sample_group_states(model,keys,rng,True)
    vals={z[0]:x for z,x in states.items()}
    value=ut_word_eval(vals,factors,model.d,model.q)
    return (value,stats) if diagnostics else value

if __name__=='__main__':
    d,q=3,3
    # state tuple order is (0,1),(1,2),(0,2); noncommutative commutator.
    # The coordinates correspond to the prior H_3 group (a,b,c) in different order.
    residual=tuple(dict([((0,1),1),((1,2),0),((0,2),1)]).get(ch,0) for ch in channels(d))
    m=UTModel(n=2,d=3,q=3,s=.16,r=.12,residual=residual,gates={
      0:[('v',0,1),('v',1,1),('v',0,-1),('v',1,-1)],
      1:[('v',1,1),('v',0,1),('v',1,1)]})
    rng=random.Random(4)
    for i in range(3):
        states,st=sample_group_states(m,[(0,0),(1,0)],rng,True)
        print(i,states,st)
