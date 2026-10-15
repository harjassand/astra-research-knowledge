#!/usr/bin/env python3
"""Standalone integer proof of complete A^2 H^2 null-correction spaces.

No symbolic package, numerical optimization, source files or stored certificate
is an input. Nonzero minors are certified over a finite prime field. Together
with exact image containment they prove the rational and real ranks.
"""
from collections import defaultdict
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib,json,time

ROOT=Path(__file__).resolve().parent
PRIME=1009
assert all(PRIME%d for d in range(2,32))
tick=time.monotonic()
jets=[(c,i,n-i) for n in range(1,5) for c in range(2) for i in range(n,-1,-1)]
ji={j:i for i,j in enumerate(jets)}
A=[ji[(0,1,0)],ji[(0,0,1)],ji[(1,1,0)],ji[(1,0,1)]]
H=[ji[(0,2,0)],ji[(0,1,1)],ji[(0,0,2)],ji[(1,2,0)],ji[(1,1,1)],ji[(1,0,2)]]
apairs=list(combinations_with_replacement(range(4),2))
hpairs=list(combinations_with_replacement(range(6),2))
labels=[(aa,hh) for aa in apairs for hh in hpairs]
index={label:i for i,label in enumerate(labels)}
def mon(*inds):
    e=[0]*len(jets)
    for i in inds:e[i]+=1
    return tuple(e)
def pd(p,i):
    out={}
    for e,v in p.items():
        if e[i]:
            ee=list(e);ee[i]-=1;out[tuple(ee)]=v*e[i]
    return out
def total(p,axis):
    out=defaultdict(int)
    for e,v in p.items():
        for i,k in enumerate(e):
            if not k:continue
            c,nx,ny=jets[i];j=ji[(c,nx+(axis==0),ny+(axis==1))]
            ee=list(e);ee[i]-=1;ee[j]+=1;out[tuple(ee)]+=v*k
    return {e:v for e,v in out.items() if v}
def euler(p,c):
    out=defaultdict(int)
    for nx,ny in [(1,0),(0,1),(2,0),(1,1),(0,2)]:
        q=pd(p,ji[(c,nx,ny)])
        for _ in range(nx):q=total(q,0)
        for _ in range(ny):q=total(q,1)
        for e,v in q.items():out[e]+=(-1)**(nx+ny)*v
    return {e:v for e,v in out.items() if v}

mons=[mon(*(A[i] for i in aa),*(H[i] for i in hh)) for aa,hh in labels]
ecols=[{(c,e):v for c in range(2) for e,v in euler({m:1},c).items()} for m in mons]
erows=sorted(set(k for col in ecols for k in col));eri={k:i for i,k in enumerate(erows)}
E=[{eri[k]:v for k,v in col.items()} for col in ecols]

alpha_labels=[(aa,j) for aa in combinations_with_replacement(range(4),3) for j in range(4)]
b1=[0,1,3,4];b2=[1,2,4,5]
ncols=[]
for aa,j in alpha_labels:
    out=defaultdict(int)
    for k in range(4):
        mult=aa.count(k)
        if not mult:continue
        bb=list(aa);bb.remove(k)
        out[index[(tuple(bb),tuple(sorted((b1[k],b2[j]))))]]+=mult
        out[index[(tuple(bb),tuple(sorted((b2[k],b1[j]))))]]-=mult
    ncols.append({i:v for i,v in out.items() if v})
assert len(E)==210 and len(erows)==696 and len(ncols)==80

def apply(cols,v):
    out=defaultdict(int)
    for j,c in v.items():
        for i,a in cols[j].items():out[i]+=a*c
    return {i:a for i,a in out.items() if a}
assert all(not apply(E,n) for n in ncols)  # exact Euler-after-pullback = zero

def rows_from_columns(cols,nrows):
    rows=[{} for _ in range(nrows)]
    for j,col in enumerate(cols):
        for i,a in col.items():rows[i][j]=a
    return rows
