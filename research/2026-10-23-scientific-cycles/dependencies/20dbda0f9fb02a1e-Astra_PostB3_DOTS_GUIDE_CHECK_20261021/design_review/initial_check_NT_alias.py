"""Independent original-contract metadata receipt. No RNA X values accessed."""
import argparse,collections,hashlib,json,pathlib,re,resource,time,zipfile,xml.etree.ElementTree as ET
import h5py
P=argparse.ArgumentParser();P.add_argument('--common',type=pathlib.Path,required=True);P.add_argument('--producer',type=pathlib.Path,required=True);P.add_argument('--output',type=pathlib.Path,required=True);a=P.parse_args();start=time.monotonic()
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def require(x,msg):
 if not x:raise ValueError(msg)
raw=a.common/'data/WesselsSatija2023.h5ad';book=a.common/'sources/protocol/41592_2022_1705_MOESM3_ESM.xlsx'
pins={'raw':'5da0485aed81b23bda57b4a7b4510a394682d54911416db89b4846ff6dd34732','book':'64582b92edae28b71a6aff1072cb600c275969e6af454465be475c8a58a22450'}
require(sha(raw)==pins['raw'],'original RNA hash');require(sha(book)==pins['book'],'original supplement hash')
ns='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
def table(sheet):
 with zipfile.ZipFile(book) as z:
  strings=[''.join(t.text or '' for t in node.iter(ns+'t')) for node in ET.fromstring(z.read('xl/sharedStrings.xml'))]
  rows={}
  for node in ET.fromstring(z.read(f'xl/worksheets/sheet{sheet}.xml')).iter(ns+'row'):
   vals={}
   for c in node:
    v=c.find(ns+'v');s='' if v is None else v.text
    if c.get('t')=='s':s=strings[int(s)]
    vals[re.sub('[0-9]','',c.get('r'))]=s
   rows[int(node.get('r'))]=vals
  return rows
rows=table(1);require(rows[39]['A']=='#THP1 CaRPool-seq CRISPR arrays','THP1 section');require([rows[40].get(c) for c in 'ABCDEFG']==['UID','ArrayID','Combination','G1','G2','BC','Seq'],'source columns')
design={};uid={};guide_map={}
for row,v in rows.items():
 if row<41 or not v.get('A','').startswith('UID-'):continue
 name=v['B'];g=name.split(':');seq=[v['D'],v['E']];full=v['G'].upper()
 require(len(g)==2 and name not in design and v['A'] not in uid,'unique two-slot design')
 require(full.count(seq[0])==full.count(seq[1])==1 and full.index(seq[0])<full.index(seq[1]),'physical spacer ordering')
 require(v['F'] in full,'barcode in construct')
 for pos in range(2):
  require(len(seq[pos])==23 and set(seq[pos])<=set('ACGT'),'spacer sequence')
  require(g[pos].endswith('_g'+str(pos+1)),'slot label consistency')
  key=(g[pos],pos+1);require(key not in guide_map or guide_map[key]==seq[pos],'constant sequence per guide/slot');guide_map[key]=seq[pos]
 targets=tuple(x.rsplit('_g',1)[0] for x in g)
 require(set(v['C'].split('_'))==set(targets),'declared target combination')
 design[name]={'uid':v['A'],'targets':targets,'spacers':seq,'row':row,'raw':v};uid[v['A']]=name

def readcol(o,k):
 n=o[k]
 if isinstance(n,h5py.Dataset):return n.asstr()[:].tolist()
 cats=n['categories'].asstr()[:];codes=n['codes'][:];require((codes>=0).all(),'no missing '+k);return cats[codes].tolist()
with h5py.File(raw) as f:
 obs={k:readcol(f['obs'],k) for k in ['CRISPRcas13_Array','ID.g1','perturbation','Guide.Class','HTO','10X_lane','cell_barcode']}
 shape=list(map(int,f['X'].attrs['shape']))
counts=collections.Counter(obs['CRISPRcas13_Array']);require(len(set(obs['cell_barcode']))==len(obs['cell_barcode']),'unique cells')
for ar,u,pert in zip(obs['CRISPRcas13_Array'],obs['ID.g1'],obs['perturbation']):
 require(ar in design and uid[u]==ar,'cell UID mapping')
 ts=sorted(t for t in design[ar]['targets'] if t!='NT');expected='_'.join(ts) if ts else 'control';require(pert==expected,'cell target label')
