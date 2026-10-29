import sys,numpy as np,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'source'))
from construct_inner import *
from received_algebra_compiler_v1 import gate_rows
strings=['XZZXI','IXZZX','XIXZZ','ZXIXZ'];n=5
rows=[sum((1<<j if c in 'XY' else 0)|(1<<(n+j) if c in 'ZY' else 0) for j,c in enumerate(st)) for st in strings]
A=array(rows,n);rng=np.random.default_rng(123)
for attempt in range(50):
 B=A.copy()
 for j in range(n):
  if rng.integers(2):gate_rows(B,('H',j),n)
  if rng.integers(2):gate_rows(B,('S',j),n)
 gs=compile_algebra(B,n)['gates'];table={};errs=list(low_errors(n,1))
 for e in errs:
  q,ph=transform(e,(e&(e>>n)).bit_count()%4,gs,n);sy=q&15;logical=((q>>4)&1)|(((q>>9)&1)<<1);table[sy]=logical
 if any(table[s]!=table[int(f'{s:04b}'[::-1],2)] for s in table):break
else:raise Exception('not found')
U=np.eye(32,dtype=complex)
for g in gs:U=unitary(g,n)@U
E=U.conj().T[:,:2];rho=np.array([[1,0],[0,0]],complex);out=[]
for e in errs:
 P=(1j**((e&(e>>n)).bit_count()%4))*pauli(array([e],n)[0],n);W=(U@P@E).reshape(16,2,2)
 wrong=np.zeros((2,2),complex);right=wrong.copy()
 for sy in range(16):
  for dst,key in [(wrong,sy),(right,int(f'{sy:04b}'[::-1],2))]:
   l=table.get(key,0);C=pauli(array([((l&1)|((l>>1)<<1))],1)[0],1).conj().T;V=C@W[sy];dst+=V@rho@V.conj().T
 out.append((hex(e),float(np.linalg.norm(wrong-rho)),float(np.linalg.norm(right-rho))))
print(json.dumps({'attempt':attempt,'table':table,'cases':out},indent=2))
