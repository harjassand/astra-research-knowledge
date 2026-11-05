"""Sparse exact-operation diagnostics for 2D vacuum padding.
No Hilbert-space truncation: states produced by H on a one-particle vector
are enumerated completely. Numerical output is not a certified SDP bound.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import json
import numpy as np
rng=np.random.default_rng(581923)
B=rng.normal(size=(15,15))+1j*rng.normal(size=(15,15))
Q,_=np.linalg.qr(B)
h=np.zeros((16,16),complex)
h[1:,1:]=(Q*np.linspace(1,2,15))@Q.conj().T
K=[(0,0),(1,0),(0,1),(1,1)]
S=float(np.real(sum(h[1<<i,1<<j] for i in range(4) for j in range(4))))

def local_output(anchor,inside,amplitude=1.):
    pts=[(anchor[0]+x,anchor[1]+y) for x,y in K]
    inp=[j for j,p in enumerate(pts) if inside(p)]
    result={}
    for mask in range(1,16):
        z=amplitude*sum(h[mask,1<<j] for j in inp)
        if abs(z)>1e-15:
            result[frozenset(pts[j] for j in range(4) if mask>>j&1)]=z
    return result

def dot(a,b):return sum(np.conj(v)*b.get(k,0) for k,v in a.items())
def add(a,b):
    for k,v in b.items():a[k]=a.get(k,0)+v

base=local_output((0,0),lambda _:True)
a=dot(base,base).real/S
out=[]
for L in [2,3,4,8,16,32]:
    v=a
    for dx in range(-L+1,L):
        for dy in range(-L+1,L):
            if (dx,dy)!=(0,0):
                v+=dot(base,local_output((dx,dy),lambda _:True)).real/S
    u=L+1
    inside=lambda p: 0<=p[0]<u and 0<=p[1]<u
    interior={};seam={}
    for x in range(-1,u):
        for y in range(-1,u):
            z=local_output((x,y),inside,1/u)
            add(interior if 0<=x<L and 0<=y<L else seam,z)
    total=interior.copy();add(total,seam)
    weight=u*u/S
    energy_core=weight*sum(interior.get(frozenset([(x,y)]),0) for x in range(u) for y in range(u)).real/u
    energy_total=weight*sum(total.get(frozenset([(x,y)]),0) for x in range(u) for y in range(u)).real/u
    core_square=weight*dot(interior,interior).real
    seam_square=weight*dot(seam,seam).real
    cross=2*weight*dot(interior,seam).real
    total_square=weight*dot(total,total).real
    assert abs(energy_core-L*L)<1e-9*L*L
    assert abs(total_square-core_square-seam_square-cross)<1e-8
    out.append(dict(L=L,dual_objective=float(v),core_energy=float(energy_core),padded_energy=float(energy_total),core_second=float(core_square),seam_second=float(seam_square),cross=float(cross),padded_second=float(total_square),second_over_volume_minus_v=float(total_square/L**2-v),seam_second_per_L=float(seam_square/L),cross_per_L=float(cross/L),sparse_output_configurations=len(total)))

# Small periodic Hamiltonian establishes a concrete noncommuting entangled example.
n=3;ns=n*n;dim=1<<ns
H=np.zeros((dim,dim),complex)
for x in range(n):
  for y in range(n):
    sites=[((x+dx)%n)+n*((y+dy)%n) for dx,dy in K]
    clear=sum(1<<s for s in sites)
    for state in range(dim):
      local=sum(((state>>s)&1)<<j for j,s in enumerate(sites))
      rem=state&~clear
      for mask in range(16):
        z=h[mask,local]
        if abs(z)>1e-15:
          dest=rem+sum(((mask>>j)&1)<<s for j,s in enumerate(sites))
          H[dest,state]+=z
w=np.linalg.eigvalsh(H)
# A fixed finite edge coloring schedules CZ layers after one on-site H layer.
edges=set()
for x in range(n):
  for y in range(n):
    i=x+n*y
    for dx,dy in [(1,0),(0,1)]:edges.add(tuple(sorted((i,(x+dx)%n+n*((y+dy)%n)))))
phase=np.array([(-1)**sum(((s>>i)&1)*((s>>j)&1) for i,j in edges) for s in range(dim)])
U=np.array([[(-1)**((i&j).bit_count()) for j in range(dim)] for i in range(dim)],float)/np.sqrt(dim)
U=phase[:,None]*U
Ht=U@H@U.conj().T
wt=np.linalg.eigvalsh(Ht)
ground=phase/np.sqrt(dim)
mat=ground.reshape(2,-1);rdm=mat@mat.conj().T
vals=np.linalg.eigvalsh(rdm)
# Two overlapping translates on a 3 by 2 region need not commute.
def embed6(anchor):
    op=np.zeros((64,64),complex)
    sites=[anchor[0]+dx+3*(anchor[1]+dy) for dx,dy in K]
    clear=sum(1<<z for z in sites)
    for state in range(64):
        local=sum(((state>>z)&1)<<j for j,z in enumerate(sites))
        rem=state&~clear
        for mask in range(16):
            dest=rem+sum(((mask>>j)&1)<<z for j,z in enumerate(sites))
            op[dest,state]+=h[mask,local]
    return op
hx,hy=embed6((0,0)),embed6((1,0))
commutator_norm=float(np.linalg.norm(hx@hy-hy@hx,2))
assert commutator_norm>1e-3
summary=dict(overlapping_translate_commutator_norm=commutator_norm,h_min_positive=float(np.linalg.eigvalsh(h)[1]),h_norm=float(np.linalg.norm(h,2)),h_single_particle_coherent_weight=S,padding=out,periodic_3x3_gap=float(w[1]),periodic_3x3_ground_multiplicity=int((abs(w)<1e-9).sum()),circuit_spectral_max_error=float(np.max(abs(w-wt))),cluster_ground_residual=float(np.linalg.norm(Ht@ground)),cluster_single_site_entropy_bits=float(-sum(x*np.log2(x) for x in vals if x>1e-14)))
np.save(Path(__file__).with_name('interaction.npy'),h)
Path(__file__).with_name('padding_results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
