#!/usr/bin/env python3
"""Bounded exact 2-species checks; no SDE execution or large-N certificate."""
import itertools,json,pathlib,time
import sympy as s
R=s.Rational
ROOT=pathlib.Path(__file__).resolve().parent
t0=time.monotonic()

def clean(x):return x.applyfunc(s.simplify)
def tensor(xs):
    z=s.ones(1)
    for x in xs:z=s.kronecker_product(z,x)
    return z
def dk(r,n,v):
    z=s.zeros(r.rows**n)
    for j in range(n):
        xs=[r]*n;xs[j]=v;z+=tensor(xs)
    return z
def collective(f,n):
    z=s.zeros(f.rows**n)
    for j in range(n):
        xs=[s.eye(f.rows)]*n;xs[j]=f;z+=tensor(xs)
    return z
def v(r,f):return f*r+r*f-2*s.trace(f*r)*r
def w(r,f):return -s.I*(f*r-r*f)

rp=s.diag(R(2,5),R(3,5));rq=s.diag(R(1,2),R(1,3),R(1,6))
fp=s.Matrix([[0,1],[1,0]])+s.diag(1,-1)/4
fq=s.Matrix([[0,1,0],[1,0,0],[0,0,0]])+s.diag(1,1,-2)/3
assert s.trace(fp*rp)!=0 and s.trace(fq*rq)!=0
checks=0
det_checks=0
for np,nq in [(1,1),(1,2),(2,1)]:
    kp,kq=tensor([rp]*np),tensor([rq]*nq)
    k=s.kronecker_product(kp,kq)
    jp=s.kronecker_product(collective(fp,np),s.eye(3**nq))
    jq=s.kronecker_product(s.eye(2**np),collective(fq,nq))
    vp,vq=v(rp,fp),v(rq,fq)
    wp,wq=w(rp,fp),w(rq,fq)
    bp,bq=2*np*s.trace(fp*rp),2*nq*s.trace(fq*rq)
    dpk,dqk=dk(rp,np,vp),dk(rq,nq,vq)
    drp,drq=dk(rp,np,wp),dk(rq,nq,wq)
    assert clean(jp*k+k*jp-bp*k-s.kronecker_product(dpk,kq))==s.zeros(k.rows)
    assert clean(jq*k+k*jq-bq*k-s.kronecker_product(kp,dqk))==s.zeros(k.rows)
    assert clean(jp*k-k*jp-s.I*s.kronecker_product(drp,kq))==s.zeros(k.rows)
    assert clean(jq*k-k*jq-s.I*s.kronecker_product(kp,drq))==s.zeros(k.rows)
    BpBq=bp*bq*k+bp*s.kronecker_product(kp,dqk)+bq*s.kronecker_product(dpk,kq)+s.kronecker_product(dpk,dqk)
    RpRq=s.kronecker_product(drp,drq)
    assert clean(BpBq-RpRq-2*(jp*jq*k+k*jp*jq))==s.zeros(k.rows)
    checks+=5
    # Cross local-filter drift and log determinant convention.
    delta=R(1,10000);n=np+nq
    ap=delta*nq/(2*n)*s.trace(fq*rq)*vp
    aq=delta*np/(2*n)*s.trace(fp*rp)*vq
    assert s.simplify(s.trace(rp.inv()*ap)+2*delta*nq/n*s.trace(fp*rp)*s.trace(fq*rq))==0
    assert s.simplify(s.trace(rq.inv()*aq)+3*delta*np/n*s.trace(fp*rp)*s.trace(fq*rq))==0
    det_checks+=2

def basis(d):
    fs=[];gs=[]
    for i in range(d):
        for j in range(i+1,d):
            x,y=s.zeros(d),s.zeros(d)
            x[i,j]=x[j,i]=1;y[i,j]=-s.I;y[j,i]=s.I
            fs.extend([x,y]);gs.extend([s.Integer(2)]*2)
    for j in range(1,d):
        fs.append(s.diag(*([1]*j+[-j]+[0]*(d-j-1))))
        gs.append(s.Integer(j*(j+1)))
    return fs,gs
def iso_form(r,fs,gs):
    V=s.Matrix([[s.trace(z*v(r,f)) for f in fs] for z in fs])
    W=s.Matrix([[s.trace(z*w(r,f)) for f in fs] for z in fs])
    gi=s.diag(*[1/g for g in gs])
    return clean(V*gi*V.T-W*gi*W.T),V,W
def psd(a):
    assert clean(a-a.H)==s.zeros(a.rows)
    count=0
    for k in range(1,a.rows+1):
        for ix in itertools.combinations(range(a.rows),k):
            t=s.factor(a.extract(ix,ix).det());assert t>=0,(ix,t);count+=1
    return count
fpb,gp=basis(2);fqb,gq=basis(3)
Dp,Vp,Wp=iso_form(rp,fpb,gp)
Dq,Vq,Wq=iso_form(rq,fqb,gq)
np,nq=1,2;n=3;alpha_p=1;alpha_q=2;delta=R(1,10000)
# Only the two normalized X axes interact, so global offblock B has norm 1.
# Both axis squared norms are 2; the 1/sqrt(2*2) coefficient is exactly 1/2.
X=delta/(4*n)*(Vp[:,0]*Vq[:,0].T-Wp[:,0]*Wq[:,0].T)
gamma=R(1,600) # public gap alpha_min*eta^2/(2N), eta=1/10.
P=R(alpha_p,np)*Dp-gamma*s.diag(*gp)
Q=R(alpha_q,nq)*Dq-gamma*s.diag(*gq)
schur=clean(Q-X.T*P.inv()*X)
p_minors=psd(P);s_minors=psd(schur)
assert p_minors==7 and s_minors==255
assert P.det()>0

# Heterogeneous local dimensions: the parity-sign mixture has exactly
# (I+P tensor Q)/6 for r=2, without equal-dimensional local factors.
F=fpb[0];G=fqb[6]
parity=(s.kronecker_product((s.eye(2)+F)/2,(s.eye(3)+G)/3)+s.kronecker_product((s.eye(2)-F)/2,(s.eye(3)-G)/3))/2
assert clean(parity-(s.eye(6)+s.kronecker_product(F,G))/6)==s.zeros(6)

out={'status':'PASS_EXACT_SMALL_FIXTURES_ONLY','species_dimensions':[2,3],'population_checks':[[1,1],[1,2],[2,1]],'cross_product_kernel_identities':checks,'local_cross_logdet_drift_checks':det_checks,'covariance_gap_fixture':{'Np':1,'Nq':2,'alpha':[1,2],'delta':str(delta),'eta':'1/10','M':1,'gamma':str(gamma),'Schur_complement_PSD_principal_minors':[p_minors,s_minors]},'unequal_dimension_separable_parity_identity':True,'large_N_or_SDE_execution':False,'priority':'UNKNOWN','wall_seconds':time.monotonic()-t0}
(ROOT/'multispecies_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
