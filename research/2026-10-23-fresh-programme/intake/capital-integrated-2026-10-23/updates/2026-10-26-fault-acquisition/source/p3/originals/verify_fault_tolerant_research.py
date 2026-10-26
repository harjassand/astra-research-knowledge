"""Independent data-and-certificate verifier, without importing producer modules."""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json

ROOT=Path(__file__).resolve().parent
N=12;A=F(1,10);V=F(1,200);ETA=F(1,10000);M=F(2)
SITES=(F(0),F(1,2),F(1))
FAULT={(0,1):F(7),(4,6):F(-11)}

def raw(name):return json.loads((ROOT/name).read_text())
def f(x):return F(x)
def nn(i):return i//3,SITES[i%3]
def src(i,x,t=None):
    x=f(x)
    val=F(1,16)+x/30+x*(1-x)/40
    if i==1:val+=F(1,80)+x/100
    if i==2:val-=F(1,40)-x*(1-x)/60
    if i==3:val+=F(1,100)+x/40
    if t is not None:val+=V*F(i+1,8)*(1-2*x)*f(t)
    return val

def cuts_and_edges():
    ee=set()
    for u in range(N):
        for d in (1,2,6):ee.add(tuple(sorted((u,(u+d)%N))))
    assert len(ee)==30
    degree={u:sum(u in e for e in ee) for u in range(N)}
    assert all(degree[u]==5 for u in degree)
    mincut=30;count=0
    for mask in range(0,2**11):
        subset={0}|{j+1 for j in range(11) if mask>>j&1}
        if len(subset)==N:continue
        crossing=sum((u in subset)!=(v in subset) for u,v in ee)
        mincut=min(mincut,crossing);count+=1
    assert mincut==5 and count==2047
    return ee,count

