"""Adversarial and exact geometric tests, separate from the infinite-volume proof."""
from pathlib import Path
from fractions import Fraction as F
import json, tempfile, time, random
import numpy as np
from verify_module import verify
from coarse_flow import current,divergence
from completed_current import CompletedCurrent
from certificate_bounds import radius_tail_energy,gate_probability,coarse_energy_majorant,mmul,mpow
ROOT=Path(__file__).parent;start=time.perf_counter()
result=verify()
# Reject a single-unit perturbation, without altering the authentic certificate.
with tempfile.TemporaryDirectory() as temp:
    data=dict(np.load(ROOT/'module_flow.npz',allow_pickle=False))
    data['flow']=data['flow'].copy();data['flow'][0]+=1
    corrupt=Path(temp)/'corrupt.npz';np.savez(corrupt,**data)
    try:verify(corrupt)
    except ValueError as exc:
        assert 'source--sink' in str(exc)
    else:raise AssertionError('Corrupted current was not rejected')
# A finite obstacle field suffices to check the exact geometric identities.
obstacles=[{(0,0)}, {(0,0),(1,1)}, {(0,0),(0,1),(0,2)},
           {(0,0),(1,0),(2,1),(3,1)}, {(0,0),(2,0),(2,2)}]
vertices=[(x,y)for x in range(-5,10)for y in range(-5,10)]
max_defect=F(0)
for badset in obstacles:
    bad=badset.__contains__
    assert all(divergence(x,bad)==0 for x in vertices)
    assert sum((current(x,0,bad)-1 for x in vertices),F(0))==0
    assert sum((current(x,1,bad)for x in vertices),F(0))==0
    for x in vertices:
        for direction in (0,1):
            y=(x[0]+(direction==0),x[1]+(direction==1))
            if x in badset or y in badset:
                assert current(x,direction,bad)==current(x,direction,bad,1)==0
        max_defect=max(max_defect,abs(divergence(x,bad,1)))
assert max_defect>0   # truncated currents really retain defects
# Verify the local chordless-path transition counts geometrically.
steps=[(a,b)for a in (-1,0,1)for b in (-1,0,1)if(a,b)!=(0,0)]
counts=[]
for previous in ((1,0),(1,1)):
    choices=[d for d in steps if max(abs(previous[0]+d[0]),abs(previous[1]+d[1]))>=2]
    counts.append([sum((d[0]==0 or d[1]==0)for d in choices),
                   sum((d[0]!=0 and d[1]!=0)for d in choices)])
assert counts==[[1,2],[2,3]]
# Exact tail formula dominates direct finite summation of its matrix series.
b=F(1,10);A=((b,2*b),(2*b,3*b))
def Pbound(r):
    if r==1:return 4*b
    B=mpow(A,r-2)
    return 16*b*b*sum(B[i][j]for i in range(2)for j in range(2))
for cutoff in (0,1,2,5,10):
    direct=(cutoff+1)**2*Pbound(cutoff+1)+sum(F(2*r-1)*Pbound(r)for r in range(cutoff+2,120))
    assert radius_tail_energy(b,cutoff)>=direct
b40=1-gate_probability(F(2,5))
assert 1-4*b40-b40*b40>0
try:coarse_energy_majorant(F(1,4))
except ValueError:pass
else:raise AssertionError('A non-subcritical tail was accepted')
# Evaluate the microscopic current itself. The test field has finitely many
# occupied sites, so all bad clusters are finite and exact evaluation terminates.
rng=random.Random(7941)
occupied={ (x,y)for x in range(-9,10)for y in range(-9,10)if rng.random()<0.3 }
eta=lambda z:int(z in occupied)
J=CompletedCurrent();samples=[]
for x,d in [((-3,-3),0),((-3,-3),1),((-3,-2),0),((-3,-2),1)]:
    y=(x[0]+(d==0),x[1]+(d==1))
    swapped=lambda z,x=x,y=y:eta(y)if z==x else eta(x)if z==y else eta(z)
    value=J.bond(x,d,eta,None)
    assert value != 0
    assert J.bond(x,d,swapped,None)==-value
    value_R=J.bond(x,d,eta,1)
    assert J.bond(x,d,swapped,1)==-value_R
    shift=(1,2)
    shifted_eta=lambda z:eta((z[0]+shift[0],z[1]+shift[1]))
    assert J.bond(x,d,shifted_eta,None)==J.bond((x[0]+shift[0],x[1]+shift[1]),d,eta,None)
    samples.append({'site':x,'direction':d,'completed':str(value),'cutoff_1':str(value_R)})
blocked={(0,0),(-1,0),(0,-1),(0,1)}
assert J.bond((0,0),0,lambda z:int(z in blocked),None)==0
out={'passed':True,'corruption_rejected':True,'coarse_divergence_exact':True,
     'coarse_total_flux_checked':True,'largest_truncated_divergence_seen':str(max_defect),
     'hard_legality_checked':True,'microscopic_antisymmetry_checked':True,
     'unit_translation_covariance_checked':True,'current_samples':samples,
     'wall_seconds':time.perf_counter()-start}
(ROOT/'selftest_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
