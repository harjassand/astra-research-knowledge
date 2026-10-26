#!/usr/local/bin/python3
"""Certified arbitrary-reference evaluator for positive rational 3x3 channels.

Numerics propose a certificate and witness; verify.py establishes the interval
by exact rational arithmetic. No hardcoded instance coefficient is used.
"""
import time
_PROCESS_START=time.perf_counter()
import json
import math
import sys
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import eigh
from scipy.optimize import minimize,nnls
from verify import data,mat,serial,psd,upper_check,lower_check,verify


def rat(x,den=10**10): return s.Rational(int(round(float(x)*den)),den)
def ceilrat(x,den=10**10): return s.Rational(int(math.ceil(float(x)*den)),den)
def arr(m):return np.array(m).astype(float)
def mins(bs):return [[str(a[0,0]),str(a[1,1]),str(a.det())] for a in bs]

def scalar_form(a,i):
    b=s.Matrix([[1,0],[0,1],[-1,-1]])
    return b.T*a.T*s.diag(*[1/a[y,i] for y in range(3)])*a*b

def raw_form(a,es):
    af=arr(a);ef=[arr(e) for e in es];d=ef[0].shape[0]
    out=np.zeros((2*d,2*d))
    for row in af:
        da=sum(row[i]*ef[i] for i in range(3))
        v=row[:2]-row[2]
        out+=np.kron(np.outer(v,v),np.linalg.inv(da))
    return (out+out.T)/2

def rational_witness(k,l,es,vec):
    d=es[0].rows
    vec=np.array(vec,float);vec/=max(abs(vec))
    hs=[s.Matrix([rat(v,10**9) for v in vec[j*d:(j+1)*d]]) for j in range(2)]
    hs.append(-hs[0]-hs[1])
    return {'effects_unnormalized':[serial(e) for e in es],
            'vectors_unnormalized':[[str(a) for a in h] for h in hs],
            'dimension':d,
            'interpretation':'Q_i=G^(-1/2) E_i G^(-1/2), u_i=G^(-1/2) h_i; G=sum E_i'}

