"""Audit 7-bit coherent carry/borrow, including relative phases and clean work."""
import json
from pathlib import Path
import numpy as np
from logical_circuit import Circuit,simulate

def main():
    rng=np.random.default_rng(101); rows=[]
    for inverse in [False,True]:
        for control_value in [0,1]:
            b=7; c=b; work=list(range(b+1,2*b-1)); C=Circuit(2*b-1)
            C.increment(list(range(b)),work,c,inverse=inverse,control_value=control_value)
            v=np.zeros(1<<C.nqubits,complex)
            v[:1<<(b+1)]=rng.normal(size=1<<(b+1))+1j*rng.normal(size=1<<(b+1)); v/=np.linalg.norm(v)
            target=np.zeros_like(v)
            for ell in range(1<<b):
                for control in [0,1]:
                    final=(ell+(-1 if inverse else 1))%(1<<b) if control==control_value else ell
                    target[final+(control<<b)]=v[ell+(control<<b)]
            out=simulate(C,v); phase=np.vdot(target,out)
            err=float(np.linalg.norm(out-target*phase/abs(phase))); assert err<1e-10
            rows.append({'bits':b,'inverse':inverse,'control_value':control_value,
                         'gates':len(C.gates),'binary64_norm_error':err})
    (Path(__file__).resolve().parent/'RIPPLE_AUDIT.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(rows,indent=2))

if __name__=='__main__': main()
