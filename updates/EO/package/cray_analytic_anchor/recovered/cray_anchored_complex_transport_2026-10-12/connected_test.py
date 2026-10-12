"""Independent chain instances; specialised transfer quadrature is the baseline.
The transfer method is NOT exponential in chain length. No superiority claim.
"""
import json,time,math
import numpy as np
from numpy.polynomial.hermite import hermgauss
from numpy.polynomial.legendre import leggauss
from experiment import ROOT, certificate,run_chain,pair

def make(n,seed=802367):
    rng=np.random.default_rng(seed); A=np.zeros((n,n));C=np.diag(rng.uniform(.3,.5,n))
    edges=np.array([(i,i+1) for i in range(n-1)],dtype=np.int64)
    for i,j in edges:
        A[i,j]=A[j,i]=-rng.uniform(.3,.5);C[i,j]=C[j,i]=rng.uniform(.05,.1)
    for i in range(n): A[i,i]=3+sum(abs(A[i,j]) for j in range(n) if i!=j)
    return A,C,edges,.5,.2,.4

def transfer_logZ(A,C,a,c,t,order):
    n=len(A);q,w=hermgauss(order);scale=math.sqrt(min(np.diag(A))/2);x=q/scale
    v=np.ones(order,dtype=complex);logscale=0.
    for i in range(n):
        onsite=.5*(A[i,i]-1j*t*C[i,i])*x*x+a*x**4/4
        f=w*np.exp(-onsite+q*q)/scale
        if i:
            xx=x[:,None]; yy=x[None,:]
            edge=(A[i-1,i]-1j*t*C[i-1,i])*xx*yy+c*((xx+yy)**4+(xx-yy)**4)/4
            v=(v@np.exp(-edge))*f
        else:v=f
        s=max(abs(v));v/=s;logscale+=math.log(s)
    return complex(np.log(v.sum())+logscale)

def main():
    A,C,edges,a,c,r=make(10);cert=certificate(A,C,edges,a,c,r);assert cert['passed']
    t0=time.perf_counter();truth=[]
    for order in (64,100,160):
        L=transfer_logZ(A,C,a,c,1,order)-transfer_logZ(A,C,a,c,0,order)
        truth.append({'order':order,'log_ratio':pair(L)})
    basetime=time.perf_counter()-t0
    # Warm compilation and short chain excluded from reported trajectory time.
    run_chain(1,10,0,.01,A,C,edges,a,c,.5,r,5)
    nodes,weights=leggauss(6);nodes=(nodes+1)/2;weights/=2
    h=.005;duration=600.;burn=20;bs=int(10/h);nb=int(duration/10)
    value=0j;vr=0.;vi=0.;recs=[];t0=time.perf_counter()
    for j,(t,w) in enumerate(zip(nodes,weights)):
        means,mi,mr,it,fail=run_chain(617000+j,int(burn/h)+nb*bs,int(burn/h),h,A,C,edges,a,c,float(t),r,bs)
        assert not fail
        mean=means.mean(); sr=means.real.std(ddof=1)/np.sqrt(nb);si=means.imag.std(ddof=1)/np.sqrt(nb)
        value+=w*mean;vr+=(w*sr)**2;vi+=(w*si)**2
        recs.append(dict(t=float(t),mean=pair(mean),batch_se=[float(sr),float(si)],max_abs_imag=float(mi),max_residual=float(mr),failures=int(fail)))
    result=dict(status='floating diagnostic, not finite-bit certificate',seed=802367,n=10,
                fixture=dict(A=A.tolist(),C=C.tolist(),edges=edges.tolist(),a=a,c=c,r=r),certificate=cert,
                transfer_truth=truth,transfer_seconds=basetime,h=h,duration_per_node=duration,nodes=6,
                CL_log_ratio=pair(value),CL_batch_se=[math.sqrt(vr),math.sqrt(vi)],
                CL_error=pair(value-L),CL_seconds=time.perf_counter()-t0,node_records=recs)
    (ROOT/'connected_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['transfer_truth','CL_log_ratio','CL_batch_se','CL_error','transfer_seconds','CL_seconds']},indent=2))
if __name__=='__main__':main()