def modular_minor(rows,ncols):
    """Return pivot row/column labels and determinant of that minor mod PRIME."""
    work=[{j:a%PRIME for j,a in row.items() if a%PRIME} for row in rows]
    names=list(range(len(rows)));pivrows=[];pivcols=[];det=1;sign=1;r=0
    for c in range(ncols):
        pivot=next((i for i in range(r,len(work)) if work[i].get(c,0)),None)
        if pivot is None:continue
        if pivot!=r:
            work[r],work[pivot]=work[pivot],work[r]
            names[r],names[pivot]=names[pivot],names[r];sign=-sign
        v=work[r][c];det=det*v%PRIME
        inv=pow(v,-1,PRIME);rr={j:a*inv%PRIME for j,a in work[r].items() if j>=c}
        work[r]=rr;pivrows.append(names[r]);pivcols.append(c)
        for i in range(r+1,len(work)):
            f=work[i].get(c,0)
            if not f:continue
            wi=work[i]
            for j,a in rr.items():
                v=(wi.get(j,0)-f*a)%PRIME
                if v:wi[j]=v
                elif j in wi:del wi[j]
        r+=1
        if r==len(work):break
    # The accumulated row-swap sign is relative to all rows, whereas the
    # selected minor uses recorded original pivot-row order; eliminate the
    # selected minor independently to report its actual determinant.
    minor=[[rows[i].get(j,0)%PRIME for j in pivcols] for i in pivrows]
    md=1
    for k in range(r):
        p=next(i for i in range(k,r) if minor[i][k])
        if p!=k:minor[k],minor[p]=minor[p],minor[k];md=-md
        v=minor[k][k];md=md*v%PRIME;iv=pow(v,-1,PRIME)
        for i in range(k+1,r):
            f=minor[i][k]*iv%PRIME
            for j in range(k+1,r):minor[i][j]=(minor[i][j]-f*minor[k][j])%PRIME
            minor[i][k]=0
    assert md%PRIME
    return {'rank_mod_prime':r,'rows':pivrows,'columns':pivcols,'determinant_mod_prime':md%PRIME}

em=modular_minor(rows_from_columns(E,696),210)
nm=modular_minor(rows_from_columns(ncols,210),80)
assert em['rank_mod_prime']==165 and nm['rank_mod_prime']==45
# rank(E)>=165, rank(N)>=45 and EN=0 imply exact ranks and ker E=im N.

# Infinitesimal common output rotation acting on A and on H.
rotation_pairs=[(0,2),(1,3)]
rotcols=[]
for aa,hh in labels:
    out=defaultdict(int)
    for indices,pairs,other,is_a in [(aa,[(0,2),(1,3)],hh,True),(hh,[(0,3),(1,4),(2,5)],aa,False)]:
        for lo,hi in pairs:
            for source,target,sgn in [(lo,hi,-1),(hi,lo,1)]:
                mult=indices.count(source)
                if not mult:continue
                changed=list(indices);changed.remove(source);changed.append(target);changed=tuple(sorted(changed))
                key=(changed,other) if is_a else (other,changed)
                out[index[key]]+=sgn*mult
    rotcols.append({i:v for i,v in out.items() if v})
rotation_minor=modular_minor(rows_from_columns(rotcols,210),210)
assert rotation_minor['rank_mod_prime']==138
stack=[{**ecol,**{696+i:v for i,v in rcol.items()}} for ecol,rcol in zip(E,rotcols)]
stack_minor=modular_minor(rows_from_columns(stack,906),210)
assert stack_minor['rank_mod_prime']==195

# Explicit 32 invariant cubic primitives, generating all 15 invariant corrections.
# Linear one-forms are represented as (coefficient, A-variable, dA-component).
quadratics={
 'u':[(1,(0,0)),(1,(2,2))],
 'v':[(1,(1,1)),(1,(3,3))],
 'w':[(1,(0,1)),(1,(2,3))],
 'q':[(1,(0,3)),(-1,(1,2))]}
linear_forms={
 'du':[(2,0,0),(2,2,2)],'dv':[(2,1,1),(2,3,3)],
 'dw':[(1,1,0),(1,0,1),(1,3,2),(1,2,3)],
 'dq':[(1,3,0),(-1,2,1),(-1,1,2),(1,0,3)],
 'theta_u':[(1,0,2),(-1,2,0)],'theta_v':[(1,1,3),(-1,3,1)],
 'theta_cross':[(1,0,3),(1,1,2),(-1,2,1),(-1,3,0)],
 'zeta':[(1,0,1),(1,2,3),(-1,1,0),(-1,3,2)]}
ai={label:i for i,label in enumerate(alpha_labels)}
invlabels=[];invcols=[];invalpha=[]
for qname,qt in quadratics.items():
    for lname,lt in linear_forms.items():
        ac=defaultdict(int)
        for qco,qa in qt:
            for lco,lv,lc in lt:ac[ai[(tuple(sorted((*qa,lv))),lc)]]+=qco*lco
        ac={i:v for i,v in ac.items() if v};nc=apply(ncols,ac)
        assert not apply(rotcols,nc)
        invlabels.append(qname+' * '+lname);invcols.append(nc);invalpha.append(ac)
