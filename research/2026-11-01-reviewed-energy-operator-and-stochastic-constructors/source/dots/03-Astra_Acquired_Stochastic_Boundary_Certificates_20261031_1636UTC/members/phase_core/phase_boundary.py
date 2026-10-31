"""Acquired finite inactive-head / rational-tail certificates.
Trusted exact-rational research input. No stationary fiber or decomposition oracle.
"""
from fractions import Fraction as F
from itertools import combinations
from math import prod,ceil,comb
import json,hashlib

def weak_reversible(edges):
    vertices={x for edge in edges for x in edge}
    reach={x:{x} for x in vertices}
    for u,v in edges:reach[u].add(v)
    for k in vertices:
        for i in vertices:
            if k in reach[i]:reach[i]|=reach[k]
    return all(u in reach[v] for u,v in edges)

def compositions(n,d):
    if d==1:
        yield (n,);return
    for i in range(n+1):
        for rest in compositions(n-i,d-1):yield (i,)+rest

def solve(A,b):
    n=len(b);M=[[F(z) for z in row]+[F(rhs)] for row,rhs in zip(A,b)]
    for j in range(n):
        k=next(i for i in range(j,n) if M[i][j])
        M[j],M[k]=M[k],M[j];d=M[j][j];M[j]=[x/d for x in M[j]]
        for i in range(n):
            if i!=j and M[i][j]:
                d=M[i][j];M[i]=[x-d*y for x,y in zip(M[i],M[j])]
    x=[row[-1] for row in M]
    assert all(sum(F(a)*v for a,v in zip(row,x))==F(rhs) for row,rhs in zip(A,b))
    return x

def recognize(species,reactions):
    n=len(species);rs=[]
    for u,v,k in reactions:
        assert len(u)==len(v)==n and all(type(x)==int and x>=0 for x in (*u,*v))
        assert isinstance(k,(int,F)) and F(k)>0
        if tuple(u)!=tuple(v):rs.append((tuple(u),tuple(v),F(k)))
    if not weak_reversible([(u,v) for u,v,k in rs]):return {'accepted':False,'reason':'full graph not weakly reversible'}
    trials=[]
    for m in range(1,n):
      for S in combinations(range(n),m):
        T=tuple(i for i in range(n) if i not in S);core=[];neutral=[];bad=[]
        alpha={(h,j):F(0) for h in S for j in T};beta=alpha.copy()
        for z,(u,v,k) in enumerate(rs):
            if all(u[j]==v[j]==0 for j in T) and sum(u)<=1 and sum(v)<=1:
                core.append((tuple(u[i] for i in S),tuple(v[i] for i in S),k));continue
            caught=False
            for h in S:
              aa=tuple(2*int(i==h) for i in range(n))
              for j in T:
                az=tuple(int(i==h)+int(i==j) for i in range(n))
                if u==aa and v==az:alpha[h,j]+=k;caught=True;break
                if u==az and v==aa:beta[h,j]+=k;caught=True;break
              if caught:break
            if caught:continue
            if all(u[i]==v[i] for i in S) and sum(u)==sum(v):neutral.append(z)
            else:bad.append(z)
        H=tuple(h for h in S if any(alpha[h,j] or beta[h,j] for j in T))
        if bad or not H or any(not(alpha[h,j]>0 and beta[h,j]>0) for h in H for j in T):
            trials.append({'service':S,'reason':'shape or complete positive hub rows'});continue
        zero=(0,)*m;units=[tuple(int(i==j) for i in range(m)) for j in range(m)]
        vertices={zero,*units};edges=[(u,v) for u,v,k in core]
        # Strong connectivity of the entire monomolecular core, including zero.
        reach={u:{u} for u in vertices}
        for u,v in edges:reach[u].add(v)
        for h in vertices:
            for i in vertices:
                if h in reach[i]:reach[i]|=reach[h]
        if any(reach[u]!=vertices for u in vertices):
            trials.append({'service':S,'reason':'core not strongly connected through zero'});continue
        death=[sum(k for u,v,k in core if u==units[i] and v==zero) for i in range(m)]
        Hl=tuple(S.index(h) for h in H);Il=tuple(i for i in range(m) if i not in Hl)
        if any(death[i]<=0 for i in Hl) or any(death[i] for i in Il):
            trials.append({'service':S,'reason':'deaths must occur at and at every active hub'});continue
        immigration=[sum(k for u,v,k in core if u==zero and v==units[i]) for i in range(m)]
        conv=[[sum(k for u,v,k in core if u==units[i] and v==units[j]) if i!=j else F(0) for j in range(m)] for i in range(m)]
        return {'accepted':True,'species':species,'service':S,'satellites':T,'hubs':Hl,'inactive':Il,
          'core':core,'immigration':immigration,'death':death,'conversion':conv,
          'alpha':[[alpha[S[h],j] for j in T] for h in range(m)],
          'beta':[[beta[S[h],j] for j in T] for h in range(m)],
          'neutral_indices':neutral,'reactions':rs,'recognition_trials':len(trials)+1}
    return {'accepted':False,'reason':'no acquired compatible service/hub partition','trials':trials}

