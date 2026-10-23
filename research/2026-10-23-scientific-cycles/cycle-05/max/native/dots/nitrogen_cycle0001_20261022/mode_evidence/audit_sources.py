"""Source-schema/hash audit only. No kinetics contraction or trajectory."""
from pathlib import Path
import json,re,hashlib,collections
p=Path(__file__).parent
manifest=[]
for f in sorted(p.glob('jp*')):
 if f.name.endswith('_extracted.txt') or (f.suffix=='.txt' and f.name.startswith('jp7')):continue
 b=f.read_bytes();manifest.append({'file':f.name,'bytes':len(b),'md5':hashlib.md5(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest()})
(p/'manifest.json').write_text(json.dumps(manifest,indent=2))
s={}; T=None
for line in (p/'jp0c09999_si_002.txt').read_text().splitlines():
 if line.startswith('#ix='):T=int(re.search('tt=([0-9]+)',line)[1])
 elif line and not line.startswith('#'):
  v,w,k,var=line.split(',');s.setdefault(T,[]).append((int(v),int(w),float(k),float(var)))
summary={T:{'rows':len(a),'v_range':[min(r[0] for r in a),max(r[0] for r in a)],'w_range':[min(r[1] for r in a),max(r[1] for r in a)],'unique_pairs':len(set((r[0],r[1]) for r in a)),'negative_rate_rows':sum(r[2]<0 for r in a),'selected_rows':[r for r in a if r[0] in [0,1,10] and r[1] in [0,1,10]]}for T,a in s.items()}
(p/'reactive_table_audit.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({T:{k:v for k,v in d.items() if k!='selected_rows'} for T,d in summary.items()},indent=2))
# Extract high-precision level assignments as source transcription, without fitting.
t=(p/'jp7b04442_si_002.txt').read_text()
energies={}
for name,pattern in [('N2',r'En2_onn_3Asec\((\d+)\)\s*=\s*([-+0-9.E]+)'),('NO',r'Eno\((\d+)\)\s*=\s*([-+0-9.E]+)')]:
 energies[name]=[{ 'v':int(v),'energy_eV_dissociation_zero':float(e)} for v,e in re.findall(pattern,t)]
(p/'2017_levels_transcribed.json').write_text(json.dumps(energies,indent=2))
