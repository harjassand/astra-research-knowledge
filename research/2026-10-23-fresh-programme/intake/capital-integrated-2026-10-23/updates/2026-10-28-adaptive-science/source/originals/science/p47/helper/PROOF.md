# All-frequency compliance-dual certificate

27 October 2026. Self-contained derivation by the authorised helper. Governing model and spectral identities are frozen sources F, C and A. The result below is a sufficient certificate, not an assertion that every cap satisfies its coefficient signs. No physical specimen, external audit or historical novelty is asserted.

## 1. The certificate theorem

Fix positive K, theta, total mass M and backbone mass m<M. Write A=4K/m, B=4K/M and let r>0. The actual one-pendant construction in F has bands [0,p] and [r,s], with

p²+s²-r²=A, p²s²/r²=B, 0<p<r<s,

and spring k=r² m(M-m)/M. Its exact CM compliance is C*=1/k. Define g(w)=[w/(2theta)/sinh(w/(2theta))]². There is a unique triple (lambda,a,nu) such that

R(w)=g(w)+lambda/w+a w+nu/w³

vanishes at p,r,s. Uniqueness follows because, after multiplying the three equations by w³, the coefficients of (lambda,a,nu) are (w²,w⁴,1), a Vandermonde matrix at the three distinct positive squared endpoints.

**Theorem.** If

nu<0, a>=0, and either a>0 or lambda>0,

then R is strictly negative exactly on (0,p) union (r,s), and strictly positive on (p,r) union (s,infinity). Therefore this actual one-pendant construction minimizes the full Bose-weighted conductance over every connected positive finite internal network having these m,M,K and CM compliance C<=C*. Its active spectrum is the unique minimizing spectrum. The same proof also admits backbone allocations m_comp>=m, with total mass fixed and the same cap C<=C*, because both charged moment inequalities then have the correct signs.

The endpoint equations plus these three inequalities are finite data. The global sign conclusion is analytic over every w>0; no grid of frequencies is used.

## 2. A Descartes lemma for convergent Laurent series

Let f(x)=sum_(j=j0)^infinity b_j x^j be real analytic on x>0, with only finitely many negative exponents, convergence locally uniform together with derivatives, and finitely many sign changes V among its nonzero coefficients in increasing exponent order. Then f has at most V positive zeros, counting multiplicities.

Proof is by induction on V. When V=0, every term has one sign and f has no positive zero. For V>0, the first constant-sign block is finite. Let k be its last nonzero exponent and set h=x^(-k)f. The derivative h' has coefficients (j-k)b_j at exponents j-k-1. Terms before k reverse sign, the term at k disappears, and later terms keep their signs. Thus the first two sign blocks merge, and h' has exactly V-1 sign changes (or fewer if an entire block disappears). This Laurent series again satisfies the hypotheses. If h has N positive zeros counting multiplicities in any finite compact interval, Rolle's theorem gives at least N-1 positive zeros of h'. Induction gives N-1<=V-1, hence N<=V. Arbitrarily many distinct zeros would violate the same bound on a sufficiently large compact interval. Multiplication by x^(-k) preserves positive zeros and their multiplicities. This proves the lemma, including infinite positive tails and exact zero coefficients.

## 3. Entire-series root bound

Put c=2theta and x=w/c. Multiplying w³R(w) by sinh²(x)/x², a strictly positive factor for x>0, gives the positive-root-equivalent entire function

Q(x)=c³ x³+L sinh²(x)+P x² sinh²(x)+N sinh²(x)/x²,

where L=lambda c², P=a c⁴ and N=nu. Define

d_n=2^(2n-1)/(2n)!, so sinh²(x)=sum_(n>=1) d_n x^(2n).

Then

Q(x)=N+(L+N/3)x²+c³x³+sum_(n>=2) q_n x^(2n),

q_n=P d_(n-1)+L d_n+N d_(n+1)
    =d_(n-1) [P+4L/u_n+16N/(u_n v_n)],

u_n=(2n)(2n-1), v_n=(2n+2)(2n+1).

(The symbol u_n in the final expression is the positive denominator defined on the preceding line; it is distinct from the compliance multiplier nu.)

The nonzero coefficient signs of the even tail q_n change at most once, from negative to positive:

* If L<0, N<0, the bracket strictly increases with n to P. Under the theorem's hypotheses P>0 in this case, so the tail is eventually positive.
* If L>=0, multiplying the bracket by the positive denominator u_n v_n gives P u_n v_n+4L v_n+16N. This strictly increases with n whenever P>0 or L>0, and is eventually positive.

Thus the full ordered coefficient sequence of Q begins with N<0, has a possibly positive or negative coefficient at x², a strictly positive coefficient c³ at x³, and an even tail with at most one negative-to-positive change. Its sign variation is at most three. All manipulations are valid for entire series, and the Descartes lemma applies. Consequently R has at most THREE positive roots counting multiplicities.

The already prescribed distinct roots p,r,s exhaust that bound, hence all are simple and there are no others. R is negative near zero since nu<0. It is positive for all sufficiently large w since a>0, or, when a=0, since lambda>0 and the Bose term tends to zero exponentially. Simple roots then give exactly the asserted alternating sign intervals. This also establishes the a=0 boundary case without taking a limit of positive a.

## 4. Moment comparison, compliance sign and equality

Let chi* be the pendant's full two-band indicator and chi any competitor's active indicator after cancelling dark intervals. Frozen F supplies 0<=chi<=1, the trace identity integral 2w chi=4K/m_comp and the fixed logarithmic moment. Frozen C/A supplies

N_CM(chi):=integral [chi_rigid-chi]/w³
            =(M-m_comp)² C_CM/(2M),

where chi_rigid=1_[0,sqrt(B)]. Every difference integral below exists: each finite connected spectrum equals one on a positive interval at the origin and is supported on a bounded frequency interval.

Pointwise sign minimization gives

I:=integral R(w)[chi(w)-chi*(w)]dw>=0.

The logarithmic moment difference vanishes. Define DeltaT=integral 2w(chi-chi*) and DeltaW=integral (chi-chi*)/w³. For fixed m, DeltaT=0. With variable allowed backbone m_comp>=m, DeltaT=4K/m_comp-4K/m<=0. Under the common cap C_CM<=C*,

DeltaW=N_CM(chi*)-N_CM(chi)
      =[(M-m)²C*-(M-m_comp)²C_CM]/(2M)>=0.

Therefore

J(chi)-J(chi*)=I-(a/2)DeltaT-nu DeltaW>=0.

The negative nu is the correct sign for an upper compliance cap in this convention. Using +nu times the unsigned compliance itself would reverse this bookkeeping.

If equality holds, I=0. Since R is nonzero except at three isolated frequencies, the indicators agree almost everywhere. Thus the minimizing active spectrum/response is unique. For variable m_comp the common spectrum itself fixes its trace and therefore m_comp=m. This does not assert a unique physical topology: dark or isospectral realizations remain possible.

## 5. Target point

At the requested K=1,M=2,m=1,theta=1/2 and cap C*=1/4, take k=4, r=sqrt(8),

p=sqrt(5)-1, s=sqrt(5)+1.

Here the exactly specified finite object consists of two unit masses, internal spring 4, and intercell spring 1. Fitting the dual at the three algebraic endpoints gives the following floating values (numerical certificates are owned by the parent):

lambda approximately -0.591137020902619,
a approximately 0.0395789001514940,
nu approximately -0.351276884506193.

These are strictly inside the theorem's sign region. Once their signs are enclosed rigorously, the theorem supplies an all-frequency no-improvement certificate for every finite positive internal network, including all acoustic/optical bands. It automatically compares with the strongest pendant allowed by the cap: k=4 is globally minimal over this larger class and so over every legal pendant k>=4.

## 6. Actual extension and boundary of the result

The theorem is a general sufficient test across K,M,m,theta and cap: compute the three attainable endpoints, fit the unique three-moment dual, and certify the multiplier signs. It does not claim these signs for arbitrarily stiff pendants. For the same resource tuple, exploratory coefficients show a becomes negative for sufficiently large r (e.g. r=6, k=18). There the required sign at infinity fails and this theorem cannot be used. The parent owns the remaining frontier/positive extra-band construction. The a=0,lambda>0,nu<0 threshold is included exactly in the theorem above.

This result strengthens the supplied two-moment machinery for the charged CM-compliance objective. It remains a scalar single-link harmonic ballistic theorem; it does not settle connector mass, displacement of each internal mass, finite material modulus, contacts, vector elasticity, anharmonicity, historical priority or practical device advantage.
