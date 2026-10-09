from pathlib import Path
import sys,json,hashlib,random,time
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'gaussian_transfer'))
SOURCE_PATH=Path(__file__).resolve().parents[2]/'gaussian_transfer/displaced_sampler.py'
SOURCE_BYTES=SOURCE_PATH.read_bytes()
SOURCE_SHA256=hashlib.sha256(SOURCE_BYTES).hexdigest()
from displaced_sampler import ParityEnvelope
from flint import ctx,arb
rows=[]
for a,b,c,h in [(F(0),F(1),F(1),10**20),(F(0),F(3,7),F(1,1<<128),(1<<256)+1),(F(0),F(3,7),F(1<<128),(1<<256)+1),(F(0),F(1),F(1),(1<<1024)+1),(F(1),F(1),F(1),100),(F(1),F(1),F(1,10**30),101),(F(1),F(1),F(1),10**20)]:
 start=time.perf_counter();law=ParityEnvelope(a,b,c,h,F(1,1000));anchors=[]
 with ctx.workprec(law._precision(256)):
  for e in (0,1):
   k=e+2*law.anchors[e]
   value=law._logweight_narrow(k,160)
   scaled=(value-law.reference).exp()*law.scale
   lo,hi=law.bounds(k)
   assert scaled>=lo and scaled<=hi
   anchors.append({'k':str(k),'normalized_mass':str(scaled/law.scale),'bounds':[lo,hi]})
  masses=[(law._logweight_narrow(e+2*law.anchors[e],160)-law.reference).exp() for e in (0,1)]
  assert max(v.lower() for v in masses)>(-arb(1)/8).exp()
 outputs=[]
 for j in range(5):
  output=law.draw(random.Random(j));assert law.fallback_count==0;outputs.append(str(output))
 row={'a':str(a),'b':str(b),'c':str(c),'h':str(h),'anchors':anchors,'draws':outputs,'seconds':time.perf_counter()-start}
 rows.append(row);print('checked',len(rows),'h_bits',h.bit_length(),'seconds',row['seconds'],flush=True)
path=Path(__file__).resolve().parents[2]/'gaussian_transfer/displaced_sampler.py'
out={'source_sha256':SOURCE_SHA256,'cases':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',len(rows),flush=True)
