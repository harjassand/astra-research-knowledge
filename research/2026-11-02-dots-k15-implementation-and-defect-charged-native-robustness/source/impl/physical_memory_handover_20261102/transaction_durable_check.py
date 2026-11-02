"""Finite availability checker, with durable epoch/output records kept distinct.
This is NOT an autonomous concatenation or controller threshold proof.
"""
import itertools,json
from pathlib import Path
import numpy as np

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
    # A durable commitment is never rolled back. A conflicting/corrupted
    # ledger is not evidence that an already committed payload is workspace.
    if st['owner']==i and j>0 and st['active'][i]!=st['last'][i]:
        st['op']=U[j-1].conj().T@st['op'];st['j'][i]-=1
    else:st['j'][i]=0

def clear(st,i):
    if st['mode'][i]=='backward' and st['j'][i]==0:
        if st['owner']==i:st['owner']=None
        st['mode'][i]='idle';st['active'][i]=None
        # Crucially: do not change last, output, or caller's request.

def acquire(st,i):
    if (st['owner'] is None and st['request'][i] is not None
        and st['request'][i]!=st['last'][i]):
        st['owner']=i;st['mode'][i]='forward';st['j'][i]=0
        st['active'][i]=st['request'][i]

def forward(st,i):
    if (st['owner']==i and st['mode'][i]=='forward' and st['j'][i]<d
        and st['active'][i] is not None and st['active'][i]!=st['last'][i]):
        st['op']=U[st['j'][i]]@st['op'];st['j'][i]+=1

def commit(st,i):
    if (st['owner']==i and st['mode'][i]=='forward' and st['j'][i]==d
        and st['active'][i] is not None and st['active'][i]!=st['last'][i]):
        st['last'][i]=st['active'][i]
        st['output'][i]=('new',st['active'][i])
        st['owner']=None;st['mode'][i]='idle';st['j'][i]=0
        st['active'][i]=None;st['commits'][i]+=1

def clear_all(st):
    old=(list(st['last']),list(st['output']),list(st['request']))
    for i in [0,1]:
        abort(st,i)
        for _ in range(d):reverse(st,i)
        clear(st,i)
    assert old==(st['last'],st['output'],st['request'])
    assert st['owner'] is None

def word(st):
    clear_all(st)
    acquire(st,0)
    for _ in range(d):forward(st,0)
    commit(st,0)

def state(owner,mode,j,active,last,request):
    return dict(owner=owner,mode=list(mode),j=list(j),active=list(active),
        last=list(last),request=list(request),output=[('old',0),('old',1)],
        op=np.eye(2,dtype=complex),commits=[0,0])

tested=0
fresh=0
stale_or_absent=0
# Two epoch values suffice only for this bounded one-outstanding local port.
# Global wraparound, reliable request generation, and stale remote packets are
# NOT certified by this model.
for owner in [None,0,1]:
 for ma,mb,ja,jb in itertools.product(modes,modes,range(d+1),range(d+1)):
  for aa,ab,la,lb,ra in itertools.product([None,0,1],[None,0,1],[0,1],[0,1],[None,0,1]):
    st=state(owner,[ma,mb],[ja,jb],[aa,ab],[la,lb],[ra,None])
    expected=int(ra is not None and ra!=la)
    word(st)
    assert st['owner'] is None and st['commits']==[expected,0]
    assert st['last'][1]==lb and st['output'][1]==('old',1)
    if expected:
        assert st['last'][0]==ra and st['output'][0]==('new',ra)
        fresh+=1
    else:
        assert st['last'][0]==la and st['output'][0]==('old',0)
        stale_or_absent+=1
    # Repeating the entire successful word is harmless: durable record blocks replay.
    old_commits=list(st['commits']); old_output=list(st['output']); oldop=st['op'].copy()
    word(st)
    assert st['commits']==old_commits and st['output']==old_output
    assert np.linalg.norm(st['op']-oldop)<1e-12
    tested+=1
restore_error=0.
for j in range(d+1):
    pref=np.eye(2,dtype=complex)
    for k in range(j):pref=U[k]@pref
    st=state(0,['forward','idle'],[j,0],[1,None],[0,0],[1,None]);st['op']=pref
    clear_all(st)
    restore_error=max(restore_error,float(np.linalg.norm(st['op']-np.eye(2),2)))
assert restore_error<1e-12
# Honest completed irreversible action followed by arbitrary number of clearing
# words preserves the persistent output. No reexecution is authorized.
st=state(None,['idle','idle'],[0,0],[None,None],[1,0],[1,None])
st['output'][0]=('committed_measurement_record', '11')
for _ in range(10):word(st)
assert st['output'][0]==('committed_measurement_record','11') and st['commits']==[0,0]
result=dict(primitive_stages=d,arbitrary_lock_ledger_durable_states_checked=tested,
 fresh_requests_committed_once=fresh,already_committed_or_absent_requests_not_reissued=stale_or_absent,
 repeated_word_replay_preventions=tested,maximum_honest_abort_unitary_error=restore_error,
 scope='Private availability, durable record retention, one-outstanding local replay guard, clean-prefix rollback. No global wraparound, encoded request generation, recursive FT controller, or physical contact compilation.')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
