#!/usr/bin/env python3
"""Clock-constrained mean-record completion: LP proposal, exact certificates.

No source observations or random draws. SciPy proposes LP primal/dual values;
Fractions certify the implicit infinite family of envelope constraints.
The finite-rate completion is then checked by full generator elimination.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib, json, math, time
import numpy as np
import scipy
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent

def rat(x):
    return Q(float(x)).limit_denominator(10**8)

def dot(a,b):
    return sum((x*y for x,y in zip(a,b)),Q())

def psi(x,f,rate):
    assert x>=0 and f>=0 and rate>0
    if not f:
        assert not x
        return Q()
    u=rate*x/f; n=u.numerator//u.denominator
    return f*(n+1)*(2*u-n)/(rate*rate)

def solve_clock_transport(flow,vr,vl,wb,port_cap,hidden_cap):
    m=len(wb);v=sum(vr);assert sum(vl)==v
    spare=[wb[i]*port_cap[i]-sum(flow[i][j] for j in range(m) if j!=i) for i in range(m)]
    if min(spare)<0:
        return {'status':'port_budget_impossible','spare':spare}
    keys=[(i,j) for i in range(m) for j in range(m)
          if (spare[i]>0 if i==j else flow[i][j]>0)]
    caps=[spare[i] if i==j else flow[i][j] for i,j in keys]
    # Exact support-cut certificate, not a floating infeasibility status.
    for mask in range(1,1<<m):
        rows={i for i in range(m) if mask>>i&1}
        cols={j for i,j in keys if i in rows}
        if sum(vr[i] for i in rows)>sum(vl[j] for j in cols):
            return {'status':'transport_impossible','rows':sorted(rows),'columns':sorted(cols),
                    'row_mass':sum(vr[i] for i in rows),'column_mass':sum(vl[j] for j in cols)}
    r=len(keys); eq=[]; rhs=list(vr)+list(vl)
    for i in range(m):eq.append([Q(a==i) for a,b in keys]+[Q()]*r)
    for j in range(m):eq.append([Q(b==j) for a,b in keys]+[Q()]*r)
    objective=[Q()]*r+[Q(1)]*r
    planes={(e,0) for e in range(r)}; iterations=0
    while True:
        iterations+=1
        assert iterations<=100, 'prototype separation limit reached'
        ordered=sorted(planes); ub=[]; bounds=[]
        for e,n in ordered:
            row=[Q()]*(2*r);row[e]=2*Q(n+1)/hidden_cap;row[r+e]=-1
            ub.append(row);bounds.append(Q(n*(n+1))*caps[e]/hidden_cap**2)
        res=linprog(np.array(objective,dtype=float),A_ub=np.array(ub,dtype=float),
                    b_ub=np.array(bounds,dtype=float),A_eq=np.array(eq,dtype=float),
                    b_eq=np.array(rhs,dtype=float),bounds=(0,None),method='highs')
        assert res.success,res.message
        candidate=list(map(rat,res.x)); x=candidate[:r]; y=candidate[r:]
        assert min(candidate)>=0
        assert all(dot(row,candidate)==b for row,b in zip(eq,rhs)), 'rational primal reconstruction failed'
        violated=[]
        for e in range(r):
            if y[e]<psi(x[e],caps[e],hidden_cap):
                u=hidden_cap*x[e]/caps[e];n=u.numerator//u.denominator
                assert (e,n) not in planes,'solver failed an installed exact cut'
                violated.append((e,n))
        if violated:
            planes.update(violated);continue
        dual_ub=list(map(rat,res.ineqlin.marginals))
        dual_eq=list(map(rat,res.eqlin.marginals))
        assert all(t<=0 for t in dual_ub)
        reduced=[objective[j]-sum(ub[i][j]*dual_ub[i] for i in range(len(ub)))
                 -sum(eq[i][j]*dual_eq[i] for i in range(len(eq))) for j in range(2*r)]
        assert min(reduced)>=0, 'rational dual reconstruction failed'
        primal=dot(objective,candidate);dual=dot(bounds,dual_ub)+dot(rhs,dual_eq)
        assert primal==dual
        assert all(y[e]==psi(x[e],caps[e],hidden_cap) for e in range(r))
        mat=[[Q() for j in range(m)] for i in range(m)]
        for (i,j),value in zip(keys,x):mat[i][j]=value
        return {'status':'certified','M':mat,'J':primal,'spare':spare,
                'iterations':iterations,'keys':keys,'planes':ordered,
                'primal_variables':candidate,'dual_inequality':dual_ub,
                'dual_equality':dual_eq,'nonnegative_reduced_costs':reduced,
                'dual_objective':dual}

def solve(a,b):
    n=len(b)
    if not n:return []
    u=[list(a[i])+[b[i]] for i in range(n)]
    for j in range(n):
        p=next(i for i in range(j,n) if u[i][j])
        u[j],u[p]=u[p],u[j];z=u[j][j];u[j]=[x/z for x in u[j]]
        for i in range(n):
            if i!=j:
                z=u[i][j];u[i]=[x-z*y for x,y in zip(u[i],u[j])]
    x=[row[-1] for row in u]
    assert all(dot(row,x)==bb for row,bb in zip(a,b))
    return x

def sub(a,ii,jj=None):
    if jj is None:jj=ii
    return [[a[i][j] for j in jj] for i in ii]

def construct_minimum(flow,wb,port_cap,hidden_cap,certificate):
    """Shared-prefix adjacent-Erlang channels; no fictitious self-jump."""
    mat=certificate['M'];m=len(wb);w=list(wb);edges=[];channels=[]
    def edge(i,j,f):
        if f:
            assert f>0 and i!=j
            edges.append((i,j,f))
    def state(f):
        assert f>0
        j=len(w);w.append(f/hidden_cap);return j
    for i in range(m):
        for j in range(m):
            x=mat[i][j]
            f=flow[i][j] if i!=j else min(certificate['spare'][i],hidden_cap*x)
            if not f:
                assert not x;continue
            u=hidden_cap*x/f;n=u.numerator//u.denominator;t=u-n
            if i==j:assert n>=1
            channels.append({'from':i,'to':j,'flow':f,'mass':x,'prefix':n,'extra_probability':t})
            if n==0:
                edge(i,j,f*(1-t))
                if t:
                    new=state(f*t);edge(i,new,f*t);edge(new,j,f*t)
            else:
                previous=i
                for z in range(n):
                    new=state(f);edge(previous,new,f);previous=new
                edge(previous,j,f*(1-t))
                if t:
                    new=state(f*t);edge(previous,new,f*t);edge(new,j,f*t)
    count=len(w);lap=[[Q()]*count for _ in range(count)]
    for i,j,f in edges:lap[i][i]+=f;lap[i][j]-=f
    assert all(sum(row)==0 for row in lap)
    assert all(sum(lap[i][j] for i in range(count))==0 for j in range(count))
    rates=[lap[i][i]/w[i] for i in range(count)]
    assert all(rates[i]<=port_cap[i] for i in range(m))
    assert all(rates[i]<=hidden_cap for i in range(m,count))
    assert all(wi>0 for wi in w)
    # Port flow is strongly connected by the declared S; check the
    # full graph too so unused branch states cannot silently survive.
    for start in range(count):
        seen={start};todo=[start]
        while todo:
            i=todo.pop()
            for j in range(count):
                if i!=j and lap[i][j]<0 and j not in seen:seen.add(j);todo.append(j)
        assert len(seen)==count
    ii=list(range(m,count));wi=w[m:];g=sub(lap,ii)
    right=solve(g,wi);left=solve([list(row) for row in zip(*g)],wi)
    br=[w[i]-dot([lap[i][z] for z in ii],right) for i in range(m)]
    bl=[w[i]-dot(left,[lap[z][i] for z in ii]) for i in range(m)]
    sc=[[lap[i][j]-dot([lap[i][z] for z in ii],solve(g,[lap[z][j] for z in ii]))
         for j in range(m)] for i in range(m)]
    desired_s=[[sum(flow[i][z] for z in range(m) if z!=i) if i==j else -flow[i][j]
                for j in range(m)] for i in range(m)]
    assert sc==desired_s
    assert br==[wb[i]+sum(mat[i]) for i in range(m)]
    assert bl==[wb[j]+sum(mat[i][j] for i in range(m)) for j in range(m)]
    c=dot(wi,right);assert 2*c==certificate['J']
    queries=[]
    for mask in range(1,1<<m):
        target={i for i in range(m) if mask>>i&1}
        keep=[i for i in range(count) if i not in target]
        if not keep:continue
        ww=[w[i] for i in keep];h=solve(sub(lap,keep),ww)
        full=dot(ww,h)/sum(ww)
        live=[i for i in range(m) if i not in target]
        hb=solve(sub(sc,live),[br[i] for i in live])
        reduced=(c+dot([bl[i] for i in live],hb))/(sum(w)-sum(w[i] for i in target))
        assert full==reduced
        queries.append({'target_mask':mask,'full_mean':full,'record_mean':reduced})
    return {'w':w,'L':lap,'rates':rates,'port_count':m,'hidden_count':count-m,
            'S':sc,'bR':br,'bL':bl,'c':c,'channels':channels,'queries':queries,
            'maximum_coefficient_fraction_bits':max(max(z.numerator.bit_length(),z.denominator.bit_length())
              for z in [z for row in lap for z in row]+w+rates)}

def serialize(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):serialize(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serialize(v) for v in x]
    return x

def main():
    start=time.perf_counter();cases=[];source_calls=0
    f2=[[Q(),Q(1)],[Q(1),Q()]]
    for cap in [Q(1,2),Q(1),Q(3,2),Q(2),Q(5)]:
        cases.append((f'two_port_unbalanced_rate_{cap}',f2,[Q(1),Q()],[Q(),Q(1)],
                      [Q(1),Q(1)],[Q(1),Q(1)],cap))
    cycle=[[Q(),Q(1),Q()],[Q(),Q(),Q(1)],[Q(1),Q(),Q()]]
    for port_rate in [Q(1),Q(2),Q(5)]:
        cases.append((f'balanced_cycle_port_cap_{port_rate}',cycle,[Q(1)]*3,[Q(1)]*3,
                      [Q(1)]*3,[port_rate]*3,Q(4)))
    cases.append(('balanced_cycle_no_spare_support_failure',cycle,
                  [Q(1),Q(2),Q(1)],[Q(1),Q(2),Q(1)],[Q(1)]*3,[Q(1)]*3,Q(4)))
    cases.append(('impossible_port_trace_budget',f2,[Q(1),Q()],[Q(),Q(1)],
                  [Q(1),Q(1)],[Q(1,2),Q(1)],Q(4)))
    f3=[[Q(),Q(1),Q(1,10)],[Q(1),Q(),Q(1)],[Q(1,10),Q(1),Q()]]
    for cap in [Q(2),Q(4),Q(7)]:
        cases.append((f'split_three_port_hidden_cap_{cap}',f3,[Q(2),Q(1),Q(1)],
                      [Q(1),Q(1),Q(2)],[Q(1)]*3,[Q(2),Q(3),Q(2)],cap))
    results=[];target_count=0
    for name,flow,vr,vl,wb,ports,hidden in cases:
        cert=solve_clock_transport(flow,vr,vl,wb,ports,hidden)
        item={'case':name,'hidden_rate_ceiling':hidden,'port_rate_ceilings':ports,
              'flow_off':flow,'vR':vr,'vL':vl,'wB':wb,'certificate':cert}
        if cert['status']=='certified':
            model=construct_minimum(flow,wb,ports,hidden,cert)
            assert 2*sum(vr)/hidden<=cert['J']
            item['model']=model;target_count+=len(model['queries'])
        results.append(item)
    # Exact boundary sensitivity: an Erlang-n record requires hidden cap >=n.
    witness=[]
    for n in [2,3,5,17,128]:
        c=Q(n+1,2*n)
        for cap in [Q(n)-Q(1,10),Q(n),Q(n)+Q(1,10)]:
            floor=psi(Q(1),Q(1),cap)/2
            assert (c>=floor)==(cap>=n)
            witness.append({'n':n,'hidden_rate_ceiling':cap,'c':c,'minimum_c':floor,'feasible':c>=floor})
    out={'status':'PASS','source_observations':source_calls,'source_preparations':0,
         'software_versions':{'numpy':np.__version__,'scipy':scipy.__version__},
         'random_draws':0,'verified_LP_optima':sum(r['certificate']['status']=='certified' for r in results),
         'exact_infeasibility_certificates':sum(r['certificate']['status']!='certified' for r in results),
         'full_generator_target_checks':target_count,'ceiling_witnesses':witness,
         'cases':results,'wall_seconds':time.perf_counter()-start,
         'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'method':'SciPy/HiGHS proposals; all primal constraints, envelope separation, dual feasibility and equality checked using Fractions. Full rational CTMC elimination and killed solves.',
         'scope':'Exact supplied records and rate ceilings. No learned source, physical implementation, runtime scaling claim, or arbitrary precision LP reconstruction guarantee.'}
    destination=HERE/'CLOCK_CAPPED_TRANSPORT_RESULTS.json'
    destination.write_text(json.dumps(serialize(out),indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','verified_LP_optima','exact_infeasibility_certificates','full_generator_target_checks','wall_seconds']}))

if __name__=='__main__':main()
