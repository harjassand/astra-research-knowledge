"""Independent finite nozzle/reset check. No trajectory or kinetics run.

No import of admission/calculate.py, ThermoKernel, scipy, or an LP solver.
1. Exact Fraction primal/dual witness for the stored binary64 endpoint LP.
2. Independent 80-digit NASA7 scalar properties and shock-temperature root.
3. Closed-form calorically-perfect nozzle/shock identities.
4. Exact Bernstein positivity certificate for source species cp/R.

This is an arithmetic/model check, not physical model qualification.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb, floor
import hashlib, json, time
import numpy as np
import mpmath as mp

D = Path(__file__).resolve().parent
ROOT = D.parents[1]
ADMISSION = ROOT / 'nitrogen_cycle5_20261022/nozzle_admission/result.json'
CACHE = ROOT / 'nitrogen_finite_cycle_20261021/thermo_helper/cache.npz'
MANIFEST = CACHE.with_name('manifest.json')
start = time.monotonic()
original = json.loads(ADMISSION.read_text())
manifest = json.loads(MANIFEST.read_text())
assert hashlib.sha256(CACHE.read_bytes()).hexdigest() == manifest['cache_sha256']
mp.mp.dps = 80

def frac(x):
    return F.from_float(float(x))

def m(x):
    q = frac(x) if not isinstance(x, F) else x
    return mp.mpf(q.numerator) / q.denominator

def record(q):
    return {'fraction': str(q), 'decimal_50_digits': mp.nstr(m(q), 50)}

def exact_endpoint(c, atoms, nmin, nmax, ncap, ocap):
    # Max c.n; A.n=atoms; n>=0; nmin<=NO+NO2<=nmax; N/O caps.
    # Dual identity: B-c.n equals nonnegative bound slacks plus NO2 slack.
    lam_n, lam_o = c[0] / 2, c[1] / 2
    mu = c[4] - lam_n - lam_o
    nu_n, nu_o = c[2] - lam_n, c[3] - lam_o
    species_majorant = [2*lam_n, 2*lam_o, lam_n+nu_n,
                         lam_o+nu_o, lam_n+lam_o+mu, lam_n+2*lam_o+mu]
    slack = [a-b for a, b in zip(species_majorant, c)]
    x = [(atoms[0]-ncap-nmax)/2, (atoms[1]-ocap-nmax)/2,
         ncap, ocap, nmax, F(0)]
    assert min(x) >= 0 and nmin <= x[4]+x[5] <= nmax
    assert 2*x[0]+x[2]+x[4]+x[5] == atoms[0]
    assert 2*x[1]+x[3]+x[4]+2*x[5] == atoms[1]
    assert min(mu, nu_n, nu_o, *slack) >= 0
    bound = lam_n*atoms[0]+lam_o*atoms[1]+mu*nmax+nu_n*ncap+nu_o*ocap
    objective = sum(a*b for a, b in zip(c, x))
    assert bound == objective
    return {'x': x, 'bound': bound, 'dual': [lam_n, lam_o, mu, nu_n, nu_o],
            'slack': slack, 'gap': bound-objective}

lp = original['endpoint_lp']
assert lp['atom_matrix'] == [[2,0,1,0,1,1],[0,2,0,1,1,2]]
assert lp['count_matrix'] == [[0,0,0,0,1,1],[0,0,0,0,-1,-1]]
c = list(map(frac, lp['enthalpy_J_mol']))
atoms = list(map(frac, lp['atom_rhs']))
nmin, nmax = -frac(lp['count_rhs'][1]), frac(lp['count_rhs'][0])
# These bounds are copied exactly from calculate.py, not inferred from x.
ncap, ocap = frac(1e-7), frac(.003)
cert = exact_endpoint(c, atoms, nmin, nmax, ncap, ocap)
export = frac(original['hot_enthalpy_J_kgfresh']) - cert['bound']
lower_1microjoule = F(export.numerator*10**6//export.denominator, 10**6)
assert lower_1microjoule <= export
exact = {
    'scope': 'Exact optimality for stored binary64 c, atom RHS, count RHS and N/O caps; not physical uncertainty intervals.',
    'species': manifest['species'],
    'primal_mol_per_kgfresh': [record(q) for q in cert['x']],
    'dual_order': ['atom_N', 'atom_O', 'NOx_upper', 'N_upper', 'O_upper'],
    'dual_exact': [record(q) for q in cert['dual']],
    'dual_species_slack_exact_J_mol': [record(q) for q in cert['slack']],
    'primal_dual_gap_exact_J_kgfresh': str(cert['gap']),
    'maximum_final_enthalpy_J_kgfresh': record(cert['bound']),
    'minimum_net_heat_plus_shaft_work_out_J_kgfresh': record(export),
    'certified_decimal_lower_bound_J_kgfresh': str(lower_1microjoule),
    'difference_from_reported_bound_J_kgfresh': float(export-frac(lp['minimum_total_heat_plus_shaft_work_export_before_rest_J_kgfresh'])),
}

with np.load(CACHE, allow_pickle=False) as z:
    nasa = [[frac(v) for v in row] for row in z['nasa']]
    weights = [m(v) for v in z['molecular_weights']]
Y = [m(v) for v in original['initial_hot_Y']]
Ru = m(manifest['constants']['R_J_kmol_K'])
Rm = sum(y*Ru/w for y,w in zip(Y,weights))
T0, P0, cap = mp.mpf(2700), mp.mpf(101325), mp.mpf(1700)

def pure(i, T):
    row = nasa[i]
    a = list(map(m, row[8:15] if T <= m(row[0]) else row[1:8]))
    cp_R = sum(a[k]*T**k for k in range(5))
    h_R = a[5]+sum(a[k]*T**(k+1)/(k+1) for k in range(5))
    s_R = a[6]+a[0]*mp.log(T)+sum(a[k]*T**k/k for k in range(1,5))
    return cp_R, h_R, s_R

def mix(T):
    vals = [pure(i,T) for i in range(6)]
    return tuple(sum(Y[i]*Ru/weights[i]*vals[i][j] for i in range(6)) for j in range(3))

def bisect(fun, lo, hi):
    flo, fhi = fun(lo), fun(hi)
    assert flo*fhi < 0
    for _ in range(260):
        mid = (lo+hi)/2
        fm = fun(mid)
        if fm == 0:
            return mid
        if flo*fm < 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return (lo+hi)/2

cp0, h0, s0 = mix(T0)
hc = mix(cap)[1]
rows = []
max_relative_residual = mp.mpf(0)
for ref in original['nozzle_rows']:
    Ts = m(ref['static_T_K'])
    cp1,h1,s1 = mix(Ts)
    P1 = P0*mp.exp((s1-s0)/Rm)
    v1 = mp.sqrt(2*(h0-h1))
    rho1 = P1/(Rm*Ts)
    j = rho1*v1
    # Solve in downstream temperature, not admission's downstream velocity.
    B = v1+Rm*Ts/v1
    def v2_at(T):
        disc = B*B-4*Rm*T
        assert disc >= 0
        return 2*Rm*T/(B+mp.sqrt(disc))
    def energy(T):
        return mix(T)[1]+v2_at(T)**2/2-h0
    T2 = bisect(energy, Ts, T0)
    v2 = v2_at(T2)
    P2 = j*Rm*T2/v2
    rho2 = P2/(Rm*T2)
    cp2,h2,s2 = mix(T2)
    entropy = s2-s1-Rm*mp.log(P2/P1)
    P02 = P2*mp.exp((s0-s2)/Rm)
    M1 = v1/mp.sqrt(cp1/(cp1-Rm)*Rm*Ts)
    M2 = v2/mp.sqrt(cp2/(cp2-Rm)*Rm*T2)
    residuals = [abs(rho2*v2-j)/j,
                 abs(P2+rho2*v2*v2-P1-rho1*v1*v1)/(P1+rho1*v1*v1),
                 abs(h2+v2*v2/2-h0)/h0,
                 abs(mp.log(P02/P0)+entropy/Rm)]
    max_relative_residual = max(max_relative_residual, *residuals)
    assert M1 > 1 and M2 < 1 and P2 > P1 and entropy > 0 and P02 < P0
    rcrit = (hc-h1)/(h0-h1)
    # Reverse the recovery calculation to test the published temperatures.
    recovery_residuals = []
    for rec in ref['recovery_temperature_examples']:
        r,Tr = m(rec['r']),m(rec['adiabatic_recovery_temperature_K'])
        recovery_residuals.append(float(mix(Tr)[1]-(h1+r*(h0-h1))))
    w_static = Rm*300*mp.log(P0/P1)
    w_shock = Rm*300*mp.log(P0/P02)
    # At unchanged composition/total temperature: R ln(P0/P02)=Delta s.
    assert abs(w_shock-300*entropy) < mp.mpf('1e-65')
    values = {'static_P_Pa': P1, 'velocity_m_s': v1,
              'Mach_caloric_reference': M1, 'normal_shock_T_K': T2,
              'normal_shock_P_Pa': P2, 'postshock_total_P_Pa': P02,
              'normal_shock_entropy_increase_J_kgK': entropy,
              'r_max_for_passive_wall_at_cap': rcrit,
              'cold_compress_cost_if_cool_at_static_pressure_J_kg': w_static,
              'cold_compress_cost_if_ideal_diffuse_after_shock_J_kg': w_shock}
    differences = {key: float(value-m(ref[key])) for key,value in values.items()}
    rows.append({'static_T_K':float(Ts), 'independent_values':{k:float(v) for k,v in values.items()},
                 'minus_reported': differences, 'downstream_Mach':float(M2),
                 'conservation_relative_residuals':[float(q) for q in residuals],
                 'recovery_enthalpy_residuals_J_kg':recovery_residuals})

def bernstein(p, lo, hi):
    # Exact power->Bernstein conversion on x=(T-lo)/(hi-lo), degree 4.
    d = len(p)-1
    shifted = [sum(p[k]*comb(k,j)*lo**(k-j)*(hi-lo)**j for k in range(j,d+1))
               for j in range(d+1)]
    return [sum(shifted[j]*F(comb(i,j),comb(d,j)) for j in range(i+1)) for i in range(d+1)]

cp_cert = []
for name,row in zip(manifest['species'],nasa):
    b_low = bernstein(row[8:13],F(200),F(1000))
    b_high = bernstein(row[1:6],F(1000),F(1700))
    assert min(*b_low,*b_high) > 0
    def h_R_exact(a,T):
        return a[5]+sum(a[k]*T**(k+1)/F(k+1) for k in range(5))
    gap = h_R_exact(row[1:8],F(1700))-h_R_exact(row[8:15],F(1000))
    assert gap > 0
    cp_cert.append({'species':name, 'lower_bound_cp_over_R':record(min(*b_low,*b_high)),
                    'high_1700_minus_low_1000_h_over_R_K':record(gap)})

# Separate analytic perfect-gas test, using no stored NASA output or roots.
perfect_rows=[]
for gamma in [mp.mpf(7)/5,mp.mpf(4)/3,mp.mpf(5)/3]:
    R = mp.mpf(287)
    cp = gamma*R/(gamma-1)
    for M1 in map(mp.mpf,['1.01','1.5','2','3','5']):
        Ts = T0/(1+(gamma-1)*M1*M1/2)
        P1 = P0*(Ts/T0)**(gamma/(gamma-1))
        v1 = M1*mp.sqrt(gamma*R*Ts)
        rho1 = P1/(R*Ts)
        pr = (2*gamma*M1*M1-(gamma-1))/(gamma+1)
        dr = (gamma+1)*M1*M1/((gamma-1)*M1*M1+2)
        T2,P2,rho2,v2 = Ts*pr/dr,P1*pr,rho1*dr,v1/dr
        M2sq = ((gamma-1)*M1*M1+2)/(2*gamma*M1*M1-(gamma-1))
        P02 = P2*(1+(gamma-1)*M2sq/2)**(gamma/(gamma-1))
        analytic_P02ratio = dr**(gamma/(gamma-1))*((gamma+1)/(2*gamma*M1*M1-(gamma-1)))**(1/(gamma-1))
        ds = cp*mp.log(T2/Ts)-R*mp.log(pr)
        errs=[abs((cp*Ts+v1*v1/2)/(cp*T0)-1),
              abs((cp*T2+v2*v2/2)/(cp*T0)-1),
              abs(rho1*v1-rho2*v2)/(rho1*v1),
              abs(P1+rho1*v1*v1-P2-rho2*v2*v2)/(P1+rho1*v1*v1),
              abs(P02/P0-analytic_P02ratio),abs(mp.log(P02/P0)+ds/R)]
        assert max(errs) < mp.mpf('1e-70') and ds > 0
        assert M2sq < 1 and T2 > Ts and P02 < P0
        perfect_rows.append({'gamma':float(gamma),'upstream_Mach':float(M1),
                             'static_T_K':float(Ts),'postshock_T_K':float(T2),
                             'postshock_total_T_K':float(T2*(1+(gamma-1)*M2sq/2)),
                             'postshock_total_P_ratio':float(P02/P0),
                             'max_relative_identity_residual':float(max(errs))})

# Clarify the convention, not a replacement bound: closed material U differs
# from steady-stream H. Boundary pressure-volume work must then be included.
rmol = frac(float(manifest['constants']['R_J_kmol_K']/1000))
cu = [v-rmol*F(1700) for v in c]
ucert = exact_endpoint(cu, atoms, nmin, nmax, ncap, ocap)
u0 = frac(original['hot_enthalpy_J_kgfresh'])-frac(original['Rmix_J_kgK'])*F(2700)
closed_batch_difference = u0-ucert['bound']

result={
    'admission_result_sha256':hashlib.sha256(ADMISSION.read_bytes()).hexdigest(),
    'source_cache_sha256':hashlib.sha256(CACHE.read_bytes()).hexdigest(),
    'methods':'Fraction exact arithmetic; independent mpmath 80-digit scalar NASA7 evaluation; temperature-root shock solve; closed-form perfect-gas shock/nozzle identities. No helper import, LP solver, kinetics or flow integration.',
    'exact_stored_lp_certificate':exact,
    'independent_property_comparison':{
        'Rmix_minus_reported_J_kgK':float(Rm-m(original['Rmix_J_kgK'])),
        'hot_h_minus_reported_J_kg':float(h0-m(original['hot_enthalpy_J_kgfresh'])),
        'cap_h_minus_reported_J_kg':float(hc-m(original['same_composition_relaxed_cap_enthalpy_J_kgfresh'])),
        'hot_Y_sum_minus_one':float(sum(Y)-1),
        'max_conservation_relative_residual':float(max_relative_residual),
        'rows':rows},
    'exact_cp_positivity':{
        'domain_K':[200,1700],
        'note':'N2 below 300 K is already a source-model extrapolation. Positivity certifies this polynomial model, not that extrapolation. Branchwise positivity plus h_high(1700)>h_low(1000) proves species endpoint maxima at 1700 even with binary64 splice residuals.',
        'species':cp_cert},
    'perfect_gas_independent_identity_tests':perfect_rows,
    'convention_clarification':{
        'steady_flow':'Q_out + W_shaft,out = H0 - Hfinal, net outward signs, same closed material inventory, negligible final kinetic/potential energy, no other carrier or inventory accumulation.',
        'closed_batch':'For a closed material batch use internal energy, and count all boundary work; enthalpy alone is not the closed-batch energy.',
        'illustrative_same_stored_data_U0_minus_Ufinalmax_J_kgfresh':record(closed_batch_difference),
        'not_a_second_physical_certificate':'Uses stored rounded Rmix and h coefficients with their binary64 conventions, only to expose the H versus U distinction.'},
    'reference_sources':[
        'https://www.grc.nasa.gov/WWW/BGH/normal.html',
        'https://www.grc.nasa.gov/WWW/BGH/isentrop.html',
        'https://www.nasa.gov/wp-content/uploads/2023/03/equations-tables-charts-compressibleflow-report-1135.pdf'],
    'limitations':[
        'Exact stored-data LP arithmetic is not coefficient, mechanism, or physical uncertainty certification.',
        'The ideal-gas NASA caloric reference below 0.5 atm is outside the helper state-evaluator pressure domain; no kinetic or transport validity is claimed there.',
        'All endpoint modes must be relaxed. Nonequilibrium mode energy, other species, excess inventory, radiation or exported matter change the accounting and must be explicit.',
        'Gross net-outward stream energy transfer is not irrecoverable loss or electrical SEC. Internal regeneration can reuse it elsewhere in a cycle.',
        'Recovery factors 0.85 and 0.89 remain illustrative and are not reacting-gas measurements.',
        'A passive adiabatic recovery-temperature estimate is not a cooled-wall temperature, heat-transfer coefficient, or wall-design qualification.',
        'Rmix*300*log(Pout/Pin) is reversible isothermal compression at 300 K for the assumed unchanged composition. The two pressure routes are alternatives, not additive charges or universal device lower bounds.'],
    'elapsed_s':time.monotonic()-start,
    'status':'PASS: exact stored-LP primal/dual witness; independent source-property and shock conservation checks; 15 analytic perfect-gas cases.'}
(D/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'exact_export_J_kg':exact['minimum_net_heat_plus_shaft_work_out_J_kgfresh'],
                  'U_difference_J_kg':float(closed_batch_difference),
                  'maximum_conservation_relative_residual':float(max_relative_residual),
                  'elapsed_s':result['elapsed_s']},indent=2))
