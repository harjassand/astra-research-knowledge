"""Observed split-feed operation and exact conditional resource headroom.
No kinetic simulation; no empirical confidence level assigned to graphic envelopes.
"""
from pathlib import Path
import json,time,resource,math
D=Path(__file__).resolve().parent;st=time.monotonic();a=json.loads((D/'digitized.json').read_text());rows=[];by={(r['configuration'],r['reported_power_W']):r for r in a['rows']}
for P in [400,500,600,700]:
 b=by['intrinsic',P];f=by['forced',P];bl,bh=b['graphic_envelope_fraction'];fl,fh=f['graphic_envelope_fraction'];bc=b['center_fraction'];fc=f['center_fraction']
 # If NOx=xNO+xNO2, 0<=xNO2<=NOx, four reactive species plus conserved inert net balance.
 glo=(fl/(1+fl/2))/bh;ghi=fh/(bl/(1+bl/2));gc=fc/bc
 # Symmetric opposite calibration error: forced*(1-e),baseline*(1+e).
 emax=(glo-1)/(glo+1)
 costs=[]
 # Explicit reference standard conventions, not recovered experimental flow definition.
 for V in [22.414,24.466]:
  nq=10/V/60
  for eta_c in [.25,.5,1.]:
   rmax=math.exp(P*(glo-1)*eta_c/(nq*8.31446261815324*300))
   costs.append({'standard_molar_volume_L_mol':V,'isothermal_compressor_efficiency_hypothesis':eta_c,'max_pressure_ratio_if_only_additional_10SLM_compression_and_equal_unity_power_efficiency':rmax})
 rows.append({'reported_power_W':P,'intrinsic_reported_NOx_center_pct':100*bc,'forced_reported_NOx_center_pct':100*fc,'reported_concentration_gain_center_ratio':gc,'four_species_graphic_product_gain_envelope':[glo,ghi],'center_reported_energy_per_NOx_reduction_fraction':1-1/gc,'four_species_graphic_reduction_envelope':[1-1/glo,1-1/ghi],'extra_power_allowance_W_if_equal_unity_conversion_and_no_baseline_aux':P*(glo-1),'minimum_eta_forced_over_eta_intrinsic_if_no_aux_and_using_glo':1/glo,'max_symmetric_opposite_relative_calibration_bias_to_preserve_positive_glo':emax,'compression_scenarios_not_measured':costs})
# At a shared tested power P, output thresholds between b.upper and f.lower
# strictly separate configurations. To imply exact matched-output lower power,
# add continuous nondecreasing response and bracket within measured range.
windows=[]
for P in [500,600]:
 b=by['intrinsic',P];f=by['forced',P];low=b['graphic_envelope_fraction'][1];high=f['graphic_envelope_fraction'][0]/(1+f['graphic_envelope_fraction'][0]/2)
 # Must be above forced lowest point, below intrinsic highest point for existence.
 low=max(low,by['forced',400]['graphic_envelope_fraction'][1]);high=min(high,by['intrinsic',700]['graphic_envelope_fraction'][0]/(1+by['intrinsic',700]['graphic_envelope_fraction'][0]/2))
 if high>low:windows.append({'separating_reported_power_W':P,'strict_target_fixedN_per_inlet_mole_interval':[low,high],'claim':'Under four-species closure and continuous nondecreasing corrected fixed-N output per inlet mole consistent with the graphic envelopes, exact target production at20SLM occurs belowP forforced and aboveP forintrinsic. No uniform positive Watt gap follows without a slope bound; no 100W savings guaranteed by grid spacing.','conditional_graphic_observation':'With the explicit four-species closure, at this shared measured setting forced exceeds the target fixed-N per feed and intrinsic does not, within graphical envelopes only.'})
# Same indicated power and true concentration ratio but opposite actual electrical ranking.
P=500.;g=rows[1]['reported_concentration_gain_center_ratio'];eb=P/.8;ef=P/.6
counter={'P_indicated_W':P,'yield_gain_ratio':g,'baseline_eta':.8,'forced_eta':.6,'baseline_electric_W':eb,'forced_electric_W':ef,'forced_over_baseline_electric_SEC':ef/eb/g,'scope':'Constructive missing-input counterexample, not inferred generator efficiencies.'}
result={'scope':__doc__,'rows':rows,'matched_quality_conditional_windows':windows,'power_ordering_counterexample':counter,'general_inequality':'With G=Nforced/Nbase, Eforced=P/etaF+AF and Ebase=P/etaB+AB, forced SEC wins exactly when AF-G*AB < P*(G/etaB-1/etaF). All terms are actual input powers under a consistent boundary. Equal indicated power alone does not establish it.','matched_target_electrical_condition':'At matched corrected production, G=1 and reported powers generally differ. Forced actual power wins exactly when AF(PF)-AB(PB) < PB/etaB(PB)-PF/etaF(PF). The same-P yield headroom is not itself a measured matched-output saving.', 'compression_scope':'Reference reversible isothermal cold compression at300K, additional pressure work on the existing10SLM quench share only: J=nRT ln(r)/etaC. Here r is an incremental pressure ratio relative to the pressure already charged to that share in the ordinary feed, not automatically pressure relative to ambient. Total original feed remains20SLM. These are thresholds, not assumed device pressures, efficiencies or qualified pump work. Different upstream feed requirements, pressure recovery, common compressor loss and gas drying must be accounted; do not charge a shared input twice.','observable_scope':'Reported FTIR NOx chart is treated as its stated observable. Four-reactive-species corrections additionally assume xNOx=xNO+xNO2, allow conserved inert gas, and exclude other uncounted reactive side gas/solid inventory. No separateNO2 data or complete product closure supplied. Bounds do not repair unknown calibration, residence time or wall integrity.','limits':['Matched original total feed and reported power are measured comparisons, not isolated quench interventions or measured wall-plug savings.','10SLM intrinsic plus late10SLM dilution control is CFD only. Model flux comparison is stronger than a concentration-only comparison but not experimental mechanism identification.','No complete300K/1atm product, gas/solid thermal reset, hot-spot lifetime, outlet enthalpy or recovered heat claim.','These data are different from the old2700K heater. Do not transplant its1.407MJ/kg bound or retention benchmark.','Graphic envelopes combine drawn bars and reading allowance; they are neither probability intervals nor full measurement uncertainty.','Exact target fixed-N interpolation requires four-species closure and continuity/monotonicity of corrected output; no measured matched-quality retrofit or positive minimum Watt gap established.'],'elapsed_s':time.monotonic()-st,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(D/'admission.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
