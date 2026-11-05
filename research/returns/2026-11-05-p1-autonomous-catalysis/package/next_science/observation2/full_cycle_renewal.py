"""Exact gate-phase renewal calculation for a complete irreversible ORR cycle.

This is a specified high-affinity model, not an empirical parameter fit.
The independent invention constructor handles fully reversible networks.
Here cold_rates are rates of six balanced forward steps. Gate phase is
0/1; the gate changes at constant up/down rates and can be reset at a
chemical step. Conditional gate-phase arrival is retained exactly.
"""
from pathlib import Path
import json
import mpmath as mp
mp.mp.dps=60
ROOT=Path(__file__).resolve().parent
KB=mp.mpf('8.617333262e-5')
T=mp.mpf(298)
TAU=mp.mpf('4.1e-8')
GAIN=mp.exp(mp.mpf('.192')/(KB*T))
QG=mp.mpf('.126')
DOWN=1/TAU
THERMAL_UP=DOWN*mp.exp(-QG/(KB*T))

def full_cycle(cold_rates, up=0, down=DOWN, hot_ratio=GAIN,
               affected=4, reset_step=None, capture=1, consume=False):
    """Return exact whole-cycle current and stationary initial gate phase.

    R_i has rows indexed by gate before the chemical reaction and columns
    by gate after it. Reset at step0 means the O2 adsorption completion
    creates an excitation. Reset at step3 means perfect alignment on
    arrival at OH*, an explicitly optimistic control comparison.
    """
    up,down,capture=mp.mpf(up),mp.mpf(down),mp.mpf(capture)
    Hs,ts=[],[]
    for i,rate in enumerate(cold_rates):
        k0=mp.mpf(rate);k1=k0*(hot_ratio if i==affected else 1)
        det=k0*k1+k0*down+k1*up
        inv=mp.matrix([[k1+down,up],[down,k0+up]])/det
        R=mp.matrix([[k0,0],[0,k1]])
        if i==reset_step:
            R=mp.matrix([[k0*(1-capture),k0*capture],[0,k1]])
        if consume and i==affected:
            R=mp.matrix([[k0,0],[k1,0]])
        H=inv*R
        assert max(abs(sum(H[r,c] for c in range(2))-1) for r in range(2))<mp.mpf('1e-45')
        Hs.append(H);ts.append(inv*mp.matrix([1,1]))
    H=mp.eye(2)
    for h in Hs:H=H*h
    total=H[0,1]+H[1,0]
    rho=mp.matrix([[1,0]]) if total==0 else mp.matrix([[H[1,0]/total,H[0,1]/total]])
    assert max(abs((rho*H-rho)[i]) for i in range(2))<mp.mpf('1e-42')
    phase=rho.copy();period=mp.mpf(0);waiting=[]
    for h,t in zip(Hs,ts):
        wait=(phase*t)[0];waiting.append(wait);period+=wait;phase=phase*h
    return dict(current=1/period,period=period,rho=rho,
                waiting=waiting,phase_matrices=Hs)

def serializable(r):
    return dict(current=float(r['current']),period=float(r['period']),
      initial_gate=[float(x) for x in r['rho']],
      waiting_seconds=[float(x) for x in r['waiting']])

results=[]
for J0 in [mp.mpf('.2'),mp.mpf(1),mp.mpf(4)]:
    for f in [mp.mpf('.5'),mp.mpf('.75'),mp.mpf('.9')]:
        fractions=[(1-f)/5]*6;fractions[4]=f
        rates=[J0/x for x in fractions]
        cold=1/sum(1/x for x in rates)
        assert abs(cold-J0)<mp.mpf('1e-55')
        cases={
          'cold':full_cycle(rates,up=0,hot_ratio=1),
          'own_adsorption_pulse':full_cycle(rates,up=0,reset_step=0),
          'perfectly_aligned_pulse':full_cycle(rates,up=0,reset_step=3),
          'thermal_gate':full_cycle(rates,up=THERMAL_UP),
          'thermal_plus100_pulses_per_second':full_cycle(rates,up=THERMAL_UP+100),
          'external100_pulses_per_second_without_thermal':full_cycle(rates,up=100),
          'external10000_pulses_per_second_without_thermal':full_cycle(rates,up=10000),
          'continuous_hot_limit':full_cycle(rates,up=mp.mpf('1e40')),
        }
        out=dict(J0=float(J0),cold_target_wait_fraction=float(f),
            cold_rates=list(map(float,rates)),cases={})
        for name,res in cases.items():
            out['cases'][name]=serializable(res)
            out['cases'][name]['gain_vs_cold']=float(res['current']/J0)
            out['cases'][name]['gain_minus_one_decimal']=mp.nstr(res['current']/J0-1,30)
        out['chemical_pump_increment_vs_thermal']=float(
          cases['thermal_plus100_pulses_per_second']['current']/cases['thermal_gate']['current']-1)
        results.append(out)

parameters=dict(T_K=float(T),gate_lifetime_s=float(TAU),
    hypothetical_gate_free_energy_eV=float(QG),barrier_reduction_eV=.192,
    hot_to_cold_rate_ratio=float(GAIN),thermal_up_rate=float(THERMAL_UP),
    thermal_down_rate=float(DOWN),
    scope='q is hypothetical thermal free energy; quoted electronic energy does not establish it. Rates/fractions are declared scenarios spanning observed turnover scale, not fits. Fixed amplitude with exponentially distributed lifetime; not a continuously decaying amplitude.')
(ROOT/'full_cycle_renewal_results.json').write_text(json.dumps(dict(parameters=parameters,results=results),indent=2)+'\n')
print(json.dumps(parameters,indent=2))
for r in results:
 if r['J0']==1:
  print('f=',r['cold_target_wait_fraction'],
    {k:round(v['gain_vs_cold'],9) for k,v in r['cases'].items()},
    'chemical_increment=',r['chemical_pump_increment_vs_thermal'])
