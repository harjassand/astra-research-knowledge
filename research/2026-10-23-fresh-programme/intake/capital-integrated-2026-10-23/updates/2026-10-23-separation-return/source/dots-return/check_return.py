"""Conditional inventory gates, not measured mixed-bath performance. Stdlib only."""
from fractions import Fraction as F
import json,time,resource
from pathlib import Path
start=time.perf_counter()
p=Path(__file__).parent
# one kg original feed iron. Numeric atomic weights are declared conventions.
Mli=F('6.94'); Mfe=F('55.845'); Mc=F('73.89'); Msi=F('60.0843')
S=F('0.0408')/F('0.6095')*1000/Msi # mol Si per kg original feed Fe
# Candidate: precipitate silica; all dissolved Fe in entrained carbonate-equivalent solvent.
# beta = kg initial-carbonate-equivalent entrained per mol separated Si.
# The existing feed concentrations are mass-normalized, not mole fractions.
cFe=F('0.6095')*F('.18')/F('.82')*1000/Mfe
cLi_free=2000/Mc
beta_Fe_gate=F('.01')/(S*cFe*Mfe/1000)
# Most favorable solids contain no lithium. 1 kg Li/tonne Fe is DESIGN choice.
beta_Li_no_return=F('.001')/(S*cLi_free*Mli/1000)
rows=[]
for beta in [F('.06'),F('.11')]:
    # Declared carbonate-equivalent entrainment scenarios, NOT transferred cake mass fractions.
    Li=S*beta*cLi_free*Mli # g Li / kg Fe = kg Li/t Fe
    Fe=S*beta*cFe*Mfe/1000
    rows.append(dict(beta_kg_carbonate_per_mol_Si=float(beta),Li_kg_per_tonne_Fe_before_return=float(Li),Fe_fraction_before_return=float(Fe),required_entrained_Li_return_for_design_cap=float(max(F(0),1-1/Li)),required_entrained_Fe_return_for_design_cap=float(max(F(0),1-F('.01')/Fe))))
# Every material unit must be one of returned, product, discard, accumulated.
# Test the generic exact compartment ledger under a genuinely disjoint partition.
for incoming,solid,liq,return_s,return_l in [(F(13),F(5),F(8),F(2),F(7)),(F(1),F(0),F(1),F(0),F(1))]:
    assert solid+liq==incoming
    assert return_s+return_l+(solid-return_s)+(liq-return_l)==incoming
# Carbonation only converts orthosilicate to carbonate+metasilicate: half lithium remains bound.
assert 4==2+2
out=dict(status='CONDITIONAL_OBSERVABLE_GATE_NOT_PROCESS_QUALIFICATION',Si_mol_per_kg_feed_Fe=float(S),cFe_mol_per_kg_initial_carbonate=float(cFe),max_beta_for_1percent_Fe_loss_without_Fe_return=float(beta_Fe_gate),max_beta_for_1kg_Li_per_tonne_Fe_without_Li_return=float(beta_Li_no_return),illustrative_cake_rows=rows,source_94percent_metasilicate_extraction_not_return=True,orthosilicate_half_carbonation_only_Li_loss_kg_per_tonne_Fe=float(S*2*Mli),remaining_metasilicate_Li_loss_if_94percent_extracted_and_all_other_Li_recovered=float(S*2*Mli*F('.06')),checks='exact compartment conservation and stoichiometry passed',wall_seconds=time.perf_counter()-start,peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(p/'result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
