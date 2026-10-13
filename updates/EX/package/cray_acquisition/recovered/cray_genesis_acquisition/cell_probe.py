#!/usr/bin/env python3
"""All-data cell-coarsening diagnostic on a 64 x 64 synthetic network.

This experiment ACQUIRES EVERY TARGET COEFFICIENT. It tests gap reduction,
not a sublinear acquisition claim. Terminals are contracted before the cell
construction, as required for the single-cell exactness theorem.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from experiment import make_network, cases


def laplacian(edges, c, n):
    u,v=edges.T
    return sparse.coo_matrix((np.r_[c,c,-c,-c],
          (np.r_[u,v,u,v],np.r_[u,v,v,u])),shape=(n,n)).tocsr()


def run():
    net=make_network((64,64,1))
    ratios=cases(net)['strong_mismatch']
    nx,ny,_=net.shape
    old_ids=np.arange(nx*ny)
    x,y=old_ids//ny, old_ids%ny
    mapped=np.where(x==0,0,np.where(x==nx-1,1,2+(x-1)*ny+y))
    ed=mapped[net.edges]
    keep=ed[:,0]!=ed[:,1]
    original_tail=net.edges[keep,0]
    ed=ed[keep]
    c0=net.c0[keep]
    c=c0*ratios[keep]
    n=int(ed.max())+1
    h0=np.empty(n); h0[:2]=[0.,1.]
    h0[2:]=np.repeat(np.arange(1,nx-1)/(nx-1),ny)
    dh0=h0[ed[:,0]]-h0[ed[:,1]]
    f0=c0*dh0
    C0=float(np.dot(c0,dh0**2))
    L=laplacian(ed,c,n)
    h=h0.copy(); h[2:]=0
    h[2:]=spsolve(L[2:,2:].tocsc(),-(L@h)[2:])
    C=float(np.dot(c,(h[ed[:,0]]-h[ed[:,1]])**2))
    total_degree=np.bincount(ed.ravel(),minlength=n)
    results=[]
    for side in [1,2,4,8,16,32,64]:
        started=time.perf_counter()
        gid=(original_tail//ny//side)*((ny+side-1)//side)+(original_tail%ny//side)
        Dsum=Nsum=0.
        count=0
        max_edges=0
        for g in np.unique(gid):
            K=np.flatnonzero(gid==g)
            count+=1; max_edges=max(max_edges,len(K))
            nodes, inv=np.unique(ed[K].ravel(),return_inverse=True)
            localedges=inv.reshape(-1,2)
            E0=float(np.dot(c0[K],dh0[K]**2))
            if E0==0:
                continue
            nn=len(nodes)
            local_degree=np.bincount(localedges.ravel(),minlength=nn)
            fixed=(local_degree<total_degree[nodes]) | (nodes<2)
            localL=laplacian(localedges,c[K],nn)
            trial=h0[nodes].copy()
            free=np.flatnonzero(~fixed)
            trial[free]=0.
            if len(free):
                trial[free]=spsolve(localL[free][:,free].tocsc(),-(localL@trial)[free])
            u,v=localedges.T
            Dsum+=float(np.dot(c[K],(trial[u]-trial[v])**2))
            b=np.bincount(u,weights=f0[K],minlength=nn)-np.bincount(v,weights=f0[K],minlength=nn)
            z=np.zeros(nn)
            z[1:]=spsolve(localL[1:,1:].tocsc(),b[1:])
            Nsum+=float(np.dot(c[K],(z[u]-z[v])**2))
        lower,upper=C0*C0/Nsum,Dsum
        results.append({'side':side,'cells':count,'largest_cell_edges':max_edges,
                        'unique_target_coefficients_acquired':len(c),
                        'lower':lower,'upper':upper,'relative_gap':upper/lower-1,
                        'contains_float64_reference':lower<=C+1e-8 and C<=upper+1e-8,
                        'compute_seconds':time.perf_counter()-started})
    return {'status':'float64 full-data gap-reduction diagnostic, NOT acquisition savings',
            'shape':[64,64], 'original_vertices':4096,'contracted_vertices':n,
            'original_edges':len(net.edges),'retained_edges':len(ed),
            'C0':C0,'target_C':C,'target_case':'strong_mismatch', 'results':results}


if __name__=='__main__':
    r=run()
    Path(__file__).with_name('cell_results.json').write_text(json.dumps(r,indent=2))
    print(json.dumps(r,indent=2))
