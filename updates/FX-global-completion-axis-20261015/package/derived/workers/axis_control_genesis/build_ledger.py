#!/usr/bin/env python3
"""Construct an explicit access/provenance ledger; HTTP 200 is not article access."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FROZEN=ROOT.parents[1]/'sources'/'axis_writing'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(sid,title,url,doi=None,access=None,local=None,locator=None,scope=None):
    d=dict(id=sid,title=title,url=url,doi=doi,access=access,local_file=local,
           locator=locator,scope=scope)
    if local and (ROOT/local).exists():
        d['sha256']=digest(ROOT/local)
    return d


sources=[
 source('G17','Synthesis of single-phase L10-FeNi magnet powder by nitrogen insertion and topotactic extraction',
        'https://www.nature.com/articles/s41598-017-13562-2','10.1038/s41598-017-13562-2',
        'FULL_PRIMARY_ARTICLE_HTML','sources/G17.html','Methods; structure/denitriding discussion',
        'NITE chemistry and retention established; no stress-selectable axis response or repeated rewrite reported.'),
 source('W22','Massive transformation in FeNi nanopowders with nanotwin-assisted nitridation',
        'https://www.nature.com/articles/s41598-022-07479-8','10.1038/s41598-022-07479-8',
        'FULL_PRIMARY_ARTICLE_HTML','sources/W22.html','Results: Nucleation; Growth; Fig.5',
        'Local microscopy evidence of interface-mediated transformation and irregular orientation relationships; no measured externally controlled switching law.'),
 source('A21','Fabrication of L10-FeNi films with island structures by nitrogen insertion and topotactic extraction for improved coercivity',
        'https://pubs.aip.org/aip/apm/article/9/9/091108/122923/Fabrication-of-L1-FeNi-films-with-island','10.1063/5.0062692',
        'FULL_PRIMARY_ARTICLE_HTML_VIA_PUBLISHER_CDN','sources/A21cdn.html','Results, Fig.2-5; TableI',
        'Random c axes, fragmentation and different-location destructive TEM; fixed film is a platform, not measured same-island transfer.'),
 source('I20','Epitaxial L10-FeNi films with high degree of order and large uniaxial magnetic anisotropy fabricated by denitriding FeNiN films',
        'https://tsukuba.repo.nii.ac.jp/record/2002585/files/APL_116-24-242404.pdf','10.1063/5.0011875',
        'FULL_PRIMARY_PAPER_IN_AUTHOR_INSTITUTIONAL_REPOSITORY','sources/I20repo.pdf','Published APL116,242404; 6PDFpages',
        'Epitaxial registration and two orthogonal small variants; no rewrite.'),
 source('AFM19','Positive Weiss Temperature in Layered Antiferromagnetic FeNiN for High-Performance Permanent Magnets',
        'https://pubs.acs.org/doi/abs/10.1021/acsanm.9b01405','10.1021/acsanm.9b01405',
        'PRIMARY_PUBLISHER_INDEXED_ABSTRACT_READ_VIA_WEB_SEARCH_NO_FULL_PAPER',None,'Abstract',
        'Reported TN178K compared to reported formation573K; no process-temperature susceptibility anisotropy acquired.'),
 source('J23','Fabrication of L10-ordered FeNi films by denitriding FeNiN(001) and FeNiN(110) films',
        'https://www.sciencedirect.com/science/article/abs/pii/S0925838823007533','10.1016/j.jallcom.2023.169450',
        'PRIMARY_PUBLISHER_INDEXED_TEXT_AND_AUTHOR_INSTITUTIONAL_ABSTRACT',None,'Abstract and indexed introduction; institutional mirror https://kyushu-u.elsevierpure.com/en/publications/fabrication-of-l1sub0sub-ordered-feni-films-by-denitriding-fenin0/',
        'Orientation-dependent retention and distinct preparation pathways; no high-S orientation combined across unlike specimens.'),
 source('LAO24','Uniaxial magnetic anisotropy of L10-FeNi films with island structures on LaAlO3(110) substrates by nitrogen insertion and topotactic extraction',
        'https://www.sciencedirect.com/science/article/abs/pii/S0925838823042950','10.1016/j.jallcom.2023.172992',
        'PRIMARY_PUBLISHER_INDEXED_ABSTRACT_NO_FULL_PAPER',None,'Abstract',
        'Closest peer-reviewed one-shot immobilized oriented NITE comparator; no same-specimen rewrite recipe acquired.'),
 source('H24','Enhancement of hard magnetism and chemical order of synthetic L10-FeNi',
        'https://www.osti.gov/servlets/purl/2283203','10.1016/j.jallcom.2024.173619',
        'FULL_PRIMARY_ACCEPTED_MANUSCRIPT_PDF_16PAGES','sources/H24.pdf','Sections2.2,2.3,3.2,3.3; PDFpp4,8-11',
        'Pressure-assisted retention, powder alignment/compaction and theoretical-density normalization. Full manuscript retrieval improves frozen access boundary; no current-record certification.'),
 source('L24','Accelerating Nature: Induced Atomic Order in Equiatomic FeNi',
        'https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/advs.202302696','10.1002/advs.202302696',
        'PRIMARY_FULL_TEXT_READ_IN_WEB_TOOL_LOCAL_DOWNLOAD403',None,'Results3.1; Abstract; Background2.2',
        'Stress/field ordering prior art; no measurable in-plane anisotropy above ~1kJ/m3 threshold in reported samples.'),
 source('ACS23','Formation of L10 Ordering in FeNi by Mechanical Alloying and Field-Assisted Heat Treatment: Synchrotron XRD Studies',
        'https://pubs.acs.org/doi/10.1021/acsomega.2c07869','10.1021/acsomega.2c07869',
        'PRIMARY_PUBLISHER_INDEXED_ABSTRACT_CONCLUSIONS_READ_VIA_WEB_NO_VALID_LOCAL_FULL_PAPER',None,'Abstract; Conclusions',
        'More chemical order and ordered fraction under field; phase/order gain is not measured chemical-axis rewriting.'),
 source('FPd08','Effect of Magnetic Field on Microstructure Evolution during Disorder-Order Transformation in an Fe-Pd Alloy',
        'https://www.jstage.jst.go.jp/article/matertrans/49/9/49_MAW200810/_article/-char/en','10.2320/matertrans.MAW200810',
        'FULL_PRIMARY_PAPER_PDF_5PAGES','sources/FPd08.pdf','ExperimentalProcedure; Fig.4-9',
        'Field-selected chemical variant inferred from orthogonal magnetization curves in a fixed single crystal. Material differs; no transfer of magnetic/elastic constants.'),
 source('F78','Stress assisted nucleation of alpha-double-prime precipitates in Fe-N single crystals',
        'https://www.sciencedirect.com/science/article/pii/0001616078901050','10.1016/0001-6160(78)90105-0',
        'PRIMARY_PUBLISHER_ABSTRACT_READ_VIA_WEB',None,'Abstract',
        'Stress-biased nitrogen-precipitate nucleation precedent; no Fe/Ni atomic-order rewrite.'),
 source('F85','Stress orientation of nitrogen during the quench-aging of nitrogen ferrite',
        'https://www.tandfonline.com/doi/abs/10.1080/01418618508237643','10.1080/01418618508237643',
        'PRIMARY_PUBLISHER_ABSTRACT_READ_VIA_WEB',None,'Abstract',
        'Stress-oriented N-cluster precursors yield retained precipitate orientation after unloading; no nitrogen-extracted FeNi endpoint.'),
 source('P24','Magnetic body, magnet, and method for manufacturing magnetic body',
        'https://patents.google.com/patent/WO2024219436A1/en',None,
        'FULL_PRIMARY_PATENT_TEXT_MACHINE_TRANSLATION_WITH_ORIGINAL_JAPANESE','sources/P24.html','Published2024-10-24; priority2023-04-21; examples and Fig.22-34 descriptions',
        'Applicant-reported FeNiN mechanical texture retained after N removal. Not independent replication or legal/FTO analysis.'),
 source('P26US','Magnetic body, magnet, and method for manufacturing magnetic body',
        'https://patents.google.com/patent/US20260004959A1/en',None,
        'FULL_PRIMARY_ENGLISH_PATENT_TEXT','sources/P26US.html','Published2026-01-01; same family asP24; paragraphs0107-0118; definition of individual particles',
        'English detailed retained-orientation disclosure and processing-order controls; unsupported particles, not registered fixed material.'),
 source('P26','Magnetic body and magnet',
        'https://patents.google.com/patent/WO2026088551A1/en',None,
        'FULL_PRIMARY_PATENT_TEXT_MACHINE_TRANSLATION_WITH_ORIGINAL_JAPANESE','sources/P26.html','Published2026-04-30; priority2024-10-21; Example3 and ComparativeExample2',
        'Later closely related coating disclosure; applicant S and Hc claims are not used as independently demonstrated current records.'),
 source('P62','Une nouvelle transition ordre-desordre dans Fe-Ni (50-50)',
        'https://doi.org/10.1051/jphysrad:019620023010084100','10.1051/jphysrad:019620023010084100',
        'ORIGINAL_PRIMARY_FULL_TEXT_NOT_ACQUIRED',None,'Bibliography only; later primary H24 discusses route',
        'No independently checked irradiation dose or repeated-axis rewrite protocol.'),
 source('N64','Magnetic Properties of an Iron-Nickel Single Crystal Ordered by Neutron Bombardment',
        'https://doi.org/10.1063/1.1713516','10.1063/1.1713516',
        'ORIGINAL_PRIMARY_FULL_TEXT_NOT_ACQUIRED',None,'Bibliography only; later primary H24 describes295C and field',
        'No original fluence, damage/activation budget or repeat-cycle evidence acquired.'),
]

receipts=[]
for name in ['source_receipts.json','additional_source_receipts.json','patent_source_receipts.json','earlier_patent_receipts.json']:
    p=ROOT/name
    if p.exists():
        receipts.extend(json.loads(p.read_text()))
for r in receipts:
    sid=r['id']
    if sid=='P62hal': r['content_validation']='ANTIBOT_HTML_NOT_PAPER'
    elif sid=='ACS23repo': r['content_validation']='SHORT_HTML_NOT_PAPER'
    elif r.get('status')=='ACCESS_FAILED': r['content_validation']='DOWNLOAD_FAILED'
    else: r['content_validation']='PRIMARY_CONTENT_CHECKED'

frozen_inputs=[]
for name in ['README.md','analyse.py','provenance.json']:
    p=FROZEN/name
    frozen_inputs.append({'path':str(p),'sha256':digest(p)})

out={
 'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'worker':'axis_control_genesis',
 'endpoint':'Permanent x-to-y Fe/Ni chemical-axis rewrite in the same immobilized material after unloading and N removal.',
 'status':'NOT_ACQUIRED',
 'physical_experiment_performed':False,
 'raw_instrument_data_acquired':False,
 'literature_retrieval_is_not_physical_response_acquisition':True,
 'generic_impossibility_proved':False,
 'conditional_mathematics':'PROOFS.md and axis_limits.py',
 'scope':'No W, frozen-source or GitHub edits. No external communication or experiments.',
 'frozen_inputs':frozen_inputs,
 'worktree_reference_supplied_by_parent':{'path':'/Users/harjas/Documents/ChatGPT/ultra/work/astra-global-completion-axis-20261015','commit':'ab5118e70a7e6a0dd39e75dd563d3a3f50b06b25','independently_read_or_changed':False},
 'sources':sources,
 'receipts':receipts,
 'known_missing':[
   'Controlled stress or field to chemical-axis response of fixed FeNiN at actual reaction temperature.',
   'Actual transform correspondence, activation-volume tensor, nucleation prefactors, growth selection and stress transfer.',
   'Registered same-particle/grain before/after N-removal retention under directional intervention.',
   'Repeated orthogonal rewrite, erasure, yield and damage budgets.',
   'End-to-end energy, net reagent use/recycling, volume density, throughput and matched performance.'
 ],
}
(ROOT/'source_ledger.json').write_text(json.dumps(out,indent=2)+'\n')
manifest=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts:
        manifest.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':digest(p)})
(ROOT/'manifest.json').write_text(json.dumps({'files':manifest},indent=2)+'\n')
print(json.dumps({'sources':len(sources),'receipt_records':len(receipts),'manifest_files':len(manifest),'status':out['status']}))
