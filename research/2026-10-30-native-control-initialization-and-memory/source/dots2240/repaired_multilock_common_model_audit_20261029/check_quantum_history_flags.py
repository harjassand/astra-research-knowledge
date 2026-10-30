"""Exact dyadic matrix checks over ALL corrupted-clock configurations.
Includes non-permutation Hadamard prefixes; no floating eigentolerance proof.
"""
import importlib.util,numpy as np,json,hashlib
from pathlib import Path
from functools import reduce
P=Path(__file__);spec=importlib.util.spec_from_file_location('c',P.with_name('check_all_clock_flags.py'));c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
kron=lambda xs:reduce(np.kron,xs)
I2=np.eye(2);X=np.array([[0,1],[1,0]]);Hscaled=np.array([[1,1],[1,-1]])
I=np.eye(32)
def local(a,j):return kron([a if i==j else I2 for i in range(5)])
def perm(fn):
 M=np.zeros((32,32))
 for j in range(32):M[fn(j),j]=1
 return M
# Tensor factor j uses bit4-j.
def bit(x,j):return(x>>(4-j))&1
def swap(x,j,k):return x^((bit(x,j)^bit(x,k))<<(4-j))^((bit(x,j)^bit(x,k))<<(4-k))
# h0: Hwork, controlled-X on shared data1, Hwork => X measurement.
# h1: swap shared data1 into workspace, Xdata2 => reset+X.
Us=[[(local(Hscaled,3),2),(perm(lambda x:x^(bit(x,3)<<(4-1))),1),(local(Hscaled,3),2)],
    [(perm(lambda x:swap(x,1,4)),1),(local(X,2),1)]]
clean=[]
for h in range(2):
 p=local(np.diag([1,0]),3+h);hist=[p]
 for U,scale2 in Us[h]:p=U@p@U.T/scale2;hist.append(p)
 for p in hist:assert np.array_equal(p@p,p)
 clean.append(hist)
def kinds(s):
 ps,ls=s;out=[]
 for h,p in enumerate(ps):
    out.append('bad' if c.flag(h,p,ls) else ('G',p[1]) if p[0]=='G' else 'idle')
 return tuple(out)
def Bs(ks):return [I if q=='bad' else I-clean[h][q[1] if isinstance(q,tuple) else 0] for h,q in enumerate(ks)]
Kreset=[[local(np.array([[1,0],[0,0]]),3+h),local(np.array([[0,1],[0,0]]),3+h)] for h in range(2)]
hsign=set();rsign=set();statesig=set()
for ps,ls in c.states:
 s=(ps,ls);ks=kinds(s);statesig.add(ks)
 for ss,kind,coherent in c.transitions(s):
    kk=kinds(ss)
    if coherent:
        gateid=None
        if kind in ['gate','ungate']:
            h=next(i for i in range(2) if ps[i]!=ss[0][i]);p=ps[h];t=0 if p[0]=='A' else p[1]
            gateid=(h,t if kind=='gate' else t-1)
        hsign.add((ks,kk,gateid))
    else:
        h=next((i for i in range(2) if ps[i]!=ss[0][i]),None)
        rsign.add((ks,kk,h))
 for h,p in enumerate(ps):
    if p[0] in ['A','Q']:rsign.add((ks,ks,h)) # phase-preserving complete workspace reset
for ks in statesig:
 b=Bs(ks);assert np.array_equal(b[0]@b[1],b[1]@b[0])
for ks,kk,gateid in hsign:
 U=I if gateid is None else Us[gateid[0]][gateid[1]][0]
 for b,d in zip(Bs(ks),Bs(kk)):assert np.array_equal(d@U,U@b),(ks,kk,gateid)
resetchecks=0
for ks,kk,h in rsign:
 before=Bs(ks);after=Bs(kk);K=[I] if h is None else Kreset[h]
 for subset in [(0,),(1,),(0,1)]:
    B=reduce(np.matmul,(before[j] for j in subset),I);D=reduce(np.matmul,(after[j] for j in subset),I)
    # Exact range inclusion plus sumK†K=I implies sumK†D K <= B.
    for k in K:assert np.array_equal(D@k@(I-B),np.zeros((32,32))),(ks,kk,h,subset)
    assert np.array_equal(sum(k.T@k for k in K),I)
    resetchecks+=1
out={'scope':'Exact dyadic block matrix identities, arbitrary corrupted clocks; non-permutation history prefixes included',
'underlying_clock_states':len(c.states),'history_flag_block_types':len(statesig),'distinct_H_intertwining_types':len(hsign),
'distinct_reset_types':len(rsign),'joint_reset_range_checks':resetchecks,'all_flags_commute':True,
'all_H_preserve_history_flags':True,'all_reset_joint_products_only_decrease':True,
'workspace_refresh_in_A_Q':'complete label-resolved one-site reset instrument including s=0',
'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest()}
P.with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
