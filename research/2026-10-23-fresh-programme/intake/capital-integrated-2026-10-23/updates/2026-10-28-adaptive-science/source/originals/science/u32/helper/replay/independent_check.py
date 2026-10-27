"""Independent exact audit of the copied count certificate; no plant import."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from decimal import Decimal, localcontext
import json

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'counts.json').read_text())
reference=json.loads((ROOT/'reference_rational_certificate.json').read_text())
tables={tuple(t['actions']):t for t in data['tables']}
assert len(tables)==len(data['tables'])==7
assert data['preparations']==[[],[0]] and data['tests']==[[],[[1,1]]]
assert data['rank_upper_bound']==2
assert data['actions']==[0,1] and data['outcomes']==[0,1]
for actions,table in tables.items():
    assert table['shots']==1000000
    assert set(table['counts'])=={''.join(map(str,b)) for b in product([0,1],repeat=len(actions))}
    assert all(isinstance(c,int) and c>=0 for c in table['counts'].values())
    assert sum(table['counts'].values())==table['shots']
assert sum(t['shots'] for t in tables.values())==data['resets']==7000000
assert sum(len(a)*t['shots'] for a,t in tables.items())==data['native_interventions']==14000000

events=[]
def event(actions,requirements,label):
    actions=tuple(actions); requirements=dict(requirements)
    assert all(0<=i<len(actions) and o in [0,1] for i,o in requirements.items())
    table=tables[actions]
    numerator=sum(c for bits,c in table['counts'].items()
                  if all(int(bits[i])==o for i,o in requirements.items()))
    key=(actions,tuple(sorted(requirements.items())))
    events.append({'slot':label,'actions':list(actions),'requirements':requirements,
                   'successes':numerator,'shots':table['shots'],'key':key})
    return F(numerator,table['shots'])

preps=[tuple(p) for p in data['preparations']]
H=[[F(1),F(1)], [event(p+(1,),{len(p):1},f'H[1,{j}]') for j,p in enumerate(preps)]]
Hz={}
for a,o in product(data['actions'],data['outcomes']):
    Hz[a,o]=[[event(p+(a,),{len(p):o},f'Hz[{a},{o}][0,{j}]') for j,p in enumerate(preps)],
              [event(p+(a,1),{len(p):o,len(p)+1:1},f'Hz[{a},{o}][1,{j}]') for j,p in enumerate(preps)]]
assert len(events)==data['confidence_pool_K']==18
distinct_events=len({e['key'] for e in events})
assert distinct_events==16  # Eighteen slots include two literal event reuses; union bound remains valid.
assert H==[[F(1),F(1)],[F(250175,1000000),F(675085,1000000)]]
w=F(*data['hoeffding_width_rational'])
assert w==F(21,10000)
exponent=2*1000000*w*w
assert exponent==F(441,50)
# Rigorous exponential sandwich from a positive Taylor series and its ratio tail.
term=F(1); exp_lower=term
for k in range(1,81):
    term*=exponent/k; exp_lower+=term
next_term=term*exponent/81
exp_upper=exp_lower+next_term/(1-exponent/82)
failure_lower=F(36)/exp_upper; failure_upper=F(36)/exp_lower
assert failure_upper<F(1,100)

def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
             for j in range(len(b[0]))] for i in range(len(a))]
def inv(a):
    d=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    assert d
    return [[a[1][1]/d,-a[0][1]/d],[-a[1][0]/d,a[0][0]/d]]
def absolute(a): return [[abs(x) for x in row] for row in a]
def plus(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def minus(a,b): return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def within(a,b): return all(abs(a[i][j])<=b[i][j] for i in range(2) for j in range(2))
def rf(value): return F(value['rational'])

S=[[F(5,4),F(-1,4)],[F(-1,4),F(5,4)]]
assert [sum(S[i][j] for i in range(2)) for j in range(2)]==[1,1]
I=[[F(1),F(0)],[F(0),F(1)]]
DH=[[F(0),F(0)],[w,w]]
DZ=[[w,w],[w,w]]
V=mm(H,S); U=inv(V); DV=mm(DH,absolute(S)); A=mm(absolute(U),DV)
nu=max(sum(row) for row in A)
assert nu==F(420,42491)<1
M=mm(inv(minus(I,A)),absolute(U))
assert all(x>=0 for row in M for x in row)
assert mm(minus(I,A),M)==absolute(U)
initial=mm(inv(S),[[F(1)],[F(0)]])
assert initial==[[F(5,6)],[F(1,6)]]
raw={z:mm(mm(U,hz),S) for z,hz in Hz.items()}
errors={z:mm(M,plus(mm(DZ,absolute(S)),mm(DV,absolute(raw[z])))) for z in raw}
margin=min(raw[z][i][j]-errors[z][i][j] for z in raw for i in range(2) for j in range(2))
assert margin==F(30002740030003,1430111088800000)>0
for a,j in product([0,1],repeat=2):
    assert sum(raw[a,o][i][j] for o in [0,1] for i in [0,1])==1

# Independent box-simplex maximum: enumerate its vertices, not subsets.
local=[]; t=F(0)
for a,j in product([0,1],repeat=2):
    p=[raw[a,o][i][j] for o in [0,1] for i in [0,1]]
    e=[errors[a,o][i][j] for o in [0,1] for i in [0,1]]
    low=[max(F(0),p0-e0) for p0,e0 in zip(p,e)]
    high=[min(F(1),p0+e0) for p0,e0 in zip(p,e)]
    vertices=set()
    for free in range(4):
        others=[i for i in range(4) if i!=free]
        for mask in product([0,1],repeat=3):
            q=[F(0)]*4
            for i,k in zip(others,mask): q[i]=[low[i],high[i]][k]
            q[free]=1-sum(q)
            if low[free]<=q[free]<=high[free]: vertices.add(tuple(q))
    assert vertices
    vertex_max=max(sum(abs(x-y) for x,y in zip(q,p))/2 for q in vertices)
    subset_max=max(min(sum(high[i] for i in range(4) if mask[i]),
                       1-sum(low[i] for i in range(4) if not mask[i]))
                   -sum(p[i] for i in range(4) if mask[i])
                   for mask in product([0,1],repeat=4))
    assert vertex_max==subset_max
    t=max(t,vertex_max)
    local.append({'action':a,'column':j,'TV':str(vertex_max),'vertices':len(vertices)})
assert t==F(4121523,210355000)
selected=reference['selected']
assert rf(selected['s'])==F(1,4) and rf(selected['margin'])==margin
assert rf(selected['nu'])==nu and rf(selected['local_tv'])==t
for z in raw:
    assert [[rf(x) for x in row] for row in selected['W'][str(z)]]==raw[z]
    assert [[rf(x) for x in row] for row in selected['entry_errors'][str(z)]]==errors[z]
delta=F(2,5); gamma=1-delta
one=gamma*t/(delta+gamma*t); two=1-(delta/(delta+gamma*t))**2
assert one==rf(selected['one_macro_tv'])==F(12364569,433074569)
assert two==rf(selected['two_macro_tv'])==F(10556678214535761,187553582314535761)

# Corner checks challenge the interval algebra; proof still covers the continuum by Neumann's inequality.
corner_checks=0
for hs in product([-1,1],repeat=2):
    HT=[[F(1),F(1)],[H[1][j]+hs[j]*w for j in range(2)]]
    VT=mm(HT,S); UT=inv(VT)
    assert within(UT,M)
    for z in raw:
        for zs in product([-1,1],repeat=4):
            HZT=[[Hz[z][i][j]+zs[2*i+j]*w for j in range(2)] for i in range(2)]
            WT=mm(mm(UT,HZT),S)
            difference=minus(raw[z],WT)
            residual=plus(mm(minus(Hz[z],HZT),S),mm(minus(VT,V),raw[z]))
            assert mm(VT,difference)==residual
            assert within(difference,errors[z])
            assert all(x>0 for row in WT for x in row)
            corner_checks+=1
assert corner_checks==256

def dec(x):
    with localcontext() as context:
        context.prec=35
        return str(Decimal(x.numerator)/Decimal(x.denominator))
for e in events: e.pop('key')
result={'status':'PASS','arithmetic':'exact fractions.Fraction; decimal display only',
        'input_scope':'Copied authorized count/theorem/certificate files; no plant',
        'replayed_certificate_byte_identical':True,
        'confidence_slots':len(events),'distinct_extracted_events':distinct_events,
        'resets':7000000,'native_interventions':14000000,
        'failure_bound_exact':'36 exp(-441/50)',
        'failure_bound_decimal_interval':[dec(failure_lower),dec(failure_upper)],
        'true_H_determinant_interval':[str(H[1][1]-H[1][0]-2*w),str(H[1][1]-H[1][0]+2*w)],
        'nu':str(nu),'positive_margin':str(margin),'local_TV':str(t),
        'one_macro_TV':str(one),'two_macro_TV':str(two),
        'independent_box_simplex_vertex_checks':local,
        'exact_inverse_residual_corner_checks':corner_checks,
        'legal_event_manifest':events,
        'limits':['Independence, repeatability, CP stationarity and architectural rank are supplied assumptions, not proved by counts.',
                  'Corner checks supplement the algebraic continuum proof; they are not its substitute.',
                  'No private-plant scoring or same-count old bound independently verified.']}
(ROOT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','confidence_slots','distinct_extracted_events','nu','positive_margin','local_TV','one_macro_TV','two_macro_TV','exact_inverse_residual_corner_checks']},indent=2))
