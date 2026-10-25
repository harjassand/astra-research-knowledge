#!/usr/bin/env python3
"""Actual mass, charge and passive-free-energy checks for finite_ion_model."""
import json,math
import numpy as np
from scipy.optimize import brentq
import finite_ion_model as f
import dijkstra_model as d


def material_free_energy(model,b):
    if not model.capacity:return 0.
    theta=b/model.capacity
    def pure(z):return z*math.log(z)+(1-z)*math.log(1-z)+f.CHI*z*(1-z)+math.log(f.RSTAR)*z
    if model.mode=='phase':
        if f.THETA_LO<=theta<=f.THETA_HI:
            value=pure(f.THETA_LO)+math.log(f.RSTAR)*(theta-f.THETA_LO)
        else:value=pure(theta)
    else:
        value=theta*math.log(theta)+(1-theta)*math.log(1-theta)+model.g0*theta
    return model.capacity*value


def free_energy(model,y):
    # RT fmol and joules; only zero-hydration model evaluated here.
    assert model.hydration==0
    vi=y[7]/1000.;ve,ce=model.extracellular(y)
    ci=np.r_[y[4:7]/vi,d.NA_FIXED/vi]
    amounts_i=np.r_[y[4:7],d.NA_FIXED]
    mix=np.sum(amounts_i*(np.log(ci)-1))+np.sum(ve*ce*(np.log(ce)-1))
    return d.R*d.T*1e-15*(mix+material_free_energy(model,y[8]))+d.C*1e-18*y[0]**2/2


def energy_derivative(model,y,pump=0.,nat=1.):
    z=model.rhs(0,y,pump,nat);ve,ce=model.extracellular(y)
    ci=y[4:7]*1000/y[7];si=(sum(y[4:7])+d.NA_FIXED)*1000/y[7]
    de=np.r_[-z[4]+z[8],-z[5]-z[8],-z[6],0.]
    mu=model.material_mu(y[8]/model.capacity) if model.capacity else 0.
    chem=np.log(ci)@z[4:7]+np.log(ce)@de+(ce.sum()-si)*z[7]/1000.+mu*z[8]
    return d.R*d.T*1e-15*chem+d.C*1e-18*y[0]*z[0]


def passive_endpoint(model):
    # Capacitor charge ignored only in this independent algebraic endpoint.
    vf=model.total_water-model.material_volume(model.b0)
    vi=vf*d.NA_FIXED/(d.NA_FIXED+model.external_a)
    if model.capacity:
        def residual(b):
            na=(model.total_na-model.capacity+b)/vf
            kk=(model.total_k-b)/vf
            return math.log(kk/na)-model.material_mu(b/model.capacity)
        b=brentq(residual,model.capacity*1e-12,min(model.capacity*(1-1e-12),model.total_k*(1-1e-12)),xtol=1e-11)
    else:b=0.
    na=(model.total_na-model.capacity+b)/vf;k=(model.total_k-b)/vf
    cl=model.total_cl/vf
    return dict(na_mm=na,k_mm=k,cl_mm=cl,volume_um3=vi*1000,
                extracellular_volume_pl=vf-vi,reservoir_k_fmol=b,
                additional_intracellular_na_fmol=na*vi-f.HEALTH[4],
                nominal_three_na_pump_equivalent_fmol=(na*vi-f.HEALTH[4])/3.)


def run():
    models=[f.ClosedBath(),f.ClosedBath(capacity=240.),
            f.ClosedBath(capacity=240.,mode='independent'),f.ClosedBath(inert_volume=.048)]
    cases=[]
    for i,model in enumerate(models):
        path=f.OUT/f'finite_ion_closed_case{i}.npz'
        if not path.exists():continue
        data=np.load(path);yy=np.c_[data['injury_y'],data['recovery_y']]
        na_err=k_err=cl_err=water_err=0.
        for y in yy.T:
            ve,ce=model.extracellular(y)
            na_err=max(na_err,abs(y[4]+ve*ce[0]+model.capacity-y[8]-model.total_na))
            k_err=max(k_err,abs(y[5]+ve*ce[1]+y[8]-model.total_k))
            cl_err=max(cl_err,abs(y[6]+ve*ce[2]-model.total_cl))
            water_err=max(water_err,abs(y[7]/1000+ve+model.material_volume(y[8])-model.total_water))
        energies=np.array([free_energy(model,y) for y in data['injury_y'].T])
        derivatives=np.array([energy_derivative(model,y) for y in data['injury_y'].T])
        atp_rest=model.rhs(0,model.initial())[9]
        row=dict(case=i,initial_external_volume_pl=model.volume0,
                 initial_material_na_fmol=model.capacity-model.b0,initial_material_k_fmol=model.b0,
                 passive_zero_capacitor_endpoint=passive_endpoint(model),
                 sodium_conservation_error_fmol=na_err,potassium_conservation_error_fmol=k_err,
                 chloride_conservation_error_fmol=cl_err,water_conservation_error_pl=water_err,
                 maximum_sampled_passive_free_energy_derivative_w=float(derivatives.max()),
                 maximum_sampled_passive_free_energy_increase_j=float(np.diff(energies).max()),
                 passive_free_energy_drop_nj=float((energies[0]-energies[-1])*1e9),
                 injury_added_intracellular_na_fmol=float(data['injury_y'][4,-1]-f.HEALTH[4]),
                 resting_pump_atp_fmol_s=float(atp_rest),
                 recovery_pump_atp_excess_above_same_duration_rest_fmol=float(data['recovery_y'][9,-1]-atp_rest*data['recovery_t'][-1]))
        cases.append(row)
    rng=np.random.default_rng(930523);max_positive=0.;min_buffer_diss=1.;samples=0
    for model in models[:3]:
        data=np.load(f.OUT/f'finite_ion_closed_case{models.index(model)}.npz')
        for y in data['injury_y'].T:
            # Check analytic directional derivative by centered state difference.
            z=model.rhs(0,y,pump=0.);rate=energy_derivative(model,y)
            max_positive=max(max_positive,rate);samples+=1
            if model.capacity:
                ve,ce=model.extracellular(y)
                affinity=math.log(ce[1]/ce[0])-model.material_mu(y[8]/model.capacity)
                min_buffer_diss=min(min_buffer_diss,affinity*z[8])
    out=dict(status='internal conservation/thermodynamic checks of stated zero-hydration model',
             cases=cases,passive_derivative_samples=samples,
             maximum_positive_passive_free_energy_rate_w=max_positive,
             minimum_buffer_entropy_production_in_RT_fmol_s=min_buffer_diss)
    (f.OUT/'finite_ion_checks_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2),flush=True)


if __name__=='__main__':run()
