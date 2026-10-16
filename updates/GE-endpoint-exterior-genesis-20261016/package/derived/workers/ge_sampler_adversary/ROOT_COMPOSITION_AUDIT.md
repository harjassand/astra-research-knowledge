# Coordinated root-code audit

Scope: after the root explicitly authorized reading its direct theorem and
implementation, this worker read `root/DIRECT_AVERAGING_CERTIFICATE.md`,
`root/direct_average.py`, and the pinned
`root/DEPENDENCY_erlang_certificate.v0001.py`. No other peer artifacts were
read. Their audited hashes are in `sourcehashes.json`. Their code was read as
data and was not executed by this worker.

The direct-limit measure theorem reconstructed independently in
`DIRECT_LIMIT_INDEPENDENT_ADDENDUM.md` agrees in constants and assumptions
with the root statement. This agreement is an internal audit, not external
validation. The minimal dimer independently gives h=1/2, G=1/2, K=3/2 at
retained boundary rate one. The direct code's formulas produce precisely
these quantities on inspection.

The positive Erlang receiving interface is correct. Write C(T) for the direct
certificate, F_e,D=a_e G_e,D, P_r=(I+H_r/s)^-1 and P_K=(I+K/s)^-1. The function
C(T)/T is nonincreasing for T>0: its atom part is h S_r(T)/T, while its
convolution part after t=Tv is an integral of two nonnegative nonincreasing
survivals. For Gamma of integer shape k>=2 and rate s,

    E[C(Gamma)/Gamma]
      = s/(k-1) sum_e a_e h_e (P_r^(k-1)1)_e
        + 1/(k-1) sum_(j=1..k-1) 1^T P_r^j F P_K^(k-j)1.

For the atom, the Gamma density divided by time changes the shape by one,
with factor s/(k-1). For the convolution, expand (u+v)^(k-2) after changing
variables t=u+v. The binomial coefficient cancels the two factorial integrals,
leaving exactly 1/(k-1) and positive resolvent powers j,k-j. The left action
1^T P_r^j equals the transpose of P_r^j1 because H_r is symmetric. K need not
be symmetric; it is only used on the right. Monotonicity then gives

    C(T) <= T E[C(Gamma)/Gamma]/P(Gamma<=T).

The root implements horizon T=1. Its CDF lower bound is valid: a lower Taylor
sum for exp(s) gives an upper reciprocal exp(-s), hence a lower
1-exp(-s)sum_(j<k)s^j/j!. Its positivity check fails closed.

The dyadic original resolvent history has a sound independent residual
interface. For a proposal z_next/Q to P_r(z_current/Q), the exact residual
of (H+sI)z_next=s z_current has infinity norm rho. Since
||(H+sI)^-1||_infinity<=1/s, its action error is at most rho/(sQ).
P_r is positive substochastic, so previous errors do not grow. The cumulative
error and [0,1] clipping used by the dependency therefore enclose the needed
history even if rounded LDL factors are poor. A nonpositive proposer pivot or
failed interval rejects the computation.

The direct implementation correctly:

* computes actual connected fast components;
* excludes replaced fast edges from B while retaining unsupported internal
  finite B edges;
* computes h and G by exact positive internal Green solves;
* constructs the nonsymmetric killed coarse pair generator from directed
  block-walker rates B_CD/|C|;
* uses original upper histories at powers j and coarse exact histories at
  powers k-j, including k-1 for the atom;
* keeps finite-boost and separate mixing-tail fields absent.

No mathematical or implementation blocker was found in this inspected scope.
An audit-trail improvement remains useful: save the complete internal h_C and
exit solution vectors so an independent checker can verify their exact
residuals from receipts, rather than relying on reexecuting the exact LDL
implementation. Current code asserts those residuals at execution and reports
only the fast-edge rows of h/G. This is a receipt completeness suggestion,
not evidence that the current equations or reported cases are wrong.

The worker's exact checker additionally verifies the Erlang identity against
an independently integrated scalar closed form for the minimal dimer at
shapes 2,3,8,16. Root-run numerical values and performance comparisons were
not independently rerun here. Sampler error must be added to a model TV bound
before claiming a total implemented endpoint tolerance.
