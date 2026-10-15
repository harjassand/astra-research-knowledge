"""Small read-only public-source intake. Does not run any OPF solver."""
from pathlib import Path
from fractions import Fraction
import urllib.request,json,hashlib,datetime,re
ROOT=Path(__file__).resolve().parent
sources=[
 ('coffrin_hijazi_vanhentenryck_2016.html','https://arxiv.org/abs/1512.04644','SDP/QC intersections, bound tightening and lifted cuts are established comparators.'),
 ('lefranc_minimal_sparsity_2023.html','https://arxiv.org/html/2305.19232v1','Second-order sparsity design is established; sparse implementations need explicit support checks.'),
 ('oustry_2022.html','https://ojmo.centre-mersenne.org/articles/10.5802/ojmo.17/','Strengthened conic relaxation and global MILP scheme are published comparators.'),
 ('oustry_pinned_README.txt','https://raw.githubusercontent.com/aoustry/SDP-MILP4OPF/3d3a2c1ca40f6ca15cc5c73d05fe4e47c2de1772/README.md','Original pinned implementation lists MOSEK, licensed CPLEX/docplex, chompack and cvxopt among required dependencies.'),
 ('pglib_v21_07_case89_api.m','https://raw.githubusercontent.com/power-grid-lib/pglib-opf/v21.07/api/pglib_opf_case89_pegase__api.m','Older public benchmark bytes for an exact version-mismatch check.'),
]
receipts=[]
for name,url,purpose in sources:
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Astra-exact-reciprocal-audit'})
  with urllib.request.urlopen(req,timeout=30) as r:
   data=r.read();status=r.status;ctype=r.headers.get('Content-Type')
  (ROOT/name).write_bytes(data)
  receipts.append({'path':name,'url':url,'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'content_type':ctype,'purpose':purpose})
 except Exception as e:
  receipts.append({'path':name,'url':url,'status':'ACQUISITION_FAILED','error':repr(e),'purpose':purpose})
out={'acquired_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':receipts,'scope':'Primary-source and original-file acquisition receipts. No performance result or novelty proof.'}
(ROOT/'PRIMARY_SOURCE_RECEIPTS.json').write_text(json.dumps(out,indent=2)+'\n')
def table(text,label):
 raw=re.search(r'mpc\.'+label+r'\s*=\s*\[(.*?)\];',text,re.S).group(1)
 return [[Fraction(x) for x in line.split('%')[0].replace(';',' ').split()] for line in raw.splitlines() if line.split('%')[0].strip()]
old=ROOT/'pglib_v21_07_case89_api.m'
if old.exists():
 new=ROOT/'pglib_opf_case89_pegase__api.m'
 oldgen=table(old.read_text(),'gen');newgen=table(new.read_text(),'gen')
 diffs=[]
 for a,b in zip(oldgen,newgen):
  assert a[0]==b[0]
  if a!=b:diffs.append({'bus':int(a[0]),'old_Pmax_MW':str(a[8]),'new_Pmax_MW':str(b[8]),'all_changed_column_indices_1based':[j+1 for j,(x,y) in enumerate(zip(a,b)) if x!=y]})
 (ROOT/'PGLIB_VERSION_COMPARISON.json').write_text(json.dumps({'status':'EXACT_RATIONAL_COMPARISON','older_url':sources[-1][1],'selected_blob':'9b5c0548be7dd4baaa01a8b6359a81d8ec2faf3f','generator_differences':diffs,'boundary':'This checks differing generator rows, not a full fieldwise model audit.'},indent=2)+'\n')
print(json.dumps(out,indent=2))
