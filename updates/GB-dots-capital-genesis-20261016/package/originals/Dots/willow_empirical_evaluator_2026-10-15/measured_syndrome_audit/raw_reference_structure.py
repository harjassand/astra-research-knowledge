import pathlib,json,re
O=pathlib.Path(__file__).parent;D=(pathlib.Path(__file__).resolve().parent.parent / 'measured_syndrome_acquisition/data/google_105Q_surface_code_d3_d5_d7/d5_at_q8_7/X')
def mul(a,b):
 x,z,p,g=a;u,v,q,h=b
 return x^u,z^v,(p+q+2*(z&u).bit_count())%4,g^h
class SymState:
 def __init__(self,n):self.n=n;self.rows=[(0,1<<q,0,0) for q in range(n)];self.variables=0
 def gate(self,op,a,b=None,signmask=0):
  out=[]
  for x,z,p,g in self.rows:
   xa=x>>a&1;za=z>>a&1
   if op=='H':p+=2*xa*za;x^=(xa^za)<<a;z^=(xa^za)<<a
   elif op=='CZ':xb=x>>b&1;p+=2*xa*xb;z^=(xb<<a)^(xa<<b)
   elif op=='X':p+=2*za;g^=signmask if za else 0
   elif op=='Y':p+=2*(xa^za)
   elif op=='SYMX':g^=signmask if za else 0
   else:raise ValueError(op)
   out.append((x,z,p%4,g))
  self.rows=out
 def m(self,q):
  anti=[i for i,r in enumerate(self.rows) if r[0]>>q&1]
  if anti:
   k=anti[0];old=self.rows[k]
   for j in anti[1:]:self.rows[j]=mul(self.rows[j],old)
   mask=1<<self.variables;self.variables+=1;self.rows[k]=(0,1<<q,0,mask);return 0,mask,True
  basis={}
  for row in self.rows:
   v=row[0]|row[1]<<self.n
   while v:
    bit=v.bit_length()-1
    if bit not in basis:basis[bit]=row;break
    row=mul(row,basis[bit]);v=row[0]|row[1]<<self.n
  target=(0,1<<q,0,0);v=target[1]<<self.n
  while v:target=mul(target,basis[v.bit_length()-1]);v=target[0]|target[1]<<self.n
  assert target[2] in (0,2)
  return target[2]//2,target[3],False
for rounds in [50,13]:
 lines=(D/f'r{rounds}'/'circuit_ideal.stim').read_text().splitlines();n=1+max(int(l.split()[-1]) for l in lines if l.startswith('QUBIT_COORDS'));st=SymState(n);x=[0]*n;z=[0]*n;measure=[];det=[];obs=[]
 for line in lines:
  match=re.match(r'(\w+)(?:\(([^)]*)\))?\s*(.*)',line);op,args,rest=match.groups();ts=rest.split()
  if op in ['QUBIT_COORDS','TICK']:continue
  if op=='CX':
   for a,b in zip(ts[::2],ts[1::2]):assert a.startswith('sweep[');x[int(b)]^=1<<int(a[6:-1])
  elif op in ['H','X','Y']:
   for q in map(int,ts):
    st.gate(op,q)
    if op=='H':x[q],z[q]=z[q],x[q]
  elif op=='CZ':
   for a,b in zip(map(int,ts[::2]),map(int,ts[1::2])):st.gate(op,a,b);z[a]^=x[b];z[b]^=x[a]
  elif op=='R':
   for q in map(int,ts):
    c,g,_=st.m(q)
    if c:st.gate('X',q)
    if g:st.gate('SYMX',q,signmask=g)
    x[q]=z[q]=0
  elif op=='M':
   for q in map(int,ts):
    c,g,fresh=st.m(q);measure.append({'index':len(measure),'qubit':q,'constant':c,'sweep_indices':[i for i in range(25) if x[q]>>i&1],'random_variables':[i for i in range(st.variables) if g>>i&1],'introduces_fresh_random_variable':fresh})
  elif op in ['DETECTOR','OBSERVABLE_INCLUDE']:
   inds=[len(measure)+int(t[4:-1]) for t in ts];g=0
   for i in inds:
    for b in measure[i]['random_variables']:g^=1<<b
   assert g==0
  else:raise ValueError(op)
 summary={'rounds':rounds,'fresh_random_measurement_indices':[m['index'] for m in measure if m['introduces_fresh_random_variable']],'first_round_random_indices':[m['index'] for m in measure[:24] if m['random_variables']],'first_round_determined_indices':[m['index'] for m in measure[:24] if not m['random_variables']],'random_dependent_ancilla_measurements':sum(bool(m['random_variables']) for m in measure[:24*rounds]),'total_ancilla_measurements':24*rounds,'all_detector_and_observable_random_variables_cancel':True,'measurements':measure}
 (O/f'r{rounds}_raw_reference_structure.json').write_text(json.dumps(summary,indent=2));print({k:v for k,v in summary.items() if k!='measurements'})
# Rank audit on the measurement parity map; sweep is treated as known input.
def rank(rows):
 basis={}
 for row in rows:
  while row:
   k=row.bit_length()-1
   if k not in basis:basis[k]=row;break
   row^=basis[k]
 return len(basis)
for rounds in [50,13]:
 mapping=json.loads((O/f'r{rounds}_independent_map.json').read_text());rows=[]
 for e in mapping['detectors']:
  row=0
  for i in e['measurement_indices']:row^=1<<i
  rows.append(row)
 obs=[]
 for e in mapping['observables']:
  row=0
  for i in e['measurement_indices']:row^=1<<i
  obs.append(row)
 p=O/f'r{rounds}_raw_reference_structure.json';a=json.loads(p.read_text());a.update(measurement_to_detector_rank=rank(rows),measurement_to_detector_and_observable_rank=rank(rows+obs),raw_measurement_nullity_given_detectors_sweep=mapping['measurements']-rank(rows),raw_measurement_nullity_given_detectors_observable_sweep=mapping['measurements']-rank(rows+obs));p.write_text(json.dumps(a,indent=2))
