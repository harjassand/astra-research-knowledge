"""Construct and verify exact dyadic, thermodynamic transport certificates.
All physical parameters in the main fixture are rational. Floating optimization is
only discovery. Bounds, population balance and the gap identity are checked using
integer arithmetic and Fraction. The independent small-system checks live separately.
"""
from __future__ import annotations
import math,json,time,argparse,hashlib
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
import numpy as np
import scipy.sparse as sp
from local_solver import nullspace_columns
from fast_algebra import build

def integer_matrix(A,scale=2):
    C=A.copy();r=np.rint(C.data*scale)
    if not np.all(np.isfinite(r)) or not np.all(np.abs(r)<2**62):
        raise ValueError("Matrix entries exceed checked integer range")
    assert np.array_equal(r,C.data*scale)
    C.data=r.astype(np.int64)
    return C

def safe_dot(A,x):
    # This conservative bound certifies that int64 multiplication and summation do not overflow.
    m=max((abs(int(a)) for a in x),default=0)
    csr=A.tocsr()
    max_entry=max((abs(int(a)) for a in csr.data),default=0)
    max_row_nnz=int(np.max(np.diff(csr.indptr))) if csr.shape[0] else 0
    if max_entry*max_row_nnz>=2**63:
        raise ValueError("Row-sum overflow bound")
    rows=np.asarray(abs(A).sum(axis=1)).ravel()
    bound=int(max(rows,default=0))*m
    assert bound<np.iinfo(np.int64).max, ('overflow bound',bound)
    return np.asarray(A@x).ravel()

def weighted_squares(x,q,inverse=False):
    sums=defaultdict(int)
    for a,b in zip(x,q):
      if not a:continue
      b=int(b);a=int(a)
      if inverse:
        assert b>0
        sums[b]+=a*a
      else:sums[1]+=b*a*a
    return sum((F(a,b) for b,a in sums.items()),F())

def exact_bounds(fw,gw,fn,gn,den,t=F(1),U=F(4),V=F(1),d=F(2)):
    # Scale the rational physical coefficients BEFORE compiled arithmetic.
    # Every emitted coefficient is then an integer, represented exactly in binary64.
    # The bound below ensures that every duplicate-summation partial sum is also exact.
    t,U,V,d=map(F,(t,U,V,d))
    if d!=2:
        raise ValueError("This fast certificate implementation currently verifies d=2 only")
    if den<=0 or not fw or not gw:
        raise ValueError("Nonempty packets and a positive denominator are required")
    L=max((int(x)|int(z)).bit_length() for x,z in fw+gw)
    if L>18:
        raise ValueError("20-bit word encoding requires input support at most 18")
    scale=math.lcm(t.denominator,U.denominator,V.denominator)*2
    scaled=[p*scale for p in (t,U,V)]
    if not all(a.denominator==1 for a in scaled):
        raise ValueError("Internal rational scaling error")
    if 100*(L+4)*max(abs(a.numerator) for a in scaled)>=2**50:
        raise ValueError("Exact compiled coefficient range exceeded; use arbitrary-precision assembly")
    tt,uu,vv=map(float,scaled)
    er,AF=build(fw,tt,uu,vv);orr,AG=build(gw,tt,uu,vv)
    if (3,1) not in orr:
      orr.append((3,1));AG=sp.vstack([AG,sp.csc_matrix((1,len(gw)))],format="csc")
    AF=integer_matrix(AF,1);AG=integer_matrix(AG,1)
    af=safe_dot(AF,fn);ag=safe_dot(AG,gn)
    qf=[w[0].bit_count() for w in fw];qg=[w[0].bit_count() for w in gw]
    qe=[w[0].bit_count() for w in er];qo=[w[0].bit_count() for w in orr]
    assert all(int(a)==0 for a,q in zip(af,qe) if q==0), 'population imbalance'
    # S=(d/2)*flip_count. Orbit-pair norm squared is 2.
    fj=int(fn[fw.index((3,1))])
    low=-2*t*F(fj,den) - d*weighted_squares(fn,qf)/den**2 - (4/d)*weighted_squares(af,qe,True)/(scale*den)**2
    residual=-ag
    jloc=orr.index((3,1));jn=-t*F(scale*den,2)
    assert jn.denominator==1
    residual[jloc]+=int(jn)
    up=(4/d)*weighted_squares(residual,qo,True)/(scale*den)**2 + d*weighted_squares(gn,qg)/den**2
    # Independent exact gap expansion: r1=Sf-J+Ag; r2=Sg+Af, common scale*den.
    assert d==2, 'fast integer gap verification uses fixture d=2'
    r1=defaultdict(int);r2=defaultdict(int)
    for w,c,q in zip(fw,fn,qf):r1[w]+=scale*int(c)*q
    r1[(3,1)]+=int(t*F(scale*den,2))
    for w,c in zip(orr,ag):r1[w]+=int(c)
    for w,c,q in zip(gw,gn,qg):r2[w]+=scale*int(c)*q
    for w,c in zip(er,af):r2[w]+=int(c)
    sq=F()
    for r in [r1,r2]:
      qs=[w[0].bit_count() for w in r]
      sq+=2*weighted_squares(list(r.values()),qs,True)/(scale*den)**2
    assert up-low==sq, 'gap identity'
    return low,up,dict(commutator_nnz=int(AF.nnz+AG.nnz),f_nonzero=int(np.count_nonzero(fn)),g_nonzero=int(np.count_nonzero(gn)),balance_exact=True,gap_identity_exact=True)

