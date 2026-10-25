#!/usr/bin/env python3
"""Conditional interface calculations; no fitted material or biological data."""
from pathlib import Path
import json
import math
import numpy as np

OUT=Path(__file__).resolve().parent


def retardation(p,bmax=2.0,p50=3.3,hill=2.0,alpha=.0013):
    # Concentration units mol/m^3; 1 mM == 1 mol/m^3.
    bp=bmax*hill*p50**hill*p**(hill-1)/(p50**hill+p**hill)**2
    return 1+bp/alpha,bp


def slab_residual(t,a,deff):
    k=2*np.arange(256)+1
    return float(8/np.pi**2*np.sum(np.exp(-deff*(k*np.pi/(2*a))**2*t)/(k*k)))


def slab_t90(a,deff):
    lo,hi=0.,100*a*a/deff
    for _ in range(70):
        mid=(lo+hi)/2
        if slab_residual(mid,a,deff)>.1:
            lo=mid
        else:
            hi=mid
    return (lo+hi)/2


def main():
    rows=[]
    alpha,dfree=.0013,2e-9
    for p in [.3,1.,3.3,20.]:
        for hill in [1.,2.,3.]:
            rr,bp=retardation(p,hill=hill)
            for db in [0.,1e-12,1e-11,1e-10]:
                deff=(dfree*alpha+db*bp)/(alpha+bp)
                for a in [5e-6,10e-6,25e-6,50e-6]:
                    t=slab_t90(a,deff)
                    assert abs(slab_residual(t,a,deff)-.1)<1e-12
                    rows.append(dict(p_torr=p,hill=hill,carrier_diffusivity=db,
                                     half_thickness_um=a*1e6,binding_retardation=rr,
                                     effective_diffusivity=deff,t90_s=t))
    force,stroke,G,eps=40e-9,20e-6,100.,.06
    vmin=4*force*stroke/(G*eps**2)
    bmax=2.0
    nmin=bmax*vmin
    kv,pres,ytol=.002,1900.,1e-6
    ares=kv*ytol/pres
    k0,tau,om,uu=.001,600.,.02,60e-6
    zg=k0*tau/(1+1j*om*tau)
    copt=abs(zg)
    pmax=(om*uu)**2*abs(zg)**2/(4*(abs(zg)+zg.real))
    cgrid=copt*np.geomspace(.01,100,100001)
    pp=.5*cgrid*(om*uu)**2*abs(zg)**2/np.abs(zg+cgrid)**2
    assert np.max(pp)<=pmax*(1+1e-12)
    assert abs(np.max(pp)/pmax-1)<1e-12
    be=np.geomspace(.001,1000,100001)
    assert np.max(be/(1+be)**2)<=.25+1e-12
    ref=next(v for v in rows if v['p_torr']==3.3 and v['hill']==2 and v['carrier_diffusivity']==0 and v['half_thickness_um']==50)
    small=next(v for v in rows if v['p_torr']==3.3 and v['hill']==2 and v['carrier_diffusivity']==0 and v['half_thickness_um']==10)
    assert abs(ref['t90_s']/small['t90_s']-25)<1e-12
    kinetic=[]
    rr=ref['binding_retardation']
    for b in [.01,.1,1.,10.,100.]:
        a=(rr-1)*b
        for half in [1e-6,5e-6,10e-6,50e-6]:
            d=dfree*(np.pi/(2*half))**2
            tr=d+a+b
            slow=2*d*b/(tr+np.sqrt(tr*tr-4*d*b))
            assert 0<slow<=min(d,b)*(1+1e-12)
            kinetic.append(dict(half_thickness_um=half*1e6,
                chemical_bound_state_rate_per_s=b,free_to_bound_linear_rate_per_s=a,
                slow_modal_rate_per_s=slow,slow_modal_time_s=1/slow,
                local_equilibrium_modal_time_s=rr/d,
                clamped_oxygen_intrinsic_t90_floor_s=np.log(10)/b))
    result=dict(status='conditional illustrative interface bounds, not measured gel kinetics',
                nominal_inputs=dict(Bmax_mol_m3=2.,P50_torr=3.3,
                                    free_oxygen_solubility_mol_m3_per_torr=alpha,
                                    free_diffusivity_m2_s=dfree),
                mechanical_bound=dict(force_n=force,stroke_m=stroke,modulus_pa=G,
                    strain_limit=eps,minimum_volume_m3=vmin,
                    minimum_oxygen_charge_mol_per_phase=nmin,
                    minimum_8_phase_oxygen_charge_mol=8*nmin),
                pressure_bias=dict(spring_n_m=kv,pressure_pa=pres,tolerance_m=ytol,
                    max_residual_area_m2=ares,residual_fraction_of_1e_9_m2=ares/1e-9),
                purely_viscous_load=dict(gel_impedance_real=zg.real,gel_impedance_imag=zg.imag,
                    optimum_load_ns_per_m=copt,max_power_w_per_phase=pmax,
                    max_power_w_8_phases=8*pmax,example_hydraulic_duty_w=100*1e-12),
                reference_50um=ref,reference_10um=small,transport_sweep=rows,
                finite_binding_kinetic_modes=kinetic,
                checks=['slab residual at t90 equals .1 to 1e-12',
                        '25-fold t90 reduction at 5-fold half-thickness reduction',
                        'viscous-load power maximum replayed on 100001 load values',
                        'series transmission volume factor <=1/4 on 100001 beta values',
                        'finite-binding slow rate positive and bounded by diffusion and chemical rate'])
    (OUT/'interface_constraints.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='transport_sweep'},indent=2))


if __name__=='__main__':
    main()
