"""Bounded numerical checks of unequal-word truncation and both EB anchors.

The positive terms of the analytic EB-order decompositions are checked
separately. The maps need not be PPT: these lemmas hold for arbitrary
bistochastic CP maps. This is not a test of the universal word theorem.
"""
from pathlib import Path
import json
import numpy as np

rng=np.random.default_rng(20261009)
tol=2e-10

def unitary(d):
    a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    q,r=np.linalg.qr(a)
    return q @ np.diag(np.diag(r)/np.abs(np.diag(r)))
def h(x):return (x+x.conj().T)/2
def cn(ks):return sum(np.outer(k.ravel(),k.ravel().conj()) for k in ks)
def sp(j,d):return j.reshape(d,d,d,d).transpose(0,2,1,3).reshape(d*d,d*d)
def cj(s,d):return s.reshape(d,d,d,d).transpose(0,2,1,3).reshape(d*d,d*d)
def psd(x):return float(np.linalg.eigvalsh(h(x)).min())
def effect(ks):return sum(k.conj().T@k for k in ks)
def output(ks):return sum(k@k.conj().T for k in ks)
def apply(s,x):return (s@x.ravel()).reshape(x.shape)
def trunct(k):
    u,s,vh=np.linalg.svd(k)
    return s[0]*np.outer(u[:,0],vh[0,:])
def wedge(k):
    s=np.linalg.svd(k,compute_uv=False)
    return float(s[0]*s[1])
def family(d,t):
    u,v=unitary(d),unitary(d)
    return [np.sqrt(1-t)*np.outer(u[:,i],v[:,i].conj()) for i in range(d)]+[np.sqrt(t)*unitary(d)]

rows=[]
for d in [2,3,4]:
  for ts in [[.02,.06],[.05,.01,.03],[.08,.04,.01]]:
    maps=[family(d,t) for t in ts]
    words=[np.eye(d,dtype=complex)]
    product=np.eye(d*d,dtype=complex)
    bprod=1.0
    for ks in maps:
      assert np.linalg.norm(effect(ks)-np.eye(d))<tol
      assert np.linalg.norm(output(ks)-np.eye(d))<tol
      bprod*=sum(wedge(k) for k in ks)
      words=[k@a for k in ks for a in words]
      product=sp(cn(ks),d)@product
    ls=[trunct(w) for w in words]
    e=sp(cn(ls),d);delta=float(np.linalg.norm(product-e))
    bound=np.sqrt(d*d-1)*bprod
    assert delta<=bound+tol
    ei=output(ls);esi=effect(ls)
    assert psd(ei-np.eye(d)/2)>-tol
    assert psd(esi-np.eye(d)/2)>-tol
    # Anchor has the exact strict-output margin f=a/d.
    a=.6;u=unitary(d);f=a/d
    anchor=(1-a)*np.kron(u,u.conj())+a*np.outer(np.eye(d).ravel(),np.eye(d).ravel())/d
    left=np.zeros((d*d,d*d),complex)
    right=np.zeros_like(left)
    min_term=1.0
    for l in ls:
      s2=float(np.linalg.norm(l)**2)
      if s2<1e-28:continue
      sigma=l@l.conj().T/s2
      F=l.conj().T@l
      al=apply(anchor,sigma)-f*np.eye(d)
      ar=apply(anchor.conj().T,F)-f*np.trace(F)*np.eye(d)
      min_term=min(min_term,psd(al),psd(ar))
      assert psd(al)>=-tol and psd(ar)>=-tol
      left+=np.kron(al,F.T)
      right+=np.kron(sigma,ar.T)
    left+=f*np.kron(np.eye(d),(esi-np.eye(d)/2).T)
    right+=f*np.kron(ei-np.eye(d)/2,np.eye(d))
    jleft=cj(anchor@e,d)-f*np.eye(d*d)/2
    jright=cj(e@anchor,d)-f*np.eye(d*d)/2
    assert np.linalg.norm(left-jleft)<tol
    assert np.linalg.norm(right-jright)<tol
    errleft=float(np.linalg.norm(anchor@(product-e)))
    errright=float(np.linalg.norm((product-e)@anchor))
    assert errleft<=delta+tol and errright<=delta+tol
    rows.append({'d':d,'mixing_parameters':ts,'kraus_words':len(words),
      'delta':delta,'wedge_bound':float(bound),'ratio':delta/bound,
      'left_error':errleft,'right_error':errright,'minimum_positive_term':min_term,
      'anchor_margin':f,'all_checks_pass':True})
res={'status':'PASS','seed':20261009,'absolute_tolerance':tol,'cases':rows,
 'scope':'Bounded floating-point checks of unequal-word truncation, both explicit positive Holevo-margin decompositions and bistochastic error contraction. No Lojasiewicz exponent, full theorem or priority certified.'}
Path(__file__).with_name('bistochastic_anchor_verification.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'status':'PASS','cases':len(rows),'kraus_words':sum(r['kraus_words'] for r in rows),'max_ratio':max(r['ratio'] for r in rows)}))
