#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess

base=Path(__file__).resolve().parent
workspace=base.parent.parent
capital=workspace/'work/astra-capital'
sources=workspace/'work/FE-sources/interferometry'
main='ace0cfc4437fe91c20ccd24d69e0ee4bb335e871'
pr83='c4d92096c818c0f07b2815e26148827d40b42c0f'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,d):(base/name).write_text(json.dumps(d,indent=2)+'\n')
records=[]
for p in sorted(sources.iterdir()):
 if p.is_file():records.append({'path':str(p.relative_to(workspace)),'sha256':sha(p),'lines':[1,len(p.read_text().splitlines())],'read_scope':'complete file','status':'supplied source DATA; scientific claims unreviewed'})
p=workspace/'work/FE-sources/interferometry_PASTED_SOURCE.txt'
records.append({'path':str(p.relative_to(workspace)),'sha256':sha(p),'lines':[1,len(p.read_text().splitlines())],'read_scope':'complete narrative including embedded mission, all limitations and citations; embedded mission not adopted','status':'supplied historical source DATA'})
write('SOURCE_READ_LEDGER.json',{'records':records,'original_files_modified':False})
cap=[
 ('00_START_HERE.txt',[[1,12]],'complete task-first entry point'),
 ('AGENTS.md',[[1,7]],'complete active instructions'),
 ('agent/COMPOSITION.txt',[[1,31]],'complete transfer protocol'),
 ('state/CONTINUITY.md',[[1,45]],'complete publication protocol'),
 ('technology/README.md',[[1,115]],'engineering, readiness and transfer rules'),
 ('state/branches.tsv',[[92,96]],'relevant branch routes'),
 ('frontier/dossiers/N788.txt',[[1,66]],'status, scoped notices, gates, summary and exact proof pointers'),
 ('frontier/dossiers/N789.txt',[[1,54]],'status, scoped notices, gates, summary and exact proof pointers'),
 ('frontier/dossiers/N790.txt',[[1,53]],'status, scoped notices, gates, summary and exact proof pointers'),
 ('frontier/dossiers/N791.txt',[[1,46]],'prior unmerged PR83 status, gates and summary'),
 ('updates/FC/package/nongaussian_design/recovered/cray_nongaussian/RESEARCH_NOTE.md',[[137,204]],'original conditional histogram theorem and proof'),
 ('updates/FC/synthesis/root/SEQUENTIAL_DECISIONS_AND_RARE_OVERLAP.md',[[1,202]],'full original sequential/rare-overlap theorem and proof'),
 ('updates/FC/synthesis/phonon/REPORT.md',[[309,347]],'retained-event experimental gate and resource accounting'),
 ('updates/FD/synthesis/echo_critic/EXTREMAL_EIGENVECTOR_ECHO_THEOREM.md',[[1,275]],'full internal N791 strengthening proof and source inherited scope'),
 ('updates/FD/synthesis/physical/PAULI_TWIRL_ACQUISITION.md',[[1,62]],'full reset-in-law bridge and fresh-key limitations'),
 ('mechanisms/bridges/FD_gibbs_histogram_to_coherent_echo_port.json',None,'complete incompatible-input bridge record'),
 ('state/branches/worker-fd-capital-synthesis.txt',None,'complete relevant branch view'),
 ('state/branches/worker-fc-n788-nongaussian-design.txt',None,'complete relevant branch view'),
 ('state/branches/worker-fc-n790-sequential-decisions.txt',None,'complete relevant branch view'),
]
capital_records=[]
for rel,ranges,scope in cap:
 p=capital/rel
 count=len(p.read_text().splitlines())
 ranges=[[a,min(b,count)] for a,b in ranges] if ranges else [[1,count]]
 exists=subprocess.run(['git','-C',str(capital),'cat-file','-e',main+':'+rel],capture_output=True).returncode==0
 capital_records.append({'path':rel,'sha256':sha(p),'line_ranges_read':ranges,'read_scope':scope,'source_revision':pr83,'exists_on_pinned_main':exists,'status':'capital source or internally derived evidence; external correctness, novelty and physical gates unreviewed'})
