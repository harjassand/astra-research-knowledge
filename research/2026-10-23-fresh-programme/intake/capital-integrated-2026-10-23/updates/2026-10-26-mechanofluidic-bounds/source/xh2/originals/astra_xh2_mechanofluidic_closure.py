"""ASTRA XH2: dimensional mechanofluidic closure of a repair comparator.
26 October 2026. Original analytic feasibility derivations and independent numerical checks.
All sample geometry, strain, valve area, cellulose yield, fluid conditions, noise,
oxygen requirement and biological rates are explicit *illustrations*, NOT measured
parameters for an integrated living repair system.

Scaffold: linear matched mechanical bridge, pressure-biased hydraulic gate, culture.
A required external mechanical/hydraulic energy source is always charged.
"""
from math import sqrt, exp, erf, pi
import numpy as np
from scipy.optimize import brentq

# SI mechanics and fluid
K0=1000.       # N/m per normalized reference spring, illustrative
DELTA=20e-6     # imposed tensile displacement over example test region
P=1000.        # Pa external hydraulic bias
WIDTH=100e-6    # m nutrient channel width
LENGTH=1e-3    # m nutrient channel length
MU=0.001        # Pa s, water-like media
A_VALVE=(100e-6)**2  # m^2 wetted area of hypothetical gate
M_CELL=5.       # ug final cellulose required per day
SUGAR_M=0.010   # mol/L nutrient supply glucose
Y=0.2          # gram cellulose per max theoretical gram glucose-to-cellulose
MW_GLUCOSE=180.16
MW_AGU=162.14


def bridge(d,Delta=DELTA,base=K0,k_probe=0):
    a=b=c=base;bottom=d*base
    A=np.array([[a+b+k_probe,-k_probe],[-k_probe,c+bottom+k_probe]])
    u=np.linalg.solve(A, np.array([a,c])*Delta)
    delta0=Delta*((c/(c+bottom))-(a/(a+b)))
    R=1/(a+b)+1/(c+bottom)
    gap=u[1]-u[0]
    gap_exact=delta0/(1+k_probe*R)
    energy_spring=.5*k_probe*gap*gap
    return dict(gap=gap,gap_exact=gap_exact,delta_free=delta0,R=R,
                available_energy=delta0*delta0/(2*R),
                best_spring_energy=delta0*delta0/(8*R),
                best_probe_k=1/R,
                spring_energy=energy_spring,force=k_probe*gap)


def flow(h,pressure=P,w=WIDTH,L=LENGTH,mu=MU):
    assert 0<h<=w
    # low-aspect-ratio laminar rectangular-channel correction, approximate
    m=(1-0.63*h/w)
    q=w*h**3*pressure/(12*mu*L)*m
    return dict(Q_m3_s=q,Q_ul_day=q*86400*1e9,Q_ul_hr=q*3600*1e9)


def cellulose_mass(q_ul_day,yield_fraction=Y,glucose_molar=SUGAR_M):
    glucose_ug=q_ul_day*glucose_molar*MW_GLUCOSE  # 1 mol/L * 1 uL -> 1 umol; g/mol -> ug
    max_ug=glucose_ug*(MW_AGU/MW_GLUCOSE)
    return max_ug*yield_fraction


def gate_cost(h,pressure=P,A=A_VALVE):
    return pressure*A*h  # p dV mechanical work scale, joules


def minimum_h(m_cell=M_CELL,yield_fraction=Y):
    return brentq(lambda h:cellulose_mass(flow(h)['Q_ul_day'],yield_fraction)-m_cell,1.e-7,20e-6)


def sensor_noise_error(d,Delta=DELTA,sigma=50e-9):
    sig=bridge(d,Delta=Delta)['delta_free']/2 # use k=1/R optimal energy probe
    return .5* (1-erf(abs(sig)/(sigma*sqrt(2))))


def d_equal_energy(required,kind='available',Delta=DELTA):
    label='available_energy' if kind=='available' else 'best_spring_energy'
    return brentq(lambda d:bridge(d,Delta=Delta)[label]-required,.2,.999999)


