"""Finalize the calibration continuation without changing frozen parent files."""
from pathlib import Path
import json,hashlib,os,ast,math
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT.parent
os.environ.setdefault('MPLBACKEND','Agg');os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'cache/mpl'))
import numpy as np
import matplotlib.pyplot as plt

def read(name):return json.loads((ROOT/'outputs'/name).read_text())
def main():
    final=read('differential_final32.json');metadata=[json.loads(f.read_text()) for f in (ROOT/'outputs').glob('*_metadata.json')]
    frozen=json.loads((BASE/'outputs/MANIFEST.json').read_text());bad=[]
    for row in frozen:
        if hashlib.sha256((BASE/row['path']).read_bytes()).hexdigest()!=row['sha256']:bad.append(row['path'])
    assert not bad
    code_checks=[]
    for f in (ROOT/'analysis').glob('*.py'):ast.parse(f.read_text());code_checks.append(f.name)
    template_checks=[]
    for f in (ROOT/'outputs').glob('*_state*.npz'):
        p=np.load(f)['p'];assert np.isfinite(p).all() and (p>=0).all() and (p.sum(1)<=1.00001).all()
        template_checks.append({'file':f.name,'shape':list(p.shape)})
    verification={'frozen_parent_files_checked':len(frozen),'frozen_parent_hash_mismatches':bad,
        'parent_manifest_sha256':hashlib.sha256((BASE/'outputs/MANIFEST.json').read_bytes()).hexdigest(),
        'analysis_scripts_parse':code_checks,'valid_new_probability_templates':template_checks,
        'profile_verification':read('profile_verification.json'),
        'interval_certificate':False,'numerical_coverage_conditional_on_conservative_profile_bounds':True}
    (ROOT/'outputs/VERIFICATION.json').write_text(json.dumps(verification,indent=2))
    durations=sum(m['elapsed_seconds'] for m in metadata)
    configs=sum(len(m['states'])*m['thermal_model']['num_snapshots'] for m in metadata)
    e=1.602176634e-19
    costs={'new_multislice_configurations':configs,'new_multislice_recorded_wall_seconds':durations,
           'reference_and_read_patterns':90,'nominal_union_scan_footprint_angstrom2':7.875,
           'dose_1000000_pair':{'before_dose_e_per_angstrom2':500000,'after_dose_e_per_angstrom2':500000,
             'incident_electrons':7875000,'beam_on_seconds_at20pA':7875000*e/20e-12,
             'aggregate_sigma_eff_ceiling_barn_if_static_pair_survival_0_995_is_required':-math.log(.995)/(1e6*1e-8)},
           'reused_frozen_library_cost_reference':str(BASE/'outputs/RESULTS.json'),
           'unknown':['Native-state preparation and independent verification','Incident-dose/detector calibration','Focus and registration exposure','Changed-state contrast-family acquisition','Changes during native/read acquisition','All-species/multi-defect coverage','Retention or transition kernel','Recovery/replacement','Full instrument and specimen setup'],
           'physical_acquisitions':0,'paid_services':0,'public_writes':0,'new_packages_installed':0,
           'threads_cap':2,'source_acquisition':json.loads((ROOT/'sources/acquisition.json').read_text())}
    result={'status':'PHYSICAL_OPERATION_NOT_ACHIEVED','inference_operation':'Constructed and executed conditional paired differential calibration with latent contrast parameter and arbitrary shared native means.',
       'physical_depth_accuracy':'UNKNOWN','physical_damage_or_retention':'UNKNOWN','physical_model_coverage':'NOT_ACQUIRED',
       'novelty':'NOT_ESTABLISHED','matched_ordinary_advantage':'NOT_ESTABLISHED',
       'scope':'Native/15/16 power checks within five candidate classes; static, registered before/after Poisson records. Not the full17-state operation.',
       'theory_and_numeric_qualification':str(ROOT/'INFERENCE_CONTRACT.md'),
       'final_fresh_seed_tests':final,'paired_ratio_failure':read('paired_screen.json'),
       'ordinary_joint_nuisance_screen':read('joint_screen.json'),'additive_contrast_expected_KL':read('additive_expected_KL.json'),
       'training_only_compression':read('compression.json'),'history_boundary':read('history_boundary.json'),
       'costs':costs,'verification':verification,
       'core_limits':['Native means do not identify the changed-state response family.','A native before-state is a preparation assumption; arbitrary background estimation does not prove purity.','Rejected drift/two-Cr controls do not establish rejection of every multiple-defect or species-loss state.','A static no-change envelope is a contract of this operation, not a universal necessity for time-resolved tracking.','Repeated reference reuse and optional stopping need their own dependence-aware construction.']}
    (ROOT/'outputs/RESULTS.json').write_text(json.dumps(result,indent=2))
    fig,axes=plt.subplots(1,2,figsize=(11.8,4.7),gridspec_kw={'width_ratios':[1.5,1]})
    for h,color in [(15,'#315f8c'),(16,'#ba672f')]:
        for truth,style in [('covered_mix_w05','--'),('heldout_sigma0065_seed8021','-')]:
            rr=sorted([r for r in final['rows'] if r['true_label']==h and r['truth']==truth],key=lambda x:x['total_nominal_dose_e_per_angstrom2'])
            x=[r['total_nominal_dose_e_per_angstrom2'] for r in rr];y=np.array([r['frequencies']['correct_singleton'] for r in rr])*100
            ci=np.array([r['correct_singleton_clopper_pearson_95'] for r in rr])*100
            axes[0].errorbar(x,y,yerr=np.maximum(np.vstack([y-ci[:,0],ci[:,1]-y]),0),fmt='o'+style,color=color,capsize=3,
                label=f'Layer {h}, '+('covered mixture' if truth=='covered_mix_w05' else 'held-out nuisance'))
    axes[0].set_xscale('log');axes[0].set_ylim(40,102);axes[0].set_xlabel('Total before + after dose (electrons/Å²)');axes[0].set_ylabel('Correct unique reports (%)');axes[0].grid(alpha=.2);axes[0].legend(fontsize=8)
    axes[0].set_title('Paired calibration with latent nuisance\nFresh Poisson trials; 2,000 per point',fontsize=10)
    labels=['Native pattern drift','Two Cr at layers 15 + 16'];fr=[]
    for truth in ['post_calibration_nuisance_drift_native','unmodeled_two_cr15_16_sigma0065']:
        rr=next(r for r in final['rows'] if r['truth']==truth and r['total_nominal_dose_e_per_angstrom2']==1e6);fr.append(rr['frequencies']['empty_rejection']*100)
    axes[1].barh(np.arange(2),fr,color=['#7b7774','#8b594b']);axes[1].set_yticks(np.arange(2),labels,fontsize=8);axes[1].set_xlim(0,105);axes[1].set_xlabel('Model rejections (%)');axes[1].grid(axis='x',alpha=.2)
    axes[1].set_title('Two deliberate failures at total dose 10⁶\nOne control each; no general coverage claim',fontsize=10)
    fig.suptitle('CrSBr calibration inference in simulation — physical contrast and damage calibration remain unacquired',fontsize=11)
    fig.tight_layout();fig.savefig(ROOT/'outputs/calibration_operation.png',dpi=180);plt.close(fig)
    manifest=[]
    for f in sorted(ROOT.rglob('*')):
        if f.is_file() and 'cache' not in f.parts and f.name!='MANIFEST.json':manifest.append({'path':str(f.relative_to(ROOT)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
    (ROOT/'outputs/MANIFEST.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps({'status':result['status'],'costs':costs,'frozen_parent_files_unchanged':len(frozen),'new_templates':len(template_checks)},indent=2))
if __name__=='__main__':main()
