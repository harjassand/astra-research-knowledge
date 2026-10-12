"""Independent finite certificate verifier: no optimizer, graph components, or CG.

Uses NumPy for vectorized *integer* checks.  It checks an explicit overflow
bound before accumulating int64 incidences.  Energy sums use Python integers.
The independent REPORT.md proof is required for the infinite-lattice conclusion.
"""
from pathlib import Path
from collections import Counter
import json, time
import numpy as np

ROOT=Path(__file__).parent

def verify(path: Path = ROOT/'module_flow.npz', meta_path: Path=ROOT/'module_metadata.json') -> dict:
    start=time.perf_counter()
    meta=json.loads(meta_path.read_text())
    if (meta['width'],meta['height'],meta['ports']) != (6,3,[7,10]):
        raise ValueError('This verifier is specialized to the stated 6 by 3 module.')
    den=int(meta['denominator'])
    if den<=0: raise ValueError('Invalid denominator')
    z=np.load(path,allow_pickle=False)
    u=z['u'].astype(np.int64);v=z['v'].astype(np.int64)
    bid=z['bond'].astype(np.int64);flow=z['flow'].astype(np.int64)
    E=len(u);N=1<<18
    if not (u.shape==v.shape==bid.shape==flow.shape):raise ValueError('Array shape mismatch')
    if np.any(u<0) or np.any(v>=N) or np.any(u>=v):raise ValueError('Invalid oriented configuration edge')
    if len(np.unique(u*N+v))!=E:raise ValueError('Duplicate configuration edges')
    sites=[(x,y)for y in range(3)for x in range(6)];index={z:i for i,z in enumerate(sites)}
    physical=[(index[(x,y)],index[(x+dx,y+dy)])for x,y in sites
              for dx,dy in [(1,0),(0,1)]if(x+dx,y+dy)in index]
    if np.any(bid<0)or np.any(bid>=len(physical)):raise ValueError('Invalid bond index')
    overlap=[]
    for j,(a,b) in enumerate(physical):
        rows=np.flatnonzero(bid==j);uu=u[rows];vv=v[rows]
        if np.any(vv != (uu^(1<<a)^(1<<b))):raise ValueError('Not the declared nearest-neighbor exchange')
        if np.any((((uu>>a)^(uu>>b))&1)!=1):raise ValueError('Exchange of equal occupations')
        # All exterior sites are occupied. Each endpoint requires at least one
        # vacant INTERNAL neighbor other than the other exchange endpoint.
        for endpoint,other in [(a,b),(b,a)]:
            x,y=sites[endpoint]
            neighbors=[index[(x+dx,y+dy)]for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]
                       if(x+dx,y+dy)in index and index[(x+dx,y+dy)]!=other]
            mask=sum(1<<t for t in neighbors)
            if np.any((uu&mask)==mask):raise ValueError('Illegal hard KA transition')
        overlap.append(1 if (sites[a][0]==2 and sites[b][0]==3) else 4)
    gate=sorted(int(x)for x in meta['gate_allowed'])
    if len(gate)!=len(set(gate)) or any(x<0 or x>=256 for x in gate):raise ValueError('Invalid gate')
    offsets=[(x,y)for y in range(-1,2)for x in range(-1,2)if(x,y)!=(0,0)]
    if [list(o) for o in offsets]!=meta['gate_offsets']:raise ValueError('Gate indexing mismatch')
    off_index={o:i for i,o in enumerate(offsets)};gate_set=set(gate)
    rule_set={pattern for pattern in range(256) if all((pattern & mask)!=mask for mask in (7,41,90,148,224))}
    if gate_set!=rule_set:raise ValueError('Gate differs from the five-clause rule')
    for pattern in gate:
        for reflect in [False,True]:
            for rotate in range(4):
                out=0
                for bit,(x,y) in enumerate(offsets):
                    if not ((pattern>>bit)&1):continue
                    if reflect:x=-x
                    for _ in range(rotate):x,y=-y,x
                    out|=1<<off_index[(x,y)]
                if out not in gate_set:raise ValueError('Gate is not square-symmetric')
    counts=[sum(v.bit_count()==n for v in gate)for n in range(9)]
    expected=[1,8,28,52,49,16,0,0,0]
    if counts!=expected:raise ValueError('Gate probability polynomial mismatch')
    # Compute the full required source--sink vector from scratch.
    state=np.arange(N,dtype=np.int64);allow=np.zeros(256,bool);allow[gate]=True
    left=np.zeros(N,np.int64);right=np.zeros(N,np.int64)
    for j,(x,y) in enumerate(offsets):
        left|=((state>>index[(x+1,y+1)])&1)<<j
        right|=((state>>index[(x+4,y+1)])&1)<<j
    demand=(((state>>7)&1)-((state>>10)&1))*allow[left]*allow[right]
    # An edge is uniquely determined by state and one of 27 physical bonds.
    # No state can have more than 27 stored incident edges.
    maxflow=max((abs(int(x))for x in flow),default=0)
    if maxflow*len(physical)+den >= 2**63:
        raise OverflowError('Certificate exceeds the verified int64 accumulation bound')
    div=np.zeros(N,np.int64)
    np.add.at(div,u,flow);np.add.at(div,v,-flow)
    if not np.array_equal(div,demand*den):
        raise ValueError('Exact source--sink identity failed')
    # Recompute both equilibrium energy polynomials and both transport moments.
    energy=[0]*19;weighted=[0]*19;rx=[0]*19;ry=[0]*19
    for uu,j,f in zip(u,bid,flow):
        uu=int(uu);j=int(j);f=int(f);n=uu.bit_count();a,b=physical[j]
        energy[n]+=f*f;weighted[n]+=overlap[j]*f*f
        sign=((uu>>a)&1)-((uu>>b)&1)
        rx[n]+=2*f*sign*(sites[b][0]-sites[a][0])
        ry[n]+=2*f*sign*(sites[b][1]-sites[a][1])
    if [str(x)for x in energy]!=meta['energy_squares_by_particle_count']:
        raise ValueError('Unweighted energy polynomial mismatch')
    if [str(x)for x in weighted]!=meta['weighted_energy_squares_by_particle_count']:
        raise ValueError('Weighted energy polynomial mismatch')
    for n in range(19):
        conv=sum(counts[k]*counts[n-1-k] for k in range(9) if 0<=n-1-k<9)
        if rx[n]!=6*den*conv or ry[n]!=0:
            raise ValueError('Exact transport normalization identity failed')
    return {'passed':True,'states_checked':N,'configuration_edges_checked':E,
            'gate_patterns':len(gate),'gate_particle_counts':counts,
            'nonzero_demands':int(np.count_nonzero(demand)),
            'integer_divergence_residual':0,'response_polynomial_checked':True,
            'wall_seconds':time.perf_counter()-start}

if __name__=='__main__':
    result=verify()
    (ROOT/'verification_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
