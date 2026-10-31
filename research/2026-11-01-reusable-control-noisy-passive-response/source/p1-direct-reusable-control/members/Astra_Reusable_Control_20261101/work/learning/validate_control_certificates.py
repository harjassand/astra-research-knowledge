#!/usr/bin/env python3
"""Independent exact checker using scalar reports, specifications and duals only.

No import of control_demo, no B/g, no known-source diagnostic file, no optimizer.
Run from any cwd. All certificate mathematics uses fractions.Fraction.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json, argparse

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'control'/'results'
OUT=Path(__file__).resolve().with_name('independent_control_validation.json')

# Public, supplied source/measurement/task specifications.
N=3; R=3; K=6; Q=F(4); DELTA=F(1); G=F(1)
ETA=F(1,10**6)
TASKS=[('all_controls',[F(0)]*N,[F(1)]*N,F(1)),
       ('price_change',[F(1,20),F(0),F(1,5)],[F(1)]*N,F(1)),
       ('actuator_2_unavailable',[F(0)]*N,[F(1),F(0),F(1)],F(1)),
       ('half_budget',[F(0)]*N,[F(1)]*N,F(1,2))]

def prod(xs):
    z=F(1)
    for x in xs:z*=x
    return z

def compositions(k,n):
    if n==1:
        yield (k,)
    else:
        for i in range(k+1):
            for rest in compositions(k-i,n-1):yield (i,)+rest

SS=[s for j in range(1,min(N,R)+1) for s in combinations(range(N),j)]
P=len(SS)
U=[Q**len(s) for s in SS]+[F(len(s)**2)*Q**(len(s)-1) for s in SS]

def mono(x):return [prod(x[i] for i in s) for s in SS]
def dmono(x,i):return [prod(x[j] for j in s if j!=i) if i in s else F(0) for s in SS]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))

def public_constraints(records):
    A=[]; b=[]
    nodes=set()
    for row in records:
        x=tuple(F(t) for t in row['x']); y=F(row['y']); eta=F(row['eta'])
        assert len(x)==N and min(x)>=0 and sum(x)<=DELTA
        assert eta==ETA
        assert x not in nodes; nodes.add(x)
        m=mono(x); lo=y-eta; hi=y+eta
        A.append([lo*t for t in m]+[-t for t in m]); b.append(-lo)
        A.append([-hi*t for t in m]+[t for t in m]); b.append(hi)
    expected={tuple(F(t,K) for t in aa[1:]) for aa in compositions(K,N+1)}
    assert nodes==expected
    assert len(nodes)==comb(N+K,K)==84
    return A,b

def validate_raw_transfer(raw,records):
    """Prove only raw-to-normalized interval transport, without source truth."""
    scale=F(raw['physical_gain_scale'])
    assert scale==F(1,4)
    observed_zero=F(raw['observed_zero_current'])
    zero_radius=F(raw['zero_current_radius'])
    assert zero_radius==F(1,8000000)
    raw_by_command={}
    for row in raw['records']:
        x=tuple(F(v) for v in row['x'])
        assert x not in raw_by_command
        raw_by_command[x]=(F(row['raw_current']),F(row['absolute_radius']))
    assert len(raw_by_command)==len(records)==84
    origin=(F(0),)*N
    assert origin in raw_by_command
    assert raw_by_command[origin]==(observed_zero,zero_radius)
    for row in records:
        x=tuple(F(v) for v in row['x']); y=F(row['y']);eta=F(row['eta'])
        measured,radius=raw_by_command[x]
        assert radius==F(1,8000000)
        assert y==(measured-observed_zero)/scale
        assert eta>=(radius+zero_radius)/scale
    assert F(next(row['y'] for row in records if tuple(F(v) for v in row['x'])==origin))==0
    return {'verdict':'PASS','settings':len(records),'baseline_is_one_of_settings':True,
            'physical_gain_scale':str(scale),'raw_current_radius':str(zero_radius),
            'normalized_radius':str((2*zero_radius)/scale),
            'shared_baseline_handling':'same measured zero in every exact difference; triangle bound retains arbitrary correlation',
            'scope':'Interval transport conditional on the supplied raw measurement radii; no unknown source truth was read.'}

def validate_one(cert,A,b,expected_x,expected_objective):
    assert cert['kind']=='linear_fractional_upper'
    x=tuple(F(t) for t in cert['x']); assert x==expected_x
    objective=[F(t) for t in cert['objective']]
    assert objective==expected_objective
    c0=F(cert['constant']); assert c0==0
    rows=[row+[-rhs] for row,rhs in zip(A,b)]
    for j,cap in enumerate(U):
        row=[F(0)]*(2*P+1);row[j]=F(1);row[-1]=-cap;rows.append(row)
    equation=mono(x)+[F(0)]*P+[F(1)]
    caps=U+[F(1)]
    lam=[F(0)]*len(rows);indices=set()
    for i,v in cert['dual_nonzero']:
        assert isinstance(i,int) and 0<=i<len(rows) and i not in indices
        indices.add(i);lam[i]=F(v);assert lam[i]>0
    nu=F(cert['equality_dual'])
    target=objective+[c0]
    residual=[target[j]-sum((lam[i]*rows[i][j] for i in range(len(rows))),F(0))
              -nu*equation[j] for j in range(2*P+1)]
    repair=sum((max(F(0),v)*cap for v,cap in zip(residual,caps)),F(0))
    bound=nu+repair
    assert repair==F(cert['residual_box_repair'])
    assert bound==F(cert['upper_bound'])
    # Neither solver_proposal nor any floating value is used.
    return bound,len(indices),repair

def main(data=DATA,output=OUT):
    data=Path(data);output=Path(output)
    records=json.loads((data/'scalar_records.json').read_text())
    certificates=json.loads((data/'dual_certificates.json').read_text())
    inputs=[str(data/'scalar_records.json'),str(data/'dual_certificates.json')]
    raw_transfer=None
    if (data/'raw_current_records.json').exists():
        raw_transfer=validate_raw_transfer(json.loads((data/'raw_current_records.json').read_text()),records)
        inputs.append(str(data/'raw_current_records.json'))
    A,b=public_constraints(records)
    assert len(certificates)==len(TASKS)*(2+2*N)==32
    verified=[];count=0;repairs=[]
    for task_no,(name,cost,cap,budget) in enumerate(TASKS):
        block=certificates[task_no*8:(task_no+1)*8]
        x=tuple(F(v) for v in block[0]['x'])
        assert min(x)>=0 and all(xi<=ci for xi,ci in zip(x,cap)) and sum(x)<=budget
        m=mono(x);value_objective=[F(0)]*P+m
        upper,_,repair=validate_one(block[0],A,b,x,value_objective);repairs.append(repair)
        negative_lower,_,repair=validate_one(block[1],A,b,x,[-v for v in value_objective]);repairs.append(repair)
        lo=max(F(0),-negative_lower);hi=min(F(1),upper)
        assert lo<=hi
        lows=[];highs=[]
        for i in range(N):
            dm=dmono(x,i)
            high,_,repair=validate_one(block[2+2*i],A,b,x,[-lo*v for v in dm]+dm);repairs.append(repair)
            negative_low,_,repair=validate_one(block[3+2*i],A,b,x,[hi*v for v in dm]+[-v for v in dm]);repairs.append(repair)
            lows.append(max(F(0),-negative_low));highs.append(max(F(0),high))
        assert all(l<=h for l,h in zip(lows,highs))
        remaining=budget;linear_max=F(0);greedy=[F(0)]*N
        for i in sorted(range(N),key=lambda i:highs[i]-cost[i],reverse=True):
            if highs[i]-cost[i]<=0:continue
            greedy[i]=min(cap[i],remaining);remaining-=greedy[i]
            linear_max+=(highs[i]-cost[i])*greedy[i]
        regret=max(F(0),linear_max-dot([l-c for l,c in zip(lows,cost)],x))
        verified.append({'task':name,'action':list(map(str,x)),
                         'response_interval':list(map(str,[lo,hi])),
                         'gradient_lower':list(map(str,lows)),
                         'gradient_upper':list(map(str,highs)),
                         'global_regret_exact':str(regret),
                         'global_regret_float_for_display':float(regret),
                         'requested_2e_minus_5_target_met':regret<F(1,50000),
                         'exact_linear_maximizer':list(map(str,greedy))})
        count+=8
    result={'verdict':'PASS','arithmetic':'exact Fraction',
            'inputs_used':inputs,
            'specifications':{'n':N,'r':R,'k':K,'q':str(Q),'delta':str(DELTA),'G':str(G),'eta':str(ETA)},
            'hidden_source_or_diagnostics_loaded':False,
            'raw_to_normalized_interval_transfer':raw_transfer,
            'scalar_settings':len(records),'dual_certificates_verified':count,
            'all_requested_2e_minus_5_targets_met':all(t['requested_2e_minus_5_target_met'] for t in verified),
            'maximum_exact_dual_residual_repair':str(max(repairs)),
            'certificate_scope':'Conditional on supplied fixed physical source and valid scalar intervals; no physical apparatus claim.',
            'tasks':verified}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='tasks'},indent=2))
    print(json.dumps([{'task':t['task'],'certified_regret':t['global_regret_float_for_display']} for t in verified],indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',type=Path,default=DATA)
    parser.add_argument('--output',type=Path,default=OUT)
    args=parser.parse_args()
    main(args.data,args.output)