im=modular_minor(rows_from_columns(invcols,210),32)
assert im['rank_mod_prime']==15
# rank stacked>=195 and 15 independent invariant null columns prove exact
# invariant null dimension 15, with the displayed generators spanning it.

# Seventy-two explicit invariant densities establish the upper rank bound
# for the rotation map; no floating weight-space dimension is assumed.
def qp_mul(aq,hq):
    out=defaultdict(int)
    for ca,aa in aq:
        for ch,hh in hq:out[index[(tuple(sorted(aa)),tuple(sorted(hh)))]]+=ca*ch
    return {i:v for i,v in out.items() if v}
def complex_product(i,j,pairs):
    xi,yi=pairs[i];xj,yj=pairs[j]
    return [(1,(xi,xj)),(-1,(yi,yj))],[(1,(xi,yj)),(1,(yi,xj))]
hinv=[];hp=[(0,3),(1,4),(2,5)]
for i in range(3):
    xi,yi=hp[i];hinv.append([(1,(xi,xi)),(1,(yi,yi))])
for i in range(3):
    for j in range(i+1,3):
        xi,yi=hp[i];xj,yj=hp[j]
        hinv.extend([[(1,(xi,xj)),(1,(yi,yj))],[(1,(xi,yj)),(-1,(yi,xj))]])
allinv=[qp_mul(aq,hq) for aq in quadratics.values() for hq in hinv]
for i in range(2):
    for j in range(i,2):
        ar,az=complex_product(i,j,[(0,2),(1,3)])
        for p in range(3):
            for q0 in range(p,3):
                hr,hz=complex_product(p,q0,hp)
                re=defaultdict(int);imag=defaultdict(int)
                for col,sgn in [(qp_mul(ar,hr),1),(qp_mul(az,hz),1)]:
                    for n,v0 in col.items():re[n]+=sgn*v0
                for col,sgn in [(qp_mul(az,hr),1),(qp_mul(ar,hz),-1)]:
                    for n,v0 in col.items():imag[n]+=sgn*v0
                allinv.extend([{n:v0 for n,v0 in col.items() if v0} for col in [re,imag]])
assert len(allinv)==72 and all(not apply(rotcols,n) for n in allinv)
allinv_minor=modular_minor(rows_from_columns(allinv,210),72)
assert allinv_minor['rank_mod_prime']==72

def digest(columns):
    return hashlib.sha256(json.dumps([sorted(col.items()) for col in columns],separators=(',',':')).encode()).hexdigest()
result={
 'schema':'astra-compatible-null-corrections/1','status':'EXACT_PASS',
 'matrix_order':['a','b','c','d'],
 'compatible_jet_order':['phi1_xx','phi1_xy','phi1_yy','phi2_xx','phi2_xy','phi2_yy'],
 'ambient_density_dimension':210,'no_symmetry_null_dimension':45,
 'left_SO2_invariant_density_dimension':72,'left_SO2_invariant_null_dimension':15,
 'finite_field_prime':PRIME,'euler_matrix_shape':[696,210],
 'euler_sparse_sha256':digest(E),'pullback_sparse_sha256':digest(ncols),
 'euler_nonzero_minor':em,'pullback_nonzero_minor':nm,
 'rotation_nonzero_minor':rotation_minor,'stacked_nonzero_minor':stack_minor,
 'all_invariants_nonzero_minor':allinv_minor,
 'invariant_nonzero_minor':im,
 'full_null_basis_primitives':[{'A_factors':list(alpha_labels[j][0]),'dA_component':alpha_labels[j][1]} for j in nm['columns']],
 'invariant_null_basis_primitives':[invlabels[j] for j in im['columns']],
 'exact_image_containment':'Euler_after_closed_pullback_equals_zero_on_all_80_generators',
 'classification':'Every homogeneous A^2 H^2 null density equals omega_A(B1,B2), omega a unique closed quadratic two-form.',
 'scope':'Local polynomial density at precisely first/second derivative order and bidegree (2,2); not cone equality or QC universality.',
 'historical_novelty':'UNKNOWN; classical null-Lagrangian and differential-form machinery credited',
 'seconds':time.monotonic()-tick}
(ROOT/'NULL_CORRECTION_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','ambient_density_dimension','no_symmetry_null_dimension','left_SO2_invariant_density_dimension','left_SO2_invariant_null_dimension','seconds']},indent=2))
