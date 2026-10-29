"""Exact Pauli propagation for Chao--Reichardt 1705.02329v1, Sec. II.
No numerical tolerances; phases omitted, since equivalence is projective.
Native parity couplings are compiled as H(data)-CX(data,s)-H(data).
"""
from itertools import product
from pathlib import Path
import json
N=7; S=5; F=6

def pauli(q,p):
 return ((1<<q) if p in 'XY' else 0)|((1<<(N+q)) if p in 'ZY' else 0)
def word(w):
 return sum(pauli(q,p) for q,p in enumerate(w))
def string(e):
 return ''.join('IXZY'[((e>>q)&1)+2*((e>>(N+q))&1)] for q in range(5))
def weight(e):return sum(((e>>q)|(e>>(N+q)))&1 for q in range(5))
def symp(a,b):return (((a&127)&(b>>N)).bit_count()+((b&127)&(a>>N)).bit_count())%2
G=list(map(word,['XZZXI','IXZZX','XIXZZ','ZXIXZ']))
STAB={0}
for g in G:STAB|={e^g for e in list(STAB)}
def canon(e):return min(e^g for g in STAB)
def syn(e):return tuple(symp(e,g) for g in G)
W1=[0]+[pauli(q,p) for q in range(5) for p in 'XYZ']
W1COR={syn(e):e for e in W1}
CORRECTABLE={canon(e) for e in W1}
DATAMASK=sum(pauli(q,'Y') for q in range(5))
def apply(e,op):
 kind,qs=op
 if kind=='H':
  q=qs[0]
  if ((e>>q)^(e>>(N+q)))&1:e^=pauli(q,'Y')
 elif kind=='CX':
  c,t=qs
  if (e>>c)&1:e^=pauli(t,'X')
  if (e>>(N+t))&1:e^=pauli(c,'Z')
 return e

def circuit(k,flagged):
 ops=[('prepZ',(S,))]
 if flagged:ops += [('prepX',(F,))]
 supp=[(q,p) for q,p in enumerate(['XZZXI','IXZZX','XIXZZ','ZXIXZ'][k]) if p!='I']
 for j,(q,p) in enumerate(supp):
  if flagged and j in (1,3):ops.append(('CX',(F,S)))
  if p=='X':ops.append(('H',(q,)))
  ops.append(('CX',(q,S)))
  if p=='X':ops.append(('H',(q,)))
 ops += [('measureZ',(S,)),('readoutZ',(S,))]
 if flagged:ops += [('measureX',(F,)),('readoutX',(F,))]
 return ops

def faults_for(op):
 kind,qs=op
 if kind in ('measureZ','measureX','readoutZ','readoutX'):return [('flip',0)]
 return [('pauli',sum(pauli(q,p) for q,p in zip(qs,ps))) for ps in product('IXYZ',repeat=len(qs)) if any(p!='I' for p in ps)]

def measure(e,k,flagged,tag,fault=None,trace=None,idles=False):
 e &= DATAMASK; outs=[0,0]
 for j,op in enumerate(circuit(k,flagged)):
  kind,qs=op
  loc=(tag,k,j,'gate')
  if trace is not None:
   trace.extend((loc,f) for f in faults_for(op))
  if kind.startswith('prep'):
   for q in qs:e &= ~pauli(q,'Y')
  elif kind=='measureZ':outs[0]=(e>>S)&1
  elif kind=='measureX':outs[1]=(e>>(N+F))&1
  else:e=apply(e,op)
  if fault is not None and fault[0]==loc:
   ft,v=fault[1]
   if ft=='flip':outs[int(kind.endswith('X'))]^=1
   else:e^=v
  # Explicit serial implementation: all unused qubits idle at every step (including conservative inactive ancilla idles).
  if idles:
   for q in range(7):
    if q in qs:continue
    iloc=(tag,k,j,'idle'+str(q))
    if trace is not None:trace.extend((iloc,('pauli',pauli(q,p))) for p in 'XYZ')
    if fault is not None and fault[0]==iloc:e ^= fault[1][1]
 return e&DATAMASK,tuple(outs)

# Build flag correction table from all one-location faults within each check.
# Include harmless representatives caused by either flag CX, preparations, readout.
FLAGCOR=[];FLAGAMB=[]
for k in range(4):
 tr=[];measure(0,k,True,'F',trace=tr,idles=True)
 table={};amb=[]
 for fault in tr:
  e,(s,f)=measure(0,k,True,'F',fault,idles=True)
  if f:
   sy=syn(e)
   if sy in table and canon(e^table[sy])!=0:amb.append((string(e),string(table[sy])))
   table.setdefault(sy,e)
 FLAGCOR.append(table);FLAGAMB.append(amb)

