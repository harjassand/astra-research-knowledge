"""Additional adversarial checks; run beside verify_torus.py."""
import runpy
from pathlib import Path
z=runpy.run_path(str(Path(__file__).with_name('verify_torus.py')))
globals().update({k:v for k,v in z.items() if not k.startswith('__')})
rng=np.random.default_rng(8923)
a1=[ai[e] for e in edges];a2=[ai[v] for v in verts];a0=[ai[f] for f in faces]
b1=[bi[e] for e in edges];b2=[bi[f] for f in faces];b0=[bi[v] for v in verts]
da=DA[np.ix_(a2,a1)]; db=DB[np.ix_(b2,b1)]
f1=F[np.ix_(b1,a1)];f2=F[np.ix_(b2,a2)];g1=G[np.ix_(a1,b1)];h2=H[np.ix_(a1,a2)];h1=H[np.ix_(a0,a1)];d0=DA[np.ix_(a1,a0)]
def reps(d):
    piv=pivcols(d); result={}
    for bits in range(1<<len(piv)):
        e=np.zeros(d.shape[1],dtype=np.int64)
        e[piv]=[(bits>>i)&1 for i in range(len(piv))]
        result[tuple(mm(d,e))]=e
    return result
rb=reps(db); ra=reps(da)
# Make the decoder deliberately nonlinear, with arbitrary syndrome-dependent cycles.
for s in list(rb):
    e=rng.integers(0,2,len(b1));cycle=(e+rb[tuple(mm(db,e))])%2
    rb[s]=(rb[s]+cycle)%2
    assert np.array_equal(mm(db,rb[s]),s)
def RB(s):return rb[tuple(s)]
def RA(s):return (mm(g1,RB(mm(f2,s)))+mm(h2,s))%2
count=0; bad_without_h=0
for skey in ra:
    s=np.array(skey)
    assert np.array_equal(mm(da,RA(s)),s)
    bad_without_h+=not np.array_equal(mm(da,mm(g1,RB(mm(f2,s)))),s)
    for j in range(len(a1)):
        e=np.eye(len(a1),dtype=np.int64)[:,j]
        ja=(RA(s)+e+RA((s+mm(da,e))%2))%2
        v=mm(f1,e); fs=mm(f2,s)
        jb=(RB(fs)+v+RB((fs+mm(db,v))%2))%2
        assert np.array_equal(ja,(mm(g1,jb)+mm(d0,mm(h1,e)))%2)
        count+=1
# Explicit degree checks, absent from original script.
at=np.array([2-dim[c] for c in A]);bt=np.array([dim[c] for c in B]);tt=np.array([dim[s]+2-dim[t] for s,t in coords])
for mat,outs,ins,shift in [(F,bt,at,0),(G,at,bt,0),(H,at,at,-1),(K,bt,bt,-1),(ha,tt,tt,-1),(hb,tt,tt,-1)]:
    ii,jj=np.nonzero(mat);assert np.all(outs[ii]==ins[jj]+shift)
print(f'PASS: grading; {count} nonlinear-decoder exact jumps; {len(ra)} valid syndromes.')
print(f'Without H correction decoder fails syndrome correctness on {bad_without_h}/{len(ra)} syndromes.')
