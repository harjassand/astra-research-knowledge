"""Independent Python-integer oracle tests for the guarded limb kernel."""
from pathlib import Path
import json, random, resource, sys, time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from exact_matmul import exact_dot, radix_bits, LIMIT


def naive(a, b):
    return np.array([[sum(int(a[i,k])*int(b[k,j]) for k in range(a.shape[1]))
                      for j in range(b.shape[1])] for i in range(a.shape[0])],
                    dtype=object).reshape(a.shape[0],b.shape[1])


def main():
    start=time.perf_counter(); cpu=time.process_time()
    rng=random.Random(20261021)
    checked=[]; rejected=[]
    fixtures=[]
    for bits in [1,25,26,31,62,63,90,130]:
        for shape in [(1,1,1),(3,7,4),(9,17,11)]:
            n,k,m=shape
            make=lambda r,c:np.array([[rng.randrange(-(1<<bits),(1<<bits))
                                      for _ in range(c)] for _ in range(r)],dtype=object)
            a,b=make(n,k),make(k,m)
            if bits<=63:
                a=a.astype(np.int64); b=b.astype(np.int64)
            fixtures.append((f"signed_bits{bits}_{shape}",a,b))
    extremes=np.array([[-(1<<63),(1<<63)-1,0,1,-1]],dtype=np.int64)
    fixtures.append(("int64_min_max",extremes,extremes.T))
    fixtures.append(("empty_inner",np.zeros((3,0),dtype=np.int64),np.zeros((0,5),dtype=np.int64)))
    fixtures.append(("empty_rows",np.zeros((0,3),dtype=np.int64),np.zeros((3,5),dtype=np.int64)))
    fixtures.append(("all_zero",np.zeros((3,5),dtype=np.int64),np.zeros((5,4),dtype=object)))
    fixtures.append(("numpy_ints_in_objects",np.array([[np.int64(-(1<<63)),np.int64(7)]],dtype=object),
                     np.array([[np.int64(-(1<<63))],[np.int64(-7)]],dtype=object)))
    for name,a,b in fixtures:
        t=time.perf_counter()
        c,info=exact_dot(a,b,return_info=True)
        expected=naive(a,b)
        if c.shape!=expected.shape or not np.array_equal(c,expected):
            raise AssertionError(name)
        if any(type(v) is not int for v in c.flat):
            raise AssertionError('non-Python int result '+name)
        checked.append({"case":name,"wall_seconds":time.perf_counter()-t,**info})
    one=np.array([[1]],dtype=np.int64)
    bad=[("float_dtype",np.array([[1.]],dtype=float),one),
         ("float_object",np.array([[1.]],dtype=object),one),
         ("bool_dtype",np.array([[True]],dtype=bool),one),
         ("bool_object",np.array([[True]],dtype=object),one),
         ("string_object",np.array([['1']],dtype=object),one),
         ("int32_dtype",np.array([[1]],dtype=np.int32),one),
         ("unsigned_dtype",np.array([[2**63]],dtype=np.uint64),one),
         ("wrong_rank",np.array([1],dtype=np.int64),one),
         ("wrong_shape",np.zeros((2,3),dtype=np.int64),one),
         ("list",[[1]],one)]
    for name,a,b in bad:
        try:exact_dot(a,b)
        except (TypeError,ValueError):rejected.append(name)
        else:raise AssertionError('did not reject '+name)
    for k in [0,1,2,512,1074,10**6,LIMIT]:
        b=radix_bits(k)
        if k*((1<<b)-1)**2>LIMIT:raise AssertionError('bad radix bound')
    # A small cost/scaling diagnostic; no full 1074-dimensional experiment.
    scaling=[]
    for n in [32,64,128]:
        a=np.array([[rng.randrange(-(1<<29),(1<<29)) for _ in range(n)] for _ in range(n)],dtype=np.int64)
        b=np.array([[rng.randrange(-(1<<59),(1<<59)) for _ in range(n)] for _ in range(n)],dtype=np.int64)
        t=time.perf_counter(); c,info=exact_dot(a,b,return_info=True)
        elapsed=time.perf_counter()-t
        # Independent full check of a sampled row and column plus corner entries.
        for i,j in [(0,j) for j in range(n)]+[(i,n-1) for i in range(n)]:
            if c[i,j]!=sum(int(a[i,k])*int(b[k,j]) for k in range(n)):
                raise AssertionError('scaling oracle mismatch')
        scaling.append({"n":n,"kernel_wall_seconds":elapsed,"checked_entries":2*n,**info})
    out={"PASS":True,"exact_fixtures":checked,"rejections":rejected,
         "scaling":scaling,"wall_seconds":time.perf_counter()-start,
         "cpu_seconds":time.process_time()-cpu,
         "peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
         "scope":"Independent naive integer oracle for bounded fixtures, not a proof of arbitrary matrix-multiply hardware/software correctness."}
    (ROOT/'results/exact_matmul_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['exact_fixtures']},indent=2))

if __name__=='__main__':main()