def median(ys):return sorted(ys)[len(ys)//2]
def psum(path,rr):
    res=F(0)
    for a,b in zip(path,path[1:]):
        e=tuple(sorted((a,b)))
        res+=rr[e] if a<b else -rr[e]
    return res

def pathcheck(proofs,ee,rr,expected_radii=None,source=None):
    for vs,pr in proofs.items():
        v=int(vs);ps=pr['paths'];sets=[];sums=[]
        assert len(ps)==5
        for p in ps:
            assert p[0]==0 and p[-1]==v
            E=[tuple(sorted((a,b))) for a,b in zip(p,p[1:])]
            assert len(E)==len(set(E)) and all(e in ee for e in E)
            sets.append(set(E));sums.append(psum(p,rr))
        assert all(not sets[a]&sets[b] for a in range(5) for b in range(a+1,5))
        assert list(map(f,pr['path_sums']))==sums
        assert median(sums)==f(pr['median'])
        if expected_radii is not None:
            assert abs(f(pr['median'])-source(v)+source(0))<=expected_radii[v]

def sqr_up(x,bits=36):
    x=f(x);scale=2**bits
    k=isqrt(x.numerator*scale*scale//x.denominator)
    while k*k*x.denominator<x.numerator*scale*scale:k+=1
    return F(k,scale)

def project(q):
    w=sorted(q,reverse=True);s=F(0);threshold=F(0)
    for i,w_i in enumerate(w,1):
        s+=w_i;candidate=(s-1)/i
        if w_i>candidate:threshold=candidate
    out=[max(F(0),q_i-threshold) for q_i in q]
    assert sum(out)==1
    return out

def mats():
    return [
      [[F(0),F(1,15),F(-1,24),F(0)], [F(-1,20),F(0),F(1,25),F(0)],
       [F(1,24),F(-1,18),F(0),F(1,25)], [F(0),F(1,26),F(-1,22),F(0)]],
      [[F(0),F(-1,20),F(0),F(1,30)], [F(1,24),F(0),F(-1,28),F(0)],
       [F(0),F(1,25),F(0),F(-1,30)], [F(-1,28),F(0),F(1,25),F(0)]],
      [[F(0),F(1,25),F(1,25),F(1,25)], [F(1,25),F(0),F(0),F(0)],
       [F(1,25),F(0),F(0),F(0)], [F(1,25),F(0),F(0),F(0)]],
      [[F(0)]*4 for _ in range(4)]
    ]

def envelope_bounds(centers,radii,i,x):
    nodes=[(SITES[j],centers[3*i+j],radii[3*i+j]) for j in range(3)]
    lo=max(v-r-A*abs(x-t) for t,v,r in nodes)
    hi=min(v+r+A*abs(x-t) for t,v,r in nodes)
    return lo,hi

def vi(x,K,p,resp):
    return project([(p[i]+sum(K[i][j]*x[j] for j in range(4))-resp(i,x[i]))/M for i in range(4)])

def verify_tasks(cases_obj,centers,radii,src_at):
    centers=list(map(f,centers));radii=list(map(f,radii))
    E=f(cases_obj['joint_E'])
    maxr=list(map(f,cases_obj['uniform_module_error_limits']))
    assert E*E>=sum(r*r for r in maxr)
    for i in range(4):
        upper=max((envelope_bounds(centers,radii,i,F(j,256))[1]-
                  envelope_bounds(centers,radii,i,F(j,256))[0])/2 for j in range(257)) + A/512
        assert maxr[i]>=upper
    assert len(cases_obj['cases'])==60
    cnt=0
    for case in cases_obj['cases']:
        K=mats()[int(case['network'])]
        p=list(map(f,case['load']));x=list(map(f,case['estimate']));ref=list(map(f,case['source_aware_reference']))
        rho=f(case['guaranteed_position_radius']);rr=f(case['reference_iteration_residual'])
        q=(A+sqr_up(sum(k*k for row in K for k in row)))/M
        assert q<1
        surrogate=lambda i,t:sum(envelope_bounds(centers,radii,i,t))/2
        t=vi(x,K,p,surrogate)
        er=sqr_up(sum((a-b)**2 for a,b in zip(t,x)))
        assert rho>=(er+E/M)/(1-q)
        source_off=src_at(0,F(0))
        truth=lambda i,t:src_at(i,t)-source_off
        for i in range(4):
            for xx in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
                lo,hi=envelope_bounds(centers,radii,i,xx)
                assert lo<=truth(i,xx)<=hi
        truth_next=vi(ref,K,p,truth)
        assert rr*rr>=sum((a-b)**2 for a,b in zip(truth_next,ref))
        left=sqr_up(sum((a-b)**2 for a,b in zip(x,ref)))
        assert left<=rho+rr/(1-q)
        assert f(case['reference_discrepancy'])>=left
        cnt+=1
    return cnt

def independent_main():
    g=raw('fault_tolerant_acquisition_results.json')
    ee,count=cuts_and_edges();assert g['graph']['min_cut']==5
    z=[src(*nn(i)) for i in range(N)]
    rr={e:z[e[1]]-z[e[0]]+FAULT.get(e,0) for e in ee}
    exact=g['path_decoding_certificates']
    pathcheck(exact,ee,rr,{i:F(0) for i in range(N)},lambda i:z[i])
    cz=list(map(f,g['decoded_exact_values_relative_to_node0']))
    assert cz==[a-z[0] for a in z]
    assert sorted(tuple(x['edge']) for x in g['corrupted_edge_residuals_exact'])==sorted(FAULT)
    cases=verify_tasks(g['exact_later_operations'],cz,[F(0)]*N,
                       lambda i,t:src(i,t))
    no=g['nonzero_honest_noise'];rn=list(map(f,no['certified_node_radii']))
    rrno={e:rr[e]+ETA*F((-1)**j,2) for j,e in enumerate(sorted(ee))}
    pathcheck(no['path_decoding_certificates'],ee,rrno,{i:rn[i] for i in range(N)},lambda i:z[i])
    cases+=verify_tasks(no['later_operations'],no['decoded_centers'],rn,
                        lambda i,t:src(i,t))
    w=g['deleted_edge_lower_bound'];assert w['calls_after_one_deleted_sensor']==29
    e1={tuple(x) for x in w['faults_required_for_first_source']}
    e2={tuple(x) for x in w['faults_required_for_second_source']}
    assert len(e1)==len(e2)==2
    return cases

def independent_group():
    obj=raw('group_fault_acquisition_results.json');op=obj['group_robust_operation']
    data=[[f(x) for x in row] for row in op['synthetic_report_groups']]
    assert len(data)==5 and all(len(row)==11 for row in data)
    centers=[F(0)]+[median([data[dev][j] for dev in range(5)]) for j in range(11)]
    assert centers==list(map(f,op['exact_recovered_relative_values']))
    assert centers==[src(*nn(i))-src(0,F(0)) for i in range(N)]
    cases=verify_tasks(op['future_tasks'],centers,[F(0)]*N,lambda i,t:src(i,t))
    assert len(obj['edge_connectivity_insufficient_for_group_faults']['one_bad_group_edges'])==5
    return cases

def independent_drift():
    obj=raw('drifting_fault_robust_acquisition_results.json')
    times={tuple(map(int,k.strip('()').split(', '))):f(v) for k,v in obj['native_call_times'].items()}
    assert len(times)==30
    ee,_=cuts_and_edges()
    assert set(times)==ee
    ys={}
    for j,e in enumerate(sorted(ee)):
        u,v=e;t=times[e]
        ys[e]=src(*nn(v),t)-src(*nn(u),t)+ETA*F((-1)**j,2)+FAULT.get(e,F(0))
    all_cases=0
    for key in ['planned_reference_future_operations','midpoint_reference_future_operations',
                'start_reference_future_operations','end_reference_future_operations']:
        item=obj[key];ref=f(item['reference_time']);future=f(item['future_time'])
        centers=[F(0)]*N;radii=[F(0)]*N
        for vs,pr in item['node_beliefs'].items():
            v=int(vs);centers[v]=f(pr['center']);radii[v]=f(pr['total_future_radius'])
            assert abs(centers[v]-(src(*nn(v),future)-src(*nn(0),future)))<=radii[v]
        all_cases+=verify_tasks(item['tasks'],centers,radii,
                     lambda i,t:src(i,t,future))
        assert all_cases>0
    assert f(obj['best_certified_relative_node_radius'])<=f(obj['start_reference_node_radius'])
    return all_cases


def independent_vector():
    obj=raw('vector_fault_acquisition_results.json')
    latest=raw('vector_joint_lipschitz_support_results.json')
    ee,_=cuts_and_edges()
    L=F(3,25)
    def response(i,t):
        t=f(t)
        return (src(i,t),F(i+1,24)+t/25+t*(1-t)/50+F(i,200)*t)
    def sub(x,y):return tuple(a-b for a,b in zip(x,y))
    def dot(x,y):return sum(a*b for a,b in zip(x,y))
    def squared(x):return dot(x,x)
    values=[response(*nn(i)) for i in range(N)]
    bad={(0,1):(F(7),F(-9)),(4,6):(F(-11),F(13))}
    rr={e:tuple(values[e[1]][i]-values[e[0]][i]+bad.get(e,(0,0))[i] for i in range(2)) for e in ee}
    base_paths=raw('fault_tolerant_acquisition_results.json')['path_decoding_certificates']
    recovered=[tuple(map(f,q)) for q in obj['exact_decoded_relative_vectors']]
    assert recovered==[sub(v,values[0]) for v in values]
    for vs,cert in obj['path_majority_certificates'].items():
        v=int(vs);vec_sums=[]
        for path in base_paths[vs]['paths']:
            total=(F(0),F(0))
            for a,b in zip(path,path[1:]):
                step=rr[tuple(sorted((a,b)))]
                if a>b:step=tuple(-x for x in step)
                total=tuple(total[j]+step[j] for j in range(2))
            vec_sums.append(total)
        assert vec_sums==[tuple(map(f,w)) for w in cert['path_vector_sums']]
        assert sum(w==recovered[v] for w in vec_sums)>=3
    for q in obj['new_future_vector_queries']:
        i=int(q['module']);t=f(q['unvisited_input']);radius=f(q['certified_euclidean_radius'])
        actual=sub(response(i,t),values[0]);est=tuple(map(f,q['predicted_relative_vector']))
        assert squared(sub(actual,est))<=radius*radius

    def sign_rad(a,b,q):
        if b==0 or q==0:return (a>0)-(a<0)
        if b>0:
            if a>=0:return 1
            y=b*b*q-a*a
            return (y>0)-(y<0)
        if a<=0:return -1
        y=a*a-b*b*q
        return (y>0)-(y<0)

    # Independently validate every provided quadratic radical point candidate,
    # its global disc feasibility, and the complete objective extrema bounds.
    for row in latest['later_tasks']:
        i=int(row['module']);t=f(row['input']);direction=tuple(map(f,row['direction']))
        discs=[(tuple(map(f,v)),f(rad)) for v,rad in row['candidate_discs']]
        assert squared(direction)==1
        extrema=[]
        for cc in row['sharp_support']['algebraic_candidates']:
            b=tuple(map(f,cc['base']));a=tuple(map(f,cc['coefficient']));q=f(cc['radicand'])
            assert q>=0
            for center,rad in discs:
                d=sub(b,center)
                assert sign_rad(squared(d)+q*squared(a)-rad*rad,2*dot(d,a),q)<=0
            lower,upper=map(f,cc['objective_enclosure'])
            rmin=sqr_up(q,48)
            rmax=F(isqrt(q.numerator*2**96//q.denominator),2**48)
            const=dot(direction,b);slope=dot(direction,a)
            assert (lower,upper)==(const+slope*(rmax if slope>=0 else rmin),
                                   const+slope*(rmin if slope>=0 else rmax))
            extrema.append((lower,upper))
        assert extrema
        assert f(row['sharp_support']['certified_lower'])==min(lo for lo,hi in extrema)
        assert f(row['sharp_support']['certified_upper'])==max(hi for lo,hi in extrema)
        true=dot(sub(response(i,t),values[0]),direction)
        assert min(lo for lo,hi in extrema)<=true<=max(hi for lo,hi in extrema)
        assert f(row['joint_certified_width'])<=f(row['nearest_sample_outer_width'])
    for row in latest['coupled_future_differences']:
        i=int(row['module']);ta,tb=map(f,row['inputs']);d=tuple(map(f,row['direction']))
        actual=dot(sub(response(i,ta),response(i,tb)),d)
        lo,hi=map(f,row['common_source_coupled_interval'])
        oldlo,oldhi=map(f,row['independent_one_point_interval'])
        assert oldlo<=lo<=actual<=hi<=oldhi
        assert -L*abs(ta-tb)<=lo and hi<=L*abs(ta-tb)
    return len(obj['new_future_vector_queries']),len(latest['later_tasks']),len(latest['coupled_future_differences'])

def main():
    exact=independent_main()
    grouped=independent_group()
    temporal=independent_drift()
    vector_direct,vector_sharp,vector_coupled=independent_vector()
    results={'min_cut_cuts':2047,'exact_and_noisy_equilibria_verified':exact,
             'group_robust_equilibria_verified':grouped,
             'drifting_future_equilibria_verified':temporal,
             'vector_direct_queries_verified':vector_direct,
             'vector_sharp_projections_verified':vector_sharp,
             'vector_coupled_projections_verified':vector_coupled,
             'total_source_aware_task_certificates_checked':exact+grouped+temporal+vector_direct+vector_sharp+vector_coupled,
             'result':'PASS: checked independent path sums, cut counts, medians, worst-case task radii, source-reference residuals and fault-model boundaries.'}
    (ROOT/'independent_verification_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(results)

if __name__=='__main__':main()
