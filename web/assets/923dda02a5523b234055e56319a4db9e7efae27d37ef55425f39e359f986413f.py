"""Separate bounded-observable checks and an exact nonunital certificate."""
import json, math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from universal_probe_checks import dense_probe, apply_sites, depol, sector_exact, gad, bloch, P, S, channel, pt
ROOT=Path(__file__).resolve().parent
rng=np.random.default_rng(8102028)
product=[]
for N in [4,8,16,32,64,128,256]:
    for rep in range(40):
        r=rng.normal(size=(N,3)); r/=np.linalg.norm(r,axis=1)[:,None]
        if rep%3:r*=rng.random(N)[:,None]
        if rep%5==0:r=np.tile(r[0],(N,1))
        t=float(10**rng.uniform(-2,.5))
        got=0.
        for a in range(3):
            dist=np.array([1.])
            for pp in (1+r[:,a])/2:dist=np.convolve(dist,[1-pp,pp])
            z=(np.arange(N+1)-N/2)/math.sqrt(N)
            got+=float(dist@np.exp(-t*z*z))
        upper=1+2/math.sqrt(1+t/2)+3*t**1.5/math.sqrt(N)
        product.append({'N':N,'t':t,'score_sum':got,'bound':upper,'slack':upper-got})
        assert got<=upper+1e-11

dense=[]
for N in [2,4,6,8]:
    rho,Js,J2=dense_probe(N)
    for lam in [.4,.58,.8,1.]:
        z=apply_sites(rho,depol(lam),N)
        for t in [.02,.3,1.]:
            value=0.
            for J in Js:
                ev,U=np.linalg.eigh(J)
                obs=(U*np.exp(-t*ev*ev/N))@U.conj().T
                value+=float(np.trace(z@obs).real)
            lower=3-t*float(np.trace(z@J2).real)/N
            dense.append({'N':N,'lambda':lam,'t':t,'score_sum':value,'lower':lower,'slack':value-lower})
            assert value>=lower-1e-11

# Rational radical isolation for GAD eta=1/4, fixed ground occupation 9/10.
ql=F(9879,50000); qu=F(19759,100000); q2=F(39,999)
assert ql*ql<q2<qu*qu
s_lower=(F(681,800)*ql-F(39,800))/(F(39,800)+F(281,800)*ql)
assert s_lower>F(101,100)
assert F(27,40)*qu+F(13,40)<2*(F(37,40)*ql+F(3,40))
f=F(1); terms=[]
for j in range(22):
    terms.append(F(j*(j+1)*(2*j+1)**2)*f*2**j)
    f/=2*j+3
# For j>=21, term ratio = 2(j+2)(2j+3)/(j(2j+1)^2)<1/2.
# Hence the remainder from term 21 is bounded by twice term 21.
C_upper=sum(terms[:21])+2*terms[21]
assert C_upper<140
Ncert=60000
E_upper=F(Ncert)*F(199,400)+140
assert E_upper<F(Ncert,2)
# Exact constant arithmetic for finite-size bounded witness.
assert F(1,12)-F(8,3*4096)-F(2,64)>F(1,24)

q=math.sqrt(float(q2)); ks=gad(.25,.9); A=np.diag([math.sqrt(q),1.])
pair=channel([np.kron(k,l) for k in ks for l in ks],S)
fpair=np.kron(A,A)@pair@np.kron(A,A); pn=float(np.trace(fpair).real); fpair/=pn
s= -sum(float(np.trace(fpair@np.kron(p,p)).real) for p in P)
c,T=bloch(ks)
# Eight Bloch vectors matching limiting first/second fluctuation moments.
rs=[]
for zz,rad in [(17/20,1/math.sqrt(10)),(7/20,math.sqrt(2/5))]:
    for sx in [-1,1]:
        for sy in [-1,1]:rs.append([sx*rad,sy*rad,zz])
rs=np.array(rs)
mean_error=float(np.linalg.norm(rs.mean(0)-c))
Q_error=float(np.linalg.norm(rs.T@rs/8-(np.outer(c,c)+T@T.T)))
assert mean_error<1e-12 and Q_error<1e-12
out={'status':'internal diagnostics; rational certificate exact, floating checks not a general proof',
     'seed':8102028,'product_checks':len(product),'dense_target_checks':len(dense),
     'minimum_product_bound_slack':min(v['slack'] for v in product),
     'minimum_target_lower_slack':min(v['slack'] for v in dense),
     'nonunital_certificate':{'eta':'1/4','ground_occupation':'9/10','N':Ncert,
       'q_squared':str(q2),'q_interval':[str(ql),str(qu)],'s_lower':str(s_lower),
       's_normal_numerical':s,'naive_affine_score':float(c@c+np.sum(T*T)),
       'C_exact_upper':str(C_upper),'C_upper_float':float(C_upper),
       'filtered_J2_upper':str(E_upper),'separable_floor':str(F(Ncert,2)),
       'pair_PT_min_numerical':float(np.linalg.eigvalsh(pt(pair,2)).min()),
       'pair_filter_success':pn,'physical_log_success_leading_per_qubit':.5*math.log(pn),
       'gaussian_match_Bloch_mean_error':mean_error,'gaussian_match_Q_error':Q_error},
     'bounded_witness_constants':{'N_times_s_minus_1_min':4096,'TV_lower':'(s-1)^2/72',
       'sufficient_independent_copies':'10368 (s-1)^(-4) log(2/alpha)'},
     'product_rows':product,'dense_rows':dense}
(ROOT/'bounded_witness_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k not in ['product_rows','dense_rows']},indent=2))
