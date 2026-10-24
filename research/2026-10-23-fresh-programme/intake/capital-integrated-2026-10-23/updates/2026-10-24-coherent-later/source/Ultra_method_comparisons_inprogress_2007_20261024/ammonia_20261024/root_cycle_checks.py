"""Exact element/charge and cycle-work checks; no chemical rate/device fixture.

All reactions are written per mole NH3. Free energies are symbolic coefficients
of species chemical potentials; the code does not assign favorable potentials.
"""
from fractions import Fraction as F
from pathlib import Path
import json

atoms = {
    'N2': (0,2,0,0), 'O2': (0,0,2,0), 'H2': (2,0,0,0),
    'H2O': (2,0,1,0), 'NH3': (3,1,0,0), 'H+': (1,0,0,1),
    'e-': (0,0,0,-1), 'NO2-': (0,1,2,-1), 'NO3-': (0,1,3,-1),
    'HNO2': (1,1,2,0), 'HNO3': (1,1,3,0), 'OH-': (1,0,1,-1),
}

def reaction(**kwargs):
    return {k:F(v) for k,v in kwargs.items() if v}

def add(*terms):
    result={}
    for term in terms:
        for s,v in term.items(): result[s]=result.get(s,F(0))+v
    return {s:v for s,v in result.items() if v}

def scale(k,r): return {s:F(k)*v for s,v in r.items() if F(k)*v}
def balance(r): return [sum(v*atoms[s][j] for s,v in r.items()) for j in range(4)]
def dump(r): return {s:str(v) for s,v in sorted(r.items())}

direct = reaction(N2=F(-1,2),H2O=F(-3,2),NH3=1,O2=F(3,4))
hb = reaction(N2=F(-1,2),H2=F(-3,2),NH3=1)
water_electrolysis = reaction(H2O=-1,H2=1,O2=F(1,2))
nitrite_oxidation = reaction(N2=F(-1,2),O2=F(-3,4),H2O=F(-1,2),HNO2=1)
nitrite_cell = reaction(HNO2=-1,H2=-3,NH3=1,H2O=2)
nitrate_oxidation = reaction(N2=F(-1,2),O2=F(-5,4),H2O=F(-1,2),HNO3=1)
nitrate_cell = reaction(HNO3=-1,H2=-4,NH3=1,H2O=3)
nitrite_cathode = {'NO2-':F(-1),'H+':F(-7),'e-':F(-6),'NH3':F(1),'H2O':F(2)}
nitrite_anode = {'H2':F(-3),'H+':F(6),'e-':F(6)}
nitrite_alkaline_cathode = {'NO2-':F(-1),'H2O':F(-5),'e-':F(-6),'NH3':F(1),'OH-':F(7)}
nitrite_alkaline_anode = {'H2':F(-3),'OH-':F(-6),'H2O':F(6),'e-':F(6)}
cycles={
    'HB_plus_water_electrolysis':add(hb,scale(F(3,2),water_electrolysis)),
    'nitrite_plus_water_electrolysis':add(nitrite_oxidation,nitrite_cell,scale(3,water_electrolysis)),
    'nitrate_plus_water_electrolysis':add(nitrate_oxidation,nitrate_cell,scale(4,water_electrolysis)),
}
all_reactions={
    'direct':direct,'HB':hb,'water_electrolysis':water_electrolysis,
    'nitrite_oxidation':nitrite_oxidation,'nitrite_cell':nitrite_cell,
    'nitrate_oxidation':nitrate_oxidation,'nitrate_cell':nitrate_cell,
    'nitrite_cathode':nitrite_cathode,'nitrite_anode':nitrite_anode,
    'nitrite_alkaline_cathode':nitrite_alkaline_cathode,
    'nitrite_alkaline_anode':nitrite_alkaline_anode,
}
for name,r in all_reactions.items():
    assert balance(r)==[0,0,0,0],(name,balance(r))
for name,r in cycles.items(): assert r==direct,(name,r)
acid_net=add(nitrite_cathode,nitrite_anode)
alkaline_net=add(nitrite_alkaline_cathode,nitrite_alkaline_anode)
assert acid_net=={'NO2-':F(-1),'H+':F(-1),'NH3':F(1),'H2O':F(2),'H2':F(-3)}
assert alkaline_net=={'NO2-':F(-1),'H2O':F(1),'NH3':F(1),'OH-':F(1),'H2':F(-3)}

# For a reversible gated capture/transfer/release construction, arbitrary
# bA0,bA1,bB0,bB1,d are formal coefficients. Chemical stages plus restored
# gate work cancel to d, with no asserted absolute barrier/current.
# capture bA0; transfer bB0-bA1; release d-bB1;
# gate boundA0->1+emptyrestore bA1-bA0;
# gate boundB0->1+emptyrestore bB1-bB0.
coefficients={k:F(0) for k in ('bA0','bA1','bB0','bB1','d')}
for term in ({'bA0':1},{'bB0':1,'bA1':-1},{'d':1,'bB1':-1},
             {'bA1':1,'bA0':-1},{'bB1':1,'bB0':-1}):
    for k,v in term.items(): coefficients[k]+=v
assert coefficients=={'bA0':0,'bA1':0,'bB0':0,'bB1':0,'d':1}

out={
    'scope':'exact stoichiometry and symbolic cycle identity only; no rates or apparatus acquired',
    'element_charge_order':['H','N','O','charge'],
    'balanced_reactions':{k:dump(v) for k,v in all_reactions.items()},
    'full_cycle_stoichiometry':{k:dump(v) for k,v in cycles.items()},
    'acid_cell_net':dump(acid_net),'alkaline_cell_net':dump(alkaline_net),
    'gated_cycle_free_energy_coefficients':dump(coefficients),
    'energetic_identity':'For common isothermal matched reservoirs and no uncharged heat/material input: net work = DeltaG_air_water_NH3 + irreversible losses; recovered fuel-cell work is subtracted once. Other-temperature heat requires explicit exergy accounting.',
    'not_claimed':['feasible catalyst','positive useful current','plant efficiency','novelty','route superiority'],
}
target=Path(__file__).with_name('root_cycle_checks.json')
target.write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 11 reactions balanced, 3 full cycles identical, gate-energy coefficients cancel to d.')
print(target)
