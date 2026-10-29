from itertools import product
from pathlib import Path
import json
import sympy as s
ROOT=Path(__file__).parent
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)

def bits(v,n):return tuple((v>>j)&1 for j in range(n))
def val(bs):return sum(b<<j for j,b in enumerate(bs))

def compile_and_check(gs,den,name,write=False):
 n=(gs[0].rows.bit_length()-1);d=2**n;M=len(gs)
 maxw=max(abs(int(z)) for g in gs for a in g for z in [s.re(a),s.im(a)])
 zbits=max(1,maxw.bit_length())
 nextvar=1
 def alloc(k):
  nonlocal nextvar
  ans=list(range(nextvar,nextvar+k));nextvar+=k;return ans
 wires=[alloc(n) for _ in range(M)];phases=[alloc(2) for _ in range(M+1)]
 components=[alloc(1)[0] for _ in gs];selectors=[alloc(zbits) for _ in gs]
 clauses=[[-v] for v in phases[0]]
 counts=[0]*4; localrows=0;localfullchecks=0
 # Exact transfer on path state plus phase; entries count component/selector assignments.
 lift=s.eye(4*d)
 for j,g in enumerate(gs):
  ids=wires[j]+wires[(j+1)%M]+[components[j]]+selectors[j]+phases[j]+phases[j+1]
  assert len(ids)==len(set(ids)) # Tests use M>=2.
  width=len(ids); allowed=[];forbidden=[];table=s.zeros(4*d)
  for b in product([0,1],repeat=width):
   off=0;i=val(b[off:off+n]);off+=n;o=val(b[off:off+n]);off+=n
   c=b[off];off+=1;z=val(b[off:off+zbits]);off+=zbits
   p=val(b[off:off+2]);off+=2;pn=val(b[off:off+2])
   a=int(s.im(g[o,i]) if c else s.re(g[o,i]));q=(c+(2 if a<0 else 0))%4
   ok=z<abs(a) and pn==(p+q)%4
   if ok:
    allowed.append(b);table[pn*d+o,p*d+i]+=1
   else:forbidden.append(b)
  # A forbidden-pattern CNF excludes exactly the false local rows. Validate
  # with independent set matching rather than claiming an asymptotic SAT run.
  gateclauses=[tuple(-v if bit else v for v,bit in zip(ids,b)) for b in forbidden]
  for b in allowed:
   aset={v:bit for v,bit in zip(ids,b)}
   assert all(any(aset[abs(l)]==(l>0) for l in cl) for cl in gateclauses)
  for b,cl in zip(forbidden,gateclauses):
   aset={v:bit for v,bit in zip(ids,b)}
   assert not any(aset[abs(l)]==(l>0) for l in cl)
  clauses+=gateclauses;localrows+=len(allowed);localfullchecks+=2**width
  lift=table*lift
 for p in range(4):counts[p]=sum(int(lift[p*d+i,i]) for i in range(d))
 dense=s.eye(d)
 for g in gs:dense=g*dense
 tr=s.simplify(s.trace(dense))
 assert s.simplify(tr-((counts[0]-counts[2])+s.I*(counts[1]-counts[3])))==0
 assert tr>0 and counts[1]==counts[3]
 for phase in [0,2]:
  full=clauses+[[v if bit else -v] for v,bit in zip(phases[-1],bits(phase,2))]
  if write:
   (ROOT/f'{name}_phase{phase}.cnf').write_text('p cnf %d %d\n'%(nextvar-1,len(full))+'\n'.join(' '.join(map(str,c))+' 0' for c in full)+'\n')
 return {'name':name,'qubits':n,'gates':M,'variables':nextvar-1,'clauses_per_count':len(clauses)+2,'local_truth_rows_checked':localfullchecks,'allowed_local_rows':localrows,'exact_phase_counts':counts,'exact_trace':str(tr/den**M),'scope':'Exact local-CNF truth tables and phase-lift elimination; not full released asymptotic SAT solver execution'}

Gx=2*I+X;Gy=2*I+Y;Gz=2*I+Z
# Palindrome equals Q^dagger Q; all local gates are positive definite.
cases=[('one_real_cancellation',[Gx,Gy,Gx,Gx,Gy,Gx]),('one_xz',[Gx,Gz,Gz,Gx]),('one_xyz',[Gx,Gy,Gz,Gz,Gy,Gx]),('two_noncommuting',[2*s.eye(4)+s.kronecker_product(X,X),2*s.eye(4)+s.kronecker_product(Y,I),2*s.eye(4)+s.kronecker_product(Y,I),2*s.eye(4)+s.kronecker_product(X,X)])]
res=[]
for name,gs in cases:
 for g in gs:assert g==g.H and all(l>0 for l in g.eigenvals())
 res.append(compile_and_check(gs,4,name,write=name=='one_xyz'))
(ROOT/'check_signed_cnf.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
