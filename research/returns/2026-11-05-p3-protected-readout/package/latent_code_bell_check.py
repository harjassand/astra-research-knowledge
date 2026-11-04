"""Finite audit: learn an obscured toric code from noisy product outcomes,
then learn an unsigned logical Pauli from corrected two-copy Bell outcomes.

The physical samples are generated exactly by binary stabilizer algebra.
The default matching routine is the vendored polynomial weighted-blossom
implementation from NetworkX 3.4.2. Exact exponential DP is retained as an
optional finite-instance comparison, never as the claimed scalable decoder.
"""
from collections import defaultdict, deque
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse, hashlib, json, math, random, struct, subprocess, time
import numpy as np
from latent_code_blossom import max_weight_matching

ROOT=Path(__file__).resolve().parent
RNG=random.Random(4112606)
NRNG=np.random.default_rng(4112606)
MATCHING='blossom'

class WeightedGraph:
    """Small graph interface consumed by the unchanged blossom algorithm."""
    def __init__(self,n): self.adj={i:{} for i in range(n)}
    def __iter__(self): return iter(self.adj)
    def __getitem__(self,v): return self.adj[v]
    def nodes(self): return self.adj.keys()
    def neighbors(self,v): return iter(self.adj[v])
    def add_edge(self,u,v,weight):
        self.adj[u][v]={'weight':int(weight)}
        self.adj[v][u]={'weight':int(weight)}
    def edges(self,data=False):
        for u in self.adj:
            for v,attr in self.adj[u].items():
                if u<v: yield (u,v,attr) if data else (u,v)

def parity(x): return x.bit_count()&1

def echelon(rows, width, rhs=None):
    b={} 
    for i,row in enumerate(rows):
        value=0 if rhs is None else int(rhs[i])
        while row:
            p=row.bit_length()-1
            if p in b: row,value=row^b[p][0],value^b[p][1]
            else:
                b[p]=(row,value)
                break
        if not row and value: raise ValueError('inconsistent system')
    return b

def nullspace(rows,width):
    b=echelon(rows,width)
    out=[]
    for free in range(width):
        if free in b: continue
        x=1<<free
        for p,(row,_) in sorted(b.items()):
            if parity(row&x): x^=1<<p
        out.append(x)
    return out

def solve(rows,rhs,width):
    b=echelon(rows,width,rhs)
    x=0
    for p,(row,value) in sorted(b.items()):
        if parity(row&x)!=value: x^=1<<p
    return x

def rank(rows): return len(echelon(rows, max((r.bit_length() for r in rows),default=0)))

def mul_pauli(a,b):
    x,z,r=a; u,v,s=b
    return x^u,z^v,(r+s+2*parity(z&u))%4

def toric(L):
    n=2*L*L
    h=lambda i,j:(i%L)*L+(j%L)
    v=lambda i,j:L*L+(i%L)*L+(j%L)
    mask=lambda es:sum(1<<e for e in es)
    hx=[]; hz=[]
    for i in range(L):
        for j in range(L):
            hx.append(mask([h(i,j),h(i-1,j),v(i,j),v(i,j-1)]))
            hz.append(mask([h(i,j),v(i+1,j),h(i,j+1),v(i,j)]))
    lx=[mask(h(0,j) for j in range(L)),mask(v(i,0) for i in range(L))]
    lz=[mask(h(i,0) for i in range(L)),mask(v(0,j) for j in range(L))]
    assert all(not parity(x&z) for x in hx for z in hz)
    assert [[parity(x&z) for z in lz] for x in lx]==[[1,0],[0,1]]
    return n,hx,hz,lx,lz

def axis_xz(a): return (a&1,(a>>1)&1)
def axis_phase(a): return 1 if a==3 else 0

