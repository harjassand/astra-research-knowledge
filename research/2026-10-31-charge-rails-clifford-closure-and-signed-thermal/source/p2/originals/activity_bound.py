"""Check the finite factory when idle dipole coupling is not perturbative.

The error parameter varied for derivatives acts only on the rotating cell.
All other cells may have a large dipole/source coupling. Charge-diagonal
holds are prolonged by exact logical periods. The source is retained.
This is a check of the finite density model, not a continuum or device fit.
"""
from pathlib import Path
import importlib.util
import json,math
import numpy as np
from scipy.linalg import expm,expm_frechet

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('factory',HERE/'bell_factory.py')
bf=importlib.util.module_from_spec(spec);spec.loader.exec_module(bf)
I2=np.eye(2);X=np.array([[0.,1.],[1.,0.]]);Z=np.diag([1.,-1.])
def norm(x):return float(np.linalg.norm(x,2))

def execute(active_error,idle_error,extra_periods=0,derivative=False):
    gap,j,stages=bf.setup()
    initial=np.array([[1.],[0.],[0.],[0.]])
    state=np.kron(np.kron(np.kron(initial,initial),initial),I2)
    ds=np.zeros_like(state,dtype=complex)
    es=[np.kron(bf.embed(bf.sq.Hd,k),X) for k in range(3)]
    bath=np.kron(np.eye(64),gap*Z/2)
    total=0.;active_time=0.
    for name,h,time in stages:
        if time is None:
            projector=np.zeros((4,4));projector[h,h]=1.
            projector=np.kron(bf.embed(projector,2),I2)
            state=projector@state;ds=projector@ds
            continue
        if name=='entangle_AB':time*=1+4*extra_periods
        elif name.startswith('meter_cap_'):time*=1+2*extra_periods
        active=None
        if name.startswith('prepare_quarter_'):active=int(name.rsplit('_',1)[1])
        elif name in ('meter_quarter_prepare','meter_quarter_analyze'):active=2
        perturbation=sum(idle_error*gap*es[k] for k in range(3) if k!=active)
        tangent=np.zeros((128,128),complex)
        if active is not None:
            perturbation+=active_error*gap*es[active]
            tangent=gap*es[active];active_time+=time
        generator=-1j*time*(np.kron(h,I2)+bath+perturbation)
        if derivative:
            u,du=expm_frechet(generator,-1j*time*tangent)
            ds=du@state+u@ds
        else:u=expm(generator)
        state=u@state;total+=time
    extract=np.kron(np.kron(np.eye(16),np.array([[1.,0.,0.,0.]])),I2)
    return extract@state,extract@ds,dict(coherent_time=total,active_hopping_time=active_time,
        active_error_action_per_unit_strength=gap*active_time)

def main():
    rows=[]
    for periods in (0,5):
        for idle in (0.,.1,3.):
            ideal,dideal,metadata=execute(0.,idle,periods,True)
            for active in (.01,.003):
                actual,_,_=execute(active,idle,periods)
                q=float(np.linalg.eigvalsh(I2-actual.conj().T@actual).max())
                e=norm(actual-ideal);action=active*metadata['active_error_action_per_unit_strength']
                rows.append(dict(extra_diagonal_periods=periods,idle_dipole_over_gap=idle,
                    active_dipole_over_gap=active,**metadata,
                    ideal_isometry_residual=norm(ideal.conj().T@ideal-I2),
                    accepted_first_active_derivative=norm(dideal),accepted_isometry_error=e,
                    worst_reject_probability=q,accepted_action_bound=action**2/2,
                    complete_instrument_half_diamond_upper_bound_from_matrices=e+q/2,
                    complete_instrument_half_diamond_action_bound=min(1.,action**2)))
    out=dict(scope='Six active quarter pulses; arbitrary charge-diagonal dipole/source dynamics on held cells are included exactly. Extra holds add full logical periods. Ordinary matrix-exponential precision; not a rounding enclosure.',rows=rows)
    (HERE/'activity_bound_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
