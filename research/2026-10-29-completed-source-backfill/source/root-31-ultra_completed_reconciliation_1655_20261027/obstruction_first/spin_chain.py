"""Explicit spin-2 Heisenberg sectors. Numerical spectra are diagnostics.

H=sum_j Sz_j Sz_{j+1} +(S+_j S-_{j+1}+S-_j S+_{j+1})/2.
The P twist reverses both hopping terms on the closing bond. All entries are
integers plus integer multiples of sqrt(6); no numerical diagonalization is
itself a spectral-count certificate. The real symmetric physical weight basis
is used, not a nonunitary integer-coordinate basis.
"""
from __future__ import annotations
import os
for _name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_name, "2")
import pathlib, sys, json, time, argparse
ROOT = pathlib.Path(__file__).resolve().parents[3]
VENDOR = ROOT / "sol6_openings_20261027/positive_current_operation/vendor"
if not VENDOR.exists():
    VENDOR = pathlib.Path(__file__).resolve().parents[2] / "sol6_openings_20261027/positive_current_operation/vendor"
sys.path.insert(0, str(VENDOR))
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
from scipy.linalg import eigvalsh


def sector(n: int, magnetization: int, twist: int = 0):
    """Return H, computational-basis word codes, integer entry matrices H0,H1.

    H=H0+sqrt(6)*H1. Each word is base five; digits minus two are local Sz.
    """
    assert n >= 3 and twist in (0, 1)
    powers = 5 ** np.arange(n, dtype=np.int64)
    codes = np.arange(5**n, dtype=np.int64)
    digits = ((codes[:, None] // powers) % 5).astype(np.int8)
    keep = np.sum(digits.astype(np.int16)-2, axis=1) == magnetization
    codes, digits = codes[keep], digits[keep]
    d = len(codes)
    lookup = np.full(5**n, -1, dtype=np.int32)
    lookup[codes] = np.arange(d, dtype=np.int32)
    diagonal = np.sum((digits.astype(np.int16)-2) * (np.roll(digits.astype(np.int16),-1,axis=1)-2),axis=1)
    rows0, cols0, vals0 = [np.arange(d)], [np.arange(d)], [diagonal]
    rows1, cols1, vals1 = [], [], []
    # Squared ladder entries indexed by the lower weight's digit.
    ladder2 = np.array([4,6,6,4],dtype=np.int16)
    for j in range(n):
        k = (j+1) % n
        sign = -1 if twist and j == n-1 else 1
        good = (digits[:,j] < 4) & (digits[:,k] > 0)
        col = np.flatnonzero(good)
        row = lookup[codes[good]+powers[j]-powers[k]]
        c2 = ladder2[digits[good,j]] * ladder2[digits[good,k]-1]
        for squared, rational, irrational in [(16,2,0),(24,0,1),(36,3,0)]:
            take = c2 == squared
            rr, cc = row[take], col[take]
            if rational:
                rows0 += [rr,cc];cols0 += [cc,rr];vals0 += [np.full(len(rr),sign*rational)]*2
            if irrational:
                rows1 += [rr,cc];cols1 += [cc,rr];vals1 += [np.full(len(rr),sign)]*2
    def form(rows,cols,vals):
        if not rows:return coo_matrix((d,d),dtype=np.int64).tocsr()
        return coo_matrix((np.concatenate(vals).astype(np.int64),(np.concatenate(rows),np.concatenate(cols))),shape=(d,d)).tocsr()
    h0, h1 = form(rows0,cols0,vals0), form(rows1,cols1,vals1)
    h = h0.astype(float)+np.sqrt(6.0)*h1
    assert (h-h.T).nnz == 0
    return h,codes,h0,h1


def momentum_blocks(n: int, magnetization: int, twist: int = 0):
    """Block by signed translation, retaining the exact seam holonomy.

    T rotates the last weight to the front with phase exp(-i*pi*twist*m_last).
    Thus T**n=exp(-i*pi*twist*M), and its eigenvalues are
    exp(i*(2*pi*k-pi*twist*M)/n). A word orbit of length r contributes iff
    n divides k*r. This avoids confusing ordinary translation with magnetic
    translation at the twisted seam.
    """
    h,codes,_,_=sector(n,magnetization,twist)
    lookup={int(c):i for i,c in enumerate(codes)}
    seen=set();orbits=[]
    for c in codes:
        c=int(c)
        if c in seen:continue
        orbit=[];phases=[];phase=1;w=c
        while w not in seen:
            seen.add(w);orbit.append(lookup[w]);phases.append(phase)
            digit=w//(5**(n-1));phase*=(-1 if twist and (digit-2)%2 else 1)
            w=(w%(5**(n-1)))*5+digit
        assert w==c
        assert abs(phase-(-1 if twist and (magnetization*len(orbit)//n)%2 else 1))==0
        orbits.append((np.asarray(orbit,dtype=np.int32),np.asarray(phases,dtype=np.int8)))
    hc=h.tocoo();total=0
    for k in range(n):
        tau=np.exp(1j*(2*np.pi*k-np.pi*twist*magnetization)/n)
        labels=np.full(len(codes),-1,dtype=np.int32);coeff=np.zeros(len(codes),complex);dimension=0
        for orbit,phases in orbits:
            r=len(orbit)
            if (k*r)%n:continue
            labels[orbit]=dimension;coeff[orbit]=phases*tau**(-np.arange(r))/np.sqrt(r);dimension+=1
        take=(labels[hc.row]>=0)&(labels[hc.col]>=0)
        values=hc.data[take]*np.conj(coeff[hc.row[take]])*coeff[hc.col[take]]
        block=coo_matrix((values,(labels[hc.row[take]],labels[hc.col[take]])),shape=(dimension,dimension)).tocsr()
        anti=block-block.getH();err=float(np.max(np.abs(anti.data))) if anti.nnz else 0.0
        assert err<2e-12
        block=(block+block.getH())/2
        total+=dimension
        yield k,block
    assert total==len(codes)


def run_momentum(n,twist,output,full_max=6000,count=32):
    answer={"n":n,"spin":2,"twist":twist,"status":"NUMERICAL_DIAGNOSTIC_NO_CERTIFIED_TAIL","representation":"signed_translation","sectors":[]}
    start_all=time.monotonic()
    for m in range(2*n+1):
        for k,h in momentum_blocks(n,m,twist):
            d=h.shape[0]
            if not d:continue
            start=time.monotonic();full=d<=full_max
            if full:values=eigvalsh(h.toarray(),check_finite=False,driver="evr");residual=None
            else:
                values,vectors=eigsh(h,k=min(count,d-2),which="SA",tol=1e-11,ncv=min(d,max(2*count+1,60)))
                residual=float(np.linalg.norm(h@vectors-vectors*values[None,:],ord="fro"))
            row={"magnetization":m,"momentum":k,"multiplicity":1 if m==0 else 2,"dimension":d,"nnz":int(h.nnz),"full":full,"values":values.tolist(),"ritz_residual_frobenius":residual,"seconds":time.monotonic()-start}
            answer['sectors'].append(row);pathlib.Path(output).write_text(json.dumps(answer,indent=2))
            print(n,twist,m,k,d,len(values),values[0],f"{row['seconds']:.3f}s",flush=True)
    answer['seconds']=time.monotonic()-start_all
    assert sum(r['dimension']*r['multiplicity'] for r in answer['sectors'])==5**n
    pathlib.Path(output).write_text(json.dumps(answer,indent=2));return answer


def run(n, twist, full_max=2000, count=32, output=None):
    answer={"n":n,"spin":2,"twist":twist,"status":"NUMERICAL_DIAGNOSTIC_NO_CERTIFIED_TAIL","sectors":[]}
    total_start=time.monotonic()
    for m in range(2*n+1):
        start=time.monotonic();h,codes,h0,h1=sector(n,m,twist);d=h.shape[0]
        if not d:continue
        full=d<=full_max
        if full:
            values=eigvalsh(h.toarray(),check_finite=False,driver="evr")
            residual=None
        else:
            k=min(count,d-2)
            values,vectors=eigsh(h,k=k,which="SA",tol=1e-11,ncv=min(d,max(2*k+1,60)))
            residual=float(np.linalg.norm(h@vectors-vectors*values[None,:],ord="fro"))
        row={"magnetization":m,"multiplicity":1 if m==0 else 2,"dimension":d,"nnz":int(h.nnz),"full":full,"values":values.tolist(),"ritz_residual_frobenius":residual,"seconds":time.monotonic()-start}
        answer['sectors'].append(row)
        print(n,twist,m,d,len(values),values[0],f"{row['seconds']:.3f}s",flush=True)
        if output:pathlib.Path(output).write_text(json.dumps(answer,indent=2))
    answer['seconds']=time.monotonic()-total_start
    assert sum(r['dimension']*r['multiplicity'] for r in answer['sectors'])==5**n
    if output:pathlib.Path(output).write_text(json.dumps(answer,indent=2))
    return answer


if __name__ == '__main__':
    ap=argparse.ArgumentParser();ap.add_argument('n',type=int);ap.add_argument('twist',type=int);ap.add_argument('--count',type=int,default=32);ap.add_argument('--full-max',type=int,default=2000);ap.add_argument('--momentum',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args()
    if a.momentum:run_momentum(a.n,a.twist,a.output,a.full_max,a.count)
    else:run(a.n,a.twist,a.full_max,a.count,a.output)