def run(e=0,fault=None,idles=True):
 trace=[];record=[];ng=0
 for k in range(4):
  e,(s,f)=measure(e,k,True,'F',fault,trace,idles);record.append((k,s,f));ng+=len(circuit(k,True))
  if s or f:
   ss=[]
   for h in range(4):
    e,(sh,_)=measure(e,h,False,'U',fault,trace,idles);ss.append(sh);ng+=len(circuit(h,False))
   sy=tuple(ss);record.append(('U',sy))
   # Total controller: multi-fault syndromes outside the flag table use
   # ordinary weight-one correction, without postselection.
   cor=FLAGCOR[k].get(sy,W1COR[sy]) if f else W1COR[sy]
   if cor is None:return None,record,trace,ng
   # Physically apply the conditional Pauli correction, rather than merely
   # keeping a frame that an unknown subsequent source might not respect.
   for q,p in enumerate(string(cor)):
    if p=='I':continue
    loc=('C',k,q,'gate');op=('P',(q,));ng+=1
    trace.extend((loc,f) for f in faults_for(op))
    e ^= pauli(q,p)
    if fault is not None and fault[0]==loc:e ^= fault[1][1]
    if idles:
     for r in range(7):
      if r==q:continue
      iloc=('C',k,q,'idle'+str(r))
      trace.extend((iloc,('pauli',pauli(r,p2))) for p2 in 'XYZ')
      if fault is not None and fault[0]==iloc:e ^= fault[1][1]
   return e&DATAMASK,record,trace,ng
 return e,record,trace,ng

def main():
 assert not any(FLAGAMB),FLAGAMB
 paper_g0=list(map(word,['IIIII','IIZXI','IXZXI','IYZXI','IZZXI','IIIXI','IIXXI','IIYXI']))
 paper_g1=list(map(word,['IIIII','IIIIX','IXXII','IIIXX','XIIIY','IXIII','IIIZX','IIIYX']))
 for k,paper in enumerate([paper_g0,paper_g1]):
  assert {canon(e) for e in FLAGCOR[k].values()}=={canon(e) for e in paper}
 # Exact distance-three / KL check: distinct weight-one errors have distinct
 # syndromes; stabilizer-equivalent representatives act identically on code.
 assert len({syn(e) for e in W1})==16
 assert len(STAB)==16
 assert all(symp(a,b)==0 for a in G for b in G)
 inputs=[]
 for e in W1:
  out,rec,tr,n=run(e)
  inputs.append({'input':string(e),'residual':string(out),'pass':canon(out)==0})
 assert all(t['pass'] for t in inputs)
 _,_,locations,_=run()
 results=[];bad=[];groups={};max_slots=0;max_locations=0
 for fault in locations:
  out,rec,tr,n=run(fault=fault)
  max_slots=max(max_slots,n);max_locations=max(max_locations,len({loc for loc,f in tr}))
  ok=out is not None and canon(out) in CORRECTABLE
  item={'location':fault[0],'fault':fault[1],'output':string(out) if out is not None else None,'record':rec,'pass':ok}
  results.append(item)
  if not ok:bad.append(item)
  # All output branches of each arbitrary local Kraus fault belong to the
  # same global correctable span S*{I,X_i,Y_i,Z_i}. Stronger than per-record KL.
  groups.setdefault(str(fault[0]),set()).add(canon(out) if out is not None else -1)
 out={'status':'PASS' if not bad else 'FAIL','primary':'https://arxiv.org/html/1705.02329v1#S2','implementation':'ascending support order, H-CX-H X-parity decomposition, serial data and ancilla idles, physical conditional single-qubit Pauli correction','fault_free_input_tests':inputs,'single_fault_clean_input_count':len(results),'distinct_fault_locations':len(groups),'max_reached_serial_slots':max_slots,'max_reached_locations':max_locations,'paper_first_two_flag_tables_equivalent':True,'failures':bad,'flag_tables':[{''.join(map(str,s)):string(e) for s,e in t.items()} for t in FLAGCOR],'single_fault_output_global_correctable_span':not bad,'all_fault_results':results}
 path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='all_fault_results'},indent=2))
 assert not bad
if __name__=='__main__':main()
