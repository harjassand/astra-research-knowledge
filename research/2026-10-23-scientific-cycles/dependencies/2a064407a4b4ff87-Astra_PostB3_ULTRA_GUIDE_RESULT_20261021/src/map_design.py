"""Design/count-only mapping; never reads RNA matrix values or pair scores."""
import hashlib,json,sys,time,zipfile,collections,re,xml.etree.ElementTree as E
from pathlib import Path
import h5py
ROOT=Path(__file__).resolve().parents[1];COMMON=ROOT/'common/Astra_PostB3_Empirical_Probe_20261021';NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def xlsx_rows(path,sheet):
    with zipfile.ZipFile(path) as z:
        ss=[''.join(t.text or '' for t in x.findall('.//s:t',NS)) for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
        rows=[]
        for row in E.fromstring(z.read(f'xl/worksheets/sheet{sheet}.xml')).findall('s:sheetData/s:row',NS):
            d={}
            for c in row:
                v=c.find('s:v',NS);a=v.text if v is not None else ''.join(t.text or '' for t in c.findall('.//s:t',NS));a=ss[int(a)] if c.get('t')=='s' else a
                d[re.sub(r'\d','',c.get('r'))]=a
            rows.append((int(row.get('r')),d))
        return rows

def column(group,key):
    a=group[key];decode=lambda x:x.decode() if isinstance(x,bytes) else str(x)
    if isinstance(a,h5py.Dataset):return list(map(decode,a[:]))
    cats=list(map(decode,a['categories'][:]));return [cats[i] if i>=0 else '<missing>' for i in a['codes'][:]]

def main():
    start=time.perf_counter();inp=COMMON/'data/WesselsSatija2023.h5ad';supp=COMMON/'sources/protocol/41592_2022_1705_MOESM3_ESM.xlsx'
    identity={'h5ad_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),'h5ad_bytes':inp.stat().st_size,'supplement_sha256':hashlib.sha256(supp.read_bytes()).hexdigest()}
    if identity['h5ad_sha256']!='5da0485aed81b23bda57b4a7b4510a394682d54911416db89b4846ff6dd34732':raise ValueError('wrong RNA input')
    if identity['supplement_sha256']!='64582b92edae28b71a6aff1072cb600c275969e6af454465be475c8a58a22450':raise ValueError('wrong supplement')
    design={};uid_to_array={};guides={}
    for row,d in xlsx_rows(supp,1):
        if not d.get('A','').startswith('UID-'):continue
        name=d['B'];parts=name.split(':')
        if len(parts)!=2:raise ValueError(('array arity',name))
        record={'uid':d['A'],'array':name,'combination':d['C'],'guide1':parts[0],'guide2':parts[1],'sequence1':d['D'],'sequence2':d['E'],'barcode':d['F'],'full_sequence':d['G'],'source_row':row}
        if name in design:raise ValueError('duplicate array name')
        for pos,(g,s) in enumerate(zip(parts,[d['D'],d['E']]),1):
            if len(s)!=23 or not set(s)<=set('ACGT'):raise ValueError('guide sequence format')
            if g in guides and guides[g]['sequence']!=s:raise ValueError('inconsistent guide sequence')
            guides.setdefault(g,{'sequence':s,'slots':set()})['slots'].add(pos)
            if record['full_sequence'].count(s)!=1:raise ValueError('guide is not unique in full construct')
        # Verify physical sequence order, not merely labels.
        if record['full_sequence'].find(d['D'])>=record['full_sequence'].find(d['E']):raise ValueError('sequence order mismatch')
        design[name]=record;uid_to_array[d['A']]=name
    with h5py.File(inp) as f:
        obs={k:column(f['obs'],k) for k in ['CRISPRcas13_Array','perturbation','Guide.Class','ID.g1','HTO','10X_lane','cell_barcode']};shape=list(map(int,f['X'].attrs['shape']));nnz=int(f['X/data'].shape[0])
    counts=collections.Counter(obs['CRISPRcas13_Array']);groups=collections.defaultdict(list);mismatch=[]
    for a,p,g,u in zip(obs['CRISPRcas13_Array'],obs['perturbation'],obs['Guide.Class'],obs['ID.g1']):
        if a not in design or uid_to_array.get(u)!=a:mismatch.append([a,u])
        groups[p].append(a)
    if mismatch:raise ValueError(('metadata design mismatch',mismatch[:5]))
    pair_names=sorted(k for k in groups if '_' in k and k!='control');families=[]
    control='NT_g1:NT_g2'
    for pair in pair_names:
        a,b=pair.split('_');c1=f'{a}_g1:{b}_g2';c2=f'{b}_g1:{a}_g2';arms=[c1,c2,f'{a}_g1:NT_g2',f'NT_g1:{b}_g2',f'{b}_g1:NT_g2',f'NT_g1:{a}_g2',control];reasons=[]
        for arm in arms:
            if arm not in design:reasons.append({'arm':arm,'reason':'not_in_design'})
            elif counts[arm]<5:reasons.append({'arm':arm,'reason':'fewer_than_5_delivered_cells','n':counts[arm]})
        if all(x in design for x in (c1,c2)):
            s1={design[c1]['sequence1'],design[c1]['sequence2']};s2={design[c2]['sequence1'],design[c2]['sequence2']}
            if len(s1|s2)!=4:reasons.append({'reason':'pair_constructions_do_not_have_four_distinct_target_sequences'})
        families.append({'pair':pair,'a':a,'b':b,'construction1':c1,'construction2':c2,'arms':arms,'counts':{x:counts[x] for x in arms},'eligible':not reasons,'exclusions':reasons})
    by_hl={}
    for arm in sorted(counts):
        inds=[i for i,x in enumerate(obs['CRISPRcas13_Array']) if x==arm];by_hl[arm]={'count':len(inds),'HTO':dict(collections.Counter(obs['HTO'][i] for i in inds)),'lane':dict(collections.Counter(obs['10X_lane'][i] for i in inds))}
    out={'identity':identity,'mapping_rule':'Supp Table1 THP1 UID rows; G1/G2 physically verified ordered 23nt spacers in full array sequence; ID.g1 must map to array UID. No expression read.','shape':shape,'nonzero_entries':nnz,'designed_arrays':len(design),'delivered_arrays':len(counts),'array_map':design,'guides':{g:{'sequence':v['sequence'],'slots':sorted(v['slots'])} for g,v in guides.items()},'delivered_counts':dict(sorted(counts.items())),'missing_designed_arrays':sorted(set(design)-set(counts)),'families':families,'eligible_pairs':[x['pair'] for x in families if x['eligible']],'excluded_pairs':[x for x in families if not x['eligible']],'matching_control':control,'matching_control_n':counts[control],'array_partitions':by_hl,'metadata_only':True,'wall_s':time.perf_counter()-start}
    (ROOT/'results/DESIGN_MAP.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['identity','shape','nonzero_entries','designed_arrays','delivered_arrays','missing_designed_arrays','eligible_pairs','matching_control_n','wall_s']},indent=2));print('EXCLUDED',json.dumps([{'pair':x['pair'],'reasons':x['exclusions']} for x in out['excluded_pairs']],indent=2))
if __name__=='__main__':main()
