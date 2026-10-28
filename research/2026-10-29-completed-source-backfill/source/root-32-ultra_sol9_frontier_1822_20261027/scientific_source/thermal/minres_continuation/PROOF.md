# What was minimized and what was counted

This continuation is a numerical feasibility experiment plus an exact
restriction on its saved finite matrix pencil. The first accepted connected
thermal input is not modified. No result here certifies new physical thermal
data or a gap.

## 1. Full source residual instead of compressed variance

The target operator is A=-J_3=-K_3/5 on the spin-one boundary-message
multiplicity space. The existing basis has16 vectors indexed by
r=.2,.4,...,1.6 and d=0,1. For the physical boundary spin message u_r, the
basis vector is A^d u_r. Define actual source forms

    G_ij=<f_i,f_j>, H_ij=<f_i,A f_j>, M2_ij=<f_i,A^2 f_j>.

The M2 input is the full source second form, not H G^-1 H. Replacing M2 by
that compressed expression would silently discard the outside-subspace
residual and make an unearned small-variance claim.

For real c and positive c^T G c, the actual Rayleigh and variance are

    r(c)=c^T H c/(c^T G c),
    V(c)=c^T M2 c/(c^T G c)-r(c)^2.

For prescribed shift t,

    ||(A-t)f||^2/||f||^2
      = c^T[M2-2tH+t^2G]c/(c^TGc)
      = V(c)+(r(c)-t)^2.                               (1)

The smallest generalized eigenvector of the residual pencil therefore
minimizes the full squared residual at that prescribed shift. It need not
maximize Rayleigh and need not minimize variance by itself. Both quantities
are recomputed for every proposed candidate.

The source contraction for power p=d+e+q, q=0,1,2, is the signed endpoint
spin correlation on an open p+2-site chain divided by5^p. For p=0 its bond
coupling is3rs. For p>=1 its couplings are(3r,3,...,3,3s). Consequently every
G/H/M2 entry needs at most six physical spins. Full SU(2) recoupling traces
retain every total-spin multiplet with its2J+1 multiplicity. This experiment
evaluates those finite traces in float64; their exact source error is not
certified.

## 2. Bounded scan and conditioning charge

The normalized Gram matrix uses its original diagonal to set basis norms.
Whitening retains Gram eigenvalues above relative cutoffs1e-6,1e-8,1e-10,
1e-12. This gives ranks13,15,16,16. Each retained pencil is solved with its
actual transformed G, rather than replacing an imperfectly whitened G by an
exact identity. There are85 prescribed shifts in[294000,315000], spacing250,
plus bounded scalar refinement inside the same interval.

The full-rank normalized Gram condition number is3.9679e9. The whitening
operator error is2.98e-8. Candidate quadratic contractions are also recomputed
in longdouble on the saved float64 matrices. For the best full-rank candidate,
the GEP/direct squared-residual difference is.228 against a residual around
4.73e9. On this host longdouble has the same2.22e-16 epsilon as float64, so
that cross-check supplies no additional mantissa precision. The separate
Fraction replay evaluates the saved best candidate exactly on the dyadic
matrices. Neither check encloses physical source error.

The normalized-basis coefficient amplification

    (sum_i |c_i|)^2/(c^T G c)

is2.6357e5 for that candidate. The first-order variance sensitivity to a common
relative entry perturbation is approximately9.22e16. A2e6 variance-error
allowance would therefore require relative entry errors around2.17e-11 or
less in this local sensitivity model. Such source error enclosures have not
been acquired. The same large failure is present at rank13, where the Gram
condition is only3.68e4 and coefficient amplification is5.92.

## 3. Charge all assigned and unassigned triplet modes

The parent-proposed A5 preview isolates the physical spin-one message in the
3 list. Let M denote its complete sixth moment, and let mu_i be the signed
Ritz eigenvalues of A in the retained span. The source compact self-adjoint
minmax theorem assigns distinct true positive/negative eigenvalue occurrences
with magnitudes at least the corresponding signed Ritz magnitudes. Define

    R=M-sum_i |mu_i|^6.

