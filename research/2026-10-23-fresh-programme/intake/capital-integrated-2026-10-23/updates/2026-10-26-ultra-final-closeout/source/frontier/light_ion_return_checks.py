#!/usr/bin/env python3
"""Independent energy-gradient check, inventories, and tighter method replay."""
import json
import numpy as np
from scipy.integrate import solve_ivp
import finite_ion_model as f
import finite_ion_checks as fc
import light_ion_return_model as m


def replay(current,nat,seconds,method,rtol=2e-9,max_step=2.):
    bath=f.ClosedBath();inj=bath.integrate(bath.initial(),600.,pump=0.,rtol=2e-9)
    initial=inj.y[:,-1];cell=m.LightCell(current_max_pa=current)
    y=np.r_[initial,np.zeros(4)]
    def fun(t,z):
        core=cell.rhs(t,z[:13],nat=nat)
        diss=-fc.energy_derivative(cell.bath,z[:10],pump=0.,nat=nat)
        return np.r_[core,diss]
    atols=np.r_[1e-8,np.full(3,1e-11),np.full(3,1e-10),1e-7,1e-10,1e-10,1e-10,np.full(3,1e-20)]*(rtol/2e-9)
    sol=solve_ivp(fun,(0.,seconds),y,method=method,rtol=rtol,atol=atols,
        t_eval=np.linspace(0,seconds,501),max_step=max_step)
    if not sol.success:raise RuntimeError(sol.message)
    handoff=cell.integrate(sol.y[:13,-1],1800.,light=0.,metabolism=1.,rtol=2e-9)
    max_gradient_error=0.;min_passive_diss=1.;min_motor_diss=1.;max_balance=0.
    mass=np.zeros(4);maxcharge=0.
    G0=fc.free_energy(bath,y[:10])
    for z in sol.y.T:
        dz=fun(0,z)
        # Complex-step differentiation of the complete independent G expression.
        exact=np.imag(fc.free_energy(bath,z[:10].astype(complex)+1j*1e-20*dz[:10]))/1e-20
        ip,cost,aff=cell.pump(z,1.)
        rate=-dz[13]+ip*1000/m.d.F*1e-15*cost
        max_gradient_error=max(max_gradient_error,abs(exact-rate))
        min_passive_diss=min(min_passive_diss,dz[13])
        min_motor_diss=min(min_motor_diss,ip*1000/m.d.F*1e-15*aff)
        # Useful ion work minus passive heat must equal net stored G.
        max_balance=max(max_balance,abs(fc.free_energy(bath,z[:10])-G0-z[11]+z[13]))
        ve,ce=bath.extracellular(z)
        mass=np.maximum(mass,np.abs([z[4]+ve*ce[0]-bath.total_na,
             z[5]+ve*ce[1]-bath.total_k,z[6]+ve*ce[2]-bath.total_cl,
             z[7]/1000+ve-bath.total_water]))
        maxcharge=max(maxcharge,abs(m.d.describe(z[:8])['charge_identity_error_mv']))
    gain=fc.free_energy(bath,sol.y[:10,-1])-G0
    z=sol.y[:,-1]
    return dict(current_max_pa=current,nat=nat,light_s=seconds,method=method,rtol=rtol,max_step_s=max_step,
      final_light=cell.describe(z),final_handoff=cell.describe(handoff.y[:,-1]),
      handoff_final_ionic_thresholds=m.healthy_final(handoff.y[:,-1]),
      net_light_ion_and_capacitor_free_energy_gain_j=gain,
      integrated_passive_ion_water_heat_j=float(z[13]),
      minimum_productive_photon_energy_j=float(z[12]),
      net_gradient_gain_per_minimum_productive_photon_energy=float(gain/z[12]),
      maximum_complex_step_energy_rate_error_w=max_gradient_error,
      maximum_integrated_ion_energy_balance_error_j=max_balance,
      minimum_sampled_passive_heat_rate_w=min_passive_diss,
      minimum_sampled_motor_affinity_heat_rate_w=min_motor_diss,
      maximum_mass_water_errors=mass.tolist(),maximum_charge_error_mv=maxcharge,
      minimum_voltage_mv=float(sol.y[0].min()),rhs_evaluations=sol.nfev+handoff.nfev)


def main():
    doc=dict(status='internal conservative/thermodynamic checks of added pure Na light-pump law',cases=[])
    for current,nat,seconds in [(150.,0.,200.),(350.,1.,120.),(100.,0.,600.)]:
      for method in ['BDF','Radau']:
        row=replay(current,nat,seconds,method);doc['cases'].append(row)
        (m.OUT/'light_ion_checks_results.json').write_text(json.dumps(doc,indent=2)+'\n')
        print(json.dumps(row),flush=True)
    # The native-channel rapid transition has method-dependent timing at the
    # first tighter tolerance. Refine it rather than reporting its quadratures
    # as converged just because both final basin classifiers agree.
    for method in ['BDF','Radau']:
        row=replay(350.,1.,120.,method,rtol=2e-11,max_step=.1)
        doc['cases'].append(row)
        (m.OUT/'light_ion_checks_results.json').write_text(json.dumps(doc,indent=2)+'\n')
        print(json.dumps(row),flush=True)


if __name__=='__main__':main()