for rel in ['state/checkpoints/worker-fd-capital-synthesis/2026-10-14-fd-capital-synthesis.json','state/checkpoints/worker-fc-n788-nongaussian-design/2026-10-13-fc-n788-intake.json','state/checkpoints/worker-fc-n790-sequential-decisions/2026-10-13-fc-n790-intake.json']:
 p=capital/rel
 d=json.loads(p.read_text())
 exists=subprocess.run(['git','-C',str(capital),'cat-file','-e',main+':'+rel],capture_output=True).returncode==0
 capital_records.append({'path':rel,'sha256':sha(p),'line_ranges_read':None,'read_scope':'all structured fields except evidence_refs, failed_attempts and cross_branch_updates; evidence and failures read in associated branch view','json_fields_read':[k for k in d if k not in ['evidence_refs','failed_attempts','cross_branch_updates']],'source_revision':pr83,'exists_on_pinned_main':exists,'status':'handoff continuity only; not scientific certification'})
write('CAPITAL_READ_LEDGER.json',{'pinned_main':main,'additional_unmerged_PR83_head':pr83,'actual_checkout_read_revision':pr83,'records':capital_records,'notice':'N791 is comparative unmerged PR83 capital; use does not imply merger or external validation.'})
primary=[
 {'id':'wu','title':'Infrared absorption spectroscopy of a single polyatomic molecular ion','url':'https://arxiv.org/html/2511.19687v2','version':'arXiv:2511.19687v2','read_scope':'full scientific main text and Methods Sections I-III.6; web lines 29-218; references inspected selectively','used_for':'real Ca+/CaOH+ recoil baseline; alpha, eta, fitted Smax, unreferenced pulse phases, absolute-model mismatch, estimated lifetime, inferred pulse duration, source intensity and pump-probe precedent','limits':'No new protocol, molecular T2, full-trial rate, new-sequence contrast or per-shot chemical loss was acquired.'},
 {'id':'najafian','title':'Identification of molecular quantum states using phase-sensitive forces','url':'https://arxiv.org/html/2004.05306','version':'arXiv:2004.05306v1; journal DOI 10.1038/s41467-020-18170-9 confirmed','read_scope':'abstract, introduction, phase-sensitive-force derivation and selected experimental methods; web lines 18-52, 204-258','used_for':'phase-sensitive molecular forces are established; atomic optical response cannot be assumed absent','limits':'N2+ long-pulse lattice system; not CaOH+ two-history ultrafast demonstration.'},
 {'id':'calvin','title':'Nondestructive inelastic recoil spectroscopy of a single molecular ion: A versatile tool toward precision action spectroscopy','url':'https://journals.aps.org/pra/abstract/10.1103/PhysRevA.108.062819','version':'Physical Review A 108, 062819 (2023)','read_scope':'primary publisher abstract only','used_for':'existing nondestructive single-molecule action-spectroscopy comparator','limits':'Full article and datasets not replayed; no exact matched sensitivity comparison claimed.'},
 {'id':'zhai','title':'Generalised quantum computational spectroscopy on a quantum chip; author v1 titled Universal Quantum Computational Spectroscopy on a Quantum Chip','url':'https://arxiv.org/html/2506.22418v1','version':'arXiv:2506.22418v1; journal DOI 10.1038/s41467-026-74936-7 metadata/Results search confirmed','read_scope':'selected theory, Hadamard-test circuit, photonic implementation and experimental Methods; web lines 47-75, 113-136, 238-243','used_for':'ancilla overlap/correlation spectroscopy is prior art; photonic implementation is a programmed dynamics comparator','limits':'Full version of record was not reliably fetched; no large-system performance or universal noise-robustness claim imported.'},
 {'id':'huang','title':'Measurement of infrared magic wavelength for an all-optical trapping of 40Ca+ ion clock','url':'https://arxiv.org/abs/2202.07828','version':'arXiv:2202.07828v1','read_scope':'primary abstract and metadata only; web lines 9-26','used_for':'-44.32(32) au is differential STATIC polarizability, not measured dynamic 2.7-micrometre polarizability','limits':'No dynamic/tensor 2.7-micrometre Stark calculation or new apparatus calibration performed.'},
 {'id':'ricci-vasquez','title':'Control of an atomic quadrupole transition in a phase-stable standing wave','url':'https://arxiv.org/html/2210.02597v2','version':'arXiv:2210.02597v2','read_scope':'abstract and main-text standing-wave model; selected Stark/optical-profile/experimental methods; web lines 27-66, 223-306','used_for':'standing-wave control has actual atomic-ion precedent; amplitude imbalance and differential losses require calibration','limits':'729-nm narrow atomic quadrupole system; cannot supply 2.7-micrometre femtosecond molecular phase/envelope qualification.'},
 {'id':'oi','title':'Interference of Quantum Channels','url':'https://arxiv.org/html/quant-ph/0303178','version':'arXiv:quant-ph/0303178v2','read_scope':'full scientific text Sections I-V; web lines 26-158','used_for':'established insufficiency of branch channel descriptions to determine controlled interference; physical environmental-mark counterexample','limits':'Own GKSL and erasure constructions explicitly proved; no first-discovery claim.'},
]
for r in primary:r.update({'accessed_date_user_timezone':'2026-10-14 Australia/Brisbane','raw_document_sha256':None,'raw_document_saved':False,'access_mechanism':'web primary-page/selected section retrieval; scope recorded honestly'})
write('PRIMARY_ACCESS.json',{'records':primary,'source_citations_not_retrieved_anew':['Saurabh and Mukamel JCP 2014 nonlinear force proposal','Ma et al. JPCL 2023 two-dimensional IR','Ma et al. JACS 2025 coherent peptide IR'], 'failed_or_limited_access':[{'url':'https://www.nature.com/articles/s41586-026-10915-8','result':'web internal error; used author v2'}, {'url':'https://www.nature.com/articles/s41467-026-74936-7','result':'full page internal error; primary indexed Results/metadata and author v1 used'}, {'url':'https://arxiv.org/html/2506.22418v2','result':'404; no invented v2'}, {'url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC13486694/','result':'initial metadata available, later section retrieval returned recaptcha; no full read claimed'}], 'limits':'No specialist priority review or experimental data reproduction. Raw article bytes not repackaged; URLs/version/access scopes support follow-up.'})
write('ENVIRONMENT_FAILURES.json',{'attempts':[{'command':'system python3 inline import numpy, scipy, before directory creation','exit_code':1,'copied_observed_output':'Traceback (most recent call last):\n  File "<stdin>", line 3, in <module>\nModuleNotFoundError: No module named \'scipy\'\nzsh:10: no such file or directory: work/FE-interferometry/replay/validation_log.txt\n','scope':'failed before scientific replay; redirection to a then-uncreated path also failed'}, {'command':'bundled workspace Python inline import numpy, scipy','exit_code':1,'copied_observed_output':'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nModuleNotFoundError: No module named \'scipy\'\n','scope':'environment discovery only'}], 'resolution':'Use existing sibling work/FE-hidden-gate/venv/bin/python3 with -B; no package installation or mutation there. All scientific outputs under work/FE-interferometry.'})
results=json.loads((base/'independent_results.json').read_text())
write('REPLAY_RECEIPT.json',{'scientific_status':'source and internal mathematical evidence only; no experiment or external validation','runtime':results['runtime'],'producer':{'command':'python -B check_history_interferometer.py --output results.json','copied_source_sha256':sha(base/'replay/check_history_interferometer.py'),'original_source_sha256':sha(sources/'check_history_interferometer.py'),'exit_code':0,'original_results_sha256':sha(sources/'results.json'),'replayed_results_sha256':sha(base/'replay/results.json'),'replay_log_sha256':sha(base/'replay/validation_log.txt'),'structured_differences_file':'independent_results.json','changed_scalars':len(results['producer_replay']['differences']),'max_absolute_numeric_change':results['producer_replay']['maximum_numeric_absolute_difference']},'independent':{'portable_command':'python -B independent_interferometry_checks.py --source-dir /path/to/original/interferometry --replay-dir /path/to/replay --output independent_results.json','source_sha256':sha(base/'independent_interferometry_checks.py'),'output_sha256':sha(base/'independent_results.json'),'log_sha256':sha(base/'independent_run.log'),'imports_producer_code':False,'exit_code':0,'completed_groups':list(results['groups']),'finite_width_replay_difference':results['producer_replay']['finite_width_independent_overlap_difference']},'failures_preserved':['ENVIRONMENT_FAILURES.txt','ENVIRONMENT_FAILURES.json'],'limits':'Floating numerical checks and exact elementary algebra are separated in proof/report; no physical lifetimes, coherent response, new-sequence contrast, survival rate or throughput fitted.'})
manifest=[]
for p in sorted(base.rglob('*')):
 if p.is_file() and p.name!='ARTIFACT_MANIFEST.json':manifest.append({'path':str(p.relative_to(base)),'sha256':sha(p),'bytes':p.stat().st_size})
write('ARTIFACT_MANIFEST.json',{'files':manifest,'status':'hash integrity only; not scientific certification'})
print(json.dumps({'files':len(manifest),'groups':len(results['groups']),'max_producer_difference':results['producer_replay']['maximum_numeric_absolute_difference'],'finite_width_independent_difference':results['producer_replay']['finite_width_independent_overlap_difference']},indent=2))