def hidden_frame(n):
    perm=list(range(n)); RNG.shuffle(perm)
    frames=[]
    for j in range(n):
        ax,az=RNG.sample([1,2,3],2)
        sx,sz=RNG.randrange(2),RNG.randrange(2)
        x,z=axis_xz(ax); u,v=axis_xz(az)
        ay=ax^az
        phase=(axis_phase(ax)+2*sx+axis_phase(az)+2*sz+2*z*u+1-axis_phase(ay))%4
        assert phase in [0,2]
        frames.append({1:(ax,sx),2:(az,sz),3:(ay,phase//2)})
    return perm,frames

def transform_pauli(x,z,r,perm,frames):
    out=(0,0,r-(x&z).bit_count())
    for j in range(len(perm)):
        a=((x>>j)&1)+2*((z>>j)&1)
        if not a: continue
        aa,ss=frames[j][a]; xx,zz=axis_xz(aa)
        out=mul_pauli(out,(xx<<perm[j],zz<<perm[j],axis_phase(aa)+2*ss))
    return out[0],out[1],out[2]%4

def product_outcome_columns(gens,bases,reps):
    """Uniform exact outcome distribution for the mixed stabilizer state."""
    n=len(bases); g=len(gens)
    constraints=[]
    for j,axis in enumerate(bases):
        bx,bz=axis_xz(axis)
        row=0
        for i,(x,z,r) in enumerate(gens):
            if (((x>>j)&1)*bz+((z>>j)&1)*bx)&1: row|=1<<i
        constraints.append(row)
    common=nullspace(constraints,g)
    rows=[]; rhs=[]
    for coeff in common:
        p=(0,0,0)
        for i,gen in enumerate(gens):
            if (coeff>>i)&1: p=mul_pauli(p,gen)
        x,z,r=p
        phase=(r-(x&z).bit_count())%4
        assert phase in [0,2]
        rows.append(x|z); rhs.append(phase//2)
    b=echelon(rows,n,rhs)
    allbits=(1<<reps)-1
    cols=[0]*n
    for j in range(n):
        if j not in b: cols[j]=RNG.getrandbits(reps)
    for pivot,(row,value) in sorted(b.items()):
        val=allbits if value else 0
        mask=row^(1<<pivot)
        while mask:
            low=mask&-mask; val^=cols[low.bit_length()-1]; mask^=low
        cols[pivot]=val
    return cols

def create_calibration(path,gens,n,patterns=1000,reps=256,visibility=.99):
    words=(reps+63)//64
    flipprob=(1-visibility)/2
    with path.open('wb') as f:
        f.write(struct.pack('<IIII',patterns,n,words,reps))
        for _ in range(patterns):
            bases=[RNG.choice([1,2,3]) for _ in range(n)]
            cols=product_outcome_columns(gens,bases,reps)
            flips=NRNG.random((n,reps))<flipprob
            for j in range(n):
                cols[j]^=int.from_bytes(np.packbits(flips[j],bitorder='little').tobytes(),'little')
            f.write(bytes(bases))
            for col in cols:
                f.write(col.to_bytes(words*8,'little'))

def acquire_graph(checks,n):
    # Adjacent check vertices locally anticommute on at least one wire.
    adjacency=[set() for _ in checks]
    local=[[] for _ in range(n)]
    for i,(x,z) in enumerate(checks):
        for j in range(n):
            a=((x>>j)&1)+2*((z>>j)&1)
            if a: local[j].append((i,a))
    for col in local:
        assert len(col)==4
        for (i,a),(j,b) in combinations(col,2):
            if a!=b: adjacency[i].add(j);adjacency[j].add(i)
    colors={};components=[]
    for first in range(len(checks)):
        if first in colors: continue
        colors[first]=0;q=deque([first]);comp=[]
        while q:
            i=q.popleft();comp.append(i)
            for j in adjacency[i]:
                if j in colors: assert colors[j]!=colors[i]
                else: colors[j]=1-colors[i];q.append(j)
        components.append(comp)
    # Per-wire inverse frame; signs are irrelevant for two-copy observables.
    axes=[]
    for col in local:
        a0={a for i,a in col if colors[i]==0}
        a1={a for i,a in col if colors[i]==1}
        assert len(a0)==len(a1)==1 and a0!=a1
        axes.append((next(iter(a0)),next(iter(a1))))
    hx=[x|z for i,(x,z) in enumerate(checks) if colors[i]==0]
    hz=[x|z for i,(x,z) in enumerate(checks) if colors[i]==1]
    assert all(not parity(x&z) for x in hx for z in hz)
    assert all(sum((row>>j)&1 for row in hx)==2 for j in range(n))
    assert all(sum((row>>j)&1 for row in hz)==2 for j in range(n))
    return hx,hz,axes,components

def logical_basis(hx,hz,n):
    def quotient(kernel,subspace):
        span=list(subspace);r=rank(span);out=[]
        for v in kernel:
            rr=rank(span+[v])
            if rr>r: out.append(v);span.append(v);r=rr
        return out
    lx=quotient(nullspace(hz,n),hx)
    zz=quotient(nullspace(hx,n),hz)
    k=len(lx);assert len(zz)==k
    mat=[sum(parity(x&z)<<j for j,z in enumerate(zz)) for x in lx]
    lz=[]
    for target in range(k):
        coeff=solve(mat,[int(i==target) for i in range(k)],k)
        z=0
        for j,v in enumerate(zz):
            if (coeff>>j)&1:z^=v
        lz.append(z)
    assert [[parity(x&z) for z in lz] for x in lx]==[[int(i==j) for j in range(k)] for i in range(k)]
    return lx,lz

def decoder_graph(checks,n):
    adj=[[] for _ in checks]
    for e in range(n):
        ends=[i for i,row in enumerate(checks) if (row>>e)&1]
        assert len(ends)==2
        i,j=ends;adj[i].append((j,e));adj[j].append((i,e))
    paths={}
    for start in range(len(checks)):
        q=deque([start]);dist={start:0};chain={start:0}
        while q:
            v=q.popleft()
            for w,e in adj[v]:
                if w not in dist:dist[w]=dist[v]+1;chain[w]=chain[v]^(1<<e);q.append(w)
        for end in dist:paths[start,end]=(dist[end],chain[end])
    return paths

def homological_distance(checks,opposite_logicals,n):
    """Shortest nontrivial cycle, acquired through a four-sheet cover."""
    assert len(opposite_logicals)==2
    adj=[[] for _ in checks]
    for edge in range(n):
        ends=[i for i,row in enumerate(checks) if (row>>edge)&1]
        assert len(ends)==2
        label=sum(((rep>>edge)&1)<<i for i,rep in enumerate(opposite_logicals))
        u,v=ends;adj[u].append((v,label));adj[v].append((u,label))
    best=None
    for base in range(len(checks)):
        first=(base,0);queue=deque([first]);dist={first:0}
        while queue:
            vertex,sheet=queue.popleft()
            if vertex==base and sheet!=0:
                best=dist[vertex,sheet] if best is None else min(best,dist[vertex,sheet])
                break
            for nxt,label in adj[vertex]:
                state=(nxt,sheet^label)
                if state not in dist:dist[state]=dist[vertex,sheet]+1;queue.append(state)
    assert best is not None
    return best

def acquired_graph_certificate(hx,hz,lx,lz,n):
    """Verify the acquired closed orientable torus cellulation, without L."""
    ends=[]
    for edge in range(n):
        vv=[i for i,row in enumerate(hx) if (row>>edge)&1]
        assert len(vv)==2
        ends.append(tuple(vv))
    face_orientations=[]
    for face in hz:
        edges=[e for e in range(n) if (face>>e)&1]
        incident=defaultdict(list)
        for e in edges:
            u,v=ends[e];incident[u].append((v,e));incident[v].append((u,e))
        assert len(edges)==4 and len(incident)==4
        assert all(len(es)==2 for es in incident.values())
        start=min(incident);v=start;previous=None;directions={}
        for _ in range(4):
            w,e=next((w,e) for w,e in incident[v] if e!=previous)
            directions[e]=int((v,w)!=ends[e])
            previous=e;v=w
        assert v==start and len(directions)==4
        face_orientations.append(directions)
    # The link at every vertex is a connected cycle on its incident edges.
    for vertex,star in enumerate(hx):
        star_edges=[e for e in range(n) if (star>>e)&1]
        assert len(star_edges)==4
        link={e:[] for e in star_edges}
        for face in hz:
            inter=[e for e in star_edges if (face>>e)&1]
            if inter:
                assert len(inter)==2
                a,b=inter;link[a].append(b);link[b].append(a)
        assert all(len(adj)==2 for adj in link.values())
        reached={star_edges[0]};queue=deque(reached)
        while queue:
            for w in link[queue.popleft()]:
                if w not in reached:reached.add(w);queue.append(w)
        assert len(reached)==4
    # Orient adjacent faces oppositely along each shared edge.
    orientation_constraints=[[] for _ in hz]
    for edge in range(n):
        faces=[i for i,row in enumerate(hz) if (row>>edge)&1]
        assert len(faces)==2
        a,b=faces
        parity_constraint=int(face_orientations[a][edge]==face_orientations[b][edge])
        orientation_constraints[a].append((b,parity_constraint))
        orientation_constraints[b].append((a,parity_constraint))
    flips={0:0};queue=deque([0])
    while queue:
        v=queue.popleft()
        for w,c in orientation_constraints[v]:
            if w in flips:assert flips[w]==(flips[v]^c)
            else:flips[w]=flips[v]^c;queue.append(w)
    assert len(flips)==len(hz)
    euler=len(hx)-n+len(hz)
    assert euler==0
    assert all(not parity(x&z) for x in hx for z in hz)
    assert len(lx)==len(lz)==2
    dx=homological_distance(hz,lz,n)
    dz=homological_distance(hx,lx,n)
    return {'physical_edges':n,'acquired_vertices':len(hx),'acquired_faces':len(hz),'all_faces_simple_four_cycles':True,'all_vertex_links_connected_four_cycles':True,'each_edge_has_two_endpoints_and_two_faces':True,'orientable':True,'connected':True,'Euler_characteristic':euler,'genus':1,'check_commutation_verified':True,'logical_symplectic_pairing_verified':True,'acquired_X_distance':dx,'acquired_Z_distance':dz,'distance_method':'BFS in the four-sheet homology cover, using acquired opposite logical representatives as edge labels'}

def correct(bits,checks,paths):
    defects=[i for i,row in enumerate(checks) if parity(row&bits)]
    assert len(defects)%2==0
    if not defects:return bits
    @lru_cache(None)
    def match(mask):
        if not mask:return 0,0
        lo=mask&-mask;i=lo.bit_length()-1;rest=mask^lo
        best=(10**9,0)
        remaining=rest
        while remaining:
            low=remaining&-remaining;j=low.bit_length()-1;remaining^=low
            cost,chain=paths[defects[i],defects[j]]
            c,cc=match(rest^low)
            if cost+c<best[0]:best=(cost+c,chain^cc)
        return best
    if MATCHING=='dp':
        _,correction=match((1<<len(defects))-1)
    else:
        graph=WeightedGraph(len(defects))
        cap=1+max(distance for distance,_ in paths.values())
        for i,j in combinations(range(len(defects)),2):
            if (defects[i],defects[j]) in paths:
                graph.add_edge(i,j,cap-paths[defects[i],defects[j]][0])
        pairs=max_weight_matching(graph,maxcardinality=True)
        assert len(pairs)*2==len(defects)
        correction=0
        for i,j in pairs:correction^=paths[defects[i],defects[j]][1]
    out=bits^correction
    assert all(not parity(out&row) for row in checks)
    return out

def sample_affine(rows,rhs,width):
    out=solve(rows,rhs,width)
    for v in nullspace(rows,width):
        if RNG.randrange(2):out^=v
    return out

def physical_bell_row(hx,hz,lx,lz,logical_p=None,sign_bit=0):
    n=max(max(hx).bit_length(),max(hz).bit_length());k=len(lx)
    rows=list(hx)+[z<<n for z in hz];rhs=[0]*len(rows)
    if logical_p is not None:
        u=logical_p&((1<<k)-1);v=logical_p>>k
        row=0
        for j in range(k):
            if (u>>j)&1:row^=lx[j]
            if (v>>j)&1:row^=lz[j]<<n
        rows.append(row);rhs.append(parity(u&v)^sign_bit)
    val=sample_affine(rows,rhs,2*n)
    return val&((1<<n)-1),val>>n

def logical_row(x,z,lx,lz):
    k=len(lx)
    return sum(parity(x&l)<<i for i,l in enumerate(lx))+sum(parity(z&l)<<(k+i) for i,l in enumerate(lz))

def noise_pair(x,z,n,q):
    faults=0
    for j in range(n):
        if RNG.random()<q:
            faults+=1;a=RNG.choice([1,2,3])
            if a&1:x^=1<<j
            if a&2:z^=1<<j
    return x,z,faults

def frame_bits(x,z,axes,inverse=False):
    """Fixed lab XX,ZZ outcomes -> acquired axes. Y Y = - X X Z Z."""
    outx=0;outz=0
    for j,(a,b) in enumerate(axes):
        xx=(x>>j)&1;zz=(z>>j)&1
        def value(axis,xx,zz):
            u,v=axis_xz(axis)
            return (u*xx)^(v*zz)^(u*v)
        if not inverse:
            yy=value(a,xx,zz);ww=value(b,xx,zz)
        else:
            choices=[(u,v) for u in [0,1] for v in [0,1] if value(a,u,v)==xx and value(b,u,v)==zz]
            assert len(choices)==1
            yy,ww=choices[0]
        outx|=yy<<j;outz|=ww<<j
    return outx,outz

def run_data(hx,hz,axes,n,experiments=200,rows_per_experiment=24,q=.01,signed_targets=None):
    lx,lz=logical_basis(hx,hz,n);k=len(lx)
    pathsx=decoder_graph(hx,n);pathsz=decoder_graph(hz,n)
    rowfail=0;datafail=0;faults=0;total=0;even=odd=0
    for trial in range(experiments):
        p=None if trial%2==0 else RNG.randrange(1,1<<(2*k))
        out=[]
        if p is None:even+=1
        else:odd+=1
        for _ in range(rows_per_experiment):
            x,z=physical_bell_row(hx,hz,lx,lz,p)
            true=logical_row(x,z,lx,lz)
            labx,labz=frame_bits(x,z,axes,inverse=True)
            assert frame_bits(labx,labz,axes)==(x,z)
            labx,labz,nfault=noise_pair(labx,labz,n,q);faults+=nfault
            xx,zz=frame_bits(labx,labz,axes)
            xx=correct(xx,hx,pathsx);zz=correct(zz,hz,pathsz)
            decoded=logical_row(xx,zz,lx,lz)
            rowfail+=int(decoded!=true);total+=1;out.append(decoded)
        differences=[r^out[0] for r in out[1:]]
        ker=nullspace(differences,2*k)
        if p is None:success=len(ker)==0
        else:success=len(ker)==1 and ker[0]==p
        if p is not None and success and signed_targets is not None:signed_targets.append(ker[0])
        datafail+=int(not success)
    return {'logical_qubits':k,'data_experiments':experiments,'null_experiments':even,'hidden_pauli_experiments':odd,'rows_per_experiment':rows_per_experiment,'pair_fault_probability':q,'actual_pair_faults':faults,'total_bell_rows':total,'logical_row_failures':rowfail,'learning_failures':datafail}

def run_global_data(hx,hz,axes,n,blocks=16,experiments=10,rows_per_experiment=80,q=.003,signed_targets=None):
    """Exercise a global hidden constraint across copies of the acquired block.

    This is a data-path audit; it does not claim that calibration was rerun on
    the full 800-wire register. The full-register acquisition is the theorem.
    """
    lx,lz=logical_basis(hx,hz,n);local_k=len(lx);k=local_k*blocks
    pathsx=decoder_graph(hx,n);pathsz=decoder_graph(hz,n)
    equations=list(hx)+[row<<n for row in hz]+list(lx)+[row<<n for row in lz]
    dimension=2*n;basis=nullspace(equations,dimension)
    offsets=[]
    for val in range(1<<(2*local_k)):
        rhs=[0]*(len(hx)+len(hz))+[(val>>i)&1 for i in range(2*local_k)]
        offsets.append(solve(equations,rhs,dimension))
    rowfail=0;datafail=0;faults=0;total=0
    for trial in range(experiments):
        p=None if trial%2==0 else RNG.randrange(1,1<<(2*k))
        out=[]
        for _ in range(rows_per_experiment):
            ideal=RNG.getrandbits(2*k)
            if p is not None:
                target=parity((p&((1<<k)-1))&(p>>k))
                if parity(ideal&p)!=target:ideal^=p&-p
            decoded_global=0
            for b in range(blocks):
                local=((ideal>>(local_k*b))&((1<<local_k)-1))|(((ideal>>(k+local_k*b))&((1<<local_k)-1))<<local_k)
                physical=offsets[local]
                for v in basis:
                    if RNG.randrange(2):physical^=v
                x=physical&((1<<n)-1);z=physical>>n
                assert logical_row(x,z,lx,lz)==local
                labx,labz=frame_bits(x,z,axes,inverse=True)
                labx,labz,nfault=noise_pair(labx,labz,n,q);faults+=nfault
                xx,zz=frame_bits(labx,labz,axes)
                xx=correct(xx,hx,pathsx);zz=correct(zz,hz,pathsz)
                learned=logical_row(xx,zz,lx,lz)
                decoded_global|=(learned&((1<<local_k)-1))<<(local_k*b)
                decoded_global|=(learned>>local_k)<<(k+local_k*b)
            rowfail+=int(decoded_global!=ideal);total+=1;out.append(decoded_global)
        ker=nullspace([r^out[0] for r in out[1:]],2*k)
        success=(not ker) if p is None else len(ker)==1 and ker[0]==p
        if p is not None and success and signed_targets is not None:signed_targets.append(ker[0])
        datafail+=int(not success)
    return {'physical_qubits':blocks*n,'logical_qubits':k,'acquired_blocks_reused':blocks,'data_experiments':experiments,'rows_per_experiment':rows_per_experiment,'pair_fault_probability':q,'actual_pair_faults':faults,'total_bell_rows':total,'logical_row_failures':rowfail,'learning_failures':datafail,'full_register_calibration_reexecuted':False}

def physical_logical_pauli(p,lx,lz,axes):
    """Known Hermitian representative i^(u.v) LX^u LZ^v."""
    k=len(lx);u=p&((1<<k)-1);v=p>>k
    out=(0,0,(u&v).bit_count()%4)
    for flag,reps,axis_index in [(u,lx,0),(v,lz,1)]:
        for logical,rep in enumerate(reps):
            if not ((flag>>logical)&1):continue
            for j in range(len(axes)):
                if (rep>>j)&1:
                    a=axes[j][axis_index];x,z=axis_xz(a)
                    out=mul_pauli(out,(x<<j,z<<j,axis_phase(a)))
    assert (out[2]-(out[0]&out[1]).bit_count())%2==0
    return out

def independent_signed_checks(signed_checks,n):
    out=[];binary=[];r=0
    for (x,z),sign in sorted(signed_checks.items()):
        rr=rank(binary+[x|(z<<n)])
        if rr>r:
            binary.append(x|(z<<n));r=rr
            out.append((x,z,((x&z).bit_count()+2*int(sign<0))%4))
    return out

def known_reference_specification(p,code_gens,lx,lz,axes):
    """Pure known stabilizer reference: each P_j eigenvalue +1; I -> |0>."""
    k=len(lx);n=len(axes);u=p&((1<<k)-1);v=p>>k
    logical_gens=[];reference_logical=[]
    for j in range(k):
        a=((u>>j)&1)+2*((v>>j)&1)
        if not a:a=2
        label=((a&1)<<j)+(((a>>1)&1)<<(k+j))
        logical_gens.append(label)
        reference_logical.append(physical_logical_pauli(label,lx,lz,axes))
    reference=list(code_gens)+reference_logical
    assert len(reference)==n
    assert rank([x|(z<<n) for x,z,r in reference])==n
    assert all(not parity((x&zz)^(z&xx)) for x,z,r in reference for xx,zz,rr in reference)
    target=physical_logical_pauli(p,lx,lz,axes)
    product=(0,0,0)
    for j,gen in enumerate(reference_logical):
        if ((u>>j)&1) or ((v>>j)&1):product=mul_pauli(product,gen)
    assert product==target
    return reference,target,logical_gens

def record_reference(records,p,reference,target,logical_gens):
    if records is not None:
        records[p]={'logical_pauli_label':p,'logical_reference_generators':logical_gens,
            'physical_target':{'x':target[0],'z':target[1],'i_phase':target[2]},
            'physical_reference_generators':[{'x':x,'z':z,'i_phase':r} for x,z,r in reference],
            'factory_simulated':False}

def signed_reference_audit(hx,hz,axes,signed_checks,n,targets,q=.01,reference_records=None):
    """One fresh specimen/reference pair per already learned nonnull target.

    Reference specifications are verified algebraically. The offline physical
    factory implementing them, and its delta_ref, are not simulated.
    """
    lx,lz=logical_basis(hx,hz,n);k=len(lx)
    code_gens=independent_signed_checks(signed_checks,n)
    assert len(code_gens)==n-k
    px=decoder_graph(hx,n);pz=decoder_graph(hz,n)
    cache={};rowfail=0;signfail=0;faults=0;positive=negative=0
    for index,p in enumerate(targets):
        sign_bit=index&1
        if sign_bit:negative+=1
        else:positive+=1
        if p not in cache:
            reference,target,logical_gens=known_reference_specification(p,code_gens,lx,lz,axes)
            cache[p]=(reference,target,logical_gens)
            record_reference(reference_records,p,reference,target,logical_gens)
        reference,target,_=cache[p]
        # Exact two-state Bell law. Code signs agree; specimen/reference P
        # signs have product (-1)^sign_bit. Other reference stabilizers have
        # zero expectation in the rank-half specimen and contribute nothing.
        common=list(code_gens)+[target]
        equations=[x|(z<<n) for x,z,r in common]
        rhs=[parity(x&z) for x,z,r in common]
        rhs[-1]^=sign_bit
        physical=sample_affine(equations,rhs,2*n)
        labx=physical&((1<<n)-1);labz=physical>>n
        x,z=frame_bits(labx,labz,axes)
        ideal=logical_row(x,z,lx,lz)
        quadratic=parity((p&((1<<k)-1))&(p>>k))
        assert (parity(ideal&p)^quadratic)==sign_bit
        labx,labz,nfault=noise_pair(labx,labz,n,q);faults+=nfault
        xx,zz=frame_bits(labx,labz,axes)
        xx=correct(xx,hx,px);zz=correct(zz,hz,pz)
        decoded=logical_row(xx,zz,lx,lz)
        recovered_sign_bit=parity(decoded&p)^quadratic
        rowfail+=int(decoded!=ideal);signfail+=int(recovered_sign_bit!=sign_bit)
    return {'reference_audit_seed':4112607,'nonnull_targets_already_learned':len(targets),'additional_specimen_reference_pairs':len(targets),'positive_specimens':positive,'negative_specimens':negative,'unique_known_reference_specifications':len(cache),'each_reference_has_n_independent_commuting_signed_stabilizers':True,'target_P_eigenvalue_of_reference':1,'physical_factory_simulated':False,'factory_requirement':'Offline preparation of the known signed stabilizer reference; account for its local residual faults in q and its separate preparation failure delta_ref','pair_fault_probability':q,'actual_pair_faults':faults,'logical_row_failures':rowfail,'signed_Pauli_readout_failures':signfail,'prior_unsigned_audit_counts_changed':False}

def global_signed_reference_audit(hx,hz,axes,signed_checks,n,targets,blocks=16,q=.003,reference_records=None):
    """One reference-assisted sign readout for each global learned target."""
    lx,lz=logical_basis(hx,hz,n);local_k=len(lx);k=local_k*blocks
    code_gens=independent_signed_checks(signed_checks,n)
    px=decoder_graph(hx,n);pz=decoder_graph(hz,n)
    equations=list(hx)+[row<<n for row in hz]+list(lx)+[row<<n for row in lz]
    basis=nullspace(equations,2*n)
    offsets=[solve(equations,[0]*(len(hx)+len(hz))+[(v>>i)&1 for i in range(2*local_k)],2*n) for v in range(1<<(2*local_k))]
    cache={};rowfail=signfail=faults=positive=negative=0
    for index,p in enumerate(targets):
        sign_bit=index&1
        if sign_bit:negative+=1
        else:positive+=1
        quadratic=parity((p&((1<<k)-1))&(p>>k))
        ideal=RNG.getrandbits(2*k)
        if parity(ideal&p)!=(quadratic^sign_bit):ideal^=p&-p
        decoded=0
        for b in range(blocks):
            local_p=((p>>(local_k*b))&((1<<local_k)-1))|(((p>>(k+local_k*b))&((1<<local_k)-1))<<local_k)
            if local_p not in cache:
                reference,target,logical_gens=known_reference_specification(local_p,code_gens,lx,lz,axes)
                cache[local_p]=(reference,target,logical_gens)
                record_reference(reference_records,local_p,reference,target,logical_gens)
            local=((ideal>>(local_k*b))&((1<<local_k)-1))|(((ideal>>(k+local_k*b))&((1<<local_k)-1))<<local_k)
            physical=offsets[local]
            for v in basis:
                if RNG.randrange(2):physical^=v
            x=physical&((1<<n)-1);z=physical>>n
            labx,labz=frame_bits(x,z,axes,inverse=True)
            labx,labz,nfault=noise_pair(labx,labz,n,q);faults+=nfault
            xx,zz=frame_bits(labx,labz,axes)
            xx=correct(xx,hx,px);zz=correct(zz,hz,pz)
            learned=logical_row(xx,zz,lx,lz)
            decoded|=(learned&((1<<local_k)-1))<<(local_k*b)
            decoded|=(learned>>local_k)<<(k+local_k*b)
        rowfail+=int(decoded!=ideal)
        signfail+=int((parity(decoded&p)^quadratic)!=sign_bit)
    return {'physical_qubits':blocks*n,'logical_qubits':k,'nonnull_targets_already_learned':len(targets),'additional_specimen_reference_pairs':len(targets),'positive_specimens':positive,'negative_specimens':negative,'reference_is_product_of_known_encoded_block_stabilizer_states':True,'block_reference_specifications_verified':len(cache),'physical_factory_simulated':False,'pair_fault_probability':q,'actual_pair_faults':faults,'logical_row_failures':rowfail,'signed_Pauli_readout_failures':signfail,'full_register_calibration_reexecuted':False,'prior_unsigned_audit_counts_changed':False}

def main():
    global MATCHING
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--matching',choices=['blossom','dp'],default='blossom')
    parser.add_argument('--acquisition',choices=['hash','exhaustive'],default='hash')
    parser.add_argument('--collision-risk',type=float,default=.003)
    parser.add_argument('--output',default='latent_code_bell_result.json')
    args=parser.parse_args();MATCHING=args.matching
    start=time.time();L=5
    n,hx,hz,lx,lz=toric(L)
    p=11;u=p&3;v=p>>2
    px=0;pz=0
    for i in range(2):
        if (u>>i)&1:px^=lx[i]
        if (v>>i)&1:pz^=lz[i]
    canonical=[(x,0,0) for x in hx[:-1]]+[(0,z,0) for z in hz[:-1]]+[(px,pz,(u&v).bit_count()%4)]
    perm,frames=hidden_frame(n)
    gens=[transform_pauli(*g,perm,frames) for g in canonical]
    transformed_checks=[transform_pauli(x,0,0,perm,frames) for x in hx]+[transform_pauli(0,z,0,perm,frames) for z in hz]
    expected={(x,z) for x,z,r in transformed_checks}
    expected_signs={(x,z):(1 if (r-(x&z).bit_count())%4==0 else -1) for x,z,r in transformed_checks}
    path=ROOT/'latent_code_calibration.bin'
    create_calibration(path,gens,n)
    scanner=ROOT/('latent_code_hash_scan' if args.acquisition=='hash' else 'latent_code_scan')
    subprocess.run(['g++','-O3','-march=native','-std=c++17',str(scanner.with_suffix('.cpp')),'-o',str(scanner)],check=True)
    scan_args=[str(scanner),str(path)]
    if args.acquisition=='hash':
        qc=.005;b=.5+4*qc
        discovery_rows=math.ceil(2*math.log(n)/math.log(1/b))
        runtime_failure_budget=args.collision_risk
        if not 0<runtime_failure_budget<1:raise ValueError('collision risk must lie in (0,1)')
        collision_cap=math.ceil(1000*(3*n+n*n/4)/runtime_failure_budget)
        scan_args.extend([str(discovery_rows),str(collision_cap)])
    sign_path=ROOT/'latent_code_acquired_signs.json'
    scan_args.append(str(sign_path))
    scanner_start=time.perf_counter()
    text=subprocess.check_output(scan_args,text=True)
    scanner_seconds=time.perf_counter()-scanner_start
    lines=text.strip().splitlines();checks=sorted(tuple(map(int,line.split())) for line in lines if not line.startswith('#'))
    statistics=json.loads(lines[0][2:]) if args.acquisition=='hash' else {'exhaustive_pattern_support_tests':1000*math.comb(n,4)}
    if args.acquisition=='hash':statistics['runtime_failure_budget']=runtime_failure_budget
    assert set(checks)==expected,(len(checks),len(expected),set(checks)^expected)
    signed_checks={(row['x'],row['z']):row['sign'] for row in json.loads(sign_path.read_text())}
    assert signed_checks==expected_signs
    ahx,ahz,axes,components=acquire_graph(checks,n)
    alx,alz=logical_basis(ahx,ahz,n)
    certificate=acquired_graph_certificate(ahx,ahz,alx,alz,n)
    signed_targets=[];global_signed_targets=[]
    data=run_data(ahx,ahz,axes,n,signed_targets=signed_targets)
    global_data=run_global_data(ahx,ahz,axes,n,signed_targets=global_signed_targets)
    prior_rng_state=RNG.getstate();RNG.seed(4112607)
    reference_records={}
    sign_audit=signed_reference_audit(ahx,ahz,axes,signed_checks,n,signed_targets,reference_records=reference_records)
    global_sign_audit=global_signed_reference_audit(ahx,ahz,axes,signed_checks,n,global_signed_targets,reference_records=reference_records)
    reference_path=ROOT/'latent_code_reference_specifications.json'
    reference_path.write_text(json.dumps([reference_records[p] for p in sorted(reference_records)],indent=2)+'\n')
    RNG.setstate(prior_rng_state)
    implementation='NetworkX 3.4.2 integer weighted blossom, vendored with BSD license; O(number_of_defects^3)' if MATCHING=='blossom' else 'Exact defect-matching dynamic programming; exponential, finite-audit option only'
    result={'seed':4112606,'physical_qubits':n,'toric_distance':L,'acquired_X_distance':certificate['acquired_X_distance'],'acquired_Z_distance':certificate['acquired_Z_distance'],'acquired_graph_certificate':certificate,'unknown_permutation_and_local_cliffords':True,'calibration_patterns':1000,'copies_per_pattern':256,'calibration_copies':256000,'calibration_local_visibility':.99,'calibration_outcome_flip_probability':.005,'acquisition_method':args.acquisition,'acquisition_statistics':statistics,'scanner_seconds':scanner_seconds,'learned_weight_four_checks':len(checks),'signed_checks_verified_against_ground_truth':True,'negative_signed_checks':sum(sign<0 for sign in signed_checks.values()),'signed_check_metadata_file':sign_path.name,'false_positive_checks':len(set(checks)-expected),'missed_checks':len(expected-set(checks)),'acquired_components':len(components),'acquired_X_check_rank':rank(ahx),'acquired_Z_check_rank':rank(ahz),'matching_implementation':implementation,'matching_source_sha256':hashlib.sha256((ROOT/'latent_code_blossom.py').read_bytes()).hexdigest(),'scanner_output':lines[0],**data,'global_data_path_audit':global_data,'signed_reference_readout_audit':sign_audit,'global_signed_reference_readout_audit':global_sign_audit,'known_reference_specifications_file':reference_path.name,'elapsed_seconds':time.time()-start}
    (ROOT/args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
