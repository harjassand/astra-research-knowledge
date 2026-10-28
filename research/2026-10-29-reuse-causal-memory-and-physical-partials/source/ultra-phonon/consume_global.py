"""Independent formula consumer: rational Bloch evaluations + interpolation.
No producer, chart expansion, power-to-Bernstein or split code is imported.
This is implementation separation, not an independent scientific audit.
"""
from pathlib import Path
from fractions import Fraction as F
import gzip,hashlib,itertools,json,math,time
import numpy as np
import sympy as sy
BASE=Path(__file__).parent

def multiply(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]

def power(z,n):
    if n<0:z=(z[0],-z[1]);n=-n
    a=(F(1),F(0))
    for _ in range(n):a=multiply(a,z)
    return a

def interpolating_inverse(n):
    V=sy.Matrix([[sy.binomial(n,j)*sy.Rational(i,n)**j*(1-sy.Rational(i,n))**(n-j) for j in range(n+1)] for i in range(n+1)])
    return np.array([[F(int(v.p),int(v.q)) for v in row] for row in V.inv().tolist()],dtype=object)

def root_coefficients(name,C,den):
    acoustic=name.startswith('acoustic');degrees=(12,4,4) if acoustic else (4,4,4)
    shape=tuple(n+1 for n in degrees)+(6,6);out=[np.empty(shape,dtype=object) for _ in range(2)]
    T=np.vstack([np.eye(3,dtype=int),np.eye(3,dtype=int)]).astype(object)
    Q=np.vstack([np.eye(3,dtype=int),-np.eye(3,dtype=int)]).astype(object);Z=np.hstack([T,Q])
    D0=sum(C.values(),np.zeros((6,6),dtype=object))
    for idx in itertools.product(*(range(n+1) for n in degrees)):
        t=[F(i,n) for i,n in zip(idx,degrees)]
        if acoustic:
            r=t[0];u=2*t[1]-1;v=2*t[2]-1;x=[r,r*u,r*v]
        else:x=[2*z-1 for z in t]
        if acoustic and not r:
            w=[F(1),u,v];M1=np.zeros((6,6),dtype=object);M2=M1.copy()
            for R,A in C.items():
                dot=sum((a*b for a,b in zip(R,w)),F(0));M1+=dot*A;M2+=dot*dot*A
            real=np.zeros((6,6),dtype=object);imag=real.copy()
            real[:3,:3]=-2*(T.T@M2@T);real[3:,3:]=Q.T@D0@Q
            imag[:3,3:]=2*(T.T@M1@Q);imag[3:,:3]=-imag[:3,3:].T
            for part,A in enumerate([real,imag]):out[part][idx]=np.array([[F(a,den) for a in row] for row in A],dtype=object)
            continue
        z=[((1-a*a)/(1+a*a),2*a/(1+a*a)) for a in x]
        if not acoustic:
            for j,sign in enumerate(name[-3:]):
                if sign=='1':z[j]=(-z[j][0],-z[j][1])
        phases=[]
        for R in C:
            phase=(F(1),F(0))
            for a,b in zip(z,R):phase=multiply(phase,power(a,b))
            phases.append(phase)
        pd=math.lcm(*(a.denominator for p in phases for a in p));real=np.zeros((6,6),dtype=object);imag=real.copy()
        for A,(a,b) in zip(C.values(),phases):real+=int(a*pd)*A;imag+=int(b*pd)*A
        scalar=math.prod((1+a*a)**2 for a in x)/F(pd*den)
        if acoustic:real=Z.T@real@Z;imag=Z.T@imag@Z
        for part,A in enumerate([real,imag]):
            B=np.empty((6,6),dtype=object)
            for i,j in itertools.product(range(6),repeat=2):B[i,j]=scalar*A[i,j]/(r**(int(i<3)+int(j<3)) if acoustic else 1)
            out[part][idx]=B
    for axis,n in enumerate(degrees):
        U=interpolating_inverse(n)
        out=[np.moveaxis(np.tensordot(U,A,axes=(1,axis)),0,axis) for A in out]
    common=math.lcm(*(a.denominator for A in out for a in A.flat))
    out=[np.array([int(a*common) for a in A.flat],dtype=object).reshape(A.shape) for A in out]
    assert np.array_equal(out[0],np.swapaxes(out[0],-1,-2)) and np.array_equal(out[1],-np.swapaxes(out[1],-1,-2))
    return *out,common

def bisect(re,im,axis):
    n=re.shape[axis]-1;answer=[]
    for A in [re,im]:
        work=np.moveaxis(A,axis,0);L=np.empty_like(work);R=np.empty_like(work)
        L[0]=work[0]*(1<<n);R[n]=work[n]*(1<<n)
        for level in range(1,n+1):
            work=work[:-1]+work[1:]
            L[level]=work[0]*(1<<(n-level));R[n-level]=work[-1]*(1<<(n-level))
        answer.append((np.moveaxis(L,0,axis),np.moveaxis(R,0,axis)))
    return (answer[0][0],answer[1][0]),(answer[0][1],answer[1][1]),1<<n

