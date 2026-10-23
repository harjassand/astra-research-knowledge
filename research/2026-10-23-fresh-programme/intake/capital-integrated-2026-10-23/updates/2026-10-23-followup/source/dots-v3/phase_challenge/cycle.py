"""Explicit Hess cycle with fixed source inputs. No fit or extrapolation."""
from fractions import Fraction as Q
from pathlib import Path
import math,json
R=8.31446261815324
rows=[]
for T,h,c,g,l in [(800,'-611.477','-988.225','-395.586','-494.187'),(900,'-586.510','-960.434','-395.748','-480.247'),(1000,'-561.866','-933.471','-395.886','-466.401')]:
 h,c,g,l=map(Q,(h,c,g,l));a=l+g-c
 models={'Rakshit2011':Q(-708)+Q('.1656')*T}
 if Q('673.15')<=T<=Q('873.15'):models['older_EMF_as_tabulated_Wang2005']=Q(-752)+Q('.187')*T
 for name,f in models.items():
  b=2*f-l-h;d=2*f+g-h-c
  assert a+b==d
  # Sum of balanced stoichiometric vectors equals direct reaction.
  A={'carbonate':-1,'Li2O':1,'CO2':1};B={'Li2O':-1,'hematite':-1,'ferrite':2}
  S={k:A.get(k,0)+B.get(k,0) for k in A.keys()|B.keys()}
  assert S=={'carbonate':-1,'Li2O':0,'CO2':1,'hematite':-1,'ferrite':2}
  rows.append(dict(T_K=T,model=name,LiFeO2_Gf_kJ_mol=float(f),carbonate_phase='crystal' if T<993.15 else 'liquid',carbonate_to_oxide_G_kJ_mol=float(a),ferrite_from_oxides_G_kJ_mol=float(b),net_G_kJ_mol=float(d),eq_fCO2_bar=math.exp(-float(d)*1000/R/T),hess_residual_exact=str(a+b-d)))
# Older-fit coefficient box; not a probabilistic uncertainty statement.
T=800;u=1+.003*T
f_old=-752+.187*T;f_new=-708+.1656*T
cycle_old=next(x for x in rows if x['model'].startswith('older'))['net_G_kJ_mol']
si=(-66400+89.5*T)/1000
pressure_conversion=R*T*math.log(1.01325)/1000
gap=cycle_old+si+pressure_conversion
res=dict(cycles=rows,at800=dict(Gf_difference_kJ_mol=f_new-f_old,old_coefficient_box_halfwidth=u,new_reported_fit_halfwidth=3,nonoverlap_margin_if_boxes_accepted=f_new-f_old-u-3,old_nominal_pressure_gap_affinity_kJ_mol=gap,gap_box_from_old_coefficients_only=[gap-2*u,gap+2*u]),status='CONDITIONAL_EXCLUSION_REPRODUCED_BUT_PHYSICAL_EXCLUSION_NOT_ESTABLISHED',notes=['Older fit used only within its source-tabulated400–600C range.','Quotations of uncertainty are not covariance matrices, confidence intervals or total uncertainty.','No adjustment to any thermochemical input.','Kato TG slope reversal is not imposed as an equilibrium constraint.'])
Path(__file__).with_name('cycle_result.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