def g(r,c):
    assert r>=1
    return prod((F(k)/(F(k)+c) for k in range(1,r)),start=F(1))

def core_jumps(rec,y):
    for u,v,k in rec['core']:
        if all(y[i]>=u[i] for i in range(len(y))):
            rate=k*prod(y[i] for i in range(len(y)) if u[i])
            yield tuple(y[i]-u[i]+v[i] for i in range(len(y))),rate

def construct(rec,T=F(2),max_head_states=2000):
    assert rec['accepted'] and isinstance(T,(int,F)) and T>1;T=F(T)
    m=len(rec['service']);H=rec['hubs'];I=rec['inactive'];k=rec['conversion'];d=rec['death'];lam=rec['immigration']
    # Acquire single-particle first-hit times on the inactive phase graph.
    t=[F(0)]*m
    if I:
        A=[[((sum(k[i])+d[i]) if i==j else -k[i][j]) for j in I] for i in I]
        ts=solve(A,[F(1)]*len(I))
        for i,z in zip(I,ts):t[i]=z
        assert all(t[i]>0 for i in I)
    L=max((F(1)+sum(k[h][i]*t[i] for i in I))/d[h] for h in H)
    v=[L+t[i] for i in range(m)];eta=(T-1)/L;q=[1+eta*z for z in v]
    Qv=[sum(k[i][j]*(v[j]-v[i]) for j in range(m))-d[i]*v[i] for i in range(m)]
    assert all(z<=-1 for z in Qv) and all(q[h]==T for h in H)
    delta=min(eta/qi for qi in q);alpha=max(sum(rec['alpha'][h]) for h in H)
    c=min(F(1),delta/(4*alpha));D=max(d[i]/q[i] for i in range(m));B=sum(lam[i]*(q[i]-1) for i in range(m))
    tail_epsilon=delta/4;margin=delta-c*alpha
    R=max(2,ceil((B+2*c*D+tail_epsilon)/margin))
    count=comb(R+len(I)-1,len(I)) if I else 1
    if count>max_head_states:
        return {'accepted':False,'reason':'explicit finite-head work budget exceeded','required_head_states':count,'budget':max_head_states,'R':R}
    head=[]
    if I:
      for r in range(R):
        for yi in compositions(r,len(I)):
            y=[0]*m
            for i,z in zip(I,yi):y[i]=z
            head.append(tuple(y))
    else:head=[(0,)*m]
    assert len(head)==count
    index={y:i for i,y in enumerate(head)}
    def base(y):return prod((q[i]**y[i] for i in range(m)),start=F(1))*g(sum(y),c)
    n=len(head);A=[[F(0)]*n for _ in range(n)];rhs=[F(1)]*n;exits=[]
    for i,y in enumerate(head):
        for yp,rate in core_jumps(rec,y):
            A[i][i]+=rate
            if yp in index:A[i][index[yp]]-=rate
            else:
                val=base(yp);rhs[i]+=rate*val;exits.append((y,yp,rate,val))
    u=solve(A,rhs);assert all(z>0 for z in u)
    weights=dict(zip(head,u));epsilon=min(tail_epsilon,min(1/z for z in u))
    def h(y):return weights[y] if y in weights else base(y)
    rows=[];C=F(0)
    for r in range(1,R+1):
      for y in compositions(r,m):
        if not any(y[h] for h in H):continue
        hy=h(y);core=sum(rate*(h(yp)-hy) for yp,rate in core_jumps(rec,y))/hy
        forward=sum(sum(rec['alpha'][j])*y[j]*(y[j]-1) for j in H)*c/(r-1) if r>=2 else F(0)
        constant=core+forward
        slopes=[c/(r+c)*sum(rec['beta'][j][z]*y[j] for j in H) for z in range(len(rec['satellites']))]
        slope=min(slopes);assert slope>0
        Z=max(-1,ceil((constant+epsilon)/slope))
        if Z>=0:C=max(C,hy*T**Z*max(F(0),constant+epsilon))
        rows.append({'service_state':y,'constant_quotient':constant,'satellite_slopes':slopes,'satellite_head_bound':Z})
    return {'accepted':True,'T':T,'q':q,'hitting_times':t,'common_level_L':L,'v':v,'Qv':Qv,
      'eta':eta,'delta':delta,'alpha_max':alpha,'death_weight_max':D,'immigration_bound':B,
      'c':c,'R':R,'tail_margin':margin,'tail_epsilon':tail_epsilon,
      'head_states':head,'head_matrix':A,'head_rhs':rhs,'head_weights':u,'head_exits':exits,
      'epsilon':epsilon,'foster_C':C,'active_layer_rows':rows,
      'work':{'recognition_trials':rec['recognition_trials'],'single_particle_linear_system':len(I),
              'finite_head_linear_system':n,'active_layer_states':len(rows),
              'largest_head_fraction_bits':max(max(z.numerator.bit_length(),z.denominator.bit_length()) for z in u)}}

