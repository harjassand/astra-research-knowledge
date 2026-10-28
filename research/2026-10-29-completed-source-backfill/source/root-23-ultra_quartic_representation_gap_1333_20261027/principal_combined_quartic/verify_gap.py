"""Root's independent exact replay of BOTH sides of the quartic gap.
Only stdlib polynomial operations from this root's verifier are imported;
neither positive/negative producer nor a symbolic/numerical package is used.
"""
from verify_dual import plus,times,scale,dx,var,invariants,energy,ldl,Q
from pathlib import Path
from itertools import combinations_with_replacement as cw
import json,hashlib,time
ROOT=Path(__file__).resolve().parent
def main():
    start=time.monotonic();path=ROOT.parent/'quartic_alternative/sector_gap/EXACT_MULTIPLIER_SUPPORT.json'
    raw=path.read_bytes();d=json.loads(raw)
    assert d['coefficient_vector']==['1','1','113/10','-83/10','0','0','4','-4','0']
    a=[var(i) for i in range(4)];x=[var(i+4) for i in range(4)];f=energy(a)
    u,v,w,q=invariants(a);qx=invariants(x)[3]
    kappa=plus(scale(plus(u,scale(v,-1)),Q(d['alpha'])),scale(q,Q(d['delta'])))
    bregman=plus(energy([plus(ai,xi) for ai,xi in zip(a,x)]),scale(f,-1),
       *(scale(times(dx(f,i),x[i]),-1) for i in range(4)),scale(times(kappa,qx),-1))
    norm2=plus(*(times(t,t) for t in x));target=times(norm2,bregman)
    z=[times(ai,times(x[j],x[k])) for ai in a for j,k in cw(range(4),2)]
    z += [times(x[i],times(x[j],x[k])) for i,j,k in cw(range(4),3)]
    assert len(z)==60
    R=[list(map(Q,row)) for row in d['gram']]
    assert len(R)==60 and all(len(row)==60 for row in R)
    assert all(R[i][j]==R[j][i] for i in range(60) for j in range(60))
    rebuilt={}
    for i in range(60):
        for j in range(i,60):rebuilt=plus(rebuilt,scale(times(z[i],z[j]),R[i][j]*(1 if i==j else 2)))
    assert rebuilt==target
    rho=Q(d['gram_margin']);assert rho==Q(1,200)
    pivots=ldl([[R[i][j]-(rho if i==j else 0) for j in range(60)] for i in range(60)])
    assert pivots==list(map(Q,d['shifted_LDL_pivots']))
    # Full26 dual reconstructed from the SAME literal tau113/10 polynomial.
    dualraw=(ROOT/'EXACT_SUPPORT_SEPARATOR.json').read_bytes();du=json.loads(dualraw)
    functional=dict(zip(map(tuple,du['monomial_order']),map(Q,du['lambda'])))
    def apply(p):return sum((c*functional[e] for e,c in p.items()),Q(0))
    rawbregman=plus(bregman,times(kappa,qx))
    assert apply(rawbregman)==Q(-39,125000)
    assert all(apply(times(times(a[i],a[j]),qx))==0 for i,j in cw(range(4),2))
    z26=[times(ai,xi) for ai in a for xi in x]+[times(x[i],x[j]) for i,j in cw(range(4),2)]
    moment=[[apply(times(zi,zj)) for zj in z26] for zi in z26]
    assert ldl(moment)==list(map(Q,du['positive_ldl_pivots']))
    # Independent full35-dimensional sensitivity and weighted Gram coverage.
    one={(0,)*8:Q(1)}
    def product_indices(variables,indices):
        p=one
        for i in indices:p=times(p,variables[i])
        return p
    pairings=[];weighted_l1_bounds=[]
    shifted=[plus(ai,xi) for ai,xi in zip(a,x)]
    for indices in cw(range(4),4):
        monomial=product_indices(a,indices)
        breg=plus(product_indices(shifted,indices),scale(monomial,-1),
          *(scale(times(dx(monomial,i),x[i]),-1) for i in range(4)))
        pairings.append(apply(breg))
        weighted_l1_bounds.append(sum(abs(v) for v in times(norm2,breg).values()))
    sensitivity=sum(map(abs,pairings),Q(0))
    assert len(pairings)==35 and sensitivity==Q(69749,25000)
    assert max(weighted_l1_bounds)<=44 and sum(weighted_l1_bounds)<=1540
    gram_span=set()
    for zi in z:
        for zj in z:gram_span.update(times(zi,zj))
    assert len(gram_span)==658
    assert all(e in gram_span for e in target)
    radius=Q(1,616000)
    assert rho-1540*radius==Q(1,400)
    assert Q(-39,125000)+sensitivity*radius<0
    receipt={'status':'BOTH_EXACT_CERTIFICATES_INDEPENDENTLY_REBUILT_AND_PASSED',
      'positive_certificate_sha256':hashlib.sha256(raw).hexdigest(),
      'negative_certificate_sha256':hashlib.sha256(dualraw).hexdigest(),
      'literal_candidate':'u^2+v^2+3w^2+(113/10)q^2+4q(u-v)',
      'positive_polynomial_equations':d['exact_polynomial_equations'],
      'positive_shifted_gram_pivots':len(pivots),'negative_moment_pivots':26,
      'all_ten_quadratic_selector_pairings':'EXACTLY_ZERO',
      'negative_bregman_pairing':'-39/125000',
      'global_support_remainder_lower_bound':'|A|^2|X|^2/400+|X|^4/1200',
      'full35_monomial_dual_sensitivity_l1':str(sensitivity),
      'full35_coefficient_sup_norm_radius':str(radius),
      'weighted_gram_monomial_span':len(gram_span),
      'seconds':time.monotonic()-start,
      'scope':'Finite polynomial/PSD facts independently established. Analytic support-to-PC/QC and all-degree SOS impossibility are proved in GAP_PROOF.md; no world priority, physical capability or full Morrey theorem follows.'}
    (ROOT/'INDEPENDENT_GAP_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
