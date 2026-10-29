"""Consume T's frozen model kernels; NO native-control propagation.

Standard semidefinite/trigonometric-Gram receiver, with exact rational
rounding checks on its supplied binary64 matrix inputs. This does not certify
the ODE/model truncation or physical specimen.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,time,sys
import numpy as np
import cvxpy as cp

HERE=Path(__file__).resolve().parent
SCALE=1000.
BITS=44

def dec(x):return np.array(x['real'])+1j*np.array(x['imag'])
def enc(x):return {'real':x.real.tolist(),'imag':x.imag.tolist()}
def dy(x):return F(round(float(x)*2**BITS),2**BITS)
def exact(z):return F.from_float(float(z.real)),F.from_float(float(z.imag))
def rnd(z):return dy(z.real),dy(z.imag)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[0],-a[1]
def sub(a,b):return add(a,neg(b))
def conj(a):return a[0],-a[1]
def ab(a):return abs(a[0])+abs(a[1])
ZERO=(F(0),F(0))

def herm_exact(a):
    n=len(a);out=[[ZERO]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            z=add(exact(a[i,j]),conj(exact(a[j,i])))
            out[i][j]=(z[0]/2,z[1]/2)
    return out

def round_herm(a):
    a=(a+a.conj().T)/2;n=len(a);out=[[ZERO]*n for _ in range(n)]
    for i in range(n):
        out[i][i]=(dy(a[i,i].real),F(0))
        for j in range(i+1,n):out[i][j]=rnd(a[i,j]);out[j][i]=conj(out[i][j])
    return out

def psd_ldl(q,shift):
    """Exact LDL of the realification; strictly positive pivots suffice."""
    n=len(q);N=2*n
    M=[[F(0) for _ in range(N)] for _ in range(N)]
    for i in range(n):
        for j in range(n):
            re,im=q[i][j]
            M[i][j]=M[n+i][n+j]=re
            M[i][n+j]=-im;M[n+i][j]=im
    L=[[F(0) for _ in range(N)] for _ in range(N)];D=[]
    for i in range(N):
        pivot=M[i][i]+shift-sum(L[i][k]**2*D[k] for k in range(i))
        if pivot<=0:return False
        D.append(pivot);L[i][i]=1
        for j in range(i+1,N):
            L[j][i]=(M[j][i]-sum(L[j][k]*L[i][k]*D[k] for k in range(i)))/pivot
    return True

def toeplitz_expression(hs,kind,harmonic):
    lags=sorted({int(b-a) for a in hs for b in hs})
    params={}
    if kind==0:
        for l in lags:
            if l<0:continue
            params[l]=cp.Variable() if l==0 and harmonic else (0. if l==0 else cp.Variable(complex=True))
        element=lambda l:params[l] if l>=0 else cp.conj(params[-l])
    else:
        params={l:(0. if l==0 and not harmonic else cp.Variable(complex=True)) for l in lags}
        element=lambda l:params[l]
    T=cp.bmat([[cp.reshape(element(int(b-a)),(1,1),order='C') for b in hs] for a in hs])
    return T

def solve(A,B,hs,blocks,harmonic):
    tic=time.perf_counter();n=len(hs)
    A=(A+A.conj().T)/2
    T0=toeplitz_expression(hs,0,harmonic);T1=toeplitz_expression(hs,1,harmonic)
    radius=cp.Variable(nonneg=True);constraints=[];XX=[]
    for sign in [1,-1]:
        for ids in blocks:
            d=len(ids);a=A[np.ix_(ids,ids)]*SCALE;b=B[np.ix_(ids,ids)]*SCALE
            t0=T0[np.ix_(ids,ids)];t1=T1[np.ix_(ids,ids)]
            X=cp.Variable((2*d,2*d),hermitian=True)
            constraints += [X >> 1e-8*np.eye(2*d),
                X[:d,:d]+X[d:,d:]==radius*np.eye(d)-sign*(a-t0),
                X[:d,d:]==-sign*(b-t1)]
            XX.append((sign,ids,X))
    prob=cp.Problem(cp.Minimize(radius),constraints)
    prob.solve(solver='CLARABEL',tol_gap_abs=2e-9,tol_feas=2e-9,tol_gap_rel=2e-9,max_iter=180)
    if radius.value is None:raise RuntimeError(str(prob.status))
    # The solver is an untrusted proposal. Rebuild rounded Toeplitz values exactly.
    t0=T0.value/SCALE;t1=T1.value/SCALE;r=dy(radius.value/SCALE)
    lags=sorted({int(b-a) for a in hs for b in hs})
    c0={l:rnd(t0[0,hs.index(hs[0]+l)]) for l in lags if hs[0]+l in hs}
    # For negative lags use any actual matrix entry (nonconsecutive subsets allowed).
    c0={l:rnd(t0[next(i for i,a in enumerate(hs) if a+l in hs),hs.index(next(a for a in hs if a+l in hs)+l)]) for l in lags}
    c1={l:rnd(t1[next(i for i,a in enumerate(hs) if a+l in hs),hs.index(next(a for a in hs if a+l in hs)+l)]) for l in lags}
    c0[0]=(c0[0][0],F(0))
    for l in lags:
        if l<0:c0[l]=conj(c0[-l])
    if not harmonic:c0[0]=c1[0]=ZERO
    qT0=[[c0[int(b-a)] for b in hs] for a in hs]
    qT1=[[c1[int(b-a)] for b in hs] for a in hs]
    qA=herm_exact(A);qB=[[exact(z) for z in row] for row in B]
    corrections=[];certs=[]
    for sign,ids,X in XX:
        d=len(ids);qX=round_herm(X.value/SCALE)
        delta=F(1,10**10);tries=0
        while not psd_ldl(qX,delta):
            delta*=10;tries+=1
            if tries>8:raise RuntimeError('No exact positive rounded Gram found')
        e0=F(0);e1=F(0)
        for i,ii in enumerate(ids):
            for j,jj in enumerate(ids):
                const=sub(qA[ii][jj],qT0[ii][jj])
                const=(const[0]*sign,const[1]*sign)
                desired=sub((r if i==j else F(0),F(0)),const)
                residual=sub(desired,add(qX[i][j],qX[d+i][d+j]))
                e0+=ab(residual)
                first=sub(qB[ii][jj],qT1[ii][jj]);first=(first[0]*(-sign),first[1]*(-sign))
                e1+=ab(sub(first,qX[i][d+j]))
        correction=2*delta+e0+2*e1
        corrections.append(correction)
        certs.append({'sign':sign,'ids':ids,'realified_size':4*d,'PSD_shift':str(delta),
                      'residual_constant_l1':str(e0),'residual_first_l1':str(e1),
                      'exact_positive_LDL':True,
                      'X':[[[str(a),str(b)] for a,b in row] for row in qX]})
    safe=r+max(corrections)
    return {'solver_status':str(prob.status),'solver_objective_mean_bright':float(radius.value/SCALE),
            'certified_radius_mean_bright':float(safe),'radius_exact':str(safe),
            'raw_probability_bound':float(safe/2) if not harmonic else None,
            'nonzero_harmonic_probability_bound_DFT_l1':float(safe/2) if harmonic else None,
            'nonzero_harmonic_probability_bound_5grid':float(safe/2)*(1+np.sqrt(5))/5 if harmonic else None,
            'Toeplitz0_coeff':{str(k):[str(a),str(b)] for k,(a,b) in c0.items()},
            'Toeplitz1_coeff':{str(k):[str(a),str(b)] for k,(a,b) in c1.items()},
            'rounded_radius':str(r),'certificate_blocks':certs,
            'seconds':time.perf_counter()-tic}

def main():
    start=time.perf_counter();p=HERE/'inputs'/'HISTORY_KERNELS.json';data=p.read_bytes();r=json.loads(data)
    out={'kernel_sha256':hashlib.sha256(data).hexdigest(),
         'scope':'Exact rational bounds for canonical Hermitian parts of supplied binary64 kernels; no native ODE/geometry/device qualification.',
         'normalization':'mean_bright=2*pBright-1; normalized125-setting5x5x5 nonzero DFT coefficient',
         'reports':[]}
    # Actual useful fluorescence axes; do not promote the null X science channel.
    for report in r['reports']:
        for obs in ['Z_physical_bright','Y_analysis']:
            dat=report['observables'][obs];A=dec(dat['A']);B=dec(dat['B']);hs=report['hs']
            for name in ['all_degree4','charge_preserving_second_q_minus']:
                blocks=dat['mean_bounds'][name]['blocks']
                for harmonic in [False,True]:
                    result=solve(A,B,hs,blocks,harmonic)
                    item={'pulse':report['pulse'],'observable':obs,'science_class':name,
                          'harmonic':harmonic,'baseline':{k:v for k,v in dat['mean_bounds'][name].items() if k.endswith('upper')},**result}
                    out['reports'].append(item)
                    (HERE/'KERNEL_BOUND_PARTIAL.json').write_text(json.dumps(out,indent=2)+'\n')
                    print(json.dumps({k:item[k] for k in ['pulse','observable','science_class','harmonic','certified_radius_mean_bright','seconds']}),flush=True)
    out['wall_seconds']=time.perf_counter()-start
    out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/'KERNEL_BOUND.json').write_text(json.dumps(out,indent=2)+'\n')
    print('COMPLETE '+str(out['wall_seconds']),flush=True)

if __name__=='__main__':main()
