"""Direct single-sided q8 CSS encoder/error/decoder on entangled payload; not bilateral distillation."""
import numpy as np,itertools,json,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'outer_grs_distillation_20261028'/'grs_wrapper_v1.py'
spec=importlib.util.spec_from_file_location('reviewed_grs',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
g=mod.GF(3,0b1011);q=8;J=5;t=1;c=mod.construct(g,J,t);D=q**J
labels=np.array(list(itertools.product(range(q),repeat=J)))
weights=q**np.arange(J-1,-1,-1)
# Build actual Lin(T) permutation independently from row-coordinate definition.
idx=np.array([sum(x*w for x,w in zip(g.rowmul(row.tolist(),c['T']),weights)) for row in labels])
F=np.array([[(-1)**g.trace(g.mul(i,j))/np.sqrt(q) for j in range(q)] for i in range(q)])
F2=np.kron(F,F)
rng=np.random.default_rng(539101);payload=rng.normal(size=(q,2))+1j*rng.normal(size=(q,2));payload/=np.linalg.norm(payload)
initial=np.zeros((q,q,q,q,q,2),complex);initial[0,0,:,0,0,:]=payload
pre=(F2@initial.reshape(q*q,-1)).reshape(D,2)
encoded=np.zeros_like(pre);encoded[idx]=pre
patterns=[]
for site in range(J):
    for e,f in [(v,0) for v in [1,2,4]]+[(0,v) for v in [1,2,4]]+[(3,5)]:
        ev=[0]*J;fv=[0]*J;ev[site]=e;fv[site]=f;patterns.append((ev,fv))
maxerr=0.;maxleak=0.
for e,f in patterns:
    shifted=labels^np.array(e);xidx=shifted@weights
    phase=np.array([(-1)**g.trace(g.dot(f,row.tolist())) for row in labels])
    noisy=np.zeros_like(encoded);noisy[xidx]=phase[:,None]*encoded
    # inverse Lin(T) followed by Fourier on first two registers.
    deLin=noisy[idx]
    decoded=(F2@deLin.reshape(q*q,-1)).reshape(q,q,q,q,q,2)
    ep=g.rowmul(e,c['Ti']);fp=g.rowmul(f,g.transpose(c['T']))
    out=decoded[fp[0],fp[1],:,ep[3],ep[4],:]
    leak=1-np.linalg.norm(out)**2;maxleak=max(maxleak,abs(leak))
    se=[g.dot(row,ep[3:]) for row in c['HRt']];sf=fp[:2]
    eh,ok1=mod.decode_syndrome(g,c,se);fh,ok2=mod.decode_syndrome(g,c,sf)
    assert ok1 and ok2
    # Correct actual middle residual X(ep_hat) Z(fp_hat), inverse order.
    ex=g.rowmul(eh,c['Ti'])[2];fz=g.rowmul(fh,g.transpose(c['T']))[2]
    corrected=np.array([(-1)**g.trace(g.mul(fz,z))*out[z^ex] for z in range(q)])
    overlap=np.vdot(payload,corrected);err=1-abs(overlap)**2;maxerr=max(maxerr,abs(err))
    assert abs(leak)<1e-12 and abs(err)<1e-12
out={'all_assertions_passed':True,'field':8,'J':5,'t':1,'entangled_reference_dimension':2,'actual_direct_circuit_patterns':len(patterns),'max_ancilla_wrong_syndrome_probability':maxleak,'max_corrected_entanglement_infidelity':maxerr,'scope':'direct encoded q8 payload; algebra/decoder functions reused from previously reviewed exact GRS dependency, circuit propagation independently implemented'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
