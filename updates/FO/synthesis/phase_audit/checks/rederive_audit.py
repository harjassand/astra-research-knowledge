#!/usr/bin/env python3
"""Independent standard-library checks; does not import the producer script."""
from decimal import Decimal as D, getcontext
from fractions import Fraction
from pathlib import Path
import json

getcontext().prec = 40
TREF, TM, L = D("298.15"), D("1514"), D("106720")

def Hrel(t):
    return D("47.3")*t + D("3.99e-3")*t*t + D("2.40e5")/t - D("1.53e4")

def Hs(t0):
    return Hrel(TM) if t0 == TREF else Hrel(TM)-Hrel(t0)

def Cstar(h, latent=L):
    return latent/(2*h+latent)

def f_sup(c,h,latent=L):
    return min(D(1), 2*c*h/((1-c)*latent))

temperatures = list(map(D, ("298.15","800","1000","1200","1400","1500")))
rows=[]
for t0 in temperatures:
    h=Hs(t0); c=Cstar(h)
    rows.append({"initial_temperature_K":str(t0),"Hs_J_per_mol":str(h),
                 "Cstar":str(c),"threshold_hot_to_cold_specific_dose_ratio":str((1+c)/(1-c))})

# At C=Cstar, the permitted baseline-dose interval collapses to one point;
# strict protection of the cold patch excludes that endpoint.
h=Hs(TREF); c=Cstar(h)
q_hot_min=(h+L)/(1+c)
q_cold_max=h/(1-c)
assert abs(q_hot_min-q_cold_max) < D("1e-30")

# Exact partial-melt witness: Hs=5, L=3, C=1/10, f=1/3 < f_sup=10/27.
Hf,Lf,Cf,f=Fraction(5),Fraction(3),Fraction(1,10),Fraction(1,3)
bound=2*Cf*Hf/((1-Cf)*Lf)
qlo=(Hf+f*Lf)/(1+Cf); qhi=Hf/(1-Cf); Q=(qlo+qhi)/2
assert f < bound and Q*(1+Cf) > Hf+f*Lf and Q*(1-Cf) < Hf

# Exact equal-patch sustained-cooling countermodels. Normalize G*DeltaT=Pbar=1.
cooling=[]
for C in (Fraction(1,50),Fraction(1,10),Fraction(1,2)):
    cold,hot=1-C,1+C
    assert cold < 1 < hot
    cooling.append({"C":str(C),"cold_steady_drive":str(cold),
                    "hot_power_surplus_at_Tm":str(hot-1),
                    "unit_latent_energy_time":str(1/(hot-1))})

# Exact total-energy-vs-specific-energy countermodel for unequal patch amounts.
n_hot,n_cold,each=Fraction(1,4),Fraction(1),Fraction(3,5)
q_h,q_c=each/n_hot,each/n_cold
assert q_h >= 2 and q_c < 1

# Local first-order sensitivity only; source uncertainty convention/covariance unknown.
cp= D("47.3")+2*D("3.99e-3")*TM-D("2.40e5")/(TM*TM)
dh=D("100")+cp  # table +/-100 J/mol plus local 1 K Tm sensitivity
dl=D("200")     # fusion heat +/-0.20 kJ/mol
c_lo=(L-dl)/(2*(h+dh)+L-dl)
c_hi=(L+dl)/(2*(h-dh)+L+dl)

result={
 "scope":"independent algebra and arithmetic only; no physical validation",
 "room_temperature":{"Hs_J_per_mol":str(h),"L_J_per_mol":str(L),
   "complete_melt_enthalpy_J_per_mol":str(h+L),"Cstar":str(c),
   "specific_dose_ratio_at_Cstar":str((1+c)/(1-c)),
   "collapsed_dose_gap_J_per_mol":str(q_cold_max-q_hot_min)},
 "nominal_temperature_rows":rows,
 "exact_partial_melt_witness":{"Hs":str(Hf),"L":str(Lf),"C":str(Cf),
   "melt_fraction":str(f),"fraction_supremum":str(bound),
   "baseline_dose_Q":str(Q),"hot_specific_dose":str(Q*(1+Cf)),
   "cold_specific_dose":str(Q*(1-Cf))},
 "sustained_cooling_countermodels":cooling,
 "unequal_patch_countermodel":{"n_hot":str(n_hot),"n_cold":str(n_cold),
   "equal_total_energy_each":str(each),"total_energy_contrast":"0",
   "hot_specific_dose":str(q_h),"cold_specific_dose":str(q_c),
   "conditions":"hot fully melts at Hs+L; cold remains below Hs"},
 "linearized_sensitivity_not_confidence_interval":{"Cp_Tm_J_per_mol_K":str(cp),
   "assumed_Hs_half_width_J_per_mol":str(dh),"assumed_L_half_width_J_per_mol":str(dl),
   "Cstar_low":str(c_lo),"Cstar_high":str(c_hi),
   "warning":"Source gives no statistical convention or fit covariance; 1 K derivative is local and upper endpoint lies 1 K beyond the tabulated solid-fit range."}
}
out=Path(__file__).with_name("independent_checks.json")
out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,indent=2))
