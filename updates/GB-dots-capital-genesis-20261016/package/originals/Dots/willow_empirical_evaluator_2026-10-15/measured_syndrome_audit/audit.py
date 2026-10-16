import pathlib,hashlib,json,zlib,re,struct,random
import numpy as np
A=(pathlib.Path(__file__).resolve().parent.parent / 'measured_syndrome_acquisition'); O=pathlib.Path(__file__).parent
D=A/'data/google_105Q_surface_code_d3_d5_d7/d5_at_q8_7/X'
def mul(a,b):
 x,z,p=a;u,v,q=b
 return x^u,z^v,(p+q+2*(z&u).bit_count())%4
class State:
 def __init__(self,n,seed=None):self.rng=random.Random(seed) if seed is not None else None;self.n=n;self.rows=[(0,1<<q,0) for q in range(n)]
 def gate(self,g,a,b=None):
  out=[]
  for x,z,p in self.rows:
   xa=(x>>a)&1;za=(z>>a)&1
   if g=='H':p+=2*xa*za;x^=(xa^za)<<a;z^=(xa^za)<<a
   elif g=='CZ':
    xb=(x>>b)&1;p+=2*xa*xb;z^=(xb<<a)^(xa<<b)
   elif g=='X':p+=2*za
   elif g=='Y':p+=2*(xa^za)
   else:raise ValueError(g)
   out.append((x,z,p%4))
  self.rows=out
 def m(self,q):
  anti=[k for k,(x,z,p) in enumerate(self.rows) if (x>>q)&1]
  if anti:
   k=anti[0];old=self.rows[k]
   for j in anti[1:]:self.rows[j]=mul(self.rows[j],old)
   outcome=self.rng.randrange(2) if self.rng else 0;self.rows[k]=(0,1<<q,2*outcome);return outcome
  # Gaussian-eliminate the commuting generator group, retaining Pauli phase.
  basis={}
  for row in self.rows:
   v=row[0]|(row[1]<<self.n)
   while v:
    bit=v.bit_length()-1
    if bit not in basis:basis[bit]=row;break
    row=mul(row,basis[bit]);v=row[0]|(row[1]<<self.n)
  target=(0,1<<q,0);v=target[0]|(target[1]<<self.n)
  while v:
   target=mul(target,basis[v.bit_length()-1]);v=target[0]|(target[1]<<self.n)
  assert target[2] in (0,2)
  return target[2]//2

def parse(path,seed=None,sweep=0):
 lines=path.read_text().splitlines();n=1+max(int(line.split()[-1]) for line in lines if line.startswith('QUBIT_COORDS'))
 st=State(n,seed);x=[0]*n;z=[0]*n;ref=[];masks=[];det=[];obs=[];measurement_qubits=[]
 for line in lines:
  match=re.match(r'(\w+)(?:\(([^)]*)\))?\s*(.*)',line);op,args,rest=match.groups();ts=rest.split()
  if op in ('QUBIT_COORDS','TICK'):continue
  if op=='CX':
   for a,b in zip(ts[::2],ts[1::2]):
    assert a.startswith('sweep[');x[int(b)]^=1<<int(a[6:-1])
    if sweep>>int(a[6:-1])&1:st.gate('X',int(b))
  elif op in ('H','X','Y'):
   for q in map(int,ts):
    st.gate(op,q)
    if op=='H':x[q],z[q]=z[q],x[q]
  elif op=='CZ':
   for a,b in zip(map(int,ts[::2]),map(int,ts[1::2])):st.gate(op,a,b);z[a]^=x[b];z[b]^=x[a]
  elif op=='R':
   for q in map(int,ts):
    if st.m(q):st.gate('X',q)
    x[q]=z[q]=0
  elif op=='M':
   for q in map(int,ts):ref.append(st.m(q));masks.append(x[q]);measurement_qubits.append(q)
  elif op in ('DETECTOR','OBSERVABLE_INCLUDE'):
   inds=[len(ref)+int(s[4:-1]) for s in ts];mask=offset=0
   for i in inds:mask^=masks[i];offset^=ref[i]
   e={'measurement_indices':inds,'sweep_indices':[i for i in range(25) if mask>>i&1],'reference_offset':offset}
   (det if op=='DETECTOR' else obs).append(e)
  else:raise ValueError(op)
 return {'measurements':len(ref),'detectors':det,'observables':obs,'reference_measurements':ref,'measurement_qubits':measurement_qubits}
