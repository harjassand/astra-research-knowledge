"""Reproducible conditional calculations, not an identified catalyst model.

The numerical use of 0.126 eV as a gate FREE ENERGY and 41 ns as a
thermal relaxation time is a deliberately explicit hypothesis. The primary
source reports vibrational single-point energy and a storage annotation,
which do not establish those identifications. No parameter uncertainties
are fabricated. Figure digitization errors are geometric errors only.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.special import expi
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
KB_EV = 8.617333262145e-5
T = 298.0
KT = KB_EV*T
TAU = 41e-9
GAP = .126
BARRIER0 = .375
BARRIER1 = .183
PREFACTOR = 2.3e9
GAIN = 3.3
b = 1/TAU
a = b*math.exp(-GAP/KT)
k0 = PREFACTOR*math.exp(-BARRIER0/KT)
k1 = PREFACTOR*math.exp(-BARRIER1/KT)

def effective_rate(a_up, b_down=b, cold=k0, hot=k1):
    """Inverse MFPT to reaction, starting in cold state; exact 2-state gate."""
    return (cold*(b_down+hot)+a_up*hot)/(a_up+b_down+hot)

thermal = effective_rate(a)
required_up = (b+k1)*(GAIN*thermal-k0)/(k1-GAIN*thermal)
c = (BARRIER0-BARRIER1)/KT
excess_hazard = k0*TAU*(expi(c)-np.euler_gamma-math.log(c))
results = {
    'status': 'conditional model calculations, not measured gate rates',
    'temperature_K': T,
    'kBT_eV': KT,
    'assumed_gate_free_energy_eV': GAP,
    'assumed_thermal_down_time_s': TAU,
    'thermal_up_rate_s-1': a,
    'thermal_down_rate_s-1': b,
    'cold_reaction_rate_s-1': k0,
    'hot_reaction_rate_s-1': k1,
    'thermal_gate_effective_rate_s-1': thermal,
    'thermal_gate_vs_always_cold_ratio': thermal/k0,
    'gain_target': GAIN,
    'necessary_pump_rate_s-1_single_edge_bound': (GAIN-1)*a,
    'exact_pump_rate_s-1_for_two_state_gate': required_up-a,
    'finite_exponential_pulse_excess_hazard': excess_hazard,
    'pulse_extra_reaction_probability_upper_bound': -math.expm1(-excess_hazard),
    'free_energy_requirement': [],
    'static_effective_barrier_shifts_eV': {str(g):KT*math.log(g) for g in (3.1,3.3,3.5)},
    'site_number_modified_over_bare': .04175/.079,
    'conditional_total_current_ratio_if_TOF_ratio_3point3_same_mass': 3.3*.04175/.079,
}
for lam in (1.,10.,100.,1000.,10000.,100000.,1000000.):
    required_F = KT*math.log((GAIN-1)/(lam*TAU))
    results['free_energy_requirement'].append({
        'pump_rate_s-1': lam,
        'gain_upper_bound': 1+lam/a,
        'exact_two_state_gate_gain': effective_rate(a+lam)/thermal,
        'necessary_gate_free_energy_eV': required_F,
        'entropy_deficit_kB_if_energy_is_0point126_eV': (required_F-GAP)/KT,
    })

# Digitize supplied SI page S26 (rendered previously with Poppler).
# Axes: TOF 0..18 at y=679..183, multiplier 1..4 on the same height.
im = np.asarray(Image.open(ROOT/'observation2'/'si-26.png').convert('RGB'))
digitized=[]
for eta, x in zip(range(260,341,10), np.linspace(340.5,888.5,9)):
    x=int(round(x)); patch=im[220:390,x-4:x+5,:]
    red=(patch[:,:,0]>180)&(patch[:,:,1]<130)&(patch[:,:,2]<145)
    ys=np.nonzero(red)[0]+220
    center=(float(ys.min())+float(ys.max()))/2
    # Purple bar is left of the group center; use interior pixels.
    # The legend contains a purple swatch over the 270 mV bar. Restrict the
    # vertical search below that legend for bars known to lie below y=400.
    y_start=400 if eta<=320 else (350 if eta==330 else 220)
    pp=im[y_start:679,x-25:x-8,:]
    purple=(pp[:,:,0]>120)&(pp[:,:,2]>150)&(pp[:,:,1]<150)&(pp[:,:,2]>pp[:,:,0]+10)
    yy=np.nonzero(purple)[0]+y_start
    top=float(yy.min())
    tof=(679-top)*18/(679-183)
    gain=1+(679-center)*3/(679-183)
    digitized.append({'overpotential_mV':eta, 'gain_digitized':gain,
        'gain_pixel_error_halfwidth':1.5*3/(679-183),
        'modified_TOF_digitized_s-1_per_reported_site':tof,
        'TOF_pixel_error_halfwidth':1.5*18/(679-183),
        'bare_TOF_derived_from_modified_and_gain':tof/gain,
        'red_center_pixel_y':center,'purple_top_pixel_y':top})
results['S16_digitization']={
    'source':'Liang et al., DOI 10.1021/jacs.5c15936.s001, Fig S16, page S26',
    'method':'colored bar top and red circle center from Poppler rendering',
    'uncertainty':'1.5 pixel geometric halfwidth; NOT a measurement CI; original error bars not converted to statistical uncertainty',
    'points':digitized}

# Numerical property check on independently sampled positive gate parameters.
# This checks algebraic implementation, not empirical validity or novelty.
rng=np.random.default_rng(52684)
worst=-np.inf
for _ in range(10000):
    aa,bb,kk,ratio,ll = 10**rng.uniform(-5,5,5)
    kh=kk*(1+ratio)
    observed=effective_rate(aa+ll,bb,kk,kh)/effective_rate(aa,bb,kk,kh)
    worst=max(worst, observed/(1+ll/aa)-1)
assert worst <= 1e-10
results['algebra_implementation_check_max_fractional_bound_violation']=float(worst)
(HERE/'thermal_competition_results.json').write_text(json.dumps(results,indent=2))

plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,3,figsize=(13,3.8),layout='constrained')
lam=np.geomspace(1,1e7,500)
axs[0].loglog(lam,1+lam/a,label='Single-channel upper bound',color='#242f40',ls='--')
axs[0].loglog(lam,effective_rate(a+lam)/thermal,label='Exact two-state gate',color='#087f8c')
axs[0].axhline(GAIN,color='#cf5c36',ls=':',label='Target gain 3.3')
axs[0].set(xlabel='Added excitation rate λ (s⁻¹)',ylabel='Gain over thermal gate',title='A. Competition with thermal excitation')
axs[0].legend(fontsize=7.5)
F=KT*np.log((GAIN-1)/(lam*TAU))
axs[1].semilogx(lam,F,color='#087f8c')
axs[1].axhline(GAP,color='#cf5c36',ls=':',label='Reported energy: not a measured free energy')
axs[1].set(xlabel='Added excitation rate λ (s⁻¹)',ylabel='Necessary gate free energy (eV)',title='B. Conditional requirement for gain 3.3')
axs[1].legend(fontsize=7)
etas=[p['overpotential_mV'] for p in digitized]
gains=[p['gain_digitized'] for p in digitized]
axs[2].errorbar(etas,gains,yerr=[p['gain_pixel_error_halfwidth'] for p in digitized],fmt='o-',color='#a73ab7',ms=4,label='Published figure, digitized')
axs[2].set(xlabel='Overpotential (mV)',ylabel='Modified / bare TOF',title='C. Observed gain is weakly rate dependent',ylim=(2.9,3.7))
axs[2].legend(fontsize=7.5)
fig.suptitle('Catalytic energy recycling: conditional kinetic limits and measured voltage dependence',fontsize=13)
fig.savefig(HERE/'thermal_competition.png',dpi=180)
fig.savefig(HERE/'thermal_competition.pdf')
print(json.dumps({k:v for k,v in results.items() if k not in ('S16_digitization','free_energy_requirement')},indent=2))
print(json.dumps(digitized,indent=2))
