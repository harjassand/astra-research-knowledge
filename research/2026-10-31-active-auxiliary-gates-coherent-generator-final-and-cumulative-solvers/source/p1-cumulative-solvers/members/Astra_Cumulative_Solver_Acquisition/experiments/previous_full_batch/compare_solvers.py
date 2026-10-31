"""Floating diagnostic: paid acquisition plus later solves, equal source access.

The two retained methods use the SAME confidence-rule spectral test and the
SAME affine cache.  The established Gaussian-sketch comparator is allowed to
retain everything and double its sketch.  Cold CG and retained full tomography
are also compared.  Binary64 diagnostics do not implement interval certification.
"""
import json
import math
import os
from pathlib import Path
import time
import numpy as np
from scipy.linalg import cho_factor, cho_solve


class Source:
    def __init__(self, u, hs, tails):
        self._u, self._hs, self._tails = u, hs, tails
        self.n, self.m = u.shape[0], len(hs)
        self.counts = {"cache":0,"certificate":0,"solve":0,"tomography":0}
        self.coordinate_outputs = 0
        self.source_seconds = 0.

    def apply(self, j, x, category):
        columns = 1 if x.ndim==1 else x.shape[1]
        self.counts[category] += columns
        self.coordinate_outputs += self.n*columns
        t=time.perf_counter()
        y=self._u@(self._hs[j]@(self._u.T@x))+self._tails[j]*x
        self.source_seconds+=time.perf_counter()-t
        return y

    def combined(self, theta, x, category):
        y=np.zeros_like(x)
        for j,a in enumerate(theta):
            if a:
                y+=a*self.apply(j,x,category)
        return y


class Retained:
    def __init__(self,source):
        self.source=source
        self.q=np.empty((source.n,0))
        self.cache=[np.empty((source.n,0)) for _ in range(source.m)]
        self.stages=[]
        self.assembly_seconds=0.
        self.application_seconds=0.

    def append(self,v):
        if v.ndim==1:
            v=v[:,None]
        # Two reorthogonalizations are only a numerical implementation aid.
        for _ in range(2):
            v-=self.q@(self.q.T@v)
        q,r=np.linalg.qr(v,mode="reduced")
        keep=np.abs(np.diag(r))>1e-12*np.maximum(1.,np.linalg.norm(v,axis=0))
        q=q[:,keep]
        if q.shape[1]==0:
            raise RuntimeError("A rejected certificate failed to add a floating direction")
        for j in range(self.source.m):
            self.cache[j]=np.column_stack((self.cache[j],self.source.apply(j,q,"cache")))
        self.q=np.column_stack((self.q,q))

    def build(self,theta,lam):
        start=time.perf_counter()
        y=sum((a*z for a,z in zip(theta,self.cache)),start=np.zeros_like(self.q))
        h=(self.q.T@y)
        h=(h+h.T)/2
        if h.size:
            d,v=np.linalg.eigh(h)
            keep=d>max(1e-14,1e-13*float(np.max(d)))
            f=(y@v[:,keep])/np.sqrt(d[keep])[None,:]
        else:
            f=np.empty((self.source.n,0))
        cf=cho_factor(lam*np.eye(f.shape[1])+f.T@f,lower=True) if f.shape[1] else None
        self.assembly_seconds+=time.perf_counter()-start

        def approximate(x):
            return f@(f.T@x)

        def precondition(x):
            begin=time.perf_counter()
            z=x/lam if cf is None else (x-f@cho_solve(cf,f.T@x))/lam
            self.application_seconds+=time.perf_counter()-begin
            return z

        def residual(x):
            return self.source.combined(theta,x,"certificate")-approximate(x)

        return approximate,precondition,residual


