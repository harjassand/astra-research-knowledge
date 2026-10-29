#!/usr/bin/env python3
"""Trace-decreasing branch recovery: full CPTP vs unitary, no physical gate claim."""
import os,sys,json,hashlib
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
sys.path.insert(0,'producer-workspace/quantum_sdp')
import cvxpy as cp
import numpy as np
HERE=Path(__file__).parent;Q=HERE.parent
P=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def herm(A):return (A+A.conj().T)/2
def ptr(J):return J[:2,:2]+J[2:,2:]
def to_ptm(J):return np.array([[np.trace(np.kron(P[a],P[b].T)@J).real/2 for b in range(4)] for a in range(4)])
def from_ptm(M):return sum(M[a,b]*np.kron(P[a],P[b].T)/2 for a in range(4) for b in range(4))
def score(D,M):return np.trace(D@M).real/4
def objective(M):return herm(sum(M[b,a]*np.kron(P[a],P[b].T)/8 for a in range(4) for b in range(4)))
def unitary(M):
 U,s,Vh=np.linalg.svd(M[1:,1:]);V=Vh.T;R=V@np.diag([1,1,np.linalg.det(V@U.T)])@U.T
 D=np.zeros((4,4));D[0,0]=1;D[1:,1:]=R
 return D

def solve(M):
 C=objective(M);J=cp.Variable((4,4),hermitian=True)
 constr=[J>>0,J[:2,:2]+J[2:,2:]==np.eye(2)]
 prob=cp.Problem(cp.Maximize(cp.real(cp.trace(C@J))),constr)
 prob.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_feas=1e-10,tol_gap_rel=1e-10,max_iter=300)
 raw=herm(J.value);w,V=np.linalg.eigh(raw);positive=(V*np.maximum(w,0))@V.conj().T
 G=herm(ptr(positive));w,V=np.linalg.eigh(G);W=np.kron(np.eye(2),(V*(1/np.sqrt(w)))@V.conj().T);repaired=herm(W@positive@W)
 D=to_ptm(repaired);Y=herm(constr[1].dual_value);mine=np.linalg.eigvalsh(np.kron(np.eye(2),Y)-C)[0]
 Y+=max(0,-mine+1e-12)*np.eye(2);hi=float(np.trace(Y).real);lo=score(D,M)
 assert np.max(abs(ptr(repaired)-np.eye(2)))<1e-10 and np.linalg.eigvalsh(repaired)[0]>-1e-10
 assert abs(lo-np.trace(C@repaired).real)<1e-10
 return D,repaired,{'solver_status':prob.status,'numerical_lower':lo,'numerical_upper':hi,'numerical_gap':hi-lo,'primal_min_eigenvalue':float(np.linalg.eigvalsh(repaired)[0]),'TP_residual':float(np.max(abs(ptr(repaired)-np.eye(2)))),'dual_min_eigenvalue':float(np.linalg.eigvalsh(np.kron(np.eye(2),Y)-C)[0])}

def run():
 source=Q/'continuous_inverse_control_20261028/endpoint_instrument_v1.json';src=json.loads(source.read_text());rows=[];models={}
 for key,M in src['branch_PTMs'].items():
  M=np.array(M);D,J,diag=solve(M);U=unitary(M);models['CPTP_J_'+key]=J;models['CPTP_M_'+key]=D;models['unitary_M_'+key]=U
  rows.append({'branch':key,'probability_mixed_input':M[0,0],'input_dependent_probability_vector':M[0,1:].tolist(),'unitary_oracle_score':score(U,M),'CPTP_oracle_score':score(D,M),'CPTP_translation':D[1:,0].tolist(),**diag})
 fixtures=[]
 for p in [.2,1.]:
  maps=[(1-p)*np.eye(4)]
  for s in [1,-1]:
   M=np.zeros((4,4));M[0,0]=p/2;M[0,3]=s*p/2;maps.append(M)
  full=0;uni=0
  for M in maps:
   D,J,d=solve(M);full+=score(D,M);uni+=score(unitary(M),M)
  assert abs(full-(1-p/2))<1e-7 and abs(uni-(1-3*p/4))<1e-12
  fixtures.append({'p':p,'CPTP':full,'unitary':uni,'expected_CPTP':1-p/2,'expected_unitary':1-3*p/4})
 out={'status':'SOURCE_INFORMED_IDEAL_ENDPOINT_ORACLES_NOT_ACQUIRED_OR_PHYSICALLY_COMPILED','source':str(source.relative_to(Q)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'rows':rows,'total_CPTP_oracle_Fe':sum(r['CPTP_oracle_score'] for r in rows),'total_unitary_oracle_Fe':sum(r['unitary_oracle_score'] for r in rows),'total_numerical_dual_upper':sum(r['numerical_upper'] for r in rows),'fixtures':fixtures}
 (HERE/'oracle_results_v1.json').write_text(json.dumps(out,indent=2)+'\n');np.savez_compressed(HERE/'oracle_models_v1.npz',**models)
 print(out['total_CPTP_oracle_Fe'],out['total_unitary_oracle_Fe'],out['total_numerical_dual_upper'])
if __name__=='__main__':run()