def validation(seed=2034):
    rng=np.random.default_rng(seed);err=0.;eerr=0.
    for _ in range(1000):
        d=rng.uniform(.1,2);delta=rng.uniform(1e-6,100e-6);k=rng.uniform(0,8000.)
        y=bridge(d,Delta=delta,k_probe=k)
        err=max(err,abs(y['gap']-y['gap_exact']))
        h=1e-5
        ob=bridge(d,Delta=delta)['best_spring_energy']
        kopt=bridge(d,Delta=delta)['best_probe_k']
        # Differentiate spring energy around optimum numerically
        hstep=kopt*1e-3
        numerical=(bridge(d,Delta=delta,k_probe=kopt+hstep)['spring_energy']-
                   bridge(d,Delta=delta,k_probe=kopt-hstep)['spring_energy'])/(2*hstep)
        eerr=max(eerr,abs(numerical))
        assert abs(bridge(d,Delta=delta,k_probe=kopt)['spring_energy']-ob) <1e-19
    return err,eerr


def budget():
    h=minimum_h()
    q=flow(h)['Q_ul_day']
    gc=gate_cost(h)
    r={}
    for d in [.7,.9,.94,.95,.96,.98,.99]:
        x=bridge(d)
        r[d]=dict(delta_nm=x['delta_free']*1e9,available_pJ=x['available_energy']*1e12,
                  spring_pJ=x['best_spring_energy']*1e12,
                  gate_vs_available=gc/x['available_energy'],
                  gate_vs_spring=gc/x['best_spring_energy'],
                  optimal_force_uN=x['delta_free']/(2*x['R'])*1e6,
                  optimal_stroke_nm=x['delta_free']*1e9/2)
    return dict(h_min_um=h*1e6,feed_ul_day=q,
                glucose_ug_day=q*SUGAR_M*MW_GLUCOSE,
                predicted_cellulose_ug_day=cellulose_mass(q),
                gate_energy_pJ=gc*1e12,
                d_energy_total=d_equal_energy(gc),
                d_energy_spring=d_equal_energy(gc,'spring'),
                summary=r,
                oxygen_nmol_day=q*.258, # 0.258 mM dissolved O2 == 0.258 nmol/uL
                cellulose_monomer_nmol_day=M_CELL/MW_AGU*1000.)


def steady_fraction_acid(f_glucose_to_gluconic=.2,chamber_ul=1.,Q_ul_day=None,
                         buffer_mM_per_pH=10.):
    # Only a sanity check of stoichiometric acidity and control volume.
    if Q_ul_day is None:Q_ul_day=budget()['feed_ul_day']
    glucose_nmol_day=Q_ul_day*SUGAR_M*1000. # 10mM * 1uL ==10 nmol
    produced_nmol=glucose_nmol_day*f_glucose_to_gluconic
    ph_drift_closed=produced_nmol/(chamber_ul*buffer_mM_per_pH) # 1 mM * 1uL = 1 nmol
    delta_ph_steady=produced_nmol/(Q_ul_day*buffer_mM_per_pH)
    return dict(glucose_nmol_day=glucose_nmol_day,acid_nmol_day=produced_nmol,
                closed_change_pH_day=ph_drift_closed,flowing_offset_pH=delta_ph_steady)


if __name__=='__main__':
    np.set_printoptions(precision=5,suppress=True)
    print('Validation:max exact-gap absolute err, derivative at maximum',validation())
    x=budget()
    for key,val in x.items():
        if key!='summary':print(key, val)
    print('d, delta nm, Umax pJ, spring pJ, valve/total, valve/spring, force uN')
    for d,v in x['summary'].items():
        print(d,*(round(v[k],4) for k in ['delta_nm','available_pJ','spring_pJ','gate_vs_available','gate_vs_spring','optimal_force_uN']))
    print('channel size sensitivity')
    for h in [2e-6,2.5e-6,3e-6,4e-6,5e-6]:
        z=flow(h);print(h*1e6,z['Q_ul_day'],cellulose_mass(z['Q_ul_day']))
    print('noise at 2 pct and 1 pct stiffness differences, sigma=50nm')
    for d in [.9,.96,.98,.99,1.01,1.02]:
        print(d, 'unloaded gap nm',bridge(d)['delta_free']*1e9,
              'loaded gap nm',bridge(d)['delta_free']*1e9/2,
              'error',sensor_noise_error(d))
    print('acid flux caution', steady_fraction_acid())


