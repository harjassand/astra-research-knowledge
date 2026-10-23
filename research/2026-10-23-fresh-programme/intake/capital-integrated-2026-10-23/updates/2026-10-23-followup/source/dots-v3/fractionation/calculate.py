"""Inventory and ideal binary-solubility screens, NOT a mixed-ore phase solver."""
from fractions import Fraction as Q
import json, time, resource
from pathlib import Path
start=time.perf_counter()
Fe=Q('0.6095'); Si=Q('0.0408'); Al=Q('0.0246'); ore=Q('0.18')
MFe=Q('0.055845'); MSi=Q('0.0600843'); MC=Q('0.0738909'); MLi=Q('0.00694'); MAl=Q('0.1019613')
nsi=Si/Fe/MSi; nal=2*Al/Fe/MAl
cold=Q('5.5'); hot=Q('11'); C0=(1-ore)/MC
nsi_batch=ore*Si/MSi; nfe_batch=ore*Fe/MFe; nal_batch=2*ore*Al/MAl
# Input molality based on charged carbonate, not an inferred thermodynamic activity.
mSi=nsi_batch/(1-ore); mFe=nfe_batch/(1-ore)
# Illustrative complete lithiation consumes carbonate: 2/Si, 1/2 per Fe, 1/2 per Al.
remaining_C=C0-2*nsi_batch-nfe_batch/2-nal_batch/2
assert remaining_C>0
mSi_after=nsi_batch/(remaining_C*MC)
# Sole Si sink, no other Li hosts: fraction of Li units in silicate at saturation.
def bound_stock(m):
    f=2*m*MC/(1+2*m*MC)
    # Independent check: start with 1 mol carbonate, solve n/(MC*(1-2n))=m.
    n=m*MC/(1+2*m*MC)
    assert n/(MC*(1-2*n))==m and f==2*n
    return f
# Closed temperature swing idealization: same kg carbonate solvent between hot/cold states.
circulation=nsi/(hot-cold)
li_si=4*MLi*nsi; li_al=MLi*nal
max_FeSi=(Q('.01')/MFe)/nsi
# 1kg Li/tFe is chosen screen, NOT an externally justified environmental/cost threshold.
required_Li_return=max(Q(0),1-Q('.001')/li_si)
result={
 'status':'CONDITIONAL_INVENTORY_SCREEN_NOT_ADMITTED_FRACTIONATION',
 'input_Si_mol_per_kg_initial_carbonate':float(mSi),
 'input_Fe_mol_per_kg_initial_carbonate':float(mFe),
 'binary_cold_Si_saturation_to_nominal_feed_ratio':float(cold/mSi),
 'illustrative_full_lithiation_Si_mol_per_kg_remaining_carbonate':float(mSi_after),
 'Si_mol_per_kg_original_feed_Fe':float(nsi),
 'ideal_carbonate_solvent_circulation_kg_per_kg_original_feed_Fe':float(circulation),
 'Li_units_in_Si_fraction_Si_only_closed_stock':{str(float(m)):float(bound_stock(m)) for m in [cold,hot]},
 'orthosilicate_Li_throughput_kg_per_tonne_original_feed_Fe':float(1000*li_si),
 'aluminate_Li_throughput_kg_per_tonne_original_feed_Fe':float(1000*li_al),
 'Si_only_Li_return_fraction_for_selected_1kg_per_tonne_loss_cap':float(required_Li_return),
 'max_solid_Fe_to_Si_mol_ratio_for_selected_1percent_feed_Fe_loss':float(max_FeSi),
 'Fe_loss_fraction_if_all_Si_purged_as_1to1_FeSi':float(nsi*MFe),
 'exact_arithmetic_identity_checks':'PASS',
 'elapsed_seconds':time.perf_counter()-start,
 'peak_RSS_KiB_Linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
 'scope':'Binary source endpoints; no multicomponent liquidus, activities, nucleation, occluded mother liquor, Fe partition, regeneration kinetics, heat, hydraulic or full-cycle energy admitted. Fe denominator is original feed Fe, not recovered metal.'}
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
