"""Independent workbook-only Decimal endpoint calculation; does not import candidate ledger."""
from decimal import Decimal, getcontext
import json, hashlib
from pathlib import Path
import openpyxl
getcontext().prec=40
root=Path(__file__).resolve().parents[1]
p=root/'peroxide_evidence/source_data.xlsx'
w=openpyxl.load_workbook(p,data_only=True)
raw=list(w['Supplementary Fig. 1a'].values)
r=[[Decimal(str(x)) for x in row] for row in raw[3:8]]
V=Decimal(100); a=[x[2] for x in r]; n=[x[1] for x in r]; sd=[x[5] for x in r]
D=V*Decimal(1)
def calc(indices,v=Decimal(1)):
 vf=V-v*len(indices)
 gross=vf*a[-1]+v*sum((a[i] for i in indices),Decimal(0))
 net=gross-V*a[0]
 left=vf*n[-1]+v*sum((n[i] for i in indices),Decimal(0))
 return dict(final_volume_mL=vf,gross_nitrate_umol=gross,initial_nitrate_umol=V*a[0],net_nitrate_umol=net,net_per_nominal_dose=net/D,net_per_initial_nitrite=net/(V*n[0]),net_per_nitrite_lost=net/(V*n[0]-left))
z=calc(range(4)); coeff=[Decimal(-99),Decimal(1),Decimal(1),Decimal(1),Decimal(96)]
center=sum(c*x for c,x in zip(coeff,a));rad=sum(abs(c)*s for c,s in zip(coeff,sd))
assert center==z['net_nitrate_umol']
# Endpoint withdrawal partition invariant: count endpoint sample once plus correspondingly smaller retained volume.
assert 95*a[-1]+sum(a)==96*a[-1]+sum(a[:-1])
assert sum(coeff)==0  # Constant initial nitrate concentration cancels throughout complete material boundary.
# Time-local nitrite/nitrate covariance inferred only if inorganic-N SD really is SD of their sum.
rhos=[]
for row in r:
 sN,sA,sT=row[4:7]
 rho=(sT*sT-sN*sN-sA*sA)/(2*sN*sA)
 rhos.append(rho)
wrong_fullV_plus_samples=V*a[-1]+sum(a[:-1])-V*a[0]
wrong_double_samples=96*a[-1]+2*sum(a[:-1])-V*a[0]
out={'source_workbook_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'raw_headers_preserved':raw[2], 'rows_preserved':raw[3:8], 'adopted_concentration_units':'mM, based on SI figure and main text; workbook incorrectly labels microM','sequential_four_1mL':z,'no_sampling_counterfactual':calc([]),'only_three_intermediate_withdrawals':calc([1,2,3]),'two_mL_sensitivity_not_measured_bounds':calc(range(4),Decimal(2)), 'adversarial':{'wrong_98_3pct_times_initial_feed_umol':Decimal('.983')*V*n[0], 'wrong_98_3pct_times_dose_umol':Decimal('.983')*D,'wrong_final_full_100mL_plus_samples_umol':wrong_fullV_plus_samples,'wrong_full_volume_plus_samples_overcount_umol':wrong_fullV_plus_samples-center,'wrong_sampled_nitrate_counted_twice_umol':wrong_double_samples,'wrong_no_initial_nitrate_subtraction_umol':z['gross_nitrate_umol'],'wrong_literal_microM_nitrate_per_mM_dose':center/D/1000},'uncertainty':{'one_SD_coordinate_box_radius_umol':rad,'coordinate_box_lower_umol':center-rad,'coordinate_box_upper_umol':center+rad,'coordinate_box_per_dose_lower':(center-rad)/D,'coordinate_box_per_dose_upper':(center+rad)/D,'independent_time_SD_quadrature_umol':sum((c*s)**2 for c,s in zip(coeff,sd)).sqrt(),'inferred_same_time_nitrite_nitrate_rho_if_total_SD_is_sum_SD':rhos,'not_a_CI':True}}
(root/'independent_endpoint/results.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps(out,indent=2,default=str))
