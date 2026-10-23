"""Independent algebra check of reported 80/20 effusion-nozzle comparator.

Exact decimal data transcription from SI Tables S2/S4, no flow/kinetic replay.
Conditional ballast result is not a measured wall-plug result.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json

D=Path(__file__).resolve().parent
ROOT=D.parents[1]
source=ROOT/'nitrogen_cycle5_20261022/expansion_evidence/2022_effusion_si.txt'
data={
    'with_nozzle': [('155.85','2.25','1.64'),('158.41','2.26','1.64'),('162.48','2.27','1.60')],
    'without_nozzle':[('193.43','2.28','1.46'),('205.59','2.29','1.49'),('196.73','2.28','1.48')]
}
Imean,R=F('0.135'),F(25000)
B=R*Imean**2
assert B==F('455.625')
Fin=F(2)/(F(24)*60)  # mol/s, retaining the paper's 24 L/mol convention.
out={}
for label, raw in data.items():
    p,no_pct,no2_pct=[sum(F(row[k]) for row in raw)/3 for k in range(3)]
    xno,xno2=no_pct/100,no2_pct/100
    contraction=1+xno2/2
    Fout=Fin/contraction
    NO,NO2=Fout*xno,Fout*xno2
    N2=(2*F('0.8')*Fin-NO-NO2)/2
    O2=(2*F('0.2')*Fin-NO-2*NO2)/2
    assert min(N2,O2,NO,NO2)>0
    assert N2+O2+NO+NO2==Fout
    assert 2*N2+NO+NO2==2*F('0.8')*Fin
    assert 2*O2+NO+2*NO2==2*F('0.2')*Fin
    nprod=NO+NO2
    nprod_replicates=sum(Fin*((F(row[1])+F(row[2]))/100)/(1+F(row[2])/200) for row in raw)/3
    values={
        'mean_discharge_W':p,'mean_NO_percent':no_pct,'mean_NO2_percent':no2_pct,
        'Fout_over_Fin':1/contraction,'NOx_mol_s':nprod,
        'published_convention_SEC_from_means_MJ_mol':p/(Fin*(xno+xno2))/10**6,
        'flow_corrected_discharge_SEC_MJ_mol':p/nprod/10**6,
        'conditional_arc_plus_ballast_power_lower_bound_W':p+B,
        'conditional_arc_plus_ballast_SEC_lower_bound_MJ_mol':(p+B)/nprod/10**6,
        'NOx_mol_s_mean_corrected_replicates':nprod_replicates,
        'flow_corrected_discharge_SEC_mean_power_over_mean_corrected_rate_MJ_mol':p/nprod_replicates/10**6,
        'conditional_arc_plus_ballast_SEC_mean_power_over_mean_corrected_rate_MJ_mol':(p+B)/nprod_replicates/10**6,
    }
    out[label]={k:float(v) for k,v in values.items()}
    out[label]['exact_values']={k:str(v) for k,v in values.items()}

def rate(key):
    return F(out[key]['exact_values']['NOx_mol_s_mean_corrected_replicates'])

def value(key,col):
    return F(out[key]['exact_values'][col])

reduction_paper=1-value('with_nozzle','published_convention_SEC_from_means_MJ_mol')/value('without_nozzle','published_convention_SEC_from_means_MJ_mol')
reduction_corrected=1-value('with_nozzle','flow_corrected_discharge_SEC_MJ_mol')/value('without_nozzle','flow_corrected_discharge_SEC_MJ_mol')
reduction_constant=1-value('with_nozzle','conditional_arc_plus_ballast_SEC_lower_bound_MJ_mol')/value('without_nozzle','conditional_arc_plus_ballast_SEC_lower_bound_MJ_mol')
reduction_rep_corrected=1-value('with_nozzle','flow_corrected_discharge_SEC_mean_power_over_mean_corrected_rate_MJ_mol')/value('without_nozzle','flow_corrected_discharge_SEC_mean_power_over_mean_corrected_rate_MJ_mol')
reduction_rep_constant=1-value('with_nozzle','conditional_arc_plus_ballast_SEC_mean_power_over_mean_corrected_rate_MJ_mol')/value('without_nozzle','conditional_arc_plus_ballast_SEC_mean_power_over_mean_corrected_rate_MJ_mol')
# Counterexample preserving each 135 mA time mean and the 280 mA peak envelope:
# with-nozzle current alternates 35/235 mA equally, without is constant 135 mA.
# It is a mathematical counterexample, not an assertion about the experiment.
low,high=F('.035'),F('.235')
assert (low+high)/2==Imean and high<F('.280')
Bwith=R*(low*low+high*high)/2
Bwithout=B
secwith=(value('with_nozzle','mean_discharge_W')+Bwith)/rate('with_nozzle')/10**6
secwithout=(value('without_nozzle','mean_discharge_W')+Bwithout)/rate('without_nozzle')/10**6
assert secwith>secwithout

result={
    'source_si_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'data_order':['discharge_power_W','NO_percent','NO2_percent'],
    'raw_80_20_triplicates':data,
    'ballast_inference':{
        'conditional_bound_W':float(B),
        'identity':'P_ballast = R * mean(i(t)^2) = R * mean(i(t))^2 + R * Var(i(t)).',
        'required_condition':'135 mA must mean the time mean (or mean magnitude) of the same ballast current over the matching averaging interval. Constant-current equality gives 455.625 W; 135 mA RMS also gives equality. A setpoint, peak, or on-state mean alone does not establish this bound.',
        'scope':'Arc plus ballast, not measured wall-plug or complete plant power. Series circuit/current identity, resistance and negligible average stored-energy change must apply.'},
    'flow_contraction':{
        'identity':'2 Fin = 2 Fout + Fout*xNO2, hence Fout=Fin/(1+xNO2/2).',
        'conditions':'Steady complete gas balance with N2/O2 inlet and only N2/O2/NO/NO2 products; outlet mole fractions; no leaks, extra carriers, condensation or inventory accumulation.',
        'SEC_multiplier':'Multiply the inlet-flow-based SEC by 1+xNO2/2.',
        'exact_atom_balance_verified':True},
    'groups':out,
    'comparisons':{
        'aggregation_note':'The first corrected figures apply contraction to mean percentages. Alternate figures average each replicate corrected production rate, then divide mean power by that mean rate. These are distinct legitimate summaries, not arithmetic mismatches.',
        'published_convention_discharge_SEC_reduction_percent':float(reduction_paper*100),
        'flow_corrected_discharge_SEC_reduction_percent':float(reduction_corrected*100),
        'constant_current_illustrative_arc_plus_ballast_SEC_reduction_percent':float(reduction_constant*100),
        'mean_power_over_mean_corrected_rate_discharge_SEC_reduction_percent':float(reduction_rep_corrected*100),
        'mean_power_over_mean_corrected_rate_constant_current_illustrative_reduction_percent':float(reduction_rep_constant*100),
        'warning':'The last comparison is the ratio of reconstructed values under equality/constant-current assumptions. Ratios of independent lower bounds are not bounds on actual relative savings.'},
    'counterexample_to_savings_bound':{
        'scope':'Mathematical counterexample only; not measured waveform.',
        'rate_aggregation':'Arithmetic mean of separately flow-corrected replicate production rates.',
        'with_nozzle_equal_time_current_levels_A':[float(low),float(high)],
        'without_nozzle_constant_current_A':float(Imean),
        'same_mean_current_A':float(Imean),
        'with_nozzle_ballast_power_W':float(Bwith),
        'without_nozzle_ballast_power_W':float(Bwithout),
        'with_nozzle_SEC_MJ_mol':float(secwith),
        'without_nozzle_SEC_MJ_mol':float(secwithout),
        'actual_order_reverses_despite_lower_bound_order':True},
    'status':'PASS: conditional Jensen and exact four-species contraction identities; comparative SEC cannot be certified from unpaired lower bounds.'}
(D/'comparator_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'comparisons':result['comparisons'],
                  'counterexample_to_savings_bound':result['counterexample_to_savings_bound']},indent=2))
