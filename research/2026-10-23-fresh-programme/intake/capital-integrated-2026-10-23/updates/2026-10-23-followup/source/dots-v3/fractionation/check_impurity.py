from pathlib import Path
import json
p=Path(__file__).parent
x=json.loads((p/'impurity_rows.json').read_text())
r=[]
for d in x['rows']:
 s=d['Li4SiO4_g']/x['source_molar_mass_Li4SiO4_g_mol']/(d['Li2CO3_g']/1000)
 e=x['current_A']*x['duration_hours']*d['average_cell_V']/d['Fe0_product_g']
 r.append(dict(Si_mol_per_kg_charged_carbonate=s,cell_electrical_kWh_per_kg_assayed_Fe0=e))
y=dict(rows=r,high_to_low_specific_energy_ratio=r[-1]['cell_electrical_kWh_per_kg_assayed_Fe0']/r[0]['cell_electrical_kWh_per_kg_assayed_Fe0'],scope='Same-table arithmetic only. Heating, startup, auxiliaries and recovery excluded. No identified causal mechanism or transferable concentration threshold.')
(p/'impurity_check.json').write_text(json.dumps(y,indent=2)+'\n');print(json.dumps(y,indent=2))