def biased_bridge_zero(Fbias,Delta=DELTA,base=K0):
    """Exactly solve zero readout when the valve adds unbalanced force Fbias
    to one bridge midpoint. For a=b=c=base, d is unknown normalized bottom
    stiffness, Delta prescribed. d=(base*Delta-3Fbias)/(base*Delta+Fbias).
    This assumes Fbias has sign that mimics a positive-repair-stiffness change.
    """
    return (base*Delta-3*Fbias)/(base*Delta+Fbias)


def biased_readout(d,Fbias,Delta=DELTA,base=K0,k_probe=0.):
    xx=bridge(d,Delta=Delta,base=base,k_probe=k_probe)
    return (xx['delta_free']-xx['R']*Fbias)/(1+k_probe*xx['R'])


def bias_checks():
    out=[]
    for Delta in [20e-6,5e-6,2e-6]:
        for Fb in [0,1e-7,1e-6,10e-6,100e-6]:
            d=biased_bridge_zero(Fb,Delta=Delta)
            err=abs(biased_readout(d,Fb,Delta=Delta)) if d>0 else None
            out.append((Delta*1e6,Fb*1e6,d,err))
    return out


def hydraulic_power(Q_ul_day=1,pressure=P):
    # 1 uL/day = 1e-9 m3 / 86400 seconds
    q=Q_ul_day*1e-9/86400.
    return {'pilot_ul_day':Q_ul_day,'pressure_pa':pressure,
            'energy_uJ_day':pressure*Q_ul_day*1e-3,
            'power_nW':pressure*q*1e9}

if __name__=='__main__':
    print('bias thresholds: drive um, residual force uN, apparent switch stiffness, readout err')
    for x in bias_checks():print(*x)
    print('1uL/day pilot flow expense',hydraulic_power())
    print('sugar flow expense',hydraulic_power(budget()['feed_ul_day']))


def min_drive_for_switch(d,required_energy=None,kind='absolute'):
    if required_energy is None:required_energy=gate_cost(minimum_h())
    x=bridge(d)
    E=x['available_energy' if kind=='absolute' else 'best_spring_energy']
    return DELTA*sqrt(required_energy/E)


def drive_for_sign_reliability(d,sigma=50e-9,zscore=2.326348):
    # Gaussian one-sided 1% error. Loaded probe at optimal linear-spring energy.
    gap_ratio=abs(bridge(d)['delta_free']/DELTA)/2.
    return sigma*zscore/gap_ratio

if __name__=='__main__':
    print('minimum drive delta for 2pct comparator within our illustrative valve geometry')
    for d in [.9,.94,.96,.98,.99]:
        print(d,'absolute um',round(min_drive_for_switch(d)*1e6,3),
              'optimal spring um',round(min_drive_for_switch(d,kind='spring')*1e6,3),
              '99pct sign drive um',round(drive_for_sign_reliability(d)*1e6,3))


def diagnostic_probe(d=.98,delta=DELTA,base=K0,area=1e-6):
    # Both mechanical branches between common surfaces; unloaded midpoint coupler.
    # Equivalent series stiffness of two arms, each with EAs/L-like springs.
    Keq=base*(.5+d/(1+d))
    F=Keq*delta
    return dict(effective_stiffness_N_m=Keq,force_mN=F*1e3,
                pressure_kPa=F/area/1000,
                strain_energy_uJ=.5*Keq*delta*delta*1e6,
                displaced_fluid_nL=area*delta*1e12)


def predicted_cellulose_mass_with_oxygen(Q_ul_day,oxygen_mM=.258,ox_per_agu=0.5,
                                        yield_fraction=Y):
    # Q only brings dissolved oxygen from a reservoir. Oxygen stoichiometry is
    # an illustrative *demand parameter*, not empirically established yield.
    C_by_glucose=cellulose_mass(Q_ul_day,yield_fraction)
    O2_nmol=Q_ul_day*oxygen_mM
    O2_max_agu_nmol=O2_nmol/ox_per_agu
    O2_max_cellulose_ug=O2_max_agu_nmol*MW_AGU/1000
    return min(C_by_glucose,O2_max_cellulose_ug)

