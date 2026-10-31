"""Sufficient raw-list partial-row finder. Numerical LP proposes; all acceptance is rational.
No LP-search termination or general stability completeness is claimed.
"""
from fractions import Fraction as F
from itertools import combinations,product
from math import prod,ceil,comb
import json
import numpy as np
from scipy.optimize import linprog

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
        T=tuple(i for i in range(n) if i not in S);core=[];univariate=[];neutral=[];bad=[]
        alpha={(h,j):F(0) for h in S for j in T};beta=alpha.copy()
        for z,(u,v,k) in enumerate(rs):
            if all(u[j]==v[j]==0 for j in T) and sum(u)<=1 and sum(v)<=1:
                core.append((tuple(u[i] for i in S),tuple(v[i] for i in S),k));continue
            local_u=tuple(u[i] for i in S);local_v=tuple(v[i] for i in S)
            if all(u[j]==v[j]==0 for j in T) and any(
                local_u[i]>0 and local_v[i]>0 and all(local_u[j]==local_v[j]==0 for j in range(m) if j!=i)
                for i in range(m)):
                univariate.append((local_u,local_v,k));continue
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
        if bad or not H or any((alpha[h,j]>0)!=(beta[h,j]>0) for h in H for j in T) or any(not any(beta[h,j]>0 for h in H) for j in T):
            trials.append({'service':S,'reason':'shape, paired positive stars, or an uncovered satellite'});continue
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
        if any(death[i]<=0 for i in Hl):
            trials.append({'service':S,'reason':'every active hub needs positive direct death'});continue
        if univariate:
            trials.append({'service':S,'reason':'this partial-row finder has a linear-only service core'});continue
        phase_edges=[[(sum(u),sum(v)) for u,v,rate in univariate if u[i]>0] for i in range(m)]
        if any(edges and not weak_reversible(edges) for edges in phase_edges):
            trials.append({'service':S,'reason':'positive-count univariate subgraph is not weakly reversible'});continue
        immigration=[sum(k for u,v,k in core if u==zero and v==units[i]) for i in range(m)]
        conv=[[sum(k for u,v,k in core if u==units[i] and v==units[j]) if i!=j else F(0) for j in range(m)] for i in range(m)]
        return {'accepted':True,'species':species,'service':S,'satellites':T,'hubs':Hl,'inactive':Il,
          'core':core+univariate,'linear_core':core,'univariate':univariate,'immigration':immigration,'death':death,'conversion':conv,
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
            rate=k*prod(prod(range(y[i]-u[i]+1,y[i]+1)) for i in range(len(y)))
            yield tuple(y[i]-u[i]+v[i] for i in range(len(y))),rate

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

def encode(o):
    if isinstance(o,F):return str(o)
    raise TypeError(type(o))

def tail_parameters(rec,T):
    T=F(T);assert T>1
    m=len(rec['service']);H=rec['hubs'];I=rec['inactive'];k=rec['conversion'];d=rec['death'];lam=rec['immigration']
    times=[F(0)]*m
    if I:
        mat=[[((sum(k[i])+d[i]) if i==j else -k[i][j]) for j in I] for i in I]
        t=solve(mat,[F(1)]*len(I))
        for i,x in zip(I,t):times[i]=x
    L=max((1+sum(k[h][i]*times[i] for i in I))/d[h] for h in H)
    v=[L+x for x in times];eta=(T-1)/L;q=[1+eta*x for x in v]
    Qv=[sum(k[i][j]*(v[j]-v[i]) for j in range(m))-d[i]*v[i] for i in range(m)]
    assert all(x<=-1 for x in Qv) and all(q[h]==T for h in H)
    delta=min(eta/x for x in q);alpha=max(sum(rec['alpha'][h]) for h in H)
    c=min(F(1),delta/(4*alpha));D=max(d[i]/q[i] for i in range(m));B=sum(lam[i]*(q[i]-1) for i in range(m))
    et=delta/4;R0=max(2,ceil((B+2*c*D+et)/(delta-c*alpha)))
    return {'T':T,'hitting_times':times,'L':L,'v':v,'Qv':Qv,'eta':eta,'q':q,'delta':delta,
      'alpha_max':alpha,'c':c,'death_weight_max':D,'immigration_bound':B,'tail_epsilon':et,'initial_R':R0}

def build_lp(rec,pars,R):
    m=len(rec['service']);T=pars['T'];c=pars['c'];q=pars['q'];epsilon=pars['delta']/500
    beta_min=min(x for row in rec['beta'] for x in row if x>0)
    gamma=min(epsilon,c*beta_min/(2*(R+c)))
    states=[y for r in range(R) for y in compositions(r,m)];index={y:i for i,y in enumerate(states)};n=len(states)
    def hform(y):
        a=[F(0)]*(n+1)
        if y in index:a[index[y]]=F(1)
        else:a[-1]=prod((q[i]**y[i] for i in range(m)),start=F(1))*g(sum(y),c)
        return a
    def add(a,b,k):return [x+k*y for x,y in zip(a,b)]
    inequalities=[];state_rows=[]
    for r in range(R+1):
      for y in compositions(r,m):
        hy=hform(y);constant=[F(0)]*(n+1)
        for yp,rate in core_jumps(rec,y):constant=add(constant,add(hform(yp),hy,-1),rate)
        for h in rec['hubs']:
            if y[h]>=2:
                yp=list(y);yp[h]-=1
                constant=add(constant,add([T*a for a in hform(tuple(yp))],hy,-1),sum(rec['alpha'][h])*y[h]*(y[h]-1))
        good=all(any(rec['beta'][h][j]*y[h]>0 for h in rec['hubs']) for j in range(len(rec['satellites'])))
        if not good:inequalities.append({'label':['uncovered_constant',y],'coefficients':add(constant,hy,epsilon)})
        satellite=[]
        for j in range(len(rec['satellites'])):
            a=[F(0)]*(n+1)
            for h in rec['hubs']:
                if not rec['beta'][h][j]*y[h]:continue
                yp=list(y);yp[h]+=1
                a=add(a,add([z/T for z in hform(tuple(yp))],hy,-1),rec['beta'][h][j]*y[h])
            satellite.append(a)
            constraint=add(a,hy,gamma) if good else a
            if any(constraint):inequalities.append({'label':['satellite',y,j,good],'coefficients':constraint})
        state_rows.append({'service_state':y,'covered':good,'constant_form':constant,'satellite_forms':satellite})
    return {'R':R,'head_states':states,'epsilon':epsilon,'gamma':gamma,'inequalities':inequalities,'state_rows':state_rows}

def construct(rec,T=F(2),max_head_states=2000,max_radius_trials=5,denominator=10**9,proposal_slack=F(1,10**6)):
    assert rec['accepted'] and isinstance(T,(int,F))
    pars=tail_parameters(rec,T);R=pars['initial_R'];trials=[]
    for _ in range(max_radius_trials):
        count=comb(R+len(rec['service'])-1,len(rec['service']))
        if count>max_head_states:return {'accepted':False,'reason':'explicit partial-row LP head budget exceeded','budget':max_head_states,'required_head_states':count,'search_trials':trials}
        lp=build_lp(rec,pars,R);n=len(lp['head_states']);rows=lp['inequalities']
        out=linprog(np.zeros(n),A_ub=np.array([[float(z) for z in row['coefficients'][:-1]] for row in rows]),
          b_ub=np.array([-float(row['coefficients'][-1]+proposal_slack) for row in rows]),
          bounds=[(1e-8,None)]*n,method='highs')
        receipt={'R':R,'variables':n,'inequalities':len(rows),'floating_solver_status':int(out.status),
          'floating_message':str(out.message),'exact_accepted':False}
        if out.success:
            weights=[F(float(x)).limit_denominator(denominator) for x in out.x]
            residuals=[sum(a*b for a,b in zip(row['coefficients'][:-1],weights))+row['coefficients'][-1] for row in rows]
            good=min(weights)>0 and max(residuals)<=0
            receipt.update(max_exact_residual=max(residuals),minimum_weight=min(weights),exact_accepted=good)
            if good:
                trials.append(receipt);break
        trials.append(receipt);R*=2
    else:return {'accepted':False,'reason':'explicit partial-row radius-trial budget exhausted','search_trials':trials}
    def evaluate(a):return sum(x*y for x,y in zip(a[:-1],weights))+a[-1]
    records=[];C=F(0);epsilon=lp['epsilon']
    for row in lp['state_rows']:
        y=row['service_state']
        if sum(y)<R:hy=weights[lp['head_states'].index(y)]
        else:hy=prod((pars['q'][i]**y[i] for i in range(len(y))),start=F(1))*g(sum(y),pars['c'])
        H=evaluate(row['constant_form'])/hy;slopes=[-evaluate(a)/hy for a in row['satellite_forms']]
        Z=None
        if row['covered']:
            assert min(slopes)>=lp['gamma'];Z=max(-1,ceil((H+epsilon)/min(slopes)))
            if Z>=0:C=max(C,hy*pars['T']**Z*max(F(0),H+epsilon))
        else:assert H<=-epsilon and min(slopes)>=0
        records.append({'service_state':y,'covered':row['covered'],'constant_quotient':H,'satellite_slopes':slopes,'satellite_head_bound':Z})
    return {'accepted':True,**pars,'R':R,'head_states':lp['head_states'],'head_weights':weights,'epsilon':epsilon,
      'gamma':lp['gamma'],'foster_C':C,'finite_state_rows':records,'lp_inequalities':rows,
      'exact_lp_residuals':residuals,'search_trials':trials,'proposal_slack':proposal_slack,'rationalization_denominator_limit':denominator,
      'work':{'recognition_trials':rec['recognition_trials'],'LP_variable_counts':[x['variables'] for x in trials],
        'LP_inequality_counts':[x['inequalities'] for x in trials],'total_dense_matrix_entries':sum(x['variables']*x['inequalities'] for x in trials),
        'largest_weight_fraction_bits':max(max(x.numerator.bit_length(),x.denominator.bit_length()) for x in weights)}}

def demo_network():
    sp=['B','D','C','F'];zero=(0,)*4
    def unit(i,n=1):return tuple(n*int(i==j) for j in range(4))
    rs=[]
    for h in [0,1]:rs.extend([(zero,unit(h),F(h+1,10)),(unit(h),zero,1)])
    rs.extend([(unit(0),unit(1),1),(unit(1),unit(0),1),(unit(2),unit(3),1),(unit(3),unit(2),1)])
    for h,j,a in [(0,2,1),(1,3,1)]:
        pair=tuple(int(k==h)+int(k==j) for k in range(4));rs.extend([(unit(h,2),pair,a),(pair,unit(h,2),1)])
    return sp,rs

def main():
    sp,rs=demo_network();rec=recognize(sp,rs);assert rec['accepted'];cert=construct(rec);assert cert['accepted']
    checks=0
    for r in range(cert['R']+3):
      for y in compositions(r,len(rec['service'])):
        for z in product([0,1,10,100],repeat=len(rec['satellites'])):
            x=[0]*len(sp)
            for i,a in zip(rec['service'],y):x[i]=a
            for i,a in zip(rec['satellites'],z):x[i]=a
            V,LV=generator(rec,cert,x);assert LV<=-cert['epsilon']*V+cert['foster_C'];checks+=1
    print(json.dumps({'recognition':rec,'certificate':cert,'exact_state_checks':checks},default=encode,sort_keys=True,indent=2))

if __name__=='__main__':
    from itertools import product
    main()