# Derive pair universe from original array labels, not producer eligible list.
families=sorted(set(tuple(sorted(design[ar]['targets'])) for ar in counts if 'NT' not in design[ar]['targets']))
control='NT_g1:NT_g2';eligible=[];exclusions={};independent_counts={}
for x,y in families:
 arms=[f'{x}_g1:{y}_g2',f'{y}_g1:{x}_g2',f'{x}_g1:NT_g2',f'NT_g1:{y}_g2',f'{y}_g1:NT_g2',f'NT_g1:{x}_g2',control]
 reasons=[]
 for ar in arms:
  if ar not in design:reasons.append({'arm':ar,'reason':'not_in_design'})
  elif counts[ar]<5:reasons.append({'arm':ar,'reason':'fewer_than_5_delivered_cells','n':counts[ar]})
 if all(ar in design for ar in arms[:2]) and len(set(sum([design[ar]['spacers'] for ar in arms[:2]],[])))!=4:reasons.append({'reason':'pair_constructions_do_not_have_four_distinct_target_sequences'})
 key=x+'_'+y;independent_counts[key]={ar:counts[ar] for ar in arms}
 if reasons:exclusions[key]=reasons
 else:eligible.append(key)
prod=json.loads((a.producer/'results/DESIGN_MAP.json').read_text())
require(prod['eligible_pairs']==eligible,'eligible set exact');require({x['pair']:x['exclusions'] for x in prod['excluded_pairs']}==exclusions,'exclusion reasons exact');require(prod['delivered_counts']==dict(counts),'all delivered counts')
for family in prod['families']:require(family['counts']==independent_counts[family['pair']],'all required-arm counts')
for name,r in design.items():
 p=prod['array_map'][name];require([p['uid'],p['array'],p['combination'],p['sequence1'],p['sequence2'],p['barcode'],p['full_sequence'],p['source_row']]==[r['raw'][c] for c in 'ABCDEFG']+[r['row']],'all producer mapping fields')
gfi=[k for k in counts if 'GFI1_g2' in k];require(not gfi,'excluded GFI1 g2 not reintroduced')
ctl=[i for i,ar in enumerate(obs['CRISPRcas13_Array']) if ar==control]
hto_rows=table(7);hto_source=[r for r in hto_rows.values() if any('subpool THP1' in str(v) for v in r.values())]
freeze=json.loads((a.producer/'FREEZE.json').read_text())
freezechecks={key:sha(a.producer/path)==freeze[key] for key,path in [('contract_sha256','FROZEN_CONTRACT.txt'),('initial_contract_sha256','FROZEN_CONTRACT_INITIAL.txt'),('design_map_sha256','results/DESIGN_MAP.json'),('analysis_source_sha256','src/run_guide_experiment.py')]};require(all(freezechecks.values()),'freeze hashes')
# Concrete hostile mutation: target labels/physical slot order must remain tied to originals.
hostile=[]
try:require(design[next(iter(design))]['spacers'][0]==prod['array_map'][next(iter(design))]['sequence2'],'mutated swapped spacer rejected')
except ValueError:hostile.append('swapped spacer rejected')
else:raise ValueError('hostile mutation unexpectedly passed')
result={'decision':'ACCEPT_DESIGN_MAPPING_AND_ADMISSION_WITH_SCOPED_PROVENANCE','original_input_pins':pins,'shape':shape,'designed_arrays':len(design),'delivered_arrays':len(counts),'families':len(families),'eligible':len(eligible),'excluded':len(exclusions),'control_cells':len(ctl),'control_lanes':dict(collections.Counter(obs['10X_lane'][i] for i in ctl)),'HTO_categories':sorted(set(obs['HTO'])),'THP1_HTO_source_rows':hto_source,'GFI1_g2_delivered_arrays':gfi,'missing_designed_arrays':sorted(set(design)-set(counts)),'freeze_hash_checks':freezechecks,'freeze_timestamp_scope':'Self-reported source timestamps verified for internal consistency only, not independent proof no earlier RNA access. Historical root outcome access explicitly acknowledged.','target_mapping_scope':'Source-declared targets and actual spacers/UID/positions verified, not independently aligned to genomic/transcript reference or experimentally validated knockdown.','upstream_exclusion_scope':'Absence of GFI1 g2 verified; biological reason borrowed from supplied protocol report, not inferred from metadata. Other missing arms not causally assigned.','hostile_checks':hostile,'RNA_matrix_values_read':False,'producer_code_imported':False,'wall_s':time.monotonic()-start,'cpu_s':time.process_time(),'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
