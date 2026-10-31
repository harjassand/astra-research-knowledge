"""Pending constructive partial-row coverage theorem. Exact rational finite support acquisition."""
from fractions import Fraction as F
from itertools import combinations,product
from math import prod,ceil
import json

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

def core_jumps(rec,y):
    for u,v,k in rec['core']:
        if all(y[i]>=u[i] for i in range(len(y))):
            rate=k*prod(prod(range(y[i]-u[i]+1,y[i]+1)) for i in range(len(y)))
            yield tuple(y[i]-u[i]+v[i] for i in range(len(y))),rate

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

def demo_network():
    sp=['B','D','C','F'];zero=(0,)*4
    def unit(i,n=1):return tuple(n*int(i==j) for j in range(4))
    rs=[]
    for h in [0,1]:rs.extend([(zero,unit(h),F(h+1,10)),(unit(h),zero,1)])
    rs.extend([(unit(0),unit(1),1),(unit(1),unit(0),1),(unit(2),unit(3),1),(unit(3),unit(2),1)])
    for h,j,a in [(0,2,1),(1,3,1)]:
        pair=tuple(int(k==h)+int(k==j) for k in range(4));rs.extend([(unit(h,2),pair,a),(pair,unit(h,2),1)])
    return sp,rs

def support_table(rec,q,max_support_states=512):
    m=len(rec['service']);n=2**m
    if n>max_support_states:return {'accepted':False,'reason':'explicit binary-support work budget exceeded','required_states':n,'budget':max_support_states}
    states=list(product([0,1],repeat=m))
    def covered(b):return all(any(rec['beta'][h][j]*b[h]>0 for h in rec['hubs']) for j in range(len(rec['satellites'])))
    bad=[b for b in states if not covered(b)];index={b:i for i,b in enumerate(bad)}
    rows={};A=[[F(0)]*len(bad) for _ in bad]
    for b in states:
        events=[]
        for u,v,k in rec['core']:
            if sum(u) and not b[u.index(1)]:continue
            bp=tuple(min(1,z-a+c) for z,a,c in zip(b,u,v))
            if bp==b:continue
            rate=k*prod((q[i]**(v[i]-u[i]) for i in range(m)),start=F(1))
            events.append((bp,rate))
            if b in index:
                a=index[b];A[a][a]+=rate
                if bp in index:A[a][index[bp]]-=rate
        rows[b]=events
    times=solve(A,[F(1)]*len(bad));assert min(times)>0
    f={b:F(1)+(times[index[b]] if b in index else F(0)) for b in states}
    monotone_checks=0
    for b in states:
      for bp in states:
        if all(a<=c for a,c in zip(b,bp)):
            assert f[b]>=f[bp];monotone_checks+=1
    Qf={b:sum(rate*(f[bp]-f[b]) for bp,rate in rows[b]) for b in states}
    assert all(Qf[b]==-1 for b in bad)
    Fmax=max(f.values());K=max(Qf[b] for b in states if covered(b))
    return {'accepted':True,'states':states,'bad_states':bad,'killed_matrix':A,'hitting_times':times,
      'support_rows':[{'support':b,'covered':covered(b),'f':f[b],'Qf':Qf[b],'events':rows[b]} for b in states],
      'F':Fmax,'K':K,'monotonicity_checks':monotone_checks,
      'largest_table_fraction_bits':max(max(z.numerator.bit_length(),z.denominator.bit_length()) for z in f.values())}