def bits(path,k):
 data=path.read_bytes();assert len(data)==50000*((k+7)//8)
 a=np.unpackbits(np.frombuffer(data,np.uint8).reshape(50000,-1),axis=1,bitorder='little');assert not a[:,k:].any()
 return a[:,:k]
# Every extracted original is checked against independent archive CRC/size metadata and saved SHA256.
saved=json.loads((A/'SHA256SUMS.json').read_text());integrity=[]
# Portable replay checks preserved publisher-entry metadata; original audit parsed the ZIP central directory directly.
entries={e['name']:e for e in json.loads((A/'preserved_archive_entries.json').read_text())}
for p in sorted((A/'data').rglob('*')):
 if not p.is_file():continue
 e=entries[str(p.relative_to(A/'data'))];b=p.read_bytes();h=hashlib.sha256(b).hexdigest()
 assert len(b)==e['size'] and zlib.crc32(b)==e['crc'] and h==saved[str(p.relative_to(A))]
 integrity.append({'file':str(p.relative_to(A)),'bytes':len(b),'crc32':zlib.crc32(b),'sha256':h})
result={'original_integrity':integrity,'conditions':{}}
for rounds in [50,13]:
 folder=D/f'r{rounds}';mapping=parse(folder/'circuit_ideal.stim');(O/f'r{rounds}_independent_map.json').write_text(json.dumps(mapping,indent=2))
 m=bits(folder/'measurements.b8',mapping['measurements']);s=bits(folder/'sweep_bits.b8',25)
 actual=bits(folder/'obs_flips_actual.b8',1);detections=bits(folder/'detection_events.b8',len(mapping['detectors']))
 mismatch={}
 for key,truth in [('detectors',detections),('observables',actual)]:
  count=0
  for j,e in enumerate(mapping[key]):
   pred=np.full(50000,e['reference_offset'],np.uint8)
   for i in e['measurement_indices']:pred^=m[:,i]
   for i in e['sweep_indices']:pred^=s[:,i]
   count+=int(np.count_nonzero(pred^truth[:,j]))
  mismatch[key]=count;assert count==0
 baselines={};priors={}
 for p in sorted((folder/'decoding_results').glob('*/obs_flips_predicted.b8')):
  v=bits(p,1);baselines[p.parent.name]=int(np.count_nonzero(v^actual))
 for p in sorted((folder/'decoding_results').glob('*/error_model.dem')):priors.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(),[]).append(p.parent.name)
 result['conditions'][str(rounds)]={'measurements':mapping['measurements'],'detectors':len(mapping['detectors']),'sweep_bits':25,'observables':len(mapping['observables']),'shots':50000,'all_padding_zero':True,'independent_reference_mismatch_bits':mismatch,'baseline_failures':baselines,'identical_prior_groups':priors,'observable_map':mapping['observables']}
(O/'audit_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result['conditions'],indent=2))

# Independently exercise all 25 basis sweep configurations and several measurement branches.
checks=[]
for rounds in [50,13]:
 base=parse(D/f'r{rounds}'/'circuit_ideal.stim')
 for seed,sweep in [(k,0) for k in range(4)]+[(100+i,1<<i) for i in range(25)]:
  test=parse(D/f'r{rounds}'/'circuit_ideal.stim',seed=seed,sweep=sweep)
  for category in ['detectors','observables']:
   for a,b in zip(base[category],test[category]):
    expected=a['reference_offset']
    for bit in a['sweep_indices']:expected^=(sweep>>bit)&1
    assert b['reference_offset']==expected
  checks.append({'rounds':rounds,'seed':seed,'sweep':sweep,'parities_match':True})
(O/'reference_self_checks.json').write_text(json.dumps(checks,indent=2))
