import json
import numpy as np
from pathlib import Path
N=7
D=1<<N
rows=[0b0001111,0b0110011,0b1010101]
C=[0]
for r in rows:
    C += [v^r for v in C.copy()]
z0=np.zeros(D,complex); z0[C]=1/np.sqrt(len(C))
z1=z0[np.arange(D)^127]
# state indices: source A low seven, target B next seven, reference high bit
base=np.zeros(1<<15,complex)
for r,za in enumerate([z0,z1]):
    for a in np.nonzero(za)[0]:
        for b in C:
            base[int(a)+(b<<7)+(r<<14)]=za[a]*z0[b]/np.sqrt(2)
idx=np.arange(base.size)
cnot_idx=idx^((idx&127)<<7)
def pauli_state(v,x,z,n):
    ids=np.arange(v.size)
    signs=np.array([(-1)**((int(j)&z).bit_count()) for j in ids])
    ans=np.empty_like(v); ans[ids^x]=signs*v
    return ans

def h(v,k):
    w=v.reshape((-1,1<<(k+1))).copy(); lo=w[:,:1<<k].copy(); hi=w[:,1<<k:].copy()
    w[:,:1<<k]=(lo+hi)/np.sqrt(2);w[:,1<<k:]=(lo-hi)/np.sqrt(2)
    return w.reshape(-1)
ideal=np.concatenate([z0,z1])/np.sqrt(2)
rng=np.random.default_rng(20261102)
patterns=[(0,0),(127,0),(0,127),(127,127)]+[(int(rng.integers(D)),int(rng.integers(D))) for _ in range(28)]
minimum=1.; branches=0; norm_error=0.
for x,z in patterns:
    state=pauli_state(base,x<<7,z<<7,15)
    out=np.empty_like(state);out[cnot_idx]=state
    for j in range(7):out=h(out,j)
    target=pauli_state(ideal,x,z,8)
    total=0
    for m in range(128):
        branch=out[m::128].copy();p=float(np.vdot(branch,branch).real);total+=p
        if p<1e-14:continue
        # source target-Z propagation shifts the logical X-measurement parity
        if ((m^z).bit_count()%2):branch=pauli_state(branch,0,127,8)
        fidelity=float(abs(np.vdot(target,branch/np.sqrt(p)))**2)
        minimum=min(minimum,fidelity);branches+=1
    norm_error=max(norm_error,abs(total-1))
result={"code":"Steane [[7,1,3]]", "reference":"one external Bell reference", "signed_target_Paulis":len(patterns),"nonzero_measurement_branches":branches,"minimum_reference_safe_branch_fidelity":minimum,"maximum_total_probability_error":norm_error,"scope":"Exact ideal signed-syndrome one-bit teleportation identity only; not circuit-level fault threshold or native thermal basin."}
assert minimum>1-1e-12 and norm_error<1e-12
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