This controls only UNASSIGNED modes. It is not a bound on every non-target
eigenvalue, because the other assigned modes still exist. For each assigned
mode b_i,

    |b_i|^6 <= M-sum_(j!=i)|mu_j|^6 = R+|mu_i|^6.         (2)

Thus an upper bound on all other POSITIVE eigenvalues, needed for Temple, is

    alpha=[R+max_(i!=top,mu_i>0) mu_i^6]^(1/6).

An upper bound on every other MODULUS, needed for the loop trace, is

    rho=[R+max_(i!=top)|mu_i|^6]^(1/6).

For the numerical full-rank input these are291919.41 and292238.84. The
unassigned-only radius291915.36 is slightly smaller and is not silently
substituted for either complete bound.

The target's moment-budget upper is

    U_moment=(R+mu_top^6)^(1/6)=328912.54.

If a candidate Rayleigh r>alpha, the usual highest-eigenvalue Temple bound
would give

    U_Temple=r+V/(r-alpha).                              (3)

For the best full-rank minimum-variance candidate r=292531.83,V=4.72867e9,
this is about8.014e6, much worse than U_moment. The effective bound stays
min(U_moment,U_Temple)=328912.54.

All non-target 3-list modes have sixth mass at most M-mu_top^6. Their full
ring256 contribution, relative to the scalar mode lower theta_I, is bounded
by

    3(M-mu_top^6)rho^250/theta_I^256.

The target contributes3(U/theta_I)^256. All other A5 lists retain their own
complete moments and dimensions1,3,4,5. The resulting all-mode loop-tail
proposal is393.70, so it does not give a useful connected increment. Every
A5 input in this computation is from the previous numerical preview, not
from a new exact cyclotomic acquisition.

## 4. Exact all-vector restriction for the stored dyadic forms

`verify_dyadic_span.py` interprets the symmetric parts of the saved binary64
G/H/M2 entries as exact dyadic rationals. This is an explicit finite input
different from the unverified exact physical source forms. Exact Fraction
LDL factorizations, with every pivot positive and L D L^T reconstruction
checked entry by entry, prove

    G>0,
    294200G-H>0,
    M2-588000H+(294000^2-4700000000)G>0.                 (4)

For any vector of these stored forms, (4) gives r<294200 and squared residual
at shift294000 greater than4.7e9. Any vector eligible for the present count
has r>291919.41, so it belongs to the wider favourable interval
[291900,294200]. Throughout this interval,

    (r-294000)^2 <=2100^2.

Equation(1) and (4) therefore prove for EVERY eligible vector in the stored
span, regardless of optimizer or prescribed shift,

    V>4700000000-2100^2=4695590000.                     (5)

Even granting the more favourable rest bound291900, a Temple upper below a
target t requires V<(t-r)(r-291900). For the generous targets322706 and
303344, this allowance increases on the entire interval r<=294200. Its
maximum is respectively

    (322706-294200)(294200-291900)=65563800,
    (303344-294200)(294200-291900)=21031200.

Both are far below(5). Thus no residual optimizer or choice of shift can
repair this finite pencil with the current favourable count interface.
This conclusion is exact for the saved numerical input only. No verified
entrywise error bound connects (4) to the physical forms, and no physical
or general-method impossibility is asserted.

## 5. Cost and remaining status

Regenerating full numerical source matrices, all four cutoff scans and
bounded refinements took3.808s on one thread. The final exact finite-matrix
and candidate replay took.046s; the preliminary replay took.041s. Source
reading, proof, unsuccessful numerical work and provenance
are additional costs. No costly exact field data, new message family, paid
compute, physical experiment, integration or subagent was launched.

The first connected input remains accepted. The next connected increment,
later increments, final cold purity and uniform spin-two gap remain unacquired.
