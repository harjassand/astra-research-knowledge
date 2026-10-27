# Exact finite arithmetic chain

The pinned governing notes/reviews are listed in GOVERNING_MATH.json. This
maps their formulas to code without acquiring their physical/IID premises.

Retained blocks use D_i=Y_i^a-Y_i^b,
M_i=((Y_i^a+Y_i^b)/2-Y_i^d)/K_i, W_ij=D_i conjugate(D_j)/(K_i K_j).
ANY P_i>K_i zeros ALL8 coordinates. Their order/range lengths are
ReM1,ImM1,ReM2,ImM2,W11,W22,ReW12,ImW12 /2,2,2,2,1,1,2,2.
Clipped zeros stay in N. Exact sums S_j,T_j=sum x_j,sum x_j² give
mean S_j/N and unbiased variance(T_j-S_j²/N)/(N-1).
The target covariance is2*diag(1/K)Cov(Y_on)diag(1/K); these positive
normalizations and corresponding means preserve the affinity operation.

## Log and roots

For x=32/alpha_stat>32 find the smallest integer h with2^h>=x. Since e>2
(the positive exponential series starts1+1+1/2), log x<=h. The conservative
coordinate radius is

    upper_sqrt(2*s_j²*h/N)+7*R_j*h/[3*(N-1)].

Both positive terms are monotone in h. At alpha=.01,h=12; power/sample figures
from the unrounded planning calculation are not inherited. No log/exp is called.

For x=a/b>0 and p=sqrt_bits>=1 choose
 e=(bit_length(a)-bit_length(b))//2-p, delta=2^e.
Compute k=floor sqrt(x/delta²) with integer isqrt of the integer quotient.
Lower=k*delta; upper=lower if lower²=x, otherwise(k+1)*delta. Squaring checks
the enclosure exactly. This relative grid gives positive lower for every
positive rational x, even very small ones. At0 both roots0. Only UPPER roots
enter confidence; a LOWER root displays the final scalar bound.

## Poisson/coding biases

External caps give ell_i=2*Lambda_on_i+Lambda_dark_i: conditional count MEAN
ceilings, never observed maxima. At deterministic J=K_i+1 compute
T=sum_(j=0)^J ell^j/j!. For k>ell,

    Pr(Pois(ell)>=k)<=(ell^k/k!)/[(1-ell/(k+1))*T].

Exp(ell)>=T; all successive tail ratios are<=ell/(k+1)<1. Min with1 is safe.
For k<=ell use1 without extending the formula. Nonpositive thresholds have
tail1, and ell=0 has positive-threshold tail0. All arithmetic is rational.

Use p0=Pr(Q>K),p1=ell*Pr(Q>=K),
p2=ell²*Pr(Q>=K-1)+ell*Pr(Q>=K). The reviewed factorial-moment/dominator
argument yields

    tM_i=(p1_i+ell_i*p0_other)/K_i,
    tC_ii=(p2_i+(ell_i²+ell_i)*p0_other)/K_i²,
    tC_12=(p1_1*ell_2+ell_1*p1_2)/(K1*K2).

This corrects back to UNCLIPPED target moments. Correlated source intensities
are not mistaken for independent actual counts. The justified fixed Poisson
dominators, rather than the actual records, supply independence in these bounds.

Combine each complex coordinate's two real statistical radii with upper_sqrt
of their squared sum. Add tM_i+eta to mean disks, tC_12+2eta to the offdiagonal,
and tC_ii+2eta to diagonal radii. Eta is the SUPPLIED per-photon complex coding
error, not detector efficiency. Retained normalized mean error<=eta follows
from the count bound; product differences give covariance error<=2eta. No
clock accuracy is inferred. The fixed coding rule must preserve the supplied
IID/coupling contract. Mean/covariance estimates share data; simultaneous8-
coordinate coverage, not independence of their estimates, supports transport.

## Rational geometry and coverage

Set a=C_hat12,b=conjugate(m_hat1),c=m_hat2 with radii ea,eb,ec. Rational
u=|Re|+|Im| UPPER-bounds modulus. The monotone nonnegative polynomial

    E=(ua+ea)(ub+eb)(uc+ec)-ua*ub*uc

contains every nonempty product error. Thus L=max(0,|Im(abc)|-E) lower-bounds
the true imaginary-product modulus on simultaneous coverage.

Mean disks must exclude0 (squared magnitude>radius²). Both variance lower
guards Chat_ii-e_diag_i must be>0. If either fails, or L=0, return UNKNOWN.
With d_i=Chat_ii+e_diag_i,

    rlo²=L²/[(ub+eb)²*(uc+ec)²*d1*d2].

This lower-bounds squared mean-referenced imaginary coherence, no larger than
the squared canonical imaginary radius. If rlo²>=1 return UNKNOWN/inconsistent
geometry; never clip it toward1. For0<rlo²<1 the reviewed source/cycle theorem
and pi>3 give

    Amax²>=36*rlo²/(1-rlo²).

Amax is nonnegative (maximum ABSOLUTE simple-cycle log rate ratio), so its lower
rational root is a valid displayed bound. Thermodynamic entropy per traversal
additionally needs local detailed balance; this is not entropy-production rate.

Confidence is1-alpha_stat-sum(alpha_other_total). All other budgets must bound
TOTAL-DATASET acquisition failure events or grant their premises exactly.
Physical caps, reset/tails, preparation/coupling, fixed coding and historical
precommitment remain supplied. A frozen header/hash does not repair post-data
frequency/gate/cutoff/N choice, reruns, optional stopping or invalid physical
preparation. A nonphysical fixture's positive arithmetic branch never becomes
a physical/statistical confidence achievement.
