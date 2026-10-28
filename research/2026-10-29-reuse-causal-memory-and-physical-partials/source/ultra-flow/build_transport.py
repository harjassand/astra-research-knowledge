#!/usr/bin/env python3
"""Generate ordinary numerical spline-Stokes currents, then repair them exactly.

Only the separate exact consumer will report continuous lower certificates.
The public image is not a physical subvoxel inclusion or an RVE certificate.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, itertools, json, time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla

BASE=Path(__file__).parent
DEN=2160

def stencil(axis):
    mass1={0:F(2,3),1:F(1,6),-1:F(1,6)}
    mass2={0:F(11,20),1:F(13,60),-1:F(13,60),2:F(1,120),-2:F(1,120)}
    stiff1={0:F(2),1:F(-1),-1:F(-1)}
    stiff2={0:F(1),1:F(-1,3),-1:F(-1,3),2:F(-1,6),-2:F(-1,6)}
    out=[]
    others=[j for j in range(3) if j!=axis]
    for kn in range(-2,3):
        for kt1,kt2 in itertools.product(range(-1,2),repeat=2):
            k=[0,0,0]; k[axis]=kn; k[others[0]]=kt1; k[others[1]]=kt2
            a=stiff2[kn]*mass1[kt1]*mass1[kt2]
            a+=mass2[kn]*stiff1[kt1]*mass1[kt2]
            a+=mass2[kn]*mass1[kt1]*stiff1[kt2]
            c=a*DEN
            assert c.denominator==1
            if c: out.append((tuple(k),int(c)))
    return out

def erosion(mask):
    active=mask.copy()
    for d in itertools.product(range(-1,2),repeat=3):
        active &= np.roll(mask,d,axis=(0,1,2))
    return active

def make_graph(active):
    shape=active.shape
    coords=np.argwhere(active)
    node=np.full(shape,-1,dtype=np.int64)
    node[tuple(coords.T)]=np.arange(len(coords))
    tails=[]; heads=[]; axes=[]; sites=[]; fmap=[]
    for ax in range(3):
        paired=active & np.roll(active,-1,axis=ax)
        pos=np.argwhere(paired)
        dst=pos.copy();dst[:,ax]=(dst[:,ax]+1)%shape[ax]
        idx=np.arange(len(tails),len(tails)+len(pos),dtype=np.int64)
        fm=np.full(shape,-1,dtype=np.int64);fm[tuple(pos.T)]=idx;fmap.append(fm)
        tails.extend(node[tuple(pos.T)]);heads.extend(node[tuple(dst.T)])
        axes.extend([ax]*len(pos));sites.extend(pos)
    tail=np.array(tails,dtype=np.int64); head=np.array(heads,dtype=np.int64)
    axis=np.array(axes,dtype=np.int64); site=np.array(sites,dtype=np.int64).reshape(-1,3)
    ne=len(tail);nv=len(coords)
    D=sp.coo_matrix((np.r_[np.ones(ne),-np.ones(ne)],
                    (np.r_[tail,head],np.r_[np.arange(ne),np.arange(ne)])),shape=(nv,ne)).tocsr()
    return coords,tail,head,axis,site,fmap,D

def forest(tail,head,axis,nv):
    adj=[[] for _ in range(nv)]
    for e,(a,b,ax) in enumerate(zip(tail,head,axis)):
        adj[a].append((int(b),e,-1,int(ax))) # D_child,e=-1
        adj[b].append((int(a),e,+1,int(ax)))
    parent=np.full(nv,-1,dtype=np.int64); pe=np.full(nv,-1,dtype=np.int64)
    sign=np.zeros(nv,dtype=np.int64); order=[]; roots=[]
    lift=np.zeros((nv,3),dtype=np.int64)
    for root in range(nv):
        if parent[root]!=-1:continue
        parent[root]=root;roots.append(root);queue=[root]
        for v in queue:
            order.append(v)
            for w,e,sgn,ax in adj[v]:
                if parent[w]!=-1:continue
                parent[w]=v;pe[w]=e;sign[w]=sgn
                lift[w]=lift[v];lift[w,ax]+=-sgn
                queue.append(w)
    return parent,pe,sign,np.array(order),np.array(roots),lift

def energy_matrix(axis,site,fmap):
    n=len(axis);rr=[];cc=[];vv=[];links=[]
    for ax in range(3):
        rows=np.flatnonzero(axis==ax);p=site[rows]
        for d,c in stencil(ax):
            shifted=(p+np.array(d))%np.array(fmap[ax].shape)
            col=fmap[ax][tuple(shifted.T)];good=col>=0
            r=rows[good];s=col[good]
            rr.extend(r);cc.extend(s);vv.extend([c/DEN]*len(r))
            links.append((r,s,c))
    E=sp.coo_matrix((vv,(rr,cc)),shape=(n,n)).tocsc()
    E.sum_duplicates()
    assert (E-E.T).nnz==0
    return E,links

def repair(q,tail,head,parent,pe,sign,order,roots,bits):
    scale=1<<bits
    if np.max(np.abs(q),initial=0)*scale>=2**60:
        raise OverflowError('reduce dyadic precision')
    z=np.rint(q*scale).astype(np.int64)
    r=np.zeros((len(parent),q.shape[1]),dtype=np.int64)
    np.add.at(r,tail,z);np.add.at(r,head,-z)
    maxr=int(np.max(np.abs(r),initial=0))
    assert len(parent)*maxr+int(np.max(np.abs(z),initial=0))<2**61
    before=maxr
    for v in order[::-1]:
        if pe[v]<0: continue
        z[pe[v]]-=sign[v]*r[v]
        r[parent[v]]+=r[v];r[v]=0
    assert not np.any(r[roots])
    check=np.zeros_like(r);np.add.at(check,tail,z);np.add.at(check,head,-z)
    assert not np.any(check)
    return z,before

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--crop',type=int,default=48)
    ap.add_argument('--bits',type=int,default=32)
    args=ap.parse_args();t0=time.perf_counter();stages={}
    source=BASE/'source_cache/berea_100_to_300.npz'
    raw=source.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='3f1796cd3c5f6e854ebeb3316692e10f8a6c0c57'
    im=np.load(source)['im'];M=args.crop
    assert M>=6 and all(M<=s for s in im.shape)
    start=tuple((s-M)//2 for s in im.shape)
    Fmask=im[tuple(slice(a,a+M) for a in start)].copy()
    active=erosion(Fmask)
    coords,tail,head,axis,site,fmap,D=make_graph(active)
    assert len(tail)>0, 'Erosion leaves no face flow; no lower bound acquired'
    parent,pe,sign,order,roots,lift=forest(tail,head,axis,len(coords))
    winding=[]
    for e,(a,b,ax) in enumerate(zip(tail,head,axis)):
        w=lift[a]-lift[b];w=w.copy();w[ax]+=1
        assert not np.any(w%M)
        w=w//M
        if np.any(w):winding.append(tuple(int(j) for j in w))
    distinct_winding=sorted(set(winding))
    E,links=energy_matrix(axis,site,fmap)
    stages['geometry_and_assembly']=time.perf_counter()-t0
    keep=np.ones(len(coords),dtype=bool);keep[roots]=False
    Dr=D[keep]
    A=sp.bmat([[E,Dr.T],[Dr,None]],format='csc')
    force=np.zeros((len(tail),3));force[np.arange(len(tail)),axis]=1
    rhs=np.vstack([force,np.zeros((Dr.shape[0],3))])
    t1=time.perf_counter()
    factor=sla.splu(A)
    solution=factor.solve(rhs);q=solution[:len(tail)]
    stages['ordinary_spline_Stokes_factor_and_solve']=time.perf_counter()-t1
    residual=float(np.max(np.abs(A@solution-rhs)))
    point=force.T@q/(M**3)
    t2=time.perf_counter()
    z,round_div=repair(q,tail,head,parent,pe,sign,order,roots,args.bits)
    stages['exact_divergence_repair']=time.perf_counter()-t2
    np.savez_compressed(BASE/'CURRENTS.npz',pore_mask=Fmask,active=active,
        coords=coords,tail=tail,head=head,axis=axis,site=site,current_numerators=z,
        dyadic_bits=np.array(args.bits))
    import sympy as sy
    J=sy.Matrix([[sum(int(x) for x in z[axis==ax,col]) for col in range(3)] for ax in range(3)])
    rank=int(sy.Matrix(distinct_winding).rank()) if distinct_winding else 0
    receipt=dict(status='NUMERICAL_CURRENTS_ACQUIRED_EXACT_CONSUMER_PENDING',
        source=dict(url='https://github.com/PMEAL/OpenPNM/blob/dev/tests/fixtures/berea_100_to_300.npz',
            git_blob_sha='3f1796cd3c5f6e854ebeb3316692e10f8a6c0c57',
            sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),full_shape=list(im.shape),
            full_porosity=float(im.mean()),crop_shape=list(Fmask.shape),crop_start=list(start),
            crop_rule='predeclared centered 48-cube, periodically tiled, no crop search',
            voxel_size_metres='1069/200000000',physical_inclusion_qualified=False,
            representative_volume_qualified=False),
        geometry=dict(pore_cells=int(Fmask.sum()),eroded_active_cells=int(active.sum()),
            current_edges=len(tail),components=len(roots),winding_vectors=distinct_winding,
            winding_span_rank=rank,current_mean_rank=int(J.rank())),
        ordinary_matched_spline_solver=dict(KKT_shape=list(A.shape),KKT_nnz=A.nnz,
            LU_nnz=int(factor.L.nnz+factor.U.nnz),residual_max=residual,
            permeability_point_in_voxel_squared=point.tolist(),validated_linear_solve=False),
        exact_repair=dict(bits=args.bits,rounded_divergence_max_numerator=round_div,
            repaired_divergence_exactly_zero=True,current_integer_mean=[[str(x) for x in row] for row in J.tolist()],
            largest_current_numerator=max(abs(int(x)) for x in z.flat)),
        costs=dict(stages=stages,total_wall_seconds=time.perf_counter()-t0,
            physical_measurements=0,paid_compute=0,source_bytes_downloaded=len(raw)),
        remaining='Run consume_transport.py. Numerical point prediction is not an upper or exact continuum value.')
    (BASE/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'geometry':receipt['geometry'],
        'ordinary_solver':receipt['ordinary_matched_spline_solver'],
        'costs':receipt['costs']},indent=2))

if __name__=='__main__':main()
