"""Exact finite coarse-detector fusion factory, independent small Fock replay.

The circuit and source model are mathematical inputs. The exact output and
cost are acquired computationally; no photon/memory/device is acquired.
"""
from fractions import Fraction as Q
from math import factorial,comb,lcm
from itertools import product,permutations
from pathlib import Path
from decimal import Decimal,localcontext
import json,time

HERE=Path(__file__).resolve().parent
OUT=HERE/'outputs';OUT.mkdir(exist_ok=True)

def mulpoly(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def law(n,p,det):
    p0,p1,p2=p;t=1-det
    A=p0+p1*t+p2*t*t
    B=det*(p1+2*p2*t)
    C=p2*det*det/2
    den=lcm(A.denominator,B.denominator,C.denominator)
    ai,bi,ci=[int(x*den) for x in [A,B,C]]
    coeff=[1]
    for _ in range(n):coeff=mulpoly(coeff,[ai,bi,ci])
    totalden=den**n*n**(2*n)
    terms=[c*factorial(k)*n**(2*n-k) for k,c in enumerate(coeff)]
    Znum=sum(terms)
    k1=sum(k*x for k,x in enumerate(terms))
    k2=sum(k*(k-1)*x for k,x in enumerate(terms))
    Z=Q(Znum,totalden)
    mean=Q(k1,Znum)/det
    factorial2=Q(k2,Znum)/(det*det)
    var=factorial2+mean-mean*mean
    assert 0<=mean<=2*n and var>=0
    return {'n':n,'A':A,'B':B,'C':C,'Z':Z,'mean':mean,'variance':var,
            'fano':var/mean if mean else Q(0),'terms':terms,'den':totalden}

def output_coefficients(state,det):
    # q(z)=sum_k T_k ((z-(1-det))/det)^k.
    terms=state['terms'];t=1-det
    out=[]
    for j in range(len(terms)):
        x=sum(Q(terms[k])*comb(k,j)*(-t)**(k-j)/det**k for k in range(j,len(terms)))
        out.append(x/state['den'])
    assert min(out)>=0 and sum(out)==state['Z']
    assert sum(j*x for j,x in enumerate(out))/state['Z']==state['mean']
    return out

def compositions(total,m):
    if m==1:yield (total,);return
    for x in range(total+1):
        for rest in compositions(total-x,m-1):yield (x,)+rest

def permanent(A):
    if not A:return Q(1)
    ans=Q(0)
    for perm in permutations(range(len(A))):
        v=Q(1)
        for i,j in enumerate(perm):v*=A[i][j]
        ans+=v
    return ans

def direct_small_fock(U,p,det):
    # Literal Fock amplitudes, not a permanent-of-diagonal-plus-rank-one import.
    n=len(U);out=[Q(0)]*(2*n+1)
    for occin in product(range(3),repeat=n):
        pin=Q(1)
        for x in occin:pin*=p[x]
        if not pin:continue
        total=sum(occin);cols=[j for j,x in enumerate(occin) for _ in range(x)]
        indeg=1
        for x in occin:indeg*=factorial(x)
        for occout in compositions(total,n):
            rows=[j for j,x in enumerate(occout) for _ in range(x)]
            M=[[U[i][j] for j in cols] for i in rows]
            per=permanent(M);outdeg=1
            for x in occout:outdeg*=factorial(x)
            prob=per*per/Q(indeg*outdeg)
            out[occout[0]]+=pin*prob*(1-det)**sum(occout[1:])
    return out

def asfloat(x):return float(x)
def exact(x):return str(x)
def log10q(q):
    with localcontext() as ctx:
        ctx.prec=35
        return float(Decimal(q.numerator).log10()-Decimal(q.denominator).log10())

start=time.perf_counter()
p=(Q(99,500),Q(4,5),Q(1,500));det=Q(19,20)
assert sum(p)==1
replays=[]
# Balanced two-mode beamsplitter: numerator matrix divided by sqrt(2).
# Probability denominator is 2**total photon count; represent it directly.
def direct_two(p,det):
    U=[[Q(1),Q(1)],[Q(1),Q(-1)]]
    out=[Q(0)]*5
    for occin in product(range(3),repeat=2):
        pin=p[occin[0]]*p[occin[1]];N=sum(occin)
        cols=[j for j,x in enumerate(occin) for _ in range(x)]
        for occout in compositions(N,2):
            rows=[j for j,x in enumerate(occout) for _ in range(x)]
            per=permanent([[U[i][j] for j in cols] for i in rows])
            deg=2**N
            for x in occin+occout:deg*=factorial(x)
            out[occout[0]]+=pin*per*per/Q(deg)*(1-det)**occout[1]
    return out

for n,src in [(2,p),(4,(Q(1,5),Q(4,5),Q(0)))]:
    state=law(n,src,det);formula=output_coefficients(state,det)
    if n==2:direct=direct_two(src,det)
    else:
        U=[[Q(s,2) for s in row] for row in [[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]]
        direct=direct_small_fock(U,src,det)
    assert direct==formula
    replays.append({'n':n,'source':[exact(q) for q in src],
                    'literal_Fock_output_equals_generating_function':True,
                    'unnormalized_probabilities':[exact(q) for q in direct]})

rows=[];states={};cost={1:Q(1)}
fusion_count={1:Q(0)}
# Sequential preparation of child 1 then child 2, retaining child 1. One
# source clock and one fusion clock are each a native unit in this table.
elapsed_clock={1:Q(1)};photon_memory_time={1:Q(0)}
for n in [1,2,4,8,16,32,64,128,256,512]:
    st=law(n,p,det);states[n]=st
    if n>1:
        branch=st['Z']/states[n//2]['Z']**2
        assert 0<branch<=1
        cost[n]=2*cost[n//2]/branch
        fusion_count[n]=(2*fusion_count[n//2]+1)/branch
        elapsed_clock[n]=(2*elapsed_clock[n//2]+1)/branch
        mu=states[n//2]['mean']
        photon_memory_time[n]=(2*photon_memory_time[n//2]+mu*elapsed_clock[n//2]+2*mu)/branch
    else:branch=Q(1)
    row={'n':n,'success_log10':log10q(st['Z']),
         'mean':asfloat(st['mean']),'mean_over_n':asfloat(st['mean']/n),
         'fano':asfloat(st['fano']),'last_binary_fusion_probability':asfloat(branch),
         'parallel_restart_source_cost_log10':log10q(Q(n)/st['Z']),
         'ideal_retained_binary_source_cost_log10':log10q(cost[n]),
         'expected_fusion_operations_log10':log10q(fusion_count[n]) if n>1 else None,
         'expected_wall_clock_native_log10':log10q(elapsed_clock[n]),
         'expected_photon_memory_time_native_log10':log10q(photon_memory_time[n]) if n>1 else None,
         'loss_rate_sufficient_for_0p01_trace_error_per_native_clock':float(Q(1,100)/photon_memory_time[n]) if n>1 else None}
    if n<=16:
        qc=output_coefficients(st,det)
        row['exact_success']=exact(st['Z'])
        row['normalized_output_probabilities']=[exact(x/st['Z']) for x in qc]
    rows.append(row)

A,B,C=[states[1][k] for k in ['A','B','C']]
assert B>A and B*B>2*A*C
def rootpoly(x):return C*x*x+(B-2*C)*x+(A-B)
lo,hi=Q(17,25),Q(69,100)
assert rootpoly(lo)<0<rootpoly(hi)
vupper=B/(B-2*C)
Fupper=vupper/(det*lo)-(2-det)/det
Flower=1/(det*hi)-(2-det)/det
assert Flower>Q(21,50) and Fupper<Q(9,20)
with localcontext() as ctx:
    ctx.prec=50
    dd=lambda x:Decimal(x.numerator)/Decimal(x.denominator)
    ad,bd,cd=map(dd,[A,B,C])
    # Stable quadratic root avoiding cancellation.
    xstar=2*(bd-ad)/((bd-2*cd)+((bd-2*cd)**2+4*cd*(bd-ad)).sqrt())
    h=ad+bd*xstar+cd*xstar*xstar
    v=1/(1-2*cd/h)
    ddet=dd(det)
    asym={'A':exact(A),'B':exact(B),'C':exact(C),
          'strict_log_concavity_exact':True,'supercritical_exact':True,
          'xstar_exact_interval':[exact(lo),exact(hi)],
          'mean_over_n_exact_interval':['68/95','69/95'],
          'asymptotic_fano_exact_interval':['21/50','9/20'],
          'xstar_decimal':str(xstar),'mean_over_n_decimal':str(xstar/ddet),
          'fano_decimal':str(v/(ddet*xstar)-(2-ddet)/ddet),
          'success_exponential_rate_decimal':str(xstar-h.ln())}

result={'status':'EXACT_FINITE_FACTORY_CONSTRUCTION; no independent audit, physical qualification or priority clearance',
        'source_probability_model':[exact(x) for x in p],'detector_efficiency':exact(det),
        'detector_type':'on/off; condition only on no-click; no photon-number resolution in factory',
        'exact_small_operator_replays':replays,'asymptotic_certificate':asym,'finite_factory':rows,
        'memory_scope':'lossless retained-child memory assumed for recursive source cost; no acquired loss/lifetime/latency/throughput',
        'ordinary_comparator':'existing zero-count Fock fusion with ideal retention is the same circuit; number-resolved recycling is stronger and prior',
        'useful_computational_resource':'UNKNOWN; mean/Fano and exact finite cutoff do not certify a useful approximate stellar resource',
        'elapsed_seconds':time.perf_counter()-start}
(OUT/'BUCKET_FACTORY_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'exact_small_replays':len(replays),
                  'asymptotic_certificate':asym,'finite_factory':[
                      {k:v for k,v in rr.items() if not k.startswith('normalized_') and k!='exact_success'} for rr in rows[3:]],
                  'elapsed_seconds':result['elapsed_seconds']},indent=2))