def sqrt_bracket(q,den=10**10):
    """Exact enclosure of a rational square root, width <=1/den."""
    q=s.Rational(q);assert q>=0
    n=math.isqrt((int(q.p)*den*den)//int(q.q))
    lo=s.Rational(n,den)
    hi=lo if n*n*int(q.q)==int(q.p)*den*den else s.Rational(n+1,den)
    return lo,hi

def eigen_bracket(fk,fl):
    tau=s.trace(fl.inv()*fk);sigma=fk.det()/fl.det()
    dl,du=sqrt_bracket(tau*tau-4*sigma)
    return (tau+dl)/2,(tau+du)/2

def vertex_witnesses(case,k,l):
    out=[]
    for i in range(3):
        fk,fl=scalar_form(k,i),scalar_form(l,i)
        rl,ru=eigen_bracket(fk,fl)
        a=fk-rl*fl
        if a[0,0]>=0:h=s.Matrix([1,0])
        elif a[1,1]>=0:h=s.Matrix([0,1])
        else:
            assert a.det()<=0
            h=s.Matrix([a[0,1],-a[0,0]])
        assert (h.T*a*h)[0]>=0
        hs=[s.Matrix([h[0]]),s.Matrix([h[1]]),s.Matrix([-sum(h)])]
        es=[s.Matrix([[int(i==j)]]) for j in range(3)]
        w={'effects_unnormalized':[serial(e) for e in es],
           'vectors_unnormalized':[[str(v) for v in h] for h in hs],
           'dimension':1,'closure_witness':True,
           'interpretation':'deterministic scalar effects; uniform-positive-output closure'}
        low,*_=lower_check(case,w)
        out.append((low,w,ru))
    return out

def vertex_upper(case,rguess):
    c=max(s.Rational(1),s.Rational(rguess))
    cert={'regime':'vertex','c':str(c)}
    _,bs=upper_check(case,cert);cert['principal_minors']=mins(bs)
    return cert

def subunit_proposal(x,ti,si,rvertex):
    xf=np.array([arr(v).ravel() for v in x]);tf=np.array([arr(v) for v in ti]);sf=np.array([arr(v) for v in si])
    def lm(v,i):
        c=v[0];a=v[1:];xi=xf[i]
        return np.block([[c*np.diag(xi)-sf[i]-np.outer(xi,xi)+np.outer(a,xi)+np.outer(xi,a),a[:,None]],
                         [a[None,:],np.array([[1-c]])]])
    def con(v): return np.array([eigh(lm(v,i),eigvals_only=True)[0] for i in range(3)])
    def jac(v):
        rows=[]
        for i in range(3):
            w=eigh(lm(v,i))[1][:,0];b=w[:2];d=w[2]
            rows.append([b@np.diag(xf[i])@b-d*d,*(2*b*(xf[i]@b+d))])
        return np.array(rows)
    c0=1-1e-5
    start=np.array([c0,*((1-c0)*xf.mean(axis=0))])
    fit=minimize(lambda v:v[0],start,jac=lambda v:np.array([1.,0.,0.]),method='SLSQP',
       bounds=[(max(0,rvertex-1e-8),1-1e-12),(None,None),(None,None)],
       constraints=[{'type':'ineq','fun':con,'jac':jac}],
       options={'ftol':1e-13,'maxiter':500})
    c=float(fit.x[0]);z=fit.x[1:]/(1-c)
    bs=[c*tf[i]-sf[i]-(1-c)*np.outer(z-xf[i],z-xf[i]) for i in range(3)]
    vals=[];vs=[]
    for b in bs:
        ev,v=eigh(b);vals.append(float(ev[0]));vs.append(v[:,0])
    # Complementary primal Gram effects. Inactive constraints receive no weight.
    scale=max(1,max(np.linalg.norm(b,2) for b in bs))
    active=[i for i,v in enumerate(vals) if v<=1e-7*scale]
    if not active:active=list(range(3))
    candidates=[]
    for ids in [active,list(range(3))]:
        columns=np.array([np.outer(vs[i],vs[i])@(xf[i]-z) for i in ids]).T
        cm=np.vstack([columns,np.ones(len(ids))])
        weights,resid=nnls(cm,np.array([0.,0.,1.]),maxiter=1000)
        alpha=np.zeros(3);alpha[ids]=weights
        candidates.append((alpha,float(resid)))
    diag={'optimizer_success':bool(fit.success),'message':str(fit.message),'iterations':int(fit.nit),
          'proposed_c':c,'proposed_z':z.tolist(),'LMI_min_eigenvalues':con(fit.x).tolist(),
          'B_min_eigenvalues':vals,'primal_stationarity_residuals':[r for _,r in candidates]}
    return c,z,vs,candidates,diag

def evaluate(case):
    start=time.perf_counter();k,l,x,ti,si=data(case)
    vertices=vertex_witnesses(case,k,l)
    low,witness,_=max(vertices,key=lambda row:row[0])
    rg_exact=max(row[2] for row in vertices)
    rg=float(rg_exact)
    cert=vertex_upper(case,max(1,rg_exact))
    diagnostics={'vertex_numeric_max':rg,'method':'three-LMI covariance certificate',
                 'trusted_numeric_optimization':False}
    if all(k[:,i]==k[:,0] for i in range(1,3)):
        cert={'regime':'constant','c':'0'}
    elif rg<1-1e-8:
        try:
            cnum,znum,vs,candidates,diag=subunit_proposal(x,ti,si,rg)
            diagnostics['subunit']=diag
            zr=[rat(v) for v in znum]
            margin=1e-8
            for _ in range(10):
                cup=ceilrat(cnum+margin)
                if cup>=1:break
                trial={'regime':'subunit','c':str(cup),'z':[str(v) for v in zr]}
                try:
                    _,bs=upper_check(case,trial);trial['principal_minors']=mins(bs)
                    cert=trial;break
                except AssertionError:margin*=10
            for alpha,resid in candidates:
                for reg in [s.Rational(1,10**5),s.Rational(1,10**7),s.Rational(1,10**9)]:
                    es=[]
                    for a,v in zip(alpha,vs):
                        vr=s.Matrix([rat(y,10**8) for y in v]);ar=max(s.Rational(0),rat(a,10**10))
                        es.append(ar*vr*vr.T+reg*s.eye(2))
                    try:
                        vals,vec=eigh(raw_form(k,es),raw_form(l,es))
                        trialw=rational_witness(k,l,es,vec[:,-1]);lb,*_=lower_check(case,trialw)
                        if lb>low:low,witness=lb,trialw
                    except (ValueError,np.linalg.LinAlgError):pass
        except (ValueError,np.linalg.LinAlgError,RuntimeError) as exc:
            diagnostics['subunit_failure']=repr(exc)
    up=s.Rational(cert['c'])
    result={'id':case.get('id'),'lower':str(low),'upper':str(up),
            'lower_float':float(low),'upper_float':float(up),'width':float(up-low),
            'upper_certificate':cert,'lower_witness':witness,'diagnostics':diagnostics,
            'evaluation_seconds_excluding_module_import':time.perf_counter()-start}
    result['verification']=verify(case,result)
    return result

if __name__=='__main__':
    inp=json.loads(Path(sys.argv[1]).read_text())
    if 'cases' in inp:out={'results':[evaluate(case) for case in inp['cases']]}
    else:out=evaluate(inp)
    out['process_seconds_including_imports']=time.perf_counter()-_PROCESS_START
    if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n')
    if 'results' in out:
        print(json.dumps({'results':[{k:r[k] for k in ['id','lower_float','upper_float','width']} for r in out['results']],
                          'process_seconds_including_imports':out['process_seconds_including_imports']},indent=2))
    else:
        print(json.dumps({k:out[k] for k in ['id','lower_float','upper_float','width','process_seconds_including_imports']},indent=2))