def main():
    start=time.perf_counter();data=json.loads((BASE/'MODEL.json').read_text());cert=json.loads((BASE/'GLOBAL_CERTIFICATE.json').read_text())
    assert hashlib.sha256((BASE/'MODEL.json').read_bytes()).hexdigest()==cert['model_sha256']
    transport=json.loads((BASE/'source_cache/TRANSPORT_RECEIPT.json').read_text());entry=json.loads((BASE/'source_cache/SOURCE_ENTRY.json').read_text())
    for source,item in zip(entry['sources'],transport['files']):
        raw=(BASE/'source_cache'/item['authentic_original']).read_bytes();view=(BASE/'source_cache'/item['numerical_view']).read_bytes()
        assert view==raw+b'\n' and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==source['blob_sha']
    for name,h in data['source_sha256'].items():assert hashlib.sha256((BASE/'source_cache'/name).read_bytes()).hexdigest()==h
    rows=data['coefficients'];vals=[F(v) for row in rows for a in row['matrix'] for v in a]
    den=math.lcm(*(x.denominator for x in vals));C={tuple(row['R']):np.array([[int(F(v)*den) for v in a] for a in row['matrix']],dtype=object) for row in rows}
    assert tuple(max(abs(R[j]) for R in C) for j in range(3))==(2,2,2)
    for R,A in C.items():assert np.array_equal(A,C[tuple(-x for x in R)].T)
    T=np.vstack([np.eye(3,dtype=int),np.eye(3,dtype=int)]).astype(object);D0=sum(C.values(),np.zeros((6,6),dtype=object))
    assert not np.any(D0@T)
    for j in range(3):assert not np.any(T.T@sum((R[j]*A for R,A in C.items()),np.zeros((6,6),dtype=object))@T)
    for perm in itertools.permutations(range(3)):
        for R,A in C.items():
            RR=tuple(R[j] for j in perm);indices=[*perm,*(j+3 for j in perm)]
            assert np.array_equal(C[RR],A[np.ix_(indices,indices)])
    leaves=json.loads(gzip.open(BASE/'LEAVES.json.gz','rt').read());stats=[];minimum=None;total=0
    for name in ['acoustic0+1','regular001','regular011','regular111']:
        begin=time.perf_counter();group={v['path']:v for v in leaves if v['chart']==name}
        nodes={k[:i] for k in group for i in range(len(k)+1)};assert '' in nodes
        for k in nodes:
            if k in group:assert k+'0' not in nodes and k+'1' not in nodes
            else:assert k+'0' in nodes and k+'1' in nodes
        re,im,d=root_coefficients(name,C,den);interpolation_seconds=time.perf_counter()-begin
        pending=[('',re,im,d)];count=0
        while pending:
            path,re,im,d=pending.pop()
            if path in group:
                leaf=group[path];sr=np.array(leaf['whitener_real'],dtype=object);si=np.array(leaf['whitener_imag'],dtype=object)
                a=re@sr-im@si;b=re@si+im@sr;rr=sr.T@a+si.T@b;ii=sr.T@b-si.T@a
                assert np.array_equal(rr,np.swapaxes(rr,-1,-2)) and np.array_equal(ii,-np.swapaxes(ii,-1,-2))
                diagonal=np.diagonal(rr,axis1=-2,axis2=-1)
                margin=int(np.min(diagonal-abs(rr).sum(axis=-1)-abs(ii).sum(axis=-1)+abs(diagonal)))
                assert margin>0
                assert F(margin,d)==F(int(leaf['integer_margin']),int(leaf['coefficient_denominator']))
                norm=sum(int(v)**2 for v in sr.flat)+sum(int(v)**2 for v in si.flat)
                lower=F(margin,d*norm);assert lower==F(leaf['matrix_lower_numerator'])/F(leaf['matrix_lower_denominator'])
                minimum=lower if minimum is None else min(minimum,lower);count+=1;continue
            left,right,factor=bisect(re,im,[1,2,0][len(path)%3]);pending.extend([(path+'1',*right,d*factor),(path+'0',*left,d*factor)])
        assert count==len(group);total+=count
        st=dict(chart=name,leaves=count,exact_rational_interpolation_seconds=interpolation_seconds,total_seconds=time.perf_counter()-begin)
        stats.append(st);print(json.dumps(st),flush=True)
    assert total==len(leaves)==cert['leaves'] and minimum==F(cert['common_chart_matrix_lower_bound'])
    out=dict(status='PASS_INDEPENDENT_RATIONAL_INTERPOLATION_AND_EXACT_WHOLE_DOMAIN_CONSUMER',
        model_sha256=cert['model_sha256'],consumer_imports_producer_code=False,source_git_blobs_verified=True,
        structural_constraints_exact=True,symmetry_covariance_exact=True,all_four_prefix_trees_complete=True,
        root_Bernstein_coefficients_rebuilt_by_rational_Bloch_grid_interpolation=True,
        subdivision_rebuilt_by_repeated_integer_averages=True,all_leaf_congruences_exact=True,
        leaves=total,common_chart_lower_bound=str(minimum),charts=stats,seconds=time.perf_counter()-start,
        numerical_model_scope_only=True,independent_scientific_review='NOT_PERFORMED_BY_THIS_SAME_WORKER_CONSUMER')
    (BASE/'CONSUMER_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)

if __name__=='__main__':main()
