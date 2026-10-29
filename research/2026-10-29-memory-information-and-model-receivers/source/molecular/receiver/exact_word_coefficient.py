"""Exact selected coefficient and non-null target on supplied model matrices.

No native ion dynamics. Four two-band rotations, specified p only; no claim
that CaOH realizes that p. Phase exponents are extracted symbolically.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
import numpy as np
from kernel_bound import herm_exact,exact,add,conj,ZERO,ab

HERE=Path(__file__).resolve().parent
def mul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def scale(a,b):return a[0]*b,a[1]*b
def dec(x):return np.array(x['real'])+1j*np.array(x['imag'])
def contract(C,K):
    out=ZERO
    for i in range(9):
        for j in range(9):out=add(out,mul(C[i][j],K[j][i]))
    return out

def coefficient(qs,p):
    # At pi/2 each path has common amplitude1/4 and Gaussian-integer phase.
    paths=[(0,0,(0,0,0,0),(1,0))]
    for t,q in enumerate(qs):
        new=[]
        for s,h,ex,amp in paths:
            new.append((s,h,ex,amp))
            sign=1 if s==0 else -1;e=list(ex);e[t]+=sign
            new.append((1-s,h+sign*q,tuple(e),mul(amp,(0,-1))))
        paths=new
    C=[[ZERO for _ in range(9)] for _ in range(9)];count=0
    for sa,ha,ea,aa in paths:
        for sb,hb,eb,bb in paths:
            if sa!=sb or tuple(a-b for a,b in zip(ea[:3],eb[:3]))!=(-1,1,1):continue
            assert ea[3]-eb[3]==-1
            C[ha+4][hb+4]=add(C[ha+4][hb+4],scale(mul(aa,conj(bb)),F(1,16)))
            count+=1
    # Every selected path pair contributes c*s on each pulse, so p²(1-p)².
    ratio=16*p*p*(1-p)*(1-p)
    return [[scale(a,ratio) for a in row] for row in C],count

def main():
    t=time.perf_counter();data=(HERE/'inputs'/'HISTORY_KERNELS.json').read_bytes();r=json.loads(data);out=[]
    for p in [F(3,100),F(1,2)]:
        for qs in [[1,1,1,1],[1,-1,1,1]]:
            C,count=coefficient(qs,p)
            for report in r['reports']:
                for axis in ['Z_physical_bright','Y_analysis']:
                    d=report['observables'][axis];kt=herm_exact(dec(d['Ktarget']));a=herm_exact(dec(d['A']));b=[[exact(z) for z in row] for row in dec(d['B'])]
                    bd=[[conj(b[j][i]) for j in range(9)] for i in range(9)]
                    target=scale(contract(C,kt),F(1,2));er=[scale(contract(C,x),F(1,2)) for x in [a,b,bd]]
                    radius=sum(ab(x) for x in er)
                    out.append({'pulse':report['pulse'],'axis':axis,'p':str(p),'q':qs,
                      'selected_path_pairs':count,
                      'target_probability_coefficient_exact':[str(x) for x in target],
                      'target_probability_real_display':float(target[0]),
                      'target_nonzero_exact':target!=ZERO,
                      'model_probability_error_uniform_chi_exact_upper':str(radius),
                      'model_probability_error_uniform_chi_display':float(radius)})
    result={'kernel_sha256':hashlib.sha256(data).hexdigest(),'reports':out,
      'scope':'Exact algebra on the canonical Hermitian supplied binary64 matrices; declared two-band p, not nativeCaOH parameters or physical ODE accuracy.',
      'seconds_after_imports':time.perf_counter()-t,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'EXACT_WORD_COEFFICIENT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'smooth_weak': [x for x in out if x['pulse']=='smooth_BB1' and x['p']=='3/100'], 'seconds':result['seconds_after_imports']},indent=2))

if __name__=='__main__':main()
