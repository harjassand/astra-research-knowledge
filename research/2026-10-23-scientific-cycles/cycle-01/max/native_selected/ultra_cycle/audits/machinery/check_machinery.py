"""Finite identity checks only; does not optimize or test the open tensor witness."""
import itertools, json, math, os, resource, sys, time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
started=time.perf_counter(); cpu=time.process_time()
rng=np.random.default_rng(20261021)
def e_prefix(x,D,N,i):
    k=D**i; h=D**(N-i)
    y=np.trace(x.reshape(k,h,k,h),axis1=0,axis2=2)/k
    return np.kron(np.eye(k),y)
def channel(x,D,N,t):
    u=math.exp(-t*math.log(D))
    ans=u**N*x
    for i in range(1,N+1):
        ans=ans+(1-u)*u**(N-i)*e_prefix(x,D,N,i)
    return ans
def norm2(x): return float(np.vdot(x,x).real/x.shape[0])
def endpoint(D,N,t):
    v=math.exp(-2*t*math.log(D)); z=D*v
    return z**N+(1-v)*sum(z**l for l in range(N))
errors=[]; ratios=[]; cases=0
for D,N in [(2,1),(2,2),(2,3),(2,4),(3,1),(3,2)]:
    q=D**N; rho=np.zeros((q,q)); rho[0,0]=1
    for t in [.2,.5,.9]:
        bound=endpoint(D,N,t)
        direct=q*float(np.trace(rho@channel(rho,D,N,2*t)).real)
        errors.append(abs(bound-direct))
        y=channel(rho,D,N,t); y/=math.sqrt(norm2(y))
        attained=float(np.linalg.norm(channel(y,D,N,t),ord=2)**2)
        errors.append(abs(attained-bound))
        if t==.5: errors.append(abs(bound-(1+(1-1/D)*N)))
        for _ in range(3):
            x=rng.normal(size=(q,q))+1j*rng.normal(size=(q,q))
            observed=float(np.linalg.norm(channel(x,D,N,t),ord=2)**2/norm2(x))
            ratios.append(observed/bound)
            assert observed <= bound+1e-11
        cases+=1
assert max(errors)<1e-11
chunk_cases=0
for N in range(1,10):
    for b in range(1,6):
        k=(-N)%b
        for pattern in itertools.product([0,1],repeat=N):
            padded=(0,)*k+pattern
            first=next((j for j,x in enumerate(padded) if x),len(padded))
            ell=len(padded)-first
            active=sum(any(padded[j:j+b]) for j in range(0,len(padded),b))
            assert b*active <= ell+b-1
            # Added identity-prefix factors preserve hierarchy eigenvalue.
            first_old=next((j for j,x in enumerate(pattern) if x),N)
            assert ell==N-first_old
            chunk_cases+=1
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
if sys.platform!='darwin':rss*=1024
record={
 'status':'PASS_IDENTITY_CHECKS_ONLY',
 'endpoint_cases':cases,'random_endpoint_upper_checks':len(ratios),
 'max_identity_abs_error':max(errors),'max_random_ratio_to_exact_norm':max(ratios),
 'chunk_and_identity_padding_patterns':chunk_cases,
 'wall_seconds_script_body':time.perf_counter()-started,
 'cpu_seconds_script_body':time.process_time()-cpu,'peak_rss_bytes':rss,
 'python':sys.version,'numpy':np.__version__,
 'blas_threads_requested':{k:os.environ.get(k) for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']},
 'scope':'Exact channel endpoint and spectral chunk comparison. No critical tensor theorem, numerical optimization, or physical implementation is tested.'}
(ROOT/'COMPUTE_RECEIPT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
