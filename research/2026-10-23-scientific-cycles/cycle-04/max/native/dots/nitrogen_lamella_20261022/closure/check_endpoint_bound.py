"""Independent four-species LP and analytic Cp/Cv checks of saved endpoint bound.
No integration. Actual mechanism is read, never modified.
"""
import importlib.util,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from nasa_secant import nasa7_h_secant,splice_diagnostics

D=Path(__file__).resolve().parent;root=D.parents[1]
p=root/'nitrogen_finite_cycle_20261021/signed_trial_helper/helper.py'
s=importlib.util.spec_from_file_location('closure_endpoint_thermo',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);K=m.SignedTrialKernel()
bound=json.loads((D.parent/'endpoint_bound.json').read_text())
yh=np.load(root/'nitrogen_admissibility_20261022/recycle_quench/once_through_2700_reference.npz')['hot_Y']
yc=np.load(root/'nitrogen_admissibility_20261022/recycle_quench/mix_tau_0p0001_trajectory.npz')['return_Y'];yc=np.maximum(yc,0);yc/=yc.sum()
W=K.W/1000;Ru=K.R/1000;Ri=Ru/W;ratio=.85
n=(yh+ratio*yc)/W;atoms=K.element_atoms@n
stable=[K.species_names.index(x) for x in ['N2','O2','NO','NO2']]
noix=[K.species_names.index(x) for x in ['NO','NO2']]
cp,h,s=K.thermochemistry(np.array([1700.]));hm=h[:,0]*Ru*1700;um=hm-Ru*1700
rows=[]
for kind,name in enumerate(['prescribed_pressure_enthalpy','rigid_volume_internal_energy']):
    ei=[hm,um][kind][stable]
    expected=bound['rows'][kind]
    for ceiling in expected['ceilings']:
        xmax=ceiling['max_NOx_fraction_of_initial_packet']*n[noix].sum()
        result=linprog(-ei,A_ub=np.array([[0.,0.,1.,1.]]),b_ub=[xmax],
                       A_eq=K.element_atoms[:,stable],b_eq=atoms,bounds=(0,None),method='highs')
        assert result.success,result.message
        maxe=-result.fun;export=max(0,expected['initial_energy_J_kg_fresh']-maxe)
        delta=maxe-ceiling['maximum_stable_energy_J_per_kg_fresh_at_1700']
        assert abs(delta)<2e-8
        rows.append({'contract':name,'NOx_upper_fraction':ceiling['max_NOx_fraction_of_initial_packet'],
                     'LP_minus_closed_form_J_per_kg_fresh':float(delta),
                     'minimum_export_J_per_kg_fresh':float(export),
                     'maximizer_N2_O2_NO_NO2_mol_per_kg_fresh':result.x.tolist()})
# Exact polynomial stationary-point check of positive caloric derivative on 200..1700 K.
# This remains float64, not outward-rounded interval arithmetic.
caloric=[]
for i,sp in enumerate(K.species_names):
    candidates=[]
    for lo,hi,a in [(200.,1000.,K.nasa[i,8:15]),(1000.,1700.,K.nasa[i,1:8])]:
        roots=np.polynomial.polynomial.polyroots([a[1],2*a[2],3*a[3],4*a[4]])
        ts=[lo,hi]+[float(r.real) for r in roots if abs(r.imag)<1e-8 and lo<r.real<hi]
        for t in ts:
            cp_R=np.polynomial.polynomial.polyval(t,a[:5]);candidates.append((cp_R*Ri[i],(cp_R-1)*Ri[i],t))
    minimum_cp=min(x[0] for x in candidates);minimum_cv=min(x[1] for x in candidates)
    assert minimum_cv>0
    caloric.append({'species':sp,'minimum_cp_J_kgK_200_to_1700':float(minimum_cp),
                    'minimum_cv_J_kgK_200_to_1700':float(minimum_cv)})
lo=K.nasa[:,8:15];hi=K.nasa[:,1:8]
diag={k:np.asarray(v).tolist() for k,v in splice_diagnostics(lo,hi,Ri).items()}
# Receiving-use identity at a wide cross-splice face: exact source potential jump.
tl,tr=300.,2700.;cp0,h0,s0=K.thermochemistry(np.array([tl,tr]));z=Ri[:,None]*(h0-s0)
sec=nasa7_h_secant(tl,tr,lo,hi,Ri)
reference=(z[:,1]-z[:,0])/(1/tr-1/tl)
res=sec-reference
result={'scope':'Independent stable-species LP agrees with saved closed-form ceiling; conditional on allowed species, NOx ceiling, temperature domain and stated mechanical boundary.',
        'LP_checks':rows,'caloric_derivative_checks':caloric,
        'actual_source_splice_diagnostics':diag,
        'actual_source_300_to_2700_secant_minus_potential_secant_J_per_kg':res.tolist(),
        'limitations':['Float64 checks, not interval-certified arithmetic.','Temperature monotonicity checked over the source-admitted 200..1700 K interval only.','No kinetic attainability, permanent radical absence, or device geometry is certified.']}
(D/'endpoint_independent_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
