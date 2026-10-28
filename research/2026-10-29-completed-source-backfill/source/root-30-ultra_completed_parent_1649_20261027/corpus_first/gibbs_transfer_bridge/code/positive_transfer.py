"""Actual positive periodic transfer, same9^N history size, no frame projection."""
import sys
sys.dont_write_bytecode=True
import numpy as np,json,time,hashlib
from pathlib import Path
import sympy as S
from positive_gate import factors,BASE,D
SOURCE=BASE/'sources/actual_cp_instrument_delta001.npz'

def finite_kernel(a,N):
 local=np.einsum('aij,bjk->abik',a,a,optimize=True)
 if N==1:return np.trace(local,axis1=2,axis2=3).T
 if N==2:return np.einsum('axij,byji->xyab',local,local,optimize=True).reshape(9**N,9**N)
 if N==3:return np.einsum('axij,byjk,czki->xyzabc',local,local,local,optimize=True).reshape(9**N,9**N)
 raise ValueError(N)

def apply_pair(M,gate,i,j,n):
 perm=[i,j]+[k for k in range(n) if k not in (i,j)]+[n]
 array=M.reshape((D,)*n+(D**n,));array=np.transpose(array,perm)
 array=gate@array.reshape(D*D,-1)
 return np.transpose(array.reshape((D,)*n+(D**n,)),np.argsort(perm)).reshape(D**n,D**n)

def physical_trace(gate,n,N):
 M=np.eye(D**n)
 for step in range(N):
  for parity in (0,1):
   for i in range(parity,n,2):M=apply_pair(M,gate,i,(i+1)%n,n)
 return float(np.trace(M))

def run():
 start=time.monotonic();source=np.load(SOURCE);a=source['A']
 pairs,labels,exactG,h=factors(S.Rational(1,1000))
 L=np.array([np.array(x,dtype=float) for x,y in pairs]);R=np.array([np.array(y,dtype=float) for x,y in pairs]);G=np.array(exactG,dtype=float)
 C=np.array([G@np.kron(x,y) for x in L for y in R])
 assert np.min(C)>=0
 records=[]
 for N in (1,2,3):
  KL=finite_kernel(L,N);KR=finite_kernel(R,N);T=KL@KR.T
  KA=finite_kernel(a,N);Q=KA@KA.T
  assert np.min(T)>=0
  row=dict(time_slices=N,beta=N*.001,history_dimension=9**N,
   positive_MPO_virtual_dimension=25,minimum_positive_transfer_entry=float(np.min(T)),trace_checks=[])
  for m in (1,2,4,8,16,32,64):
   exact_trace=float(np.trace(np.linalg.matrix_power(Q,m)))
   positive_trace=float(np.trace(np.linalg.matrix_power(T,m)))
   relative=abs(exact_trace-positive_trace)/max(1,abs(exact_trace));assert relative<3e-11
   row['trace_checks'].append(dict(physical_sites=2*m,relative_source_difference=relative,Z_positive=positive_trace))
  direct=physical_trace(G,4,N);closed=float(np.trace(T@T));assert abs(direct-closed)<1e-9*max(1,abs(direct))
  row['four_site_direct_physical_trace']=direct;row['four_site_closed_positive_trace']=closed
  row['frobenius_condition_proxy']=float(np.linalg.norm(T)/np.linalg.norm(Q))
  records.append(row);print('N',N,'all periodic traces pass',flush=True)
 result=dict(status='EXACT_LOCAL_POSITIVE_FACTOR_AND_ALL_SIZE_NETWORK_IDENTITY_WITH_FINITE_ORIENTATION_REPLAYS',
  source_file=str(SOURCE),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
  local_nonnegative_MPO_matrices=len(C),records=records,
  limitation='History9^N and spatially powered virtual25^m growth remain. Tested beta<=.003 is not a cold long-ring seed.',
  elapsed_seconds=time.monotonic()-start)
 (BASE/'results/POSITIVE_TRANSFER.json').write_text(json.dumps(result,indent=2)+'\n')
 np.savez(BASE/'results/positive_local_delta001.npz',L=L,R=R,C=C,G=G)
 print(json.dumps(dict(elapsed_seconds=result['elapsed_seconds'],local_nonnegative_MPO_matrices=len(C)),indent=2))

if __name__=='__main__':run()
