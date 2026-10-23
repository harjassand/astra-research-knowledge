"""Coarse physical single23V coil geometries with explicit resistance allocation.
Not low-loss component qualifications. TotalRA1e-6 is the root favorable lead
screen value. Winding DC resistivity at341K is linked to real copper volume;
remaining R must serve all electrical arms/switches/electrodes. Actual core
loss under1ms pulses remains an unknown joint requirement, never assigned.
"""
from pathlib import Path
import json,numpy as np
R=Path(__file__).resolve().parent
A=.001;LA=1.19709e-6;L=LA/A;jpk=5608.47;I=A*jpk;B=.8;N=20;mur=1e5;mu0=4*np.pi*1e-7
rho293=1.72e-8;alpha=.00393;T=341.4257;rho=rho293*(1+alpha*(T-293.15))
Ac=L*I/(N*B);s=np.sqrt(Ac);t=.008;ell=4*(s+t);fill=.5
# NIST solid copper Shomate from298-1358K, coefficients J/molK; molarmasskg/mol.
x=T/1000;cpCu=(17.72891+28.09870*x-31.25289*x*x+13.97243*x*x*x+.068611/x**2)/.063546
rows=[]
for aw in [80e-6,200e-6,470e-6]:
 # Choose declaredcoarse radii with packing>=50% candidatebudget.
 amin=(t*t+N*aw/(fill*np.pi))/(2*t);a=np.ceil(amin/.01)*.01
 lc=np.pi*(2*a+s);vc=Ac*lc;vcu=N*aw*ell
 mc=7350*vc;mcu=8960*vcu;rc=rho*N*ell/aw;RAc=rc*A;RAw=1e-6-RAc
 gap=mu0*N*N*Ac/L-lc/mur
 rows.append(dict(bank_area_m2=A,normalization='onebankA,paircombinedarea2A',L_device_H=L,peakI_A=I,N=N,
  peakB_T=B,core_Ac_m2=Ac,core_s_m=s,core_inner_radius_m=a,winding_thickness_m=t,
  turn_length_m=ell,wire_crosssection_m2=aw,packing_fraction=N*aw/(np.pi*(2*a*t-t*t)),
  outside_diameter_m=2*(a+s+t),core_path_m=lc,declared_mu_r=mur,gap_m=gap,
  copper_mass_kg=mcu,core_mass_kg=mc,Rcoil_device_ohm=rc,RA_coil_ohm_m2=RAc,
  RA_wire_switch_electrode_remaining_ohm_m2=RAw,
  WF_G_bank_to_floating_controller_W_m2K=8*2.443004509e-8*T/RAw if RAw>0 else None,
  Cnode_Cu_only_J_m2K=mcu*cpCu/A,
  Cnode_with_UNQUALIFIED_core_cp500_JkgK_J_m2K=(mcu*cpCu+mc*500)/A,
  core_specific_loss_Wkg_ceiling_if_entire_0p003869J_half_margin=.003869669575715738*A/(.0039901*mc),
  warning='Physicalgeometricfamilyonly. No measuredcoreL(B),hysteresis,eddy,fringing orpulsedloss. Specifiednewcoilfootprint/massrequiresfreshmatchedsystemallocation. RemainingRAalsoincludesnotyetcountedFET/electrodeR soWFhshownisfavorablelowerbound.'))
out=dict(scope=__doc__,copper_temperature_K=T,copper_rho_ohm_m=rho,copper_Cp_JkgK=cpCu,
 NIST_Cp_source='https://webbook.nist.gov/cgi/cbook.cgi?Name=copper&cTC=on&cTG=on&cTP=on',
 geometry_rows=rows,
 material_source='https://www.vacuumschmelze.cn/products/soft-magnetic-materials-and-stamped-parts/nanocrystalline-material-vitroperm',
 source_limits='VAC suppliesnanocrystalline500/800density7.35g/cm3,saturation1.24T,typicalpermeabilityrange20k-200kand0.03W/kg50Hz1T R-annealedreference. ItdoesNOTsupplyactualgap/pulsewaveformlossorcoreCp500usedabove. CopperalonealreadygiveslargefiniteCnode.')
(R/'single_voltage_coils.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