def value(rec,cert,x):
    y=tuple(x[i] for i in rec['service']);z=sum(x[i] for i in rec['satellites'])
    idx={tuple(y):u for y,u in zip(cert['head_states'],cert['head_weights'])}
    h=idx[y] if y in idx else prod((cert['q'][i]**y[i] for i in range(len(y))),start=F(1))*g(sum(y),cert['c'])
    return cert['T']**z*h

def generator(rec,cert,x):
    V=value(rec,cert,x);out=F(0)
    for u,v,k in rec['reactions']:
        if any(xx<yy for xx,yy in zip(x,u)):continue
        rate=k*prod(prod(range(xx-yy+1,xx+1)) for xx,yy in zip(x,u))
        xp=tuple(xx-yy+zz for xx,yy,zz in zip(x,u,v))
        out+=rate*(value(rec,cert,xp)-V)
    return V,out

def demo_network():
    sp=['A','E','B','D','C'];zero=(0,)*5
    def unit(i,n=1):return tuple(n*int(j==i) for j in range(5))
    R=[(zero,unit(0),F(1,10)),(unit(0),unit(1),1),(unit(1),unit(0),1),
       (unit(1),unit(2),2),(unit(1),unit(3),2),(unit(2),zero,1),(unit(3),zero,1)]
    for hub,alpha in [(2,1),(3,2)]:
        pair=tuple(int(j==hub)+int(j==4) for j in range(5))
        R.extend([(unit(hub,2),pair,alpha),(pair,unit(hub,2),1)])
    return sp,R

def encode(o):
    if isinstance(o,F):return str(o)
    raise TypeError(type(o))

def main():
    sp,R=demo_network();rec=recognize(sp,R);assert rec['accepted']
    assert rec['service']==(0,1,2,3) and rec['hubs']==(2,3) and rec['inactive']==(0,1)
    cert=construct(rec);assert cert['accepted']
    # Verify every head equation exactly: killed generator gives Lh=-1.
    assert all(sum(a*u for a,u in zip(row,cert['head_weights']))==rhs for row,rhs in zip(cert['head_matrix'],cert['head_rhs']))
    checks=0
    for r in range(cert['R']+5):
      for y in compositions(r,4):
        for z in [0,1,2,10,100,1000]:
            x=tuple(y)+(z,);V,LV=generator(rec,cert,x)
            assert LV<=-cert['epsilon']*V+cert['foster_C'];checks+=1
    # Previous one-species-pivot constructor has no admissible decomposition.
    # The inflow 0->A forces A to be the old pivot, but A->E is neither
    # a one-species A core reaction, an exact2A star edge, nor A-neutral.
    assert any(u==(0,0,0,0,0) and v==(1,0,0,0,0) for u,v,k in R)
    assert any(u==(1,0,0,0,0) and v==(0,1,0,0,0) for u,v,k in R)
    # Inactive death is a binding leakage guard, not silently admitted.
    bad=recognize(sp,R+[((1,0,0,0,0),(0,0,0,0,0),1)])
    assert not bad['accepted']
    # Acquiring the partition survives species and reaction permutations.
    perm=[4,2,0,3,1];Rp=[(tuple(u[j] for j in perm),tuple(v[j] for j in perm),k) for u,v,k in reversed(R)]
    rr=recognize([sp[j] for j in perm],Rp);assert rr['accepted']
    assert {[sp[j] for j in perm][i] for i in rr['service']}=={'A','E','B','D'}
    result={'status':'exact construction and challenges passed','species':sp,'raw_reactions':R,
      'acquired_service_indices':rec['service'],'acquired_hub_local_indices':rec['hubs'],
      'certificate':cert,'exact_state_checks':checks,'old_pivot_architecture_rejected_by_two_edge_witness':True,
      'inactive_death_mutation_rejected':True,'renaming_test_passed':True,
      'noncomplex_balance':'Core equations force b=d=1/20; B-star forces c=b, D-star forces c=2d, contradiction.',
      'scope':'All-state proof uses finite killed equations, rational tail bounds, and exact active-layer satellite coefficients; grids are implementation checks only.'}
    print(json.dumps(result,default=encode,indent=2))
if __name__=='__main__':main()
