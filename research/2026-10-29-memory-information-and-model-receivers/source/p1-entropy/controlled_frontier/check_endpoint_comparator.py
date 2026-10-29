#!/usr/bin/env python3
"""Exact native-endpoint rerouting controls and the C5 conventional optimum.

No observations, resets or external optimizer execution. Algebra is Fraction;
entropy comparisons reuse the prior review's outward rational log intervals.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json, math, time
from check_robust_entropy import (zeros, inv, mm, sub, entropy_bounds,
                                 g_bounds, log_bounds, ser)

ROOT = Path(__file__).resolve().parent

def add_edge(flow, i, j, a, b=None):
    flow[i][j] += a
    flow[j][i] += a if b is None else b

def balanced(flow):
    n = len(flow)
    assert all(sum(flow[i]) == sum(flow[j][i] for j in range(n))
               for i in range(n))
    assert all(flow[i][j] >= 0 for i in range(n) for j in range(n))
    assert all(bool(flow[i][j]) == bool(flow[j][i])
               for i in range(n) for j in range(n))

def endpoint(flow, m):
    n=len(flow); bi=list(range(m)); ii=list(range(m,n))
    lap=[[-v for v in row] for row in flow]
    for i in range(n): lap[i][i]=sum(flow[i])
    return mm(mm(sub(flow,bi,ii),inv(sub(lap,ii,ii))),sub(flow,ii,bi))

def eliminate_original_vertices(flow, m):
    """Only legal when each hidden component touches <=2 ports.

    A local check is enforced after every elimination. Original hidden
    labels remain stable until the final compaction.
    """
    original_n=len(flow)
    flow=[row[:] for row in flow]
    active=set(range(original_n)); stars=[]; steps=[]
    for x in range(m,original_n):
        before_entropy=entropy_bounds(flow)
        neigh=[i for i in sorted(active) if i!=x and flow[x][i]]
        ports=[i for i in neigh if i<m]
        assert len(ports)<=2, 'The complete endpoint reduction here is binary only.'
        a={i:flow[i][x] for i in neigh}; b={i:flow[x][i] for i in neigh}
        h=sum(a.values()); assert h==sum(b.values()) and h>0
        for i in range(len(flow)): flow[i][x]=flow[x][i]=F(0)
        active.remove(x)
        for i in neigh:
            for k in neigh:
                if i==k or (i<m and k<m): continue
                flow[i][k]+=a[i]*b[k]/h
        if ports:
            A=sum(a[i] for i in ports); B=sum(b[i] for i in ports)
            y=len(flow)
            for row in flow: row.append(F(0))
            flow.append([F(0)]*(y+1)); active.add(y); stars.append(y)
            for i in ports:
                flow[i][y]=a[i]*B/h
                flow[y][i]=b[i]*A/h
        balanced(flow)
        after_entropy=entropy_bounds(flow)
        assert after_entropy[0] <= before_entropy[1]
        status=('strict_rational_interval' if after_entropy[1] < before_entropy[0]
                else 'overlapping_intervals_allow_equality')
        steps.append({'removed_vertex':x,'ports':ports,'entropy_before':before_entropy,
                      'entropy_after':after_entropy,'interval_comparison':status})
    order=list(range(m))+stars
    return sub(flow,order,order),steps

def binary_control(k):
    # Genuine hidden transitions plus a directed circulation. Every edge
    # has a reverse; all stationary flux balances are exact.
    flow=zeros(5)
    for i in range(5):
        for j in range(i):
            if i<2 and j<2: continue
            add_edge(flow,i,j,F(1+(i+j+k)%4,5+k))
    cycle=[0,2,3,1,4]
    current=F(k+1,3)
    for i,j in zip(cycle,cycle[1:]+cycle[:1]): flow[i][j]+=current
    balanced(flow)
    old=endpoint(flow,2)
    reduced,steps=eliminate_original_vertices(flow,2)
    new=endpoint(reduced,2)
    assert old==new
    assert [sum(row) for row in flow[:2]]==[sum(row) for row in reduced[:2]]
    for x in range(2,len(reduced)):
        assert all(not reduced[x][y] for y in range(2,len(reduced)))
    eb=entropy_bounds(flow); ea=entropy_bounds(reduced)
    assert ea[1]<eb[0]
    return {'case':k,'original_states':len(flow),'reduced_states':len(reduced),
            'endpoint_flux':old,'exact_endpoint_preservation':True,
            'exact_port_flux_preservation':True,'entropy_original':eb,
            'entropy_reduced':ea,'strict_entropy_reduction':True,'steps':steps}

def c5_control():
    flow=zeros(15); x=5
    for i in range(5):
        j=(i+1)%5
        for a,b in [(F(5,8),F(3,8)),(F(3,8),F(5,8))]:
            h=F(16,15)
            flow[i][x]=h*a; flow[j][x]=h*b
            flow[x][i]=h*b; flow[x][j]=h*a
            x+=1
    balanced(flow); N=endpoint(flow,5)
    target=[[F(i==j)+F(17,30)*((i-j)%5 in (1,4)) for j in range(5)] for i in range(5)]
    assert N==target
    R=sum(map(sum,N)); D=sum(N[i][i] for i in range(5)); r=D/R
    assert R==F(32,3) and r==F(15,32) and 1-2*r==F(1,16)
    hpair=sum((1-2*((i-j)%5 in (1,4)))*N[i][j] for i in range(5) for j in range(5))
    assert hpair==F(-2,3)
    E=entropy_bounds(flow); gb=g_bounds(r)
    lower=(R*gb[0],R*gb[1]); ll,lh=log_bounds(F(5,3))
    exact=(F(16,3)*ll,F(16,3)*lh)
    assert max(E[0],lower[0],exact[0])<=min(E[1],lower[1],exact[1])
    # Exact identity for g(15/32), not just overlap of numerical intervals.
    assert R*2*F(1,4)==F(16,3) and (1+F(1,4))/(1-F(1,4))==F(5,3)
    return {'endpoint_flux':N,'R':R,'trace':D,'return_fraction':r,
            'horn_pairing':hpair,'minimum_exact_expression':'(16/3)*log(5/3)',
            'entropy_interval':E,'binary_lower_interval':lower,
            'closed_form_interval':exact,'equality_algebra_checked':True,
            'per_departure_exact_expression':'(1/2)*log(5/3)',
            'uncensored_linear_to_optimum':1/(2*math.log(5/3)),
            'unit_bin_linear_to_full_record_optimum':(1-math.exp(-1))/(2*math.log(5/3))}

def main():
    start=time.perf_counter()
    cases=[binary_control(k) for k in range(6)]
    result={'scope':'Exact uncensored endpoint comparator; no hidden clock ceiling',
            'binary_rerouting_controls':cases,'c5':c5_control(),
            'source_observations':0,'native_resets':0,'external_optimizer_runs':0,
            'algebra':'Fraction exact endpoint/flow operations',
            'transcendentals':'Outward rational log/sqrt intervals reused from prior review',
            'wall_seconds':time.perf_counter()-start,
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'dependency_sha256':hashlib.sha256((ROOT/'check_robust_entropy.py').read_bytes()).hexdigest()}
    (ROOT/'ENDPOINT_COMPARATOR_CHECKS.json').write_text(json.dumps(ser(result),indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('binary_rerouting_controls','c5')},indent=2))
    print(json.dumps({'binary_control_count':len(cases),
                      'c5_exact_optimum':result['c5']['minimum_exact_expression'],
                      'uncensored_linear_fraction':result['c5']['uncensored_linear_to_optimum'],
                      'unit_bin_linear_fraction':result['c5']['unit_bin_linear_to_full_record_optimum']},indent=2))

if __name__=='__main__': main()