def acquire(lib,theta,mu,delta,seed,method):
    rng=np.random.default_rng(seed)
    n=lib.source.n
    alpha=1/16
    q=max(1,math.ceil(math.log(n/alpha,4)))
    if method=="retained_gaussian":
        lib.append(rng.normal(size=(n,2)))
    while True:
        s=len(lib.stages)+1
        ds=delta/(s*(s+1))
        probes=math.ceil(math.log(ds)/math.log(181/256))
        _,_,residual=lib.build(theta,mu)
        g=rng.choice(np.array([-1.,1.]),size=(n,probes))
        v=g.copy()
        before=dict(lib.source.counts)
        # Scaling powers avoids overflow while preserving each selected vector.
        logs=np.zeros(probes)
        for _ in range(q):
            v=residual(v)
            scale=np.linalg.norm(v,axis=0)
            logs+=np.log(np.maximum(scale,np.finfo(float).tiny))
            v/=np.maximum(scale,np.finfo(float).tiny)[None,:]
        imax=int(np.argmax(logs))
        log_upper=(logs[imax]-.5*math.log(alpha))/q
        upper=math.exp(log_upper)
        accepted=upper<=mu/2
        row={"stage":s,"dimension":lib.q.shape[1],"powers":q,"probes":probes,
             "delta_stage":ds,"norm_upper_test":upper,"accepted":bool(accepted),
             "primitive_calls_test":lib.source.counts["certificate"]-before["certificate"]}
        lib.stages.append(row)
        if accepted:
            return
        if method=="cumulative_witness":
            lib.append(v[:,imax])
        else:
            extra=min(max(2,lib.q.shape[1]),n-lib.q.shape[1])
            if extra==0:
                raise RuntimeError("Full sketch failed floating certificate")
            lib.append(rng.normal(size=(n,extra)))
        if len(lib.stages)>n+1:
            raise RuntimeError("Declared diagnostic stage cap reached")


def richardson(source,lib,theta,lam,b,eps):
    _,precondition,_=lib.build(theta,lam)
    x=np.zeros_like(b)
    r=b.copy()
    den=float(b@precondition(b))
    k=0
    while True:
        z=precondition(r)
        bound=1.5*float(r@z)/den
        if bound<=eps*eps:
            return x,k
        x+=z
        r=b-lam*x-source.combined(theta,x,"solve")
        k+=1
        if k>120:
            raise RuntimeError("Richardson failed diagnostic cap")


def cg(source,theta,lam,b,eps):
    x=np.zeros_like(b)
    r=b.copy(); p=r.copy(); rr=float(r@r)
    # This criterion certifies relative A-energy error without an acquired norm:
    # ||r||² <= eps² lambda (bᵀb)² / (bᵀ A b).
    ab=lam*b+source.combined(theta,b,"solve")
    threshold=eps*eps*lam*float(b@b)**2/float(b@ab)
    k=0
    while rr>threshold:
        ap=lam*p+source.combined(theta,p,"solve")
        a=rr/float(p@ap)
        x+=a*p; r-=a*ap
        rr_new=float(r@r)
        p=r+(rr_new/rr)*p;rr=rr_new;k+=1
        if k>400:
            raise RuntimeError("CG failed diagnostic cap")
    # Pay for and use actual final residual, not recursive residual alone.
    actual=b-lam*x-source.combined(theta,x,"solve")
    if float(actual@actual)>threshold*1.05:
        raise RuntimeError("CG recursive-residual numerical problem")
    return x,k


def generate(seed=916,n=192,rank=8,m=3,tasks=512):
    rng=np.random.default_rng(seed)
    u=np.linalg.qr(rng.normal(size=(n,rank)),mode="reduced")[0]
    hs=[]
    for j in range(m):
        rot=np.linalg.qr(rng.normal(size=(rank,rank)))[0]
        hs.append((rot*np.geomspace(2.,3000.,rank)[None,:])@rot.T)
    tails=np.full(m,.002)
    jobs=[]
    for _ in range(tasks):
        theta=rng.uniform(.02,1.,m)
        lam=float(rng.uniform(1.,3.))
        b=rng.normal(size=n)
        jobs.append((theta,lam,b))
    return u,hs,tails,jobs


def true_error(u,hs,tails,theta,lam,b,x):
    base=lam+float(theta@tails)
    h=sum(a*z for a,z in zip(theta,hs))
    ub=u.T@b
    truth=(b-u@ub)/base+u@np.linalg.solve(base*np.eye(h.shape[0])+h,ub)
    e=x-truth
    en=base*float(e@e)+float((u.T@e)@h@(u.T@e))
    return math.sqrt(max(en,0.)/float(truth@b))


