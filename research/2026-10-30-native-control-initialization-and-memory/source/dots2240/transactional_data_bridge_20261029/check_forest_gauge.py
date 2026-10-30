"""Numerical nonpermutation regression accompanying the analytic forest-gauge proof."""
import contextlib,io,runpy,json
from pathlib import Path
import numpy as np
with contextlib.redirect_stdout(io.StringIO()):
    a=runpy.run_path(str(Path(__file__).with_name('check_transactional_flags.py')))
supports=a['supports'];targets=a['gate_targets'];lengths=a['lengths']
I=np.eye(32);H=np.array([[1,1],[1,-1]])/np.sqrt(2)
def one(q,u):
    out=np.array([[1.]])
    for j in range(5):out=np.kron(out,u if j==q else np.eye(2))
    return out
def cx(c,t):
    out=np.zeros((32,32))
    for j in range(32):
        k=j ^ (1<<(4-t)) if j&(1<<(4-c)) else j
        out[k,j]=1
    return out
# Each gate really acts on its declared target and its private workspace.
U={(0,0):cx(0,2)@one(0,H),(0,1):cx(3,0),(0,2):cx(0,2),
   (1,0):cx(1,3)@one(1,H),(1,1):cx(4,1)}
cache={};mats=[]
def frame_key(h,p,ls):
    if p[0]=='R':p=p[1]
    if p[0]!='C':return ()
    seq=[]
    for t in range(p[1]):
        if ls[targets[h][t]]==f'o{h}':seq.append(t)
        else:seq=[]
    return tuple(seq)
def frame(h,key):
    v=I
    for t in key:v=U[h,t]@v
    return v
def globalkey(s):return tuple(frame_key(h,p,s[1]) for h,p in enumerate(s[0]))
def glob(key):
    if key not in cache:
        x,y=(frame(h,key[h]) for h in range(2))
        assert np.allclose(x@y,y@x,atol=1e-12)
        cache[key]=x@y
    return cache[key]
seen=set();maxerr=0.;checks=0
for ps,ls in a['states']:
    s=(ps,ls);b=globalkey(s)
    for ss,kind,coherent in a['transitions'](s):
        if not coherent:continue
        d=globalkey(ss);payload=None
        if kind in ('gate','ungate'):
            h=next(h for h in range(2) if ps[h]!=ss[0][h]);t=min(ps[h][1],ss[0][h][1]);payload=(h,t,kind)
        key=(b,d,payload)
        if key in seen:continue
        seen.add(key);op=I if payload is None else U[h,t] if kind=='gate' else U[h,t].T
        err=float(np.max(np.abs(glob(d).T@op@glob(b)-I)));maxerr=max(maxerr,err)
        assert err<1e-12,(s,ss,kind,err)
        checks+=1
# Independently check transformed terminal/abort reset Kraus and summed loss.
reset_checks=0
for key,v in cache.items():
    for h in range(2):
        vh=frame(h,key[h]);other=frame(1-h,key[1-h]);loss=np.zeros((32,32))
        for ss in range(2):
            r=one(h,np.array([[1,0],[0,0]]) if ss==0 else np.array([[0,1],[0,0]]))
            transformed=other.T@r@v
            expected=r@vh
            assert np.allclose(transformed,expected,atol=1e-12)
            loss+=transformed.T@transformed
            reset_checks+=1
        assert np.allclose(loss,I,atol=1e-12)
out={'scope':'Nonpermutation matrix regression, not substitute for general block proof',
     'payload_qubits':5,'arbitrary_clock_states':len(a['states']),
     'distinct_global_frame_types':len(cache),'distinct_H_conjugacy_checks':checks,
     'reset_kraus_checks':reset_checks,'max_H_identity_error':maxerr,
     'all_global_frame_factors_commute':True,'all_bundled_reset_losses_identity':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
