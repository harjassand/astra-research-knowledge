import itertools,json
from pathlib import Path
import numpy as np
# One shared payload; two conflicting modules. All finite lock/ledger states tested.
d=3
modes=['idle','forward','backward']
H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
T=np.diag([1,np.exp(1j*np.pi/4)])
X=np.array([[0,1],[1,0]],complex)
U=[H,T,X]

def abort(st,i):
    st['mode'][i]='backward'

def reverse(st,i):
    if st['mode'][i]!='backward':return
    j=st['j'][i]
    if st['owner']==i and j>0:
        st['op']=U[j-1].conj().T@st['op'];st['j'][i]-=1
    else:st['j'][i]=0

def clear(st,i):
    if st['mode'][i]=='backward' and st['j'][i]==0:
        if st['owner']==i:st['owner']=None
        st['mode'][i]='idle'

def acquire(st,i):
    if st['owner'] is None:
        st['owner']=i;st['mode'][i]='forward';st['j'][i]=0

def forward(st,i):
    if st['owner']==i and st['mode'][i]=='forward' and st['j'][i]<d:
        st['op']=U[st['j'][i]]@st['op'];st['j'][i]+=1

def commit(st,i):
    if st['owner']==i and st['mode'][i]=='forward' and st['j'][i]==d:
        st['owner']=None;st['mode'][i]='idle';st['commits'][i]+=1

def word(st):
    for i in [0,1]:
        abort(st,i)
        for _ in range(d):reverse(st,i)
        clear(st,i)
    acquire(st,0)
    for _ in range(d):forward(st,0)
    commit(st,0)

tested=0
for owner in [None,0,1]:
 for ma,mb,ja,jb in itertools.product(modes,modes,range(d+1),range(d+1)):
    st={'owner':owner,'mode':[ma,mb],'j':[ja,jb],'op':np.eye(2,dtype=complex),'commits':[0,0]}
    word(st)
    assert st['owner'] is None and st['commits']==[1,0]
    tested+=1
# Honest abort restores arbitrary/reference-entangled input: check total unitary.
restore_error=0.
for j in range(d+1):
    pref=np.eye(2,dtype=complex)
    for k in range(j):pref=U[k]@pref
    st={'owner':0,'mode':['forward','idle'],'j':[j,0],'op':pref,'commits':[0,0]}
    abort(st,0)
    for _ in range(d):reverse(st,0)
    clear(st,0)
    restore_error=max(restore_error,float(np.linalg.norm(st['op']-np.eye(2),2)))
assert restore_error<1e-12
result={'primitive_stages':d,'arbitrary_lock_ledger_states_checked':tested,'clearing_acquisition_commit_successes':tested,'maximum_honest_abort_unitary_error':restore_error,'scope':'Finite one-resource two-module private availability and clean-prefix rollback only. No global epoch causality, recursive FT controller, or physical contact implementation is inferred.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
