"""Independent finite diagnostics for the written environmental hierarchy proof."""
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np

def annihilator(n,j):
    a=np.zeros((1<<n,1<<n))
    for x in range(1<<n):
        if (x>>j)&1:
            a[x^(1<<j),x]=(-1)**((x&((1<<j)-1)).bit_count())
    return a

exact=[]
for r in range(2,82):
    delta=F(1,8*r);a=F(r,2*(4*r*r+1));v=F(-1,2*r)
    rayleigh=(r*v*v+v+delta)/(v*v+1)
    assert rayleigh==-a
    assert r*delta-F(1,4)==F(-1,8)
    assert (3*r)*delta-F(1,4)==F(1,8)
    assert F(2*r+1)-F(1,4)>0
    exact.append(dict(r=r,a=str(a),negative_determinant='-1/8',positive_determinant='1/8',rayleigh=str(rayleigh)))

fock=[];canonical=[]
for r in range(2,8):
    n=r+1;dim=1<<n;delta=1/(8*r);a=r/(2*(4*r*r+1))
    d=annihilator(n,0);c=annihilator(n,1)
    coupling=(d.T@c+c.T@d)/2
    assert np.linalg.norm(coupling,2)<=.5+1e-13
    nb=np.array([(x>>1).bit_count() for x in range(dim)])
    nd=np.array([x&1 for x in range(dim)])
    full=(nb==r).astype(float)
    charges=nb+nd
    matrices={}
    for label,ub in [('quad',0),('hidden',-r+delta)]:
        for design,m in [(1,1),(0,2*r+1)]:
            scalar=0 if design==1 else -a/2
            matrices[label,design]=np.diag(nb+ub*full+m*nd+scalar)+coupling
    energies={str(k):float(np.linalg.eigvalsh(h)[0]) for k,h in matrices.items()}
    contrast_q=energies[str(('quad',1))]-energies[str(('quad',0))]
    contrast_h=energies[str(('hidden',1))]-energies[str(('hidden',0))]
    assert abs(contrast_q-a/2)<2e-12
    assert contrast_h<=-a/2+2e-12
    assert abs(energies[str(('hidden',0))]+a/2)<2e-12
    lower=(r+delta-np.sqrt((r-delta)**2+1))/2
    assert abs(energies[str(('hidden',1))]-lower)<2e-12
    fock.append(dict(r=r,dimension=dim,energies=energies,quadratic_contrast=contrast_q,hidden_contrast=contrast_h,certified_margin=a/2))
    for q in range(r):
        idx=np.where(charges==q)[0]
        for design in [0,1]:
            assert np.array_equal(matrices['quad',design][np.ix_(idx,idx)],matrices['hidden',design][np.ix_(idx,idx)])
        canonical.append(dict(r=r,total_charge=q,sector_dimension=len(idx),operator_equality=True))

def heisenberg_apply(v,energies,j,dagger,time):
    z=np.exp(-1j*time*energies)*v
    out=np.zeros_like(z)
    for x in range(len(z)):
        occupied=(x>>j)&1
        if occupied==int(not dagger):
            out[x^(1<<j)]+=(-1)**((x&((1<<j)-1)).bit_count())*z[x]
    return np.exp(1j*time*energies)*out

rng=np.random.default_rng(7872026);correlators=[];distinguishing=[]
for r in range(2,8):
    dim=1<<r;quad=np.array([x.bit_count() for x in range(dim)],float)
    hidden=quad.copy();hidden[-1]=1/(8*r)
    for m in range(1,r):
        for trial in range(12):
            modes=rng.choice(r,size=m,replace=False).tolist()
            left=modes.copy();rng.shuffle(left)
            # Rightmost creations act before the left annihilation sequence.
            ops=[(j,False,float(rng.uniform(-3,3))) for j in left]+[(j,True,float(rng.uniform(-3,3))) for j in modes]
            values=[]
            for energies in [quad,hidden]:
                v=np.zeros(dim,complex);v[0]=1
                for j,dagger,time in reversed(ops):v=heisenberg_apply(v,energies,j,dagger,time)
                values.append(v[0])
            assert abs(values[0]-values[1])<1e-13
            assert abs(abs(values[0])-1)<1e-12
            correlators.append(dict(r=r,probe_pairs=m,absolute_difference=float(abs(values[0]-values[1]))))
    full_values=[]
    ops=[(j,False,.7) for j in range(r)]+[(j,True,0.) for j in range(r)]
    for energies in [quad,hidden]:
        v=np.zeros(dim,complex);v[0]=1
        for j,dagger,time in reversed(ops):v=heisenberg_apply(v,energies,j,dagger,time)
        full_values.append(v[0])
    assert abs(full_values[0]-full_values[1])>1e-3
    distinguishing.append(dict(r=r,probe_pairs=r,difference=float(abs(full_values[0]-full_values[1]))))

result=dict(status='PASS',exact_rational_fixtures=exact,full_fock_fixtures=fock,fixed_sector_equalities=canonical,vacuum_correlators=correlators,higher_order_distinguishers=distinguishing,scope='Written all-k proof separate. Exact rational identities vs floating CAR/eigenvalue/correlator diagnostics. No producer imports, historical-priority or physical-validation claim.')
Path('hierarchy_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status='PASS',rational=len(exact),full_fock=len(fock),fixed_sectors=len(canonical),low_order_correlators=len(correlators),higher_order_distinguishers=len(distinguishing)),indent=2))
