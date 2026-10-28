"""Independent stdlib consumer of both enabling Grams and shifted-support SOS.

Literal polynomials rebuilt with Fraction arithmetic, separate translation
expansion for BF, and exact Fraction LDL positivity (producer uses Bareiss).
No producer import, SymPy, NumPy, CVXPY, or floating PSD premise.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement as cwr, product
from pathlib import Path
import json
import math
import time

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]


def mon(ii,n=4):
    return tuple(ii.count(i) for i in range(n))


def addexp(e,f):
    return tuple(x+y for x,y in zip(e,f))


def psum(*polys):
    out={}
    for p in polys:
        for e,c in p.items():out[e]=out.get(e,Q(0))+c
    return {e:c for e,c in out.items() if c}


def sc(c,p):
    return {e:c*v for e,v in p.items() if c*v}


def mul(p,r):
    out={}
    for e,c in p.items():
        for f,d in r.items():
            g=addexp(e,f)
            out[g]=out.get(g,Q(0))+c*d
    return {e:c for e,c in out.items() if c}


def sq(p):return mul(p,p)


def gram_poly(gram,features,denom):
    out={}
    for i,e in enumerate(features):
        for j,f in enumerate(features):
            g=addexp(e,f)
            out[g]=out.get(g,Q(0))+Q(gram[i][j],denom)
    return {e:c for e,c in out.items() if c}


def positive_ldl(mat):
    n=len(mat)
    lower=[[Q(0) for j in range(n)] for i in range(n)]
    diag=[]
    for i in range(n):
        pivot=mat[i][i]-sum((lower[i][k]**2*diag[k] for k in range(i)),Q(0))
        assert pivot>0,(i,pivot)
        diag.append(pivot)
        for j in range(i+1,n):
            assert mat[j][i]==mat[i][j]
            lower[j][i]=(mat[j][i]-sum((lower[j][k]*lower[i][k]*diag[k]
                                      for k in range(i)),Q(0)))/pivot
    return min(diag)


aa,bb,cc,dd=[{mon((i,)):Q(1)} for i in range(4)]
u,v=psum(sq(aa),sq(cc)),psum(sq(bb),sq(dd))
w=psum(mul(aa,bb),mul(cc,dd))
q=psum(mul(aa,dd),sc(-1,mul(bb,cc)))
T=psum(u,v)
x,y,z=psum(u,sc(-1,v)),sc(2,w),sc(2,q)
F=psum(sc(Q(55220381,10**10),psum(sq(u),sq(v))),
        sc(Q(114430029,625000000),mul(u,v)),
        sc(-Q(801761987,5000000000),sq(w)),
        sc(Q(118849817,4000000000),mul(q,x)))
p=psum(sc(Q(6222019,200000000),mul(sq(x),x)),
        sc(Q(1686519911,10**10),mul(sq(x),z)),
        sc(Q(81172813,2000000000),mul(x,sq(z))),
        sc(Q(1726116771,10**10),mul(sq(z),z)),
        sc(Q(128626163,5000000000),mul(x,sq(y))),
        sc(Q(373321239,2000000000),mul(sq(y),z)))


def main():
    start=time.monotonic()
    bf={}
    for e,c in F.items():
        for k in product(*(range(v+1) for v in e)):
            if sum(k)<2:continue
            ex=tuple(a-b for a,b in zip(e,k))+k
            bf[ex]=bf.get(ex,Q(0))+c*math.prod(math.comb(a,b) for a,b in zip(e,k))
    bf={e:c for e,c in bf.items() if c}
    TA={e+(0,0,0,0):c for e,c in T.items()}
    TX={(0,0,0,0)+e:c for e,c in T.items()}
    QX={(0,0,0,0)+e:c for e,c in q.items()}
    PA={e+(0,0,0,0):c for e,c in p.items()}
    raw26=json.loads((OUT/'EXACT26_SUPPORT_GRAM.json').read_text())
    C=Q(raw26['C'])
    assert C==Q(33,400)
    f26=[tuple(e) for e in raw26['features']]
    expected=[mon((i,)) +mon((j,)) for i in range(4) for j in range(4)]
    expected += [(0,0,0,0)+mon(ii) for ii in cwr(range(4),2)]
    assert f26==expected
    assert gram_poly(raw26['gram_numerators'],f26,raw26['gram_denominator'])==psum(bf,sc(C,mul(TA,TX)))
    margin26=Q(raw26['proved_Gram_margin'])
    g26=[[Q(v,raw26['gram_denominator'])-(margin26 if i==j else 0)
           for j,v in enumerate(row)] for i,row in enumerate(raw26['gram_numerators'])]
    pivot26=positive_ldl(g26)
    raw35=json.loads((OUT/'EXACT35_LEADING_GRAM.json').read_text())
    f35=[tuple(e) for e in raw35['features']]
    assert f35==[mon(ii) for ii in cwr(range(4),4)]
    leading=psum(sc(3,mul(sq(T),F)),sc(-1,mul(p,q)))
    assert gram_poly(raw35['gram_numerators'],f35,raw35['gram_denominator'])==leading
    margin35=Q(raw35['proved_Gram_margin'])
    g35=[[Q(v,raw35['gram_denominator'])-(margin35 if i==j else 0)
           for j,v in enumerate(row)] for i,row in enumerate(raw35['gram_numerators'])]
    pivot35=positive_ldl(g35)
    # Stronger scalar leading floor: weighted feature counts imply5/12 T^4.
    multinomial=[math.factorial(4)//math.prod(math.factorial(j) for j in e) for e in f35]
    stronger=[[Q(v,raw35['gram_denominator'])-(Q(multinomial[i],960000) if i==j else 0)
               for j,v in enumerate(row)] for i,row in enumerate(raw35['gram_numerators'])]
    leading_floor_pivot=positive_ldl(stronger)
    # Independently reassemble the literal X=-A map and its integer congruence.
    old=json.loads((ROOT/'work/sol8_opportunity_selection_20261027/rational_selector/EXACT_RATIONAL_SUPPORT.json').read_text())
    feats180=[mon(ai)+mon((j,)) for ai in cwr(range(4),3) for j in range(4)]
    feats180 += [mon(ai)+mon(xi) for ai in cwr(range(4),2) for xi in cwr(range(4),2)]
    index={e:i for i,e in enumerate(f35)}
    rows=[(index[addexp(e[:4],e[4:])],(-1)**sum(e[4:])) for e in feats180]
    assert rows==[tuple(r) for r in raw35['map_rows']]
    rebuilt=[[0]*35 for _ in range(35)]
    for i,(a,s) in enumerate(rows):
        for j,(b,t) in enumerate(rows):
            rebuilt[a][b]+=s*t*old['gram_integer_matrix'][i][j]
    assert rebuilt==raw35['gram_numerators']
    assert old['gram_denominator']==raw35['gram_denominator']
    counts=[sum(a==i for a,s in rows) for i in range(35)]
    assert counts==raw35['feature_multiplicities']
    assert min(counts)==2
    assert min(Q(c,m) for c,m in zip(counts,multinomial))==Q(5,12)
    # Literal denominator-shift compiler at the largest allowed sigma and a
    # conservative interior sigma. The symbolic algebra is checked by polynomials.
    one={(0,)*8:Q(1)}
    eps=Q(1,100)
    shift_rows=[]
    for sigma in [eps/(2*C),eps/(4*C)]:
        H=psum(TA,sc(sigma,one))
        lhs=psum(mul(sq(H),bf),sc(-1,mul(PA,QX)),sc(eps,mul(sq(H),TX)))
        original=psum(mul(sq(TA),bf),sc(-1,mul(PA,QX)))
        factor=psum(sc(2*sigma,TA),sc(sigma*sigma,one))
        residual=psum(sc(eps-2*C*sigma,sq(TA)),sc(sigma*(2*eps-C*sigma),TA),sc(eps*sigma*sigma,one))
        rhs=psum(original,mul(factor,psum(bf,sc(C,mul(TA,TX)))),mul(residual,TX))
        assert lhs==rhs
        coefficients=[eps-2*C*sigma,sigma*(2*eps-C*sigma),eps*sigma*sigma]
        assert min(coefficients)>=0
        shift_rows.append({'epsilon':str(eps),'sigma':str(sigma),'residual_coefficients':list(map(str,coefficients))})
    # Interior choice retains a uniform eps/2 quadratic SOS margin.
    sigma=eps/(4*C)
    H=psum(TA,sc(sigma,one))
    lhs=psum(mul(sq(H),bf),sc(-1,mul(PA,QX)),sc(eps/2,mul(sq(H),TX)))
    original=psum(mul(sq(TA),bf),sc(-1,mul(PA,QX)))
    factor=psum(sc(2*sigma,TA),sc(sigma*sigma,one))
    strong_coeffs=[eps/2-2*C*sigma,sigma*(eps-C*sigma),eps*sigma*sigma/2]
    strong_residual=psum(sc(strong_coeffs[0],sq(TA)),sc(strong_coeffs[1],TA),sc(strong_coeffs[2],one))
    rhs=psum(original,mul(factor,psum(bf,sc(C,mul(TA,TX)))),mul(strong_residual,TX))
    assert lhs==rhs and min(strong_coeffs)>=0
    # Preserve the accepted quartic and T-weighted margins simultaneously.
    gamma=Q(1,400000)
    mu=margin26
    assert mu>=gamma/2
    def squares_of_monomials(degree,in_x=False):
        out={}
        for ii in cwr(range(4),degree):
            e=tuple(2*j for j in mon(ii))
            out[((0,0,0,0)+e) if in_x else (e+(0,0,0,0))]=Q(1)
        return out
    S3A=squares_of_monomials(3)
    S2A=squares_of_monomials(2)
    S2X=squares_of_monomials(2,True)
    Z180norm=psum(mul(S3A,TX),mul(S2A,S2X))
    Z26norm=psum(mul(TA,TX),S2X)
    Rzero=psum(original,sc(-gamma,Z180norm))
    Szero=psum(bf,sc(C,mul(TA,TX)),sc(-mu,Z26norm))
    oddnorm=psum(S3A,sc(-Q(1,6),mul(sq(TA),TA)))
    evennorm=psum(S2A,sc(-Q(1,2),sq(TA)))
    Xnorm=psum(S2X,sc(-Q(1,2),sq(TX)))
    for diagonal_sos in [oddnorm,evennorm,Xnorm]:
        assert all(c>=0 and all(j%2==0 for j in e) for e,c in diagonal_sos.items())
    full_lhs=psum(lhs,sc(-gamma/6,mul(sq(H),mul(TA,TX))),
                   sc(-gamma/4,mul(sq(H),sq(TX))))
    full_rhs=psum(Rzero,sc(gamma,mul(oddnorm,TX)),
                  sc(gamma,mul(evennorm,S2X)),mul(factor,Szero),
                  sc(mu-gamma/6,mul(factor,mul(TA,TX))),
                  sc(mu-gamma/2,mul(factor,S2X)),
                  sc(gamma/2,mul(sq(H),Xnorm)),mul(strong_residual,TX))
    assert full_lhs==full_rhs
    out={'status':'INDEPENDENT_LITERAL_AND_LDL_COMPILER_REPLAY_PASSED',
         'C':str(C),'G26_margin':str(margin26),'G35_margin':str(margin35),
         'G26_shifted_LDL_min_pivot':str(pivot26),'G35_shifted_LDL_min_pivot':str(pivot35),
         'P8_minus_norm8_floor':'1/960000','stronger_floor_LDL_min_pivot':str(leading_floor_pivot),
         'feature_multiplicity_range':[min(counts),max(counts)],
         'sigma_max_per_epsilon':str(1/(2*C)),'sigma_interior_per_epsilon':str(1/(4*C)),
         'shift_examples':shift_rows,'strong_interior_residual_coefficients':list(map(str,strong_coeffs)),
         'uniform_quadratic_SOS_margin_per_epsilon':'1/2',
         'preserved_original_T_weighted_SOS_margin':str(gamma/6),
         'preserved_original_quartic_SOS_margin':str(gamma/4),
         'full_preserved_margin_decomposition':'LITERAL_ALL_COEFFICIENTS_PASSED',
         'seconds':time.monotonic()-start,
         'scope':'Independent code-path exact reconstruction, not a separate peer review. '
                 'Proves both literal Gram identities, PD margins, direct congruence and shifted-support algebra. '
                 'Global70-conic padding and calibrated local exactness are separate tasks.'}
    (OUT/'INDEPENDENT_COMPILER_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','C','G26_margin','G35_margin',
         'P8_minus_norm8_floor','sigma_max_per_epsilon','sigma_interior_per_epsilon','seconds']},indent=2))


if __name__=='__main__':main()
