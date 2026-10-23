import csv,json,math
from pathlib import Path
P=Path(__file__).parent;root=P.parent
D=root/'nitrite_finishing/dataset'; R=root/'native_reconstruction'
rec=json.loads((R/'dataset_result.json').read_text());mat=json.loads((R/'material_bounds.json').read_text());prof=json.loads((R/'profile_result.json').read_text())
with (D/'Figure_4.csv').open() as f:
 rows=list(csv.reader(f)); header=rows.pop(0)
r=next(row for row in rows if float(row[0])==2700)
assert [float(r[i]) for i in [0,2,4]]==[2700]*3
vals=dict(zip(header[1::2],map(float,r[1::2])))
assert vals=={'air':795.605,'25mM KSCN_air':378.536,'N2':273.58}
a=vals['air']/1000
with (D/'Figure_3.csv').open() as f:
 reader=csv.reader(f); next(reader);cal=[list(map(float,x)) for x in reader]
assert cal==rec['calibration']['points']
m=rec['calibration']['ratio_vs_Ceff_slope']; b=rec['calibration']['intercept']
res=[ratio-(m*C+b) for C,ratio in cal]
assert all(abs(x-y)<1e-14 for x,y in zip(res,rec['calibration']['residuals']))
maxres=max(map(abs,res))/m
assert abs(maxres-prof['largest_calibration_fit_residual_equivalent_mM'])<1e-10
F=96485.33212;eps=8.8541878128e-12;r=5e-6;gamma=.072;C=1000
n0=C*4*math.pi*r**3/3;e=max(0,8*a-6);Q=F*n0*e;QR=8*math.pi*math.sqrt(eps*gamma*r**3)
result={'source_row_2700s':r if False else dict(time_s=2700,**vals),'air_over_N2':vals['air']/vals['N2'],'KSCN_over_air':vals['25mM KSCN_air']/vals['air'],'air_y':a,'min_e_per_initial_N':e,'overstatement_factor_boundary':a/.75,'overstatement_pct_boundary':100*(a/.75-1),'downward_correction_pct_of_apparent':100*(1-.75/a),'background_equivalent_mM_boundary':1000*(a-.75),'max_descriptive_calibration_residual_mM':maxres,'reference_n0_mol':n0,'Q_if_all_redox_charge_stored_C':Q,'Rayleigh_C':QR,'Q_over_QR':Q/QR,'gamma_required_N_m':gamma*(Q/QR)**2,'source_t0_air_mM':float(rows[0][1])}
for k,mk in [('Q_if_all_redox_charge_stored_C','hypothetical_charge_if_all_stored_C'),('Rayleigh_C','Rayleigh_limit_conducting_isolated_drop_C'),('Q_over_QR','ratio_Q_needed_over_Rayleigh')]:
 assert math.isclose(result[k],mat['charge_storage_reference'][mk],rel_tol=1e-9)
(P/'native_receipt_check.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
