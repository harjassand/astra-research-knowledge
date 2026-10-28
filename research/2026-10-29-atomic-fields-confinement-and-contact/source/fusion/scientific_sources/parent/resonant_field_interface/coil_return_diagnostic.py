"""Actual finite-coil linearized return integrals; sampled diagnostics only."""
from pathlib import Path
import sys,shutil,hashlib,json,time
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
src=ROOT.parent.parent/'capability_backward_bridge/code'
runtime=ROOT/'coil_runtime';runtime.mkdir(exist_ok=True)
hashes={}
for name in ['lopez_field.py','lopez_coils.py']:
    raw=(src/name).read_bytes();hashes[name]=hashlib.sha256(raw).hexdigest()
    (runtime/name).write_bytes(raw)
sys.path.insert(0,str(runtime))
from lopez_field import X,derivative,B_at_labels
from lopez_coils import field
rows=[];start=time.monotonic()
for N,rcoil,P in [(128,1.5,257),(128,1.5,513),(256,1.2,513),(256,1.2,769)]:
    ph=2*np.pi*(np.arange(P)+.173)/P
    for lam,beta in [(.15,.02),(.15,.07)]:
        targets=X(lam,beta,ph).T
        xl=derivative(lam,beta,ph,0).T;xb=derivative(lam,beta,ph,1).T;xp=derivative(lam,beta,ph,2).T
        wl=2*lam*np.cross(xb,xp);wb=2*lam*np.cross(xp,xl)
        b0=B_at_labels(lam,beta,ph).T
        # Uniform-bias derivative is an independent check against area formula.
        polynomial=9-lam+lam*lam-lam**3
        uniform=-16*np.pi*lam**3*polynomial/(1+lam)**7
        measured=float(2*np.pi*wb[:,1].mean())
        assert abs(measured-uniform)<2e-13
        bc=field(targets,N,512,rcoil=rcoil);err=bc-b0
        dl=float(2*np.pi*np.einsum('ij,ij->i',err,wl).mean())
        db=float(2*np.pi*np.einsum('ij,ij->i',err,wb).mean())
        row={'N':N,'rcoil':rcoil,'phase_count':P,'lambda':lam,'beta':beta,
             'max_sample_relative_field_error':float(np.max(np.linalg.norm(err,axis=1)/np.linalg.norm(b0,axis=1))),
             'linearized_one_transit_delta_lambda':dl,'linearized_one_transit_delta_beta':db,
             'uniform_y_bias_delta_beta_coefficient':uniform}
        rows.append(row);print(json.dumps(row),flush=True)
result={'status':'SAMPLED_LINEARIZED_COIL_RETURN_DIAGNOSTIC_NOT_TOPOLOGY_OR_PARTICLE_CERTIFICATE',
        'source_code_hashes':hashes,'rows':rows,'seconds':time.monotonic()-start,
        'limits':'No uniform quadrature/error enclosure; one-transit first-order integrals about source orbits; not actual perturbed trajectories or a confinement certificate.'}
(ROOT/'COIL_RETURN_DIAGNOSTIC.json').write_text(json.dumps(result,indent=2)+'\n')
