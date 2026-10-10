"""Bounded checks for UNIFORM_APPROXIMATE_PPT_WORDS.md.

Numerical determinant multiplicativity and Stinespring bounds; exact
rational effect preservation in backwards normalization. No universal
contraction constant or asymptotic theorem is numerically certified.
"""
from pathlib import Path
import json
import numpy as np
import sympy as s

rng=np.random.default_rng(418271)
tol=3e-10

def herm(a):return (a+a.conj().T)/2
def effect(ks):return sum(k.conj().T@k for k in ks)
def choi(ks):return sum(np.outer(k.ravel(),k.ravel().conj()) for k in ks)
def pt(j,d):return j.reshape(d,d,d,d).transpose(0,3,2,1).reshape(d*d,d*d)
def apply(ks,x):return sum(k@x@k.conj().T for k in ks)
def bweight(ks,d):return float(sum(abs(np.linalg.det(k))**(2/d) for k in ks))
def fourier(d):return np.exp(2j*np.pi*np.outer(np.arange(d),np.arange(d))/d)/np.sqrt(d)
def channel(d,t):
    weights=np.arange(d,0,-1,dtype=float);weights/=weights.sum()
    ks=[]
    for a in range(d):
        for b in range(d):
            k=np.zeros((d,d),complex);k[a,b]=np.sqrt((1-t)*weights[a]);ks.append(k)
    ks.append(np.sqrt(t)*fourier(d))
    assert np.linalg.norm(effect(ks)-np.eye(d))<tol
    assert np.linalg.norm(apply(ks,np.eye(d))-np.eye(d))>1e-2
    assert np.linalg.eigvalsh(herm(pt(choi(ks),d))).min()>0
    return ks

rows=[]
for d in [2,3,4]:
  for ts in [[.02,.03],[.025,.04,.015]]:
    words=[np.eye(d,dtype=complex)];expected=1.0
    for t in ts:
      ks=channel(d,t);expected*=bweight(ks,d)
      words=[k@a for k in ks for a in words]
    actual=bweight(words,d)
    assert abs(actual-expected)<tol
    ls=[];rs=[]
    for a in words:
      u,sv,vh=np.linalg.svd(a)
      l=(u[:,:-1]*sv[:-1])@vh[:-1,:]
      ls.append(l);rs.append(a-l)
      assert np.linalg.eigvalsh(herm(a.conj().T@a-l.conj().T@l)).min()>-tol
    defect=float(np.linalg.norm(effect(rs),2))
    assert defect<=actual+tol
    assert np.linalg.eigvalsh(herm(np.eye(d)-effect(ls))).min()>-tol
    bound=2*np.sqrt(actual)
    max_probe=0.0
    # Probe trace-distance comparison after a full d-dimensional ancilla.
    for z in range(6):
      psi=rng.normal(size=d*d)+1j*rng.normal(size=d*d);psi/=np.linalg.norm(psi)
      rho=np.outer(psi,psi.conj())
      diff=sum(np.kron(k,np.eye(d))@rho@np.kron(k,np.eye(d)).conj().T for k in words)
      diff-=sum(np.kron(k,np.eye(d))@rho@np.kron(k,np.eye(d)).conj().T for k in ls)
      val=float(np.linalg.svd(diff,compute_uv=False).sum())
      assert val<=bound+tol
      max_probe=max(max_probe,val)
    rows.append({'d':d,'parameters':ts,'word_count':len(words),
      'determinant_weight':actual,'product_weight':expected,'stinespring_defect_squared':defect,
      'diamond_upper_bound':bound,'max_ancilla_probe_trace_distance':max_probe})

# Classical CP maps have A(X)=diag(C diag(X)); column sums need not be one.
Cs=[s.Matrix([[s.Rational(1,2),s.Rational(1,5)],[s.Rational(1,7),s.Rational(2,3)]]),
    s.Matrix([[s.Rational(2,5),s.Rational(1,3)],[s.Rational(1,4),s.Rational(3,5)]]),
    s.Matrix([[s.Rational(3,4),s.Rational(2,7)],[s.Rational(1,6),s.Rational(1,2)]])]
y=[None]*4;y[3]=s.ones(2,1)
for j in reversed(range(3)):y[j]=Cs[j].T*y[j+1]
Ds=[]
for j,C in enumerate(Cs):
    D=s.diag(*y[j+1])*C*s.diag(*(1/x for x in y[j]))
    assert s.ones(1,2)*D==s.ones(1,2)
    Ds.append(D)
T=Cs[2]*Cs[1]*Cs[0];Theta=Ds[2]*Ds[1]*Ds[0]
assert Theta*s.diag(*y[0])==T
B=s.Matrix([[1,s.Rational(1,3),0],[0,s.Rational(1,4),s.Rational(1,2)]])
input_effect=B.T*s.diag(*y[0])*B
Z=s.Matrix([[s.Rational(2,5),s.Rational(2,5)],[s.Rational(3,5),s.Rational(3,5)]])
assert s.ones(1,2)*Z==s.ones(1,2)
# Both the actual branch and its reset replacement have this exact effect.
assert s.diag(*(list((s.ones(1,2)*T))))==s.diag(*y[0])
assert s.diag(*(list(s.ones(1,2)*Z*s.diag(*y[0]))))==s.diag(*y[0])
assert input_effect.is_positive_semidefinite

result={'status':'PASS','seed':418271,'absolute_tolerance':tol,'numerical_cases':rows,
 'exact_normalization':{'arithmetic':'SymPy rational','ppt_cp_factors':3,
   'input_dimension':3,'compressed_dimension':2,'all_normalized_factors_TP':True,
   'telescoping_identity':True,'effect_preservation':True,
   'effect_matrix':[[str(v) for v in row] for row in input_effect.tolist()]},
 'scope':'Bounded algebraic/numerical checks, including 36 full-ancilla probes. Probe checks are not diamond-norm optimization or proof of the universal theorem.'}
Path(__file__).with_name('determinant_and_effect_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','cases':len(rows),'kraus_words':sum(row['word_count'] for row in rows),
'exact_effect_preservation':True}))