def main():
    u,hs,tails,jobs=generate()
    n,m=u.shape[0],len(hs)
    eps=1e-8
    summary={"kind":"binary64 diagnostic; no interval-roundoff certification",
             "n":n,"m":m,"hidden_fixture_rank":u.shape[1],"tasks":len(jobs),
             "target_relative_energy_error":eps,"confidence_rule_delta":.01,
             "source_contract":"Only apply(j,v) plus known PSD affine family, nonnegative box [0,1]^m and lambda>=1; no U,H or matrix entries supplied to learners",
             "environment":{"numpy":np.__version__,"blas_threads_requested":os.environ.get("OPENBLAS_NUM_THREADS")},
             "methods":{}}
    for method in ("cumulative_witness","retained_gaussian","cold_cg","retained_tomography"):
        source=Source(u,hs,tails)
        start=time.perf_counter()
        lib=None
        if method in ("cumulative_witness","retained_gaussian"):
            lib=Retained(source)
            acquire(lib,np.ones(m),1.,.01,335,method)
        matrices=None
        if method=="retained_tomography":
            matrices=[source.apply(j,np.eye(n),"tomography") for j in range(m)]
        acquisition_seconds=time.perf_counter()-start
        acquisition_counts=dict(source.counts)
        max_error=0.;iterations=[];prefixes=[]
        for i,(theta,lam,b) in enumerate(jobs):
            if lib is not None:
                x,it=richardson(source,lib,theta,lam,b,eps)
            elif method=="cold_cg":
                x,it=cg(source,theta,lam,b,eps)
            else:
                a=sum(t*z for t,z in zip(theta,matrices))+lam*np.eye(n)
                x=cho_solve(cho_factor(a,lower=True),b);it=1
            err=true_error(u,hs,tails,theta,lam,b,x)
            max_error=max(max_error,err)
            if err>eps*1.05:
                raise AssertionError((method,i,err))
            iterations.append(it)
            if i+1 in (1,8,32,128,512):
                prefixes.append({"tasks":i+1,"primitive_calls":sum(source.counts.values()),
                                 "calls_by_category":dict(source.counts)})
        row={"acquisition_counts":acquisition_counts,"all_counts":source.counts,
             "total_primitive_calls":sum(source.counts.values()),
             "returned_coordinates":source.coordinate_outputs,
             "acquisition_wall_seconds":acquisition_seconds,
             "total_wall_seconds_including_shared_truth_audits":time.perf_counter()-start,
             "source_wall_seconds":source.source_seconds,
             "max_actual_relative_energy_error":max_error,
             "min_iterations":min(iterations),"max_iterations":max(iterations),
             "mean_iterations":float(np.mean(iterations)),"prefixes":prefixes}
        if lib is not None:
            row.update({"retained_dimension":lib.q.shape[1],"certificate_stages":lib.stages,
                        "retained_float_count":lib.q.size+sum(z.size for z in lib.cache),
                        "assembly_wall_seconds":lib.assembly_seconds,"precondition_application_wall_seconds":lib.application_seconds})
            # Exact source formula ONLY used by the evaluator after learning.
            c=u@sum(hs)@u.T+sum(tails)*np.eye(n)
            approx,_,_=lib.build(np.ones(m),1.)
            e=c-approx(np.eye(n))
            row["audit_envelope_residual_eigenvalues"]=[float(np.linalg.eigvalsh((e+e.T)/2)[0]),float(np.linalg.eigvalsh((e+e.T)/2)[-1])]
        elif matrices is not None:
            row["retained_float_count"]=m*n*n
        else:
            row["retained_float_count"]=0
        summary["methods"][method]=row
        print(json.dumps({"method":method,"calls":row["total_primitive_calls"],"dimension":row.get("retained_dimension"),"error":max_error,"seconds":row["total_wall_seconds_including_shared_truth_audits"]}))
    c=u@sum(hs)@u.T+sum(tails)*np.eye(n)
    vals=np.linalg.eigvalsh(c)
    summary["hindsight_envelope_potential"]=float(np.log2(1+4*vals).sum())
    summary["limitations"]=["Small synthetic family; no PDE/data application established", "Binary64 tests are diagnostics, not rigorous real-number certificate execution", "Timings include shared validation and are not hardware comparisons", "Cold CG is not the strongest retaining baseline; Gaussian and tomography explicitly retain observations", "The source internally uses low-rank factors only to simulate apply; algorithms do not receive those factors", "No historical novelty inferred"]
    out=Path(__file__).resolve().parents[1]/"results"/"comparison.json"
    out.write_text(json.dumps(summary,indent=2)+"\n")


if __name__=="__main__":
    main()
