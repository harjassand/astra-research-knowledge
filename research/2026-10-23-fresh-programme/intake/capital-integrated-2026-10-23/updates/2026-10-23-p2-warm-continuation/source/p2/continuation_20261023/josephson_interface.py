"""Audit a proposed passive thermal interface; NOT an experimental device fit.

Two parallel series-RLC branches are an inadmissible shortcut for two isolated
thermal ports: they form a direct resistor-to-resistor loop when the device
port is open. All heat below is computed from this explicitly specified
passive circuit, with exact Planck occupations and no fitted loss sweep.
"""
from pathlib import Path
import json
import math
from scipy.integrate import quad

OUT = Path(__file__).resolve().parent
H, KB = 6.62607015e-34, 1.380649e-23
FA, FB = 4.155e9, 5.756e9
TC, TH = .080, .100
R, Q = 50., 20.
rho = FB/FA
D = Q*(rho-1/rho)
t = 1/(1+D*D)
v = t/(1+t)
LA, LB = [R*Q/(2*math.pi*f) for f in (FA, FB)]
CA, CB = [1/(R*Q*2*math.pi*f) for f in (FA, FB)]
F0 = math.sqrt(FA*FB)
LLOOP = LA+LB
CLOOP = CA*CB/(CA+CB)
QLOOP = 2*math.pi*F0*LLOOP/(2*R)

def bose(f, temp):
    x = H*f/(KB*temp)
    return 0. if x > 700. else 1/math.expm1(x)

def branch_y(f, center):
    x = Q*(f/center-center/f)
    return 1/(R*(1+1j*x))

def bypass(f):
    if f == 0:
        return 0.
    xsum = Q*(f/FA-FA/f+f/FB-FB/f)
    return 4/(4+xsum*xsum)

def heat_density_ghz(u):
    if u == 0:
        return 0.
    f = 1e9*u
    return 1e9*H*f*bypass(f)*(bose(f,TH)-bose(f,TC))

edges = [0., FA/1e9, F0/1e9, FB/1e9, 20., math.inf]
pieces = [quad(heat_density_ghz,a,b,epsabs=1e-29,epsrel=1e-10,limit=300)[0]
          for a,b in zip(edges[:-1],edges[1:])]
heat = sum(pieces)
area = R/(2*LLOOP)  # Integral_0^infinity transmission df, exactly.

centers = {}
for label,f in [('a',FA),('b',FB)]:
    yc,yh = branch_y(f,FA),branch_y(f,FB)
    ysum = yc+yh
    z = 1/ysum
    reflection = abs((1-R*ysum)/(1+R*ysum))**2
    centers[label] = {
        'frequency_Hz': f,
        'cold_noise_weight': yc.real/ysum.real,
        'hot_noise_weight': yh.real/ysum.real,
        'total_admittance_S_real_imag': [ysum.real,ysum.imag],
        'input_impedance_ohm_real_imag': [z.real,z.imag],
        'reflection_power_for_50ohm_reference': reflection,
        'relative_ReY_to_50ohm': R*ysum.real,
        'relative_ReZ_to_50ohm': z.real/R,
    }

# Deliberately incomplete center-only fixture illustrates why small center
# contamination is misleading. It retains original rates and omits the
# frequency-wide direct bypass; it is NOT total interface heat.
ka,kb = [2*math.pi*f for f in (29.8e6,29.5e6)]
eta = .96
fca,fcb = eta*(1-v),eta*v
nac,nah = bose(FA,TC),bose(FA,TH)
nbc,nbh = bose(FB,TC),bose(FB,TH)
nbara = fca*nac+(1-fca)*nah
nbarb = fcb*nbc+(1-fcb)*nbh
K0 = ka*kb/(ka+kb)
I = .5*K0*(nbara-nbarb)
pa,pb = nbara-I/ka,nbarb+I/kb
qc_a = H*FA*ka*fca*(nac-pa)
qc_b = H*FB*kb*fcb*(nbc-pb)
old_margin = 1.798208579233269e-18
kernel_f0 = H*F0*(bose(F0,TH)-bose(F0,TC))

result = {
    'status': 'PROPOSED CIRCUIT COUNTEREXAMPLE; NOT ACQUIRED MEASUREMENT',
    'model': 'Two parallel series-RLC thermal branches, device port open. Ideal L/C; only the two 50-ohm resistors dissipate.',
    'input': {'fa_Hz':FA,'fb_Hz':FB,'Tc_K':TC,'Th_K':TH,'R_each_ohm':R,'Q_each':Q},
    'component_values': {'L_a_H':LA,'C_a_F':CA,'L_b_H':LB,'C_b_F':CB,
                         'branch_a_conductance_FWHM_Hz':FA/Q,'branch_b_conductance_FWHM_Hz':FB/Q},
    'dimensionless_detuning_D':D,
    'offbranch_to_resonant_conductance_ratio':t,
    'wrong_temperature_noise_weight_at_centers':v,
    'center_values':centers,
    'open_port_bypass': {
        'transmission': '4/[4+Q^2*(f/fa-fa/f+f/fb-fb/f)^2]',
        'resonance_Hz':F0,'peak_transmission':bypass(F0),
        'L_loop_H':LLOOP,'C_loop_F':CLOOP,'Q_loop':QLOOP,
        'FWHM_Hz':F0/QLOOP,'integrated_transmission_area_Hz':area,
        'heat_hot_to_cold_W':heat,'integration_pieces_W':pieces,
        'ratio_to_original_C1_cold_margin':heat/old_margin,
        'kernel_at_resonance_J':kernel_f0,
        'allowed_area_Hz_if_narrow_at_resonance_and_no_other_load':old_margin/kernel_f0,
        'scope': 'Exact Planck integral for this open-port passive network. Assembled FPJA admittance can shift/load it; no exact assembled-device heat is asserted.',
    },
    'center_only_fixture_OMITS_BYPASS_AND_RATE_CHANGES': {
        'cold_rate_fractions': {'a':fca,'b':fcb},
        'C':1.,'lower_cold_heat_W':qc_a,'upper_cold_heat_W':qc_b,
        'sum_cold_heat_W':qc_a+qc_b,
        'warning':'Not a valid total cooling prediction for the RLC interface.',
    },
    'required_next_input': 'Full complex device port admittance / pumped Floquet scattering plus thermal termination scattering and all dissipative bath temperatures.',
    'receipts': {'new_workers':0,'actual_model_token_billing':'UNKNOWN'},
}
assert abs(bypass(F0)-1.) < 1e-14
assert all(abs(centers[j]['hot_noise_weight' if j=='a' else 'cold_noise_weight']-v)<1e-14 for j in ('a','b'))
assert heat > 30*old_margin
(OUT/'josephson_interface_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
