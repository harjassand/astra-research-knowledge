#!/usr/bin/env python3
"""ROOT ideal acid-base inventory diagnostic. No source data or producer code."""
import json,math
from pathlib import Path
MN=.0140067; MCO2=.0440095; MNaOH=.039997
# INTRODUCED ideal25C reference constants and equilibrium-only aqueous species.
pKaN=9.25; pKaC1=6.35; pKaC2=10.33; Kw=1e-14
KN=10**(-pKaN); KC1=10**(-pKaC1); KC2=10**(-pKaC2)
def fractions(pH):
 H=10**(-pH); den=H*H+KC1*H+KC1*KC2
 return KN/(H+KN),(KC1*H+2*KC1*KC2)/den,H
def alk(N,C,pH):
 fn,qc,H=fractions(pH)
 return fn*N+qc*C+Kw/H-H
def charge(N,C,pH,SID):
 # mol/L for introduced final volume1L per admitted initial1L.
 fn,qc,H=fractions(pH)
 return SID+(1-fn)*N+H-qc*C-Kw/H
def find_pH(N,C,SID):
 lo,hi=1.,13.
 assert charge(N,C,lo,SID)>0 and charge(N,C,hi,SID)<0
 for _ in range(100):
  mid=(lo+hi)/2
  if charge(N,C,mid,SID)>0:lo=mid
  else:hi=mid
 return (lo+hi)/2
def reference(N_gL,alk_gCaCO3L,pH0=8.,recovery=.9):
 N=N_gL/14.0067 # gN/L dividedbyg/mol
 A=alk_gCaCO3L/50.043
 fn,qc,H=fractions(pH0)
 C=(A-fn*N-Kw/H+H)/qc
 assert C>=0
 SID=A-N; Nf=N*(1-recovery); R=N-Nf
 # Exact identity for neutral NH3 and CO2 departure and no nonvolatile-ion transfer.
 initial_resid=charge(N,C,pH0,SID)
 p_noC=find_pH(Nf,C,SID)
 final_rows=[]
 for target in [6.5,7.5,8.5]:
  fnf,qcf,Hf=fractions(target)
  Cf=(SID+(1-fnf)*Nf+Hf-Kw/Hf)/qcf
  valid=(0<=Cf<=C)
  row={"target_return_pH":target,"required_DIC_mol_L":Cf,"feasible_with_only_neutral_CO2_removal":valid}
  if valid:
   row.update({"DIC_removed_fraction":1-Cf/C,
    "CO2_kg_per_kg_recoveredN":(C-Cf)*MCO2/(R*MN),
    "final_charge_residual_mol_L":charge(Nf,Cf,target,SID),
    "final_alkalinity_mol_L":alk(Nf,Cf,target),
    "predicted_final_alkalinity_by_inventory":A-R})
   assert abs(alk(Nf,Cf,target)-(A-R))<1e-12
  final_rows.append(row)
 fnlo,qclo,Hlo=fractions(6.5)
 minimum_final_A=fnlo*Nf+Kw/Hlo-Hlo # C>=0, pH>=6.5
 qmin=max(0,R+minimum_final_A-A)
 return {"TAN_gN_L":N_gL,"alkalinity_gCaCO3_L":alk_gCaCO3L,
   "initial_pH":pH0,"recovery":recovery,"initial_DIC_mol_L":C,
   "initial_SID_molEq_L":SID,"initial_charge_residual":initial_resid,
   "initial_TAN_mol_L":N,"removed_N_mol_L":R,
   "pH_if_DIC_not_removed":p_noC,
   "min_extra_strong_equivalents_mol_L_at_return_pH_ge6p5_and_C_ge0":qmin,
   "NaOH_equivalent_kg_per_kg_recoveredN":qmin*MNaOH/(R*MN),
   "return_targets":final_rows}
grid=[reference(N,A) for N in [.7,1,1.5] for A in [2,3.5,5]]
ref=next(x for x in grid if x["TAN_gN_L"]==1 and x["alkalinity_gCaCO3_L"]==3.5)
out={"status":"INTRODUCED_IDEAL_BUFFER_DIAGNOSTIC_NOT_REAL_CENTRATE_QUALIFICATION",
 "equilibrium_pKas_introduced":{"NH4":pKaN,"C1":pKaC1,"C2":pKaC2,"Kw":Kw},
 "volume_convention":"1L initial=1L final for this screen; a real gas/phase/volume balance must use amounts",
 "identity":"A_f=A_i-R_N+DeltaSID for neutral NH3/CO2 loss; DeltaSID includes paid nonvolatile-ion transfer or strong-reagent equivalents",
 "scope":"NH4/NH3, CO2/HCO3/CO3, H/OH only; no phosphate, organics, complexes, activities, kinetic, gas-solubility, membrane or energy model",
 "reference":ref,"grid":grid}
# Sensitivity to nonlinear equilibrium constants does not change exact amount identity.
sens=[]
for pn in [9.,9.25,9.5]:
 KN=10**(-pn)
 x=reference(1,3.5);t=next(y for y in x["return_targets"] if y["target_return_pH"]==7.5)
 sens.append({"introduced_pKaN":pn,"pH_without_C_removal":x["pH_if_DIC_not_removed"],"target7p5":t})
out["pKa_sensitivity"]=sens
assert all(abs(x["initial_charge_residual"])<1e-12 for x in grid)
assert ref["pH_if_DIC_not_removed"]<6.5
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"reference":ref,"equivalent_bounds":[{k:x[k] for k in ["TAN_gN_L","alkalinity_gCaCO3_L","pH_if_DIC_not_removed","NaOH_equivalent_kg_per_kg_recoveredN"]} for x in grid],"pKa_sensitivity":sens},indent=2))
