"""Expand each addressed CC-U into CNOTs and rational single-qubit gates.
The resulting circuit is exactly unitary; exact rational residuals certify error.
"""
from finite_povm_synthesis_v1 import *
from pathlib import Path
import json,cmath,math,time
P=Path(__file__).parent

def parse(z):return C(F(z[0]),F(z[1]))
def parseM(m):return [[parse(z) for z in row] for row in m]
def numeric(M):return np.array([[complex(float(z.r),float(z.i)) for z in row] for row in M])
def single(target,M):return {'kind':'single','target':target,'matrix':[[z.data() for z in row] for row in M]}
def rz(t):return su2_round(np.diag([np.exp(-.5j*t),np.exp(.5j*t)]))
def ry(t):return su2_round(np.array([[np.cos(t/2),-np.sin(t/2)],[np.sin(t/2),np.cos(t/2)]],complex))
def controlled_decomposition(control,target,U):
 alpha=np.angle(np.linalg.det(U))/2;S=U*np.exp(-1j*alpha);a,b=S[0]
 gamma=2*np.arctan2(abs(b),abs(a))
 if abs(b)<1e-14:beta=-2*np.angle(a);delta=0.
 elif abs(a)<1e-14:beta=-2*np.angle(-b);delta=0.
 else:beta=-np.angle(a)-np.angle(-b);delta=-np.angle(a)+np.angle(-b)
 # Chronological C, CX, B, CX, A; B=Ry(-g/2)Rz(-(d+b)/2), A=Rz(b)Ry(g/2).
 out=[single(target,rz((delta-beta)/2)),{'kind':'cnot','control':control,'target':target},single(target,rz(-(delta+beta)/2)),single(target,ry(-gamma/2)),{'kind':'cnot','control':control,'target':target},single(target,ry(gamma/2)),single(target,rz(beta))]
 z=phase_round(np.exp(1j*alpha));out.append(single(control,[[O,Z],[Z,z]]))
 return out

def apply_local(W,g):
 target=g['target']
 if g['kind']=='single':
  M=parseM(g['matrix'])
  for a in range(8):
   if not (a>>target)&1:apply_rows(W,[a,a|(1<<target)],M)
 else:
  control=g['control']
  for a in range(8):
   if ((a>>control)&1) and not((a>>target)&1):W[a],W[a|(1<<target)]=W[a|(1<<target)],W[a]

def exact_primitive(p):
 U=eye(8);a=sum(value<<j for j,value in p['controls']);b=a|(1<<p['target'])
 apply_rows(U,[a,b],parseM(p['matrix']));return U

def compile_one(p):
 target=p['target'];controls=[x[0] for x in p['controls']];a,b=controls
 M=numeric(parseM(p['matrix']));ev,Q=np.linalg.eig(M);V=Q@np.diag(np.exp(.5j*np.angle(ev)))@np.linalg.inv(Q)
 # Controlled V_b, CX_ab, controlled Vdag_b, CX_ab, controlled V_a.
 core=controlled_decomposition(b,target,V)+[{'kind':'cnot','control':a,'target':b}]+controlled_decomposition(b,target,V.conj().T)+[{'kind':'cnot','control':a,'target':b}]+controlled_decomposition(a,target,V)
 opens=[single(j,[[Z,O],[O,Z]]) for j,value in p['controls'] if value==0]
 gates=opens+core+list(reversed(opens));U=eye(8)
 for g in gates:
  if g['kind']=='single':assert mm(adj(parseM(g['matrix'])),parseM(g['matrix']))==eye(2)
  apply_local(U,g)
 exact=exact_primitive(p)
 err=sum((U[i][j]-exact[i][j]).norm2() for i in range(8) for j in range(8))
 _,bound=sqrt_interval(err,128)
 return gates,bound

src=json.loads((P/'compile_controlled_primitives_v2.json').read_text());out=[];start=time.time()
for r in src['runs']:
 gates=[];bounds=[]
 for i,p in enumerate(r['primitives']):
  gs,bound=compile_one(p);gates+=gs;bounds.append(bound)
 result={'seed':r['seed'],'labels':r['labels'],'single_qubit_gate_count':sum(g['kind']=='single' for g in gates),'cnot_count':sum(g['kind']=='cnot' for g in gates),'maximum_primitive_operator_error_upper':str(max(bounds)),'sum_primitive_operator_error_upper':str(sum(bounds)),'total_correction_channel_half_diamond_upper':str(F(r['correction_channel_half_diamond_upper'])+sum(bounds)),'total_correction_channel_half_diamond_upper_float':float(F(r['correction_channel_half_diamond_upper'])+sum(bounds)),'gates':gates}
 out.append(result);print(r['seed'],len(gates),result['total_correction_channel_half_diamond_upper_float'],flush=True)
(P/'compile_local_controls_v3.json').write_text(json.dumps({'status':'EXACT_RATIONAL_LOCAL_CONTROL_CERTIFICATES','elapsed_seconds':time.time()-start,'runs':out,'scope':'Known single-qubit unitary and CNOT circuit model; hardware gate/preparation/readout errors additional.'},indent=2)+'\n')
