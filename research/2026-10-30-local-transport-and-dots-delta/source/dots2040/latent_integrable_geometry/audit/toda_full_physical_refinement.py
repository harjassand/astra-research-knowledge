"""Precision refinement of actual physical bridge: eps 2^-52, q288.
Original main and decoder are reused, with only per-call rounding/perturbation
parameters overridden. Output is separate; no baseline artifacts overwritten.
"""
from pathlib import Path
import hashlib,json
import toda_full_physical_bridge as bridge
base_source=Path(bridge.__file__)
original=bridge.r.run_case

def refined(name,D0,D,qbits,epsbits,perturb=True,kernel_choice=0):
    return original(name,D0,D,288,52,perturb,kernel_choice)

if __name__=='__main__':
    bridge.r.run_case=refined
    bridge.__file__=__file__
    bridge.main()
    path=Path(__file__).with_suffix('.json');data=json.loads(path.read_text())
    data['reused_bridge_source_sha256']=hashlib.sha256(base_source.read_bytes()).hexdigest()
    data['refinement']='Only matrix rounding q256→q288 and perturbation eps2^-44→eps2^-52 changed.'
    path.write_text(json.dumps(data,indent=2))
