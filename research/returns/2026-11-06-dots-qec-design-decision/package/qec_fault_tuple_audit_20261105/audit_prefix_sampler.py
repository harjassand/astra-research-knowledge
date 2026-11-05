"""Independent exact checks of the floating categorical accelerator."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util, json, random, time
import numpy as np
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('tuple_sampler',P.parent/'qec_fault_tuple_20261105'/'exact_sampler.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rng=random.Random(5181973);began=time.perf_counter();checks=prefix_checks=0
mask=(1<<64)-1
for n,N in [(1,1),(2,2),(3,64),(17,64),(1176,64),(4840,64),(65536,1)]:
    for kind in range(4):
        # Alternating tiny/huge masses deliberately lose small increments in
        # the float prefix. Variable distance shifts exercise the whole cap.
        entries=[]
        for i in range(n*N):
            if kind==0: v=(1<<128)-1 if i%2 else 1
            elif kind==1: v=rng.getrandbits(rng.randrange(129))
            elif kind==2: v=0 if i%3 else 1<<rng.randrange(128)
            else: v=0
            entries.append(v)
        lo=np.array([v&mask for v in entries],dtype=np.uint64).reshape(n,N)
        hi=np.array([v>>64 for v in entries],dtype=np.uint64).reshape(n,N)
        sampler=mod.CertifiedPrefix(lo,hi,64)
        d=np.array([rng.randrange(65) for _ in range(n)],dtype=np.int16);r=rng.randrange(N)
        residues=(r-d)%N;prefix=[];s=0
        for i in range(n):
            s+=entries[i*N+int(residues[i])]<<(64-int(d[i]));prefix.append(s)
        float_prefix,error=sampler.enclosures(d,residues)
        assert float_prefix is not None
        for i in range(n):
            lo_i=sampler.lower_integer_bound(float_prefix[i],error)
            hi_i=sampler.upper_integer_bound(float_prefix[i],error)
            assert lo_i<=prefix[i]<=hi_i
            prefix_checks+=1
        indices=list(range(n)) if n<100 else sorted(set([0,1,n//2,n-1]+[rng.randrange(n) for _ in range(24)]))
        thresholds={0,s,s+1}
        for i in indices:
            for delta in [-1,0,1]:
                if prefix[i]+delta>=0:thresholds.add(prefix[i]+delta)
        thresholds.update(rng.randrange(s+1) for _ in range(32))
        import bisect
        for u in sorted(thresholds):
            expected=bisect.bisect_right(prefix,u)
            expected=None if expected==n else expected
            assert sampler.select(u,d,r)==expected
            checks+=1
out={'status':'PASS: outward prefixes and exact categorical selection',
     'prefix_enclosures':prefix_checks,'categorical_thresholds':checks,
     'maximum_length':65536,'all_zero_vectors_included':True,
     'elapsed_seconds':time.perf_counter()-began}
(P/'prefix_audit_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