def construct(rec,max_support_states=512,max_tilt_trials=40):
    assert rec['accepted'];trials=[]
    for n in range(max_tilt_trials):
        T=1+F(1,2**n);p=tail_parameters(rec,T);table=support_table(rec,p['q'],max_support_states)
        if not table['accepted']:return table
        Fmax=table['F'];B=p['immigration_bound'];passed=B*Fmax<=F(1,4)
        trials.append({'T':T,'B':B,'F':Fmax,'BF':B*Fmax,'passed':passed,'binary_linear_system_dimension':len(table['bad_states']),
          'largest_table_fraction_bits':table['largest_table_fraction_bits']})
        if passed:break
    else:return {'accepted':False,'reason':'explicit tilt-trial budget exhausted','search_trials':trials}
    D=p['death_weight_max'];delta=p['delta'];alpha=p['alpha_max']
    c=min(F(1),delta/(4*alpha),1/(4*D*Fmax**2));margin=delta-c*alpha
    epsilon=min(delta/4,1/(4*Fmax));A=B+table['K']+c*D*Fmax
    R=max(1,ceil((A+epsilon)/margin));beta_min=min(x for row in rec['beta'] for x in row if x>0)
    Zstar=max(0,ceil((A+epsilon)*(R+c)/(c*beta_min)))
    coefficient=Fmax*(A+epsilon);qmax=max(p['q'])
    C={'coefficient':coefficient,'service_base':qmax,'service_exponent':R,'satellite_base':T,'satellite_exponent':Zstar,
       'meaning':'coefficient * service_base**service_exponent * satellite_base**satellite_exponent',
       'expanded':False,'unreduced_numerator_bits_upper':coefficient.numerator.bit_length()+R*qmax.numerator.bit_length()+Zstar*T.numerator.bit_length(),
       'unreduced_denominator_bits_upper':coefficient.denominator.bit_length()+R*qmax.denominator.bit_length()+Zstar*T.denominator.bit_length()}
    return {'accepted':True,'T':T,'q':p['q'],'v':p['v'],'Qv':p['Qv'],'L':p['L'],'eta':p['eta'],
      'linear_hitting_times':p['hitting_times'],'delta':delta,'alpha_max':alpha,'death_weight_max':D,'immigration_bound':B,
      'support_table':table,'c':c,'margin':margin,'epsilon':epsilon,'covered_constant_bound_A':A,
      'R':R,'satellite_exception_threshold':Zstar,'reverse_rate_min':beta_min,'foster_C_expression':C,
      'tilt_search_trials':trials,'work':{'recognition_trials':rec['recognition_trials'],'tilt_trials':len(trials),
       'binary_linear_system_dimensions':[x['binary_linear_system_dimension'] for x in trials],
       'total_binary_matrix_entries':sum(x['binary_linear_system_dimension']**2 for x in trials),
       'final_monotonicity_checks':table['monotonicity_checks'],'largest_final_table_fraction_bits':table['largest_table_fraction_bits']}}

def quotient(rec,cert,x):
    y=tuple(x[i] for i in rec['service']);r=sum(y);f={tuple(row['support']):row['f'] for row in cert['support_table']['support_rows']}
    b=tuple(int(a>0) for a in y);out=F(0)
    for u,v,k in rec['reactions']:
        if any(a<z for a,z in zip(x,u)):continue
        xp=tuple(a-z+w for a,z,w in zip(x,u,v));yp=tuple(xp[i] for i in rec['service']);rp=sum(yp)
        bp=tuple(int(a>0) for a in yp)
        if rp==r:gratio=F(1)
        elif rp==r+1:gratio=F(r+1)/(r+1+cert['c'])
        elif rp==r-1:gratio=(r+cert['c'])/r
        else:raise AssertionError('service jump outside +/-1')
        ratio=prod((cert['q'][i]**(yp[i]-y[i]) for i in range(len(y))),start=F(1))
        ratio*=cert['T']**sum(v[i]-u[i] for i in rec['satellites'])*f[bp]/f[b]*gratio
        rate=k*prod(prod(range(a-z+1,a+1)) for a,z in zip(x,u))
        out+=rate*(ratio-1)
    return out

def master_bound(rec,cert,x):
    y=[x[i] for i in rec['service']];r=sum(y);b=tuple(int(a>0) for a in y)
    row=next(row for row in cert['support_table']['support_rows'] if tuple(row['support'])==b)
    support_bound=cert['support_table']['K'] if row['covered'] else -1/cert['support_table']['F']
    sat=sum(rec['beta'][h][j]*y[h]*x[rec['satellites'][j]] for h in rec['hubs'] for j in range(len(rec['satellites'])))
    return cert['immigration_bound']+support_bound+cert['c']*cert['death_weight_max']*cert['support_table']['F']-cert['margin']*r-cert['c']*sat/(r+1+cert['c'])

def main():
    sp,rs=demo_network();rec=recognize(sp,rs);assert rec['accepted'];cert=construct(rec);assert cert['accepted']
    checks=0
    for r in range(9):
      for y in compositions(r,len(rec['service'])):
        for z in product([0,1,10,100],repeat=len(rec['satellites'])):
            x=tuple(y)+tuple(z);assert quotient(rec,cert,x)<=master_bound(rec,cert,x);checks+=1
    targeted=[]
    R=cert['R'];Z=cert['satellite_exception_threshold']
    for r in [R-1,R,R+1]:
      for y in [(0,r),(r,0),(1,r-1),(r-1,1)]:
       for z in [(Z-1,0),(Z,0),(Z+1,0),(0,Z+1)]:
        x=y+z;q=quotient(rec,cert,x);bound=master_bound(rec,cert,x);assert q<=bound
        b=tuple(int(a>0) for a in y);covered=all(b)
        if not covered or r>=R or sum(z)>Z:assert bound<=-cert['epsilon']
        targeted.append({'state':x,'exact_generator_quotient':q,'master_bound':bound})
    print(json.dumps({'recognition':rec,'certificate':cert,'exact_master_bound_checks':checks,
      'targeted_large_state_checks':targeted},default=encode,sort_keys=True,indent=2))
if __name__=='__main__':main()
