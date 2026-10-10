import sys,pathlib,hashlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'python_packages'))
import pandas as pd
rows=[]
for f in (ROOT/'raw/extracted').rglob('*.xlsx'):
 group=str(f.parent.relative_to(ROOT/'raw/extracted'))
 d=pd.read_excel(f,header=None)
 for _,r in d.iterrows():
  if isinstance(r.get(1),str) and r[1].endswith('.txt'):
   cell=r[2];key=hashlib.sha256(('motor_priming_20261010:'+cell).encode()).hexdigest();rows.append(dict(group=group,file=r[1],cell=cell,strong=r[3],pulse=r.get(4),key=key,path=group+'/traces_4000Hz/'+r[1],split='discovery' if int(key[:8],16)%2==0 else 'validation'))
d=pd.DataFrame(rows);d.to_csv(ROOT/'raw/traces_manifest.csv',index=False)
selected=[]
for (group,split),g in d.groupby(['group','split']):
 if not ('03_Under pulse' in group or '01_Without' in group): continue
 # Select a single raw trace from each cell without looking at its outcomes.
 n=8 if '03_Under pulse' in group else 6
 s=g.sort_values(['key','file']).drop_duplicates('cell').head(n)
 selected+=s.to_dict('records')
s=pd.DataFrame(selected);s.to_csv(ROOT/'raw/selected_manifest.csv',index=False)
for split in ['discovery','validation']:
 (ROOT/f'raw/{split}_selection.json').write_text(json.dumps(s[s.split==split].path.tolist(),indent=2))
 print(split,s[s.split==split].group.value_counts().to_dict())
