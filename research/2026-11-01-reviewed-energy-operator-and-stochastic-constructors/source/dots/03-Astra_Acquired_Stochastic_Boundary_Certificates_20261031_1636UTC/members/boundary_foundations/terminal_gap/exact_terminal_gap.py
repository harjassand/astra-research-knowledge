#!/usr/bin/env python3
"""Exact finite cone acquisition and infinite-fiber Lyapunov checks; no simulations."""
from fractions import Fraction as F
from itertools import combinations
import json, math, hashlib

def rref(a):
    a=[[F(x) for x in row] for row in a]
    if not a: return a,[]
    n=len(a); m=len(a[0]); piv=[]; r=0
    for c in range(m):
        p=next((i for i in range(r,n) if a[i][c]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]; z=a[r][c]; a[r]=[x/z for x in a[r]]
        for i in range(n):
            if i!=r and a[i][c]:
                z=a[i][c]; a[i]=[x-z*y for x,y in zip(a[i],a[r])]
        piv.append(c); r+=1
        if r==n: break
    return a,piv

def nonnegative_solve(cols,b):
    """Complete finite basis enumeration for Bx=b, x>=0, exact rational arithmetic."""
    d=len(b); q=len(cols)
    if not any(b): return [F(0)]*q,0
    if not cols: return None,0
    _,rows=rref(cols) # rows of B become columns of B^T
    rank=len(rows)
    if not rank: return None,0
    checked=0
    for inds in combinations(range(q),rank):
        aug=[[cols[j][i] for j in inds]+[b[i]] for i in rows]
        rr,piv=rref(aug); checked+=1
        if piv[:rank]!=list(range(rank)): continue
        x=[row[-1] for row in rr]
        if any(v<0 for v in x): continue
        if any(sum(x[k]*cols[j][i] for k,j in enumerate(inds))!=b[i] for i in range(d)): continue
        ans=[F(0)]*q
        for j,v in zip(inds,x): ans[j]=v
        return ans,checked
    return None,checked

def linkage_classes(reactions):
    reactions=[(tuple(s),tuple(t)) for s,t in reactions if tuple(s)!=tuple(t)]
    C=sorted({p for e in reactions for p in e})
    adj={c:[] for c in C}; rev={c:[] for c in C}
    for s,t in reactions: adj[s].append(t);rev[t].append(s)
    seen=set();order=[]
    def dfs(x):
        seen.add(x)
        for y in adj[x]:
            if y not in seen:dfs(y)
        order.append(x)
    for c in C:
        if c not in seen:dfs(c)
    seen=set();Ls=[]
    def collect(x,out):
        seen.add(x);out.append(x)
        for y in rev[x]:
            if y not in seen:collect(y,out)
    for c in reversed(order):
        if c not in seen:
            out=[];collect(c,out);Ls.append(sorted(out))
    owner={c:j for j,L in enumerate(Ls) for c in L}
    wr=all(owner[s]==owner[t] for s,t in reactions)
    return C,Ls,wr

def compile_cones(reactions):
    reactions=[(tuple(s),tuple(t)) for s,t in reactions if tuple(s)!=tuple(t)]
    digest=hashlib.sha256(json.dumps(reactions,separators=(',',':')).encode()).hexdigest()
    C,Ls,wr=linkage_classes(reactions)
    if not C:return {'accepted':True,'trivial_no_genuine_channels':True,'input_sha256':digest}
    d=len(C[0])
    if not wr:return {'accepted':False,'reason':'not weakly reversible'}
    jumps=[tuple(t[i]-s[i] for i in range(d)) for s,t in reactions]
    trials=0; records=[];accepted=True
    for bits in range(1,2**d):
        I=[i for i in range(d) if bits>>i&1]; O=[i for i in range(d) if i not in I]
        rhs=[int(i in I) for i in range(d)]
        cols=jumps+[tuple(-v for v in x) for x in jumps]+[tuple(-int(i==j) for i in range(d)) for j in I]
        feasible,n=nonnegative_solve(cols,rhs);trials+=n
        if feasible is None:
            # Alternative: conservation ell annihilates all jumps and is
            # nonnegative, nonzero on I; outside I its signs are unrestricted.
            coords=[(i,1) for i in range(d)]+[(i,-1) for i in O]
            ellcols=[tuple(sign*nu[i] for nu in jumps)+(int(i in I)*sign,) for i,sign in coords]
            ellsol,checks=nonnegative_solve(ellcols,[0]*len(jumps)+[1]);trials+=checks
            assert ellsol is not None
            ell=[sum(sign*a for (i,sign),a in zip(coords,ellsol) if i==j) for j in range(d)]
            records.append({'I':I,'admissible':False,'excluding_invariant':list(map(str,ell))});continue
        for k,L in enumerate(Ls):
            pairs=[(s,c) for c in L for s in C if all(s[i]<=c[i] for i in O)]
            ds=[tuple(s[i]-c[i] for i in I) for s,c in pairs]
            cols=ds+[tuple(-int(i==j) for i in range(len(I))) for j in range(len(I))]
            sol,n=nonnegative_solve(cols,[1]*len(I));trials+=n
            rec={'I':I,'linkage':k,'admissible':True,'accepted':sol is not None}
            if sol is not None:
                cert=[{'source':s,'terminal':c,'weight':str(a)} for (s,c),a in zip(pairs,sol) if a]
                g=[sum(sol[j]*ds[j][i] for j in range(len(ds))) for i in range(len(I))]
                assert all(x>=1 for x in g)
                rec.update(certificate=cert,exact_gain=list(map(str,g)))
            else:
                accepted=False
                # Acquire normalized separating w>=0: D w + z=0, sum w=1.
                wc=[tuple(row[i] for row in ds)+(1,) for i in range(len(I))]
                wc += [tuple(int(i==j) for i in range(len(ds)))+(0,) for j in range(len(ds))]
                dual,m=nonnegative_solve(wc,[0]*len(ds)+[1]);trials+=m
                assert dual is not None
                rec['obstructing_weight']=list(map(str,dual[:len(I)]))
            records.append(rec)
    return {'accepted':accepted,'input_sha256':digest,'linkages':Ls,'exact_basis_candidates_tested':trials,'records':records}

def verify_certificate(reactions,receipt):
    """Independent verifier: no LP/finder call; checks all finite certificate rows."""
    reactions=[(tuple(s),tuple(t)) for s,t in reactions if tuple(s)!=tuple(t)]
    digest=hashlib.sha256(json.dumps(reactions,separators=(',',':')).encode()).hexdigest()
    if receipt.get('input_sha256')!=digest:return False
    C,Ls,wr=linkage_classes(reactions)
    if not wr:return False
    if not C:return receipt.get('accepted') and receipt.get('trivial_no_genuine_channels')
    if not receipt.get('accepted'):return False
    d=len(C[0]); jumps=[tuple(t[i]-s[i] for i in range(d)) for s,t in reactions]
    rows=receipt['records']
    for bits in range(1,2**d):
        I=[i for i in range(d) if bits>>i&1];O=[i for i in range(d) if i not in I]
        rr=[r for r in rows if r['I']==I]
        if len(rr)==1 and not rr[0]['admissible']:
            ell=list(map(F,rr[0]['excluding_invariant']))
            if len(ell)!=d or any(sum(e*v for e,v in zip(ell,nu)) for nu in jumps):return False
            if any(ell[i]<0 for i in I) or sum(ell[i] for i in I)<=0:return False
            continue
        if len(rr)!=len(Ls) or sorted(r['linkage'] for r in rr)!=list(range(len(Ls))):return False
        for r in rr:
            if not r['admissible'] or not r['accepted']:return False
            L=Ls[r['linkage']];gain=[F(0)]*d
            for term in r['certificate']:
                s=tuple(term['source']);c=tuple(term['terminal']);a=F(term['weight'])
                if s not in C or c not in L or a<0 or any(s[i]>c[i] for i in O):return False
                gain=[g+a*(x-y) for g,x,y in zip(gain,s,c)]
            if any(gain[i]<1 for i in I):return False
    return True

def cycle(C):return list(zip(C,C[1:]+C[:1]))
def h(a):return sum((F(1,k) for k in range(1,a)),F(0)) if a>=1 else F(0)
def V(a,b):return F(a+b)-h(a)/2+(F(a+b,4) if a==0 else 0)
def generator(a,b):
    out=V(a+1,b)-V(a,b)
    if a:out+=a*(V(a-1,b)-V(a,b))
    if a>=2:out+=a*(a-1)*(V(a-1,b+1)-V(a,b))
    if a and b:out+=a*b*(V(a+1,b-1)-V(a,b))
    return out

def main():
    obstruction=[((0,0),(1,0)),((1,0),(0,0)),((2,0),(1,1)),((1,1),(2,0))]
    three=cycle([(0,0,0),(1,1,0),(1,0,1),(0,1,1)])+cycle([(1,0,0),(0,1,0),(0,0,1),(2,0,0)])
    bad=compile_cones(obstruction);good=compile_cones(three)
    assert not bad['accepted'] and good['accepted'] and verify_certificate(three,good)
    finite=compile_cones([((1,0),(0,1)),((0,1),(1,0))])
    assert verify_certificate([((1,0),(0,1)),((0,1),(1,0))],finite)
    cubic=compile_cones([((0,),(3,)),((3,),(0,))])
    assert verify_certificate([((0,),(3,)),((3,),(0,))],cubic)
    tampered=json.loads(json.dumps(good))
    for r in tampered['records']:
        for c in r.get('certificate',[]):c['weight']='0'
    assert not verify_certificate(three,tampered)
    ratios=[]
    for n in range(1,129):
        a=n+2;b=n
        first=[F(a*(a-1)),F(a-1),F(1),F(a-1,b)]
        a=n+1
        second=[F(a*a),F(a),F(a,a-1),F(1)]
        assert all(x>=1 for x in first+second) and any(x>1 for x in first) and any(x>1 for x in second)
        ratios.append([list(map(str,first)),list(map(str,second))])
    for a in range(65):
        for b in range(65):
            n=a+b; lv=generator(a,b)
            expected=1-F(n,4) if a==0 else (-F(n+1,4) if a==1 else 1-F(n,2)-F(1,2*a)+F(a,2*(a-1)))
            assert lv==expected and lv<=2-F(n,4) and V(a,b)>=F(n,2)
    print(json.dumps({'three_species_cone_certificate':good,'stable_network_rejected_by_cones':bad,'finite_class_certificate':finite,'cubic_certificate':cubic,'tamper_rejected':True,'exact_target_ratio_checks':len(ratios)*8,'harmonic_generator_exact_grid_states':65**2,'grid_is_consistency_check_not_general_proof':True},indent=2))
if __name__=='__main__':main()
