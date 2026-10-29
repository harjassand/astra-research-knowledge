"""Independent noisy instrument and retained-state reconstruction, ideal-idle model only."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import numpy as np,importlib.util,json,hashlib,sys
D=Path(__file__).parent.parent;Q=D.parent;pilot=Q/'five_qubit_acquired_frame_pilot_20261028'
sys.path.insert(0,str(pilot));import code_and_channels as c
sp=importlib.util.spec_from_file_location('author',D/'run_channel.py');a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex);H=(X+Z)/np.sqrt(2);PS=[I,X,Y,Z];CX=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
G=['XZZXI','IXZZX','XIXZZ','ZXIXZ']
def embed(g,qs,n):
 out=np.zeros((2**n,2**n),complex)
 for col in range(2**n):
  inp=sum(((col>>(n-1-q))&1)<<(len(qs)-1-j) for j,q in enumerate(qs))
  for val in range(2**len(qs)):
   row=col
   for j,q in enumerate(qs):
    bit=1<<(n-1-q);row=(row&~bit)|(((val>>(len(qs)-1-j))&1)*bit)
   out[row,col]=g[val,inp]
 return out
def rot(p,x):return np.cos(x/2)*np.eye(len(p))-1j*np.sin(x/2)*p
def instr(k,flag,eta):
 n=7 if flag else 6
 init=np.kron(np.array([1,0]),np.array([1,1])/np.sqrt(2)) if flag else np.array([1,0])
 V=np.kron(np.eye(32),init[:,None]).astype(complex)
 V=embed(rot(Y,eta),[5],n)@V
 if flag:V=embed(rot(Y,eta),[6],n)@V
 supp=[(q,p) for q,p in enumerate(G[k]) if p!='I']
 gates=[]
 for j,(q,p) in enumerate(supp):
  if flag and j in [1,3]:gates.append((CX,[6,5],np.kron(Z,Z)))
  if p=='X':gates.append((H,[q],X))
  gates.append((CX,[q,5],np.kron(Z,Z)))
  if p=='X':gates.append((H,[q],X))
 for gate,qs,axis in gates:V=embed(rot(axis,eta)@gate,qs,n)@V
 V=embed(rot(Y,eta),[5],n)@V
 if flag:V=embed(rot(Z,eta),[6],n)@V
 out={}
 for sb in range(2):
  if flag:
   for fb in range(2):
    bra=np.kron(np.eye(2)[sb],np.array([1,(-1)**fb])/np.sqrt(2))
    out[sb,fb]=np.kron(np.eye(32),bra[None,:])@V
  else:out[sb]=np.kron(np.eye(32),np.eye(2)[sb][None,:])@V
 assert np.max(abs(sum(k.conj().T@k for k in out.values())-np.eye(32)))<2e-13
 return out
# Independently reconstructed controller tables from earlier audit, not author tables.
ctx={'__file__':str(Q/'flagged_five_qubit_independent_check_20261028.py')};f=Path(ctx['__file__']);exec(compile(f.read_text().split('author=D/')[0],str(f),'exec'),ctx)
labels='IXZY'
def corr(k,flag,sy,eta):
 w=(ctx['tables'][k].get(sy,ctx['normal'][sy]) if flag else ctx['normal'][sy])[:5]
 U=np.eye(32,dtype=complex)
 for q,p in enumerate(w):
  if p:U=embed(rot(X,eta)@{'X':X,'Y':Y,'Z':Z}[labels[p]],[q],5)@U
 return U
def instrument(eta):
 F=[instr(k,True,eta) for k in range(4)];U=[instr(k,False,eta) for k in range(4)]
 fresh={():np.eye(32,dtype=complex)}
 for check in U:fresh={sy+(b,):op@v for sy,v in fresh.items() for b,op in check.items()}
 prefix=np.eye(32,dtype=complex);K=[]
 for k in range(4):
  for sb,fb in [(0,1),(1,0),(1,1)]:
   for sy,v in fresh.items():K.append(corr(k,fb,sy,eta)@v@F[k][sb,fb]@prefix)
  prefix=F[k][0,0]@prefix
 return np.array(K+[prefix])
def sup(ks):return sum((np.kron(k,k.conjugate()) for k in ks),np.zeros((1024,1024),complex))
def ptm(A,rec):return np.array([[sum(np.trace(p@r@v@r.conj().T).real/2 for r in rec) for v in A] for p in PS])
M=np.load(pilot/'models.npz');R=json.loads((D/'results.json').read_text());selection=json.loads((pilot/'results.json').read_text())['selected_calibration_N_per_site'];assert selection==4096
sources=c.generator_sources();local=[[M[f'learned_frame_N4096_site{i}'].conj().T@np.array(k,complex) for k in src['Ks']] for i,src in enumerate(sources)]
full=[[embed(k,[i],5) for k in ks] for i,ks in enumerate(local)]
enc,rec=c.exact_encoder_recovery();enc=np.array(enc,complex);rec=[np.array(r,complex) for r in rec];initial=np.array([enc@p@enc.conj().T for p in PS]);rows=[]
for eta in [0.,.0001,.0003,.001,-.001,.003,.01,-.01,.03,-.03]:
 K=instrument(eta);authorK=a.ec_kraus(eta)[0];kd=float(np.max(abs(K-authorK)));assert kd<2e-14
 tp=float(np.max(abs(sum(k.conj().T@k for k in K)-np.eye(32))));assert tp<3e-13
 F=sup(K);
 if eta==0.:assert np.max(abs(F-sup([enc@r for r in rec])))<2e-13
 A=initial.copy();ref=next(r for r in R['encoded_runs'] if r['coherent_angle_per_noisy_operation']==eta);checks=[]
 for t in range(1,129):
  for ks in full:A=np.array([sum(k@v@k.conj().T for k in ks) for v in A])
  A=(F@A.reshape(4,1024).T).T.reshape(4,32,32)
  if t in [1,2,8,32,128]:
   T=ptm(A,rec);saved=next(r for r in ref['results'] if r['T']==t);err=float(np.max(abs(T-saved['logical_PTM'])));assert err<2e-11
   if t==1:first=T.copy()
   nd=float(np.max(abs(T-np.linalg.matrix_power(first,t))));assert abs(nd-saved['naive_decoded_round_product_PTM_max_difference'])<3e-11
   checks.append({'T':t,'PTM_replay_max_error':err,'naive_reset_max_difference':nd})
 rows.append({'eta':eta,'independent_instrument_Kraus_max_error':kd,'TP_max_error':tp,'checks':checks});print(eta,rows[-1],flush=True)
baseline_checks=[]
for site,ks in enumerate(local):
 B=np.array(PS);savedsite=R['matched_unencoded'][site]
 for t in range(1,129):
  B=np.array([sum(k@v@k.conj().T for k in ks) for v in B])
  if t in [1,2,4,8,16,32,64,128]:
   Mloc=np.array([[np.trace(p@v).real/2 for v in B] for p in PS]);saved=next(z for z in savedsite['results'] if z['T']==t)
   err=float(np.max(abs(Mloc-saved['logical_PTM'])));assert err<1e-12;baseline_checks.append(err)
assert hashlib.sha256((pilot/'models.npz').read_bytes()).hexdigest()==R['source_models_sha256']
assert hashlib.sha256((pilot/'code_and_channels.py').read_bytes()).hexdigest()==R['source_generator_sha256']
files=[Q/'flagged_five_qubit_storage_check_20261028.py',D/'run_channel.py',D/'results.json',D/'GOVERNING_MODEL.md',pilot/'models.npz',pilot/'code_and_channels.py',pilot/'results.json',Q/'flagged_five_qubit_independent_check_20261028.py',Path(__file__)]
out={'status':'PASS_INDEPENDENT_IDEAL_IDLE_NOISY_INSTRUMENT_AND_PHYSICAL_REUSE','rows':rows,'matched_fixed_control_baseline_PTM_max_error':max(baseline_checks),'source_draws':0,'sha256':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
