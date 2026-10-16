"""Own finite-dimensional CP-record enumeration; no experimental data or author code."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
from fractions import Fraction
import numpy as np,json,itertools
from scipy.linalg import expm
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]).astype(complex)
def kron(a,b,c):return np.kron(np.kron(a,b),c)
Id=np.eye(8,dtype=complex);ZA=kron(Z,I,I);ZC=kron(I,Z,I)
VA=.4*kron(X,I,X);VC=.5*kron(I,X,Z)
H0=.27*kron(I,I,Y)+.19*kron(Z,I,Z)+.11*kron(I,Z,X)+.09*kron(Z,Z,Y)
assert np.linalg.norm(H0@ZA-ZA@H0)<1e-13 and np.linalg.norm(H0@ZC-ZC@H0)<1e-13
assert np.linalg.norm(VA@VC-VC@VA)>0
P={name:[(Id+S)/2,(Id-S)/2] for name,S in [('A',ZA),('C',ZC)]}
# A1,A2,C1,C2,C3; staggered boundaries are prescribed, not outcomes.
a=[Fraction(1,5),Fraction(1,5),Fraction(1,6),Fraction(1,6),Fraction(1,6)]
segments=[(Fraction(1,3),0,2,[('C',2)]),(Fraction(1,6),0,3,[('A',0)]),(Fraction(1,6),1,3,[('C',3)]),(Fraction(1,3),1,4,[('A',1),('C',4)])]
def instrument(z):
 branches=[]
 for u,v in itertools.product(range(2),repeat=2):branches.append((P['C'][v]@P['A'][u],{'A':u,'C':v},0,[u,v]))
 for dt,ia,ic,measure in segments:
  U=expm(-1j*float(dt)*(H0+z[ia]*VA+z[ic]*VC))
  branches=[(U@K,last,flags,record) for K,last,flags,record in branches]
  for parent,cell in measure:
   nxt=[]
   for K,last,flags,record in branches:
    for outcome in range(2):
     newlast=dict(last);newlast[parent]=outcome
     nxt.append((P[parent][outcome]@K,newlast,flags|((outcome!=last[parent])<<cell),record+[outcome]))
   branches=nxt
 return branches
branches=instrument([1.]*5);assert len(branches)==128
effects=[K.conj().T@K for K,_,_,_ in branches];normal=sum(effects)
normal_error=float(np.linalg.norm(normal-Id,2));assert normal_error<3e-13

def bound_report(F,budget):
 F=(F+F.conj().T)/2;vals=np.linalg.eigvalsh(F);mx=float(vals[-1]);mn=float(vals[0]);assert mn>=-2e-14 and mx<=float(budget)+2e-14
 return {'budget_exact':str(budget),'budget':float(budget),'effect_max_eigenvalue':mx,'effect_min_eigenvalue':mn,'ratio':mx/float(budget)}
cells=[]
for mask in range(1,32):
 F=sum(E for E,(_,_,flags,_) in zip(effects,branches) if flags&mask==mask)
 budget=Fraction(1)
 for i in range(5):
  if mask>>i&1:budget*=a[i]**2
 cells.append({'subset':[i for i in range(5) if mask>>i&1],**bound_report(F,budget)})
parents=[]
for mask in [1,2,3]:
 F=sum(E for E,(_,_,flags,_) in zip(effects,branches) if (not(mask&1) or flags&3) and (not(mask&2) or flags&28))
 budget=(Fraction(2,25) if mask&1 else Fraction(1))*(Fraction(1,12) if mask&2 else Fraction(1))
 parents.append({'subset':[name for k,name in enumerate(['A','C']) if mask>>k&1],**bound_report(F,budget)})
# Deleting one cell keeps every measurement and predicate unchanged.
rng=np.random.default_rng(230145);deletions=[]
for cell in range(5):
 for trial in range(3):
  z=[1.]*5 if trial==0 else rng.uniform(0,1,5).tolist();z[cell]=0
  bs=instrument(z);F=sum(K.conj().T@K for K,_,flags,_ in bs if flags>>cell&1)
  norm=float(np.linalg.norm(F,2));assert norm<3e-29
  deletions.append({'cell':cell,'other_parameters':z,'deleted_bad_effect_norm':norm})
r={'status':'PASS','model_dimension':8,'input_domain':'entire 8-dimensional memory+shared-bath space; arbitrary input correlations','total_time':1,'MA':2,'MC':3,'cell_order':['A1','A2','C1','C2','C3'],'cell_actions_exact':[str(x) for x in a],'actual_kraus_records':len(branches),'normalization_operator_norm_error':normal_error,'cell_subset_checks':cells,'parent_OR_subset_checks':parents,'deletion_checks':deletions,'coupling_commutator_norm':float(np.linalg.norm(VA@VC-VC@VA,2)),'calculation':'complete CP-record enumeration with dense matrix exponentials/eigenvalues in floating point, not sampled trajectories or formal interval arithmetic','no_actual_monotonicity_claim':True}
Path(__file__).with_name('deterministic_cells_independent_results.json').write_text(json.dumps(r,indent=2));print(json.dumps({'status':r['status'],'records':len(branches),'normalization_error':normal_error,'cell_subsets':len(cells),'max_cell_effect_budget_ratio':max(v['ratio'] for v in cells),'parent_subsets':parents,'max_deleted_bad_effect_norm':max(v['deleted_bad_effect_norm'] for v in deletions)},indent=2))
