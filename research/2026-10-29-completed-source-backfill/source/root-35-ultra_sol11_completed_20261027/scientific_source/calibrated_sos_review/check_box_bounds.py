"""Independent whole-cube bounds; does not import the producer evaluator.

Direct weighted binomial sums reconstruct the uniform coefficient bounds,
rather than running the two already independently accepted query examples.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json,math,runpy,time
START=time.monotonic();OUT=Path(__file__).resolve().parent
r=runpy.run_path(str(OUT/'receiver.py'),run_name='read_literal_definitions')
s=r['s'];a=r['a'];F=r['F'];p=r['p'];q=r['q'];T=r['T'];sig=r['sig'];ee=r['ee'];kap=r['kap'];basis=r['basis']
def sym(x):return s.Rational(x.numerator,x.denominator)
def literal(expr):return {e:Q(int(v.p),int(v.q)) for e,v in s.Poly(expr,*a,domain=s.QQ).terms()}
H=F-sym(kap)*q*q;pH=p-2*sym(kap)*q*T*T;D=(T+sym(sig))**2
cof=[s.diff(q,t) for t in a]
parts=[literal(D*(-3*H-sym(ee)*T)+pH*q)]
parts += [literal(D*(s.diff(H,t)+2*sym(ee)*t)-pH*c) for t,c in zip(a,cof)]
parts += [literal(pH)]
ra,rb,rs=Q(1,4000),Q(1,32000),Q(1,10000)
weights=[Q(1)]+[rb]*4+[rs];dn={};db={};n_at_anchor_bound=Q(0)
for j,poly in enumerate(parts):
    for al,c in poly.items():
        n_at_anchor_bound+=abs(c)*ra**sum(al)*weights[j]
        for beta in product(*(range(n+1) for n in al)):
            if sum(beta)<2 or (j==0 and beta==al):continue
            v=abs(c)*math.prod(math.comb(n,k) for n,k in zip(al,beta))*ra**(sum(al)-sum(beta))*weights[j]
            dn[beta]=dn.get(beta,Q(0))+v
for al,c in literal(D).items():
    for beta in product(*(range(n+1) for n in al)):
        if sum(beta)<2:continue
        v=abs(c)*math.prod(math.comb(n,k) for n,k in zip(al,beta))*ra**(sum(al)-sum(beta))
        db[beta]=db.get(beta,Q(0))+v
t_bound=n_at_anchor_bound/sig**2
ds=[{1:Q(1,400),2:Q(1,50),3:Q(9,100),4:Q(3,100)}[sum(e)] for e in basis]
pairs={}
for i,e in enumerate(basis):
    for j in range(i,69):
        al=tuple(v+w for v,w in zip(e,basis[j]));pairs.setdefault(al,[]).append((i,j))
assert len(pairs)==490
rows=[Q(0)]*69
for al,choices in pairs.items():
    best=max(ds[i]*ds[j] for i,j in choices);chosen=[(i,j) for i,j in choices if ds[i]*ds[j]==best]
    coeff=dn.get(al,Q(0))+db.get(al,Q(0))*t_bound
    for i,j in chosen:
        contribution=coeff/(len(chosen)*(1 if i==j else 2)*ds[i]*ds[j])
        rows[i]+=contribution
        if i!=j:rows[j]+=contribution
rho=max(rows)
C=sum(map(abs,literal(H).values()));P=sum(map(abs,literal(pH).values()));rr=ra;bb=2*rb
k0=P*rr**6/sig**2;k1=6*P*rr**5/sig**2+4*P*rr**7/sig**3
k2=30*P*rr**4/sig**2+52*P*rr**6/sig**3+24*P*rr**8/sig**4
L=36*C*rr**2+24*C*rr*bb+k2*(rs+rr**2/2+rr*bb)+2*k1*(rr+bb)+k0
expected=json.loads((OUT.parent/'smooth_conic_interface/LOCAL_EVALUATION.json').read_text())['open_box']
assert rho==Q(expected['scaled_coefficient_Gram_row_bound'])
assert L==Q(expected['Hessian_deviation_from_minus2eI'])
assert rho<Q(9,20)<Q(1,2) and L<ee
assert 2*rb==ra/4 and 4*ra**2<=sig/4
result={'status':'INDEPENDENT_UNIFORM_BOX_BOUNDS_PASSED','rho':str(rho),'display_rho':float(rho),
        'Hessian_deviation':str(L),'display_Hessian_deviation':float(L),'e':str(ee),
        'nuisance_coefficient_bound':'DIRECT_BINOMIAL_WEIGHTED_SUMS',
        'maximum_anchor_radius_norm':'Euclidean ra for root; coordinate ra for coefficient Gram',
        'cube_Gram_PD_fraction':'1-rho>1/2','root_boundary_inward':'2||B||<=ra/2<ra',
        'square_completion_anchor_condition':'4ra^2<=sigma/4',
        'seconds':time.monotonic()-START,
        'scope':'Uniform all-query/all-anchor coefficient and concavity bounds, rebuilt without producer functions. '
                'Does not repeat root peer accepted two actual70 query certificates. Main theorem accepted independently in REVIEW.md.'}
(OUT/'BOX_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','display_rho','display_Hessian_deviation','seconds']},indent=2))