def run(path,bits=36):
    start=time.perf_counter();path=Path(path);dat=np.load(path)
    fw=[tuple(map(int,w)) for w in dat['fw']];gw=[tuple(map(int,w)) for w in dat['gw']]
    er,AF=build(fw,1.,4.,1.);off=np.array([w[0]!=0 for w in er])
    N,entries,free,rank=nullspace_columns(AF[~off,:].tocsc())
    lcm=math.lcm(*(x.denominator for i,j,x in entries));den=(1<<bits)*lcm
    nu=np.rint(dat['u']*(1<<bits)).astype(np.int64)
    fn0=[0]*len(fw)
    for i,j,x in entries:
      y=x*lcm;assert y.denominator==1
      fn0[i]+=int(y)*int(nu[j])
    fn=np.asarray(fn0,dtype=np.int64)
    gn=np.rint(dat['g']*den).astype(np.int64)
    params=json.loads(path.with_suffix('.json').read_text())
    physical={k:F(float(params[k])) for k in ['t','U','V','d']}
    lo,hi,meta=exact_bounds(fw,gw,fn,gn,den,**physical)
    L=max((w[0]|w[1]).bit_length() for w in fw+gw);min_n=2*(L+2)+1
    scale=10**10
    dl=4*lo;du=4*hi
    lower_display=F((dl.numerator*scale)//dl.denominator,scale)
    upper_display=F(-((-du.numerator*scale)//du.denominator),scale)
    cert=dict(parameters={k:str(v) for k,v in physical.items()},L=L,denominator=den,rounding_bits=bits,minimum_ring_size=min_n,
      D_lower_exact=str(dl),D_upper_exact=str(du),D_width_exact=str(du-dl),
      D_lower_outward_decimal=f'{float(lower_display):.10f}',D_upper_outward_decimal=f'{float(upper_display):.10f}',
      width_float=float(du-dl),discovery_coefficients_not_trusted=True,verification_seconds=time.perf_counter()-start,**meta)
    out=path.with_name(path.stem+'_exact.npz');np.savez_compressed(out,fw=np.array(fw),gw=np.array(gw),fn=fn,gn=gn,den=np.array([den],dtype=np.int64))
    cert['witness_file']=out.name;cert['witness_sha256']=hashlib.sha256(out.read_bytes()).hexdigest()
    path.with_name(path.stem+'_certificate.json').write_text(json.dumps(cert,indent=2))
    print(json.dumps(cert,indent=2),flush=True)
    return cert
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('paths',nargs='+');p.add_argument('--bits',type=int,default=36);a=p.parse_args()
 for path in a.paths:run(path,a.bits)
