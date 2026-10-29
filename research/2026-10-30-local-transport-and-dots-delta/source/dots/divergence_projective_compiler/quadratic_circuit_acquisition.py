"""Raw-circuit acquisition in a small quadratic dictionary, with honest PIT.

No chart/triangular order enters acquire(). A quadratic trial is a SEARCH BUDGET,
not a supplied promise: every interpolation is checked against raw dynamics.
Fresh system-random integer points are used; admission remains Monte Carlo.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,math,secrets,time
import sympy as s
from strong_decoder import DAG,strong_decoder,summary


def family(n):
    assert n%2==0
    c=DAG(n); x=c.variables
    F=[c.add(x[i],c.mul(x[i+1],x[i+1])) if i<n-1 else x[i] for i in range(n)]
    cf=c.zero
    for i in range(0,n,2):cf=c.add(cf,F[i])
    BF=[]
    for j in range(n//2):BF += [c.scale(-(j+1),F[2*j+1]),c.scale(j+1,F[2*j])]
    g=[c.add(b,c.scale(-1,c.mul(cf,y))) for b,y in zip(BF,F)]
    raw=list(g);term=list(g)
    for _ in range(n-1):
        term=[c.scale(-2,c.mul(x[i+1],term[i+1])) for i in range(n-1)]+[c.zero]
        raw=[c.add(a,b) for a,b in zip(raw,term)]
    return c,raw


def formal_degree(c,roots):
    deg=[]
    for op,*a in c.nodes:
        if op=='var':v=1
        elif op=='const':v=0
        elif op=='add':v=max(deg[a[0]],deg[a[1]])
        else:v=deg[a[0]]+deg[a[1]]
        deg.append(v)
    return max(deg[r] for r in roots)


def monomials(n):
    return [()]+[(i,) for i in range(n)]+[(i,j) for i in range(n) for j in range(i,n)]


def value_grad(p,mons,x):
    v=Q(0);g=[Q(0)]*len(x)
    for a,b in zip(mons,p):
        if not b:continue
        if not a:v+=b
        elif len(a)==1:v+=b*x[a[0]];g[a[0]]+=b
        else:
            i,j=a;v+=b*x[i]*x[j];g[i]+=b*x[j];g[j]+=b*x[i]
    return v,g


def acquire(c,raw,verification_points=3,sample_set_size=2**32):
    n=c.n;mons=monomials(n);idx={a:i for i,a in enumerate(mons)};d=formal_degree(c,raw)
    start=time.perf_counter();q=c.manufacture_q(raw);roots=raw+[q]
    zero=[Q(0)]*n;points=[zero]
    for i in range(n):
        a=zero.copy();a[i]=1;points.append(a)
        a=zero.copy();a[i]=-1;points.append(a)
    for i in range(n):
        for j in range(i+1,n):
            a=zero.copy();a[i]=a[j]=1;points.append(a)
    peak=1;train=[]
    for a in points:
        vals,bits=c.evaluate(roots,a);peak=max(peak,bits);train.append(vals)
    basis=[[Q(1)]+[Q(0)]*(len(mons)-1)];pivots=[0];rows=[];attempts=0;peakcoeff=1
    def Tv(p,a,vals):
        v,g=value_grad(p,mons,a)
        return vals[-1]*v+sum((f*b for f,b in zip(vals[:-1],g)),Q(0))
    k=0
    while k<len(basis):
        p=basis[k];v=[Tv(p,a,z) for a,z in zip(points,train)];t=[Q(0)]*len(mons);t[0]=v[0]
        for i in range(n):
            vp,vm=v[1+2*i:3+2*i]
            t[idx[(i,)]]=(vp-vm)/2;t[idx[(i,i)]]=(vp+vm)/2-v[0]
        pos=1+2*n
        for i in range(n):
            for j in range(i+1,n):
                t[idx[(i,j)]]=v[pos]-t[0]-t[idx[(i,)]]-t[idx[(j,)]]-t[idx[(i,i)]]-t[idx[(j,j)]];pos+=1
        attempts+=1
        for _ in range(verification_points):
            a=[Q(secrets.randbelow(sample_set_size)) for _ in range(n)]
            vals,bits=c.evaluate(roots,a);peak=max(peak,bits)
            if Tv(p,a,vals)!=value_grad(t,mons,a)[0]:
                return {'status':'NOT_ACQUIRED_QUADRATIC_RESIDUAL_FAILED','step':k}
        row={}
        for j,(b,pivot) in enumerate(zip(basis,pivots)):
            a=t[pivot]
            if a:row[j]=a;t=[u-a*v for u,v in zip(t,b)]
        if any(t):
            pivot=next(i for i,a in enumerate(t) if a);a=t[pivot];row[len(basis)]=a
            basis.append([v/a for v in t]);pivots.append(pivot)
            if len(basis)>n+1:return {'status':'NOT_ACQUIRED_RANK_EXCEEDED'}
        rows.append(row);k+=1
        peakcoeff=max(peakcoeff,*[max(abs(a.numerator).bit_length(),a.denominator.bit_length()) for p in basis for a in p],
                      *[max(abs(a.numerator).bit_length(),a.denominator.bit_length()) for row in rows for a in row.values()])
    if len(basis)!=n+1:return {'status':'NOT_ACQUIRED_RANK_DEFICIENT','rank':len(basis)}
    x=s.symbols('x0:'+str(n))
    poly=lambda p:sum((s.Rational(a.numerator,a.denominator)*s.prod(x[i] for i in m) for a,m in zip(p,mons)),s.Integer(0))
    A=s.Matrix([[s.Rational(row.get(j,0)) for j in range(n+1)] for row in rows])
    chart=s.Matrix([poly(p) for p in basis[1:]])
    return {'status':'MONTE_CARLO_RAW_CHART','chart':chart,'matrix':A,'variables':x,
        'dimension':n+1,'raw_formal_degree_bound':d,'residual_degree_bound':d+1,
        'quadratic_dictionary_size':len(mons),'training_points':len(points),
        'verification_points_per_residual':verification_points,'sample_set_size':sample_set_size,
        'adaptive_residuals_tested':attempts,
        'false_acceptance_union_bound':str(attempts*Q(d+1,sample_set_size)**verification_points),
        'peak_raw_circuit_evaluation_bits':peak,'peak_basis_generator_coefficient_bits':peakcoeff,
        'raw_plus_divergence_total_allocated_nodes':len(c.nodes),'acquisition_seconds':time.perf_counter()-start}


def main():
    out=[]
    for n in [2,4,8,16]:
        t=time.perf_counter();c,raw=family(n);construction=time.perf_counter()-t
        raw_serialized={'n':n,'nodes':[[op]+([str(a[0])] if op=='const' else a) for op,*a in c.nodes], 'roots':raw}
        raw_nodes=len(c.nodes);got=acquire(c,raw);assert got['status']=='MONTE_CARLO_RAW_CHART',got
        x=got['variables'];dec=strong_decoder(got['chart'],x)
        assert dec['status']=='EXACT_FLAG_CERTIFIED_INVERSE_DAG'
        # Independent test-only constructor equality; NOT the admission rule.
        expected=s.Matrix([x[i]+(x[i+1]**2 if i<n-1 else 0) for i in range(n)])
        assert all(s.expand(v)==0 for v in dec['normalized_chart']-expected)
        R=s.eye(n+1);R[1:,0]=dec['offset'];R[1:,1:]=dec['normalizer']
        M=R.inv()*got['matrix']*R
        target=s.zeros(n+1)
        for j in range(n//2):
            target[0,1+2*j]=1;target[1+2*j,2+2*j]=-(j+1);target[2+2*j,1+2*j]=j+1
        assert M==target
        rec={k:v for k,v in got.items() if k not in ['chart','matrix','variables']}
        rec.update({'decoder':summary(dec),'raw_circuit_nodes':raw_nodes,
                    'constructor_seconds_excluded':construction,'normalized_generator_exactly_rotation_blocks':True,
                    'normalized_chart_matches_test_constructor':True,'chart':[str(v) for v in got['chart']],
                    'matrix':[[str(v) for v in row] for row in got['matrix'].tolist()],
                    'normalized_matrix':[[str(v) for v in row] for row in M.tolist()],
                    'raw_circuit':raw_serialized})
        # Deterministic coefficient replay of the raw input, separately charged.
        if n<=4:
            t=time.perf_counter();rawpoly=c.expand(raw,x)
            q=-sum(s.diff(rawpoly[i],x[i]) for i in range(n))/(n+1)
            phi=s.Matrix([1]+list(got['chart']))
            assert all(s.expand(v)==0 for v in phi.jacobian(x)*rawpoly+q*phi-got['matrix']*phi)
            rec['independent_coefficient_replay']='ALL_MODULE_IDENTITIES_PASS';rec['coefficient_replay_seconds']=time.perf_counter()-t
        else:rec['independent_coefficient_replay']='NOT_RUN; closure admission remains Monte Carlo'
        out.append(rec);print({k:v for k,v in rec.items() if k not in ['chart','matrix','normalized_matrix','raw_circuit']},flush=True)
    root=Path(__file__).parent
    (root/'quadratic_circuit_results.json').write_text(json.dumps({'runs':out,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))


if __name__=='__main__':main()
