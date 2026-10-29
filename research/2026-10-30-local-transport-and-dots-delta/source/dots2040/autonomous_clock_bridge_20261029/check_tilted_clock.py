"""Numerical finite-chain spectral challenge only, not a norm or tail proof."""
import numpy as np
from scipy.sparse import csr_matrix,eye,kron
from scipy.sparse.linalg import eigs
from pathlib import Path
import json,hashlib
P=Path(__file__);records=[]
for n in range(2,9):
 states=[a for a in range(1<<n) if not(a&(a<<1))];ix={a:i for i,a in enumerate(states)};d=len(states)
 bs=[]
 for x in range(n):
  rows=[];cols=[]
  for a in states:
   if a>>x&1:rows.append(ix[a^(1<<x)]);cols.append(ix[a])
  bs.append(csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(d,d)))
 for g in [.03,.2]:
  H=sum((g*(b+b.T) for b in bs),csr_matrix((d,d)))
  K=-1j*H-sum((.5*b.T@b for b in bs),csr_matrix((d,d)))
  Id=eye(d,format='csr');Lbase=kron(Id,K)+kron(K.conjugate(),Id)
  for label,S in [('all',set(range(n))),('even',set(range(0,n,2))),('one',{n//2})]:
   L=Lbase+sum((kron(b.conjugate(),b) for x,b in enumerate(bs) if x not in S),csr_matrix((d*d,d*d)))
   if d*d<=100:ev=np.linalg.eigvals(L.toarray());ab=max(ev.real)
   else:ab=max(eigs(L,k=2,which='LR',return_eigenvectors=False,tol=1e-9,maxiter=20000).real)
   rate=-ab;records.append({'n':n,'legal_dim':d,'g':g,'marked':label,'marked_count':len(S),'escape_rate':float(rate),'rate_per_mark_over_4g2':float(rate/(len(S)*4*g*g))})
   print(n,g,label,rate,flush=True)
out={'status':'finite spectral diagnostic, not uniform survival bound','source_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'records':records};P.with_suffix('.json').write_text(json.dumps(out,indent=2))