if __name__=='__main__':
    print('diagnostic mechanical excitation',diagnostic_probe())
    qq=budget()['feed_ul_day']
    print('oxygen versus carbon max cellulose at oxygen per AGU')
    for beta in [.05,.1,.2,.5,1.,2.]:
        m=predicted_cellulose_mass_with_oxygen(qq,ox_per_agu=beta)
        print(beta,round(m,5),'ug/day', 'O2 mg-limited' if m<M_CELL-.01 else 'carbon-limit')


def fouling_limit(solids_fraction=1.0, Qfactor=.5):
    h0=minimum_h()
    Q0=flow(h0)['Q_m3_s']
    hleft=brentq(lambda h:flow(h)['Q_m3_s']-Qfactor*Q0,0.01e-6,h0)
    thickness=h0-hleft
    wetvolume_m3=WIDTH*LENGTH*thickness
    drymass_ug=wetvolume_m3 * 1500 * solids_fraction * 1e9 # kg to ug
    return dict(h0_um=h0*1e6,hleft_um=hleft*1e6,
                deposit_um=thickness*1e6,
                dry_mass_ug=drymass_ug,
                fraction_of_5ug_repair=drymass_ug/M_CELL,
                solids_fraction=solids_fraction)

if __name__=='__main__':
    print('uniform deposition needed to halve nutrient flow')
    for sf in [1,.1,.01]:print(fouling_limit(solids_fraction=sf))


def membrane_resistance_penalty(relative_R,nominal_flow=None):
    # Hypothetical extra membrane resistance in series with source's R0,
    # at unchanged pressure. Real membrane permeability unknown.
    if nominal_flow is None:nominal_flow=budget()['feed_ul_day']
    return {'relative_membrane_resistance':relative_R,
            'flow_ul_day':nominal_flow/(1+relative_R),
            'cellulose_ug_day':cellulose_mass(nominal_flow/(1+relative_R))}


def additional_oxygen_area(beta_o2_per_agu=.5, oxygen_feed_mM=.258,
                           D=2e-9,dc_mol_m3=.258,thickness=100e-6):
    # Required diffusive gas-side hydrated interface area, ideal Fick flux.
    q=budget()['feed_ul_day']
    O2_comes_nmol=q*oxygen_feed_mM
    AGU_nmol=M_CELL/MW_AGU*1000
    missing=max(0.,beta_o2_per_agu*AGU_nmol-O2_comes_nmol)
    flux_mol_per_m2_day=D*dc_mol_m3/thickness*86400.
    return dict(beta=beta_o2_per_agu,need_extra_nmol_day=missing,
                ideal_area_mm2=missing*1e-9/flux_mol_per_m2_day*1e6)

if __name__=='__main__':
    print('added serial membrane hydraulic resistance bound')
    for r in [0,.1,1,3,10]:print(membrane_resistance_penalty(r))
    print('ideal diffusive area to replenish oxygen independent of nutrient flow')
    for beta in [.1,.2,.5,1.,2.]: print(additional_oxygen_area(beta))


def harvested_cycles(d=.98,conversion_efficiency=1.0):
    x=bridge(d); cost=gate_cost(minimum_h());
    return {'d':d,'eta':conversion_efficiency,
            'cycles_ideal_available':int(np.ceil(cost/(conversion_efficiency*x['available_energy']))),
            'cycles_best_linear_spring':int(np.ceil(cost/(conversion_efficiency*x['best_spring_energy'])))}

if __name__=='__main__':
    print('strain powered energy harvesting cycles for one gate actuation')
    for d in [.9,.95,.98,.99]:
        for e in [1.0,.2]:print(harvested_cycles(d,e))


def independent_reads_for_reliability(d=.98,Delta=DELTA,
                                      noise_sigma=50e-9,
                                      all_regions=20,all_probability=.9):
    from scipy.special import ndtri
    signal=abs(bridge(d,Delta=Delta)['delta_free'])/2
    z=ndtri(all_probability**(1/all_regions))
    n=int(np.ceil((z*noise_sigma/signal)**2)) if signal>0 else float('inf')
    return dict(d=d,drive_um=Delta*1e6,sensor_signal_nm=signal*1e9,
                target_z=z,n_independent=n)

if __name__=='__main__':
    print('noise limited rereads under assumed Gaussian independent sensor noise')
    for Delta in [2e-6,10e-6,20e-6,40e-6]:
        for d in [.98,.99]:print(independent_reads_for_reliability(d,Delta))
