# Full-throughput noise-adapted recovery with quadratic consumed training

2026-10-27. NEW SYNTHESIS CANDIDATE, independent receipt requested. Do not treat this as received until both component proofs and this finite bookkeeping have been audited.

## Statement and access

For the fixed stationary memoryless source

 E(rho)=p VrhoV*+q Tr(rho)tau, p+q=1, p>=p0>0,

use only ordinary known-qutrit-labelled training calls producing the mixed programs T=(J+3omega)/4 and omega, fresh programs, controlled full-register SWAPs, and known ancillary gates. No source description, unknown eigenbasis, purified preparation/inverse oracle, or reusable learned device is supplied.

Let epsilon_ent=sqrt[5(p+3q)Delta] and e<=5epsilon_ent be the received polar-defect quantity. Assume e<=p/160. For every0<xi<=1, the explicit protocol below has target

 p identity+(1-p)erasure

and complete UNHALVED diamond error at most

 19800epsilon_ent+37p xi.                            (1)

Training samples consumed per data attempt are O(p0^-2 xi^-1) times the stated logarithmic factors. Gate width and memory still depend on the physical output dimension. The original noisy data call is one additional use.

## 1. Explicit finite protocol and sample count

For the nine Weyl rotations j, define analytically H_j=pPhi_j-D=4T_j-6omega. T_j is obtained from T by a known local Weyl rotation, and omega is unchanged. The source promises ensure the unique positive eigenvalue is at least p/3; the corresponding chi_j is NOT supplied as an oracle.

Set

 L=max(1,ceil log_16[1000/(p0 xi)]),
 eta=(xi/(100L))²,
 M=2^m the least power of two with M>=768/p0,
 r=ceil log_2(1/eta),
 S=9Lr pi(M-1).

For each label run L fresh nondestructive classifiers and accept that label only if all L accept. At the first rejection within a label retain A,B and move to the next label. At the first accepted label apply the known Bell correction and stop; erase if all labels reject.

Each classifier uses r coherent finite-QPE runs for

 U_j=exp[i pi(H_j+I)/2],

classifies phases into[1/4+p0/24,3/4), copies the majority decision bit, and reverses the QPE work while retaining that bit. Measure only the decision at the end. Negative-time uncomputation uses fresh mixed programs and negative collision angles, not inverse preparation. Forward controlled H-times are(pi/2)2^a; reverse times have the opposite signs. Their total absolute sum over all9L classifiers is S.

For each controlled time t, use

 N_t=ceil[10^9 |t| S/xi]

signed rounds with angles4t/N_t and-6t/N_t. Every round consumes two original training calls. The fixed worst-case training cap is

 n_train<=2*10^9 S²/xi+36Lrm.                        (2)

Every |delta|=|t|/N_t is below1/10. One classifier's squared pair time satisfies

 h=sum delta²<=xi/(9*10^9 L)<=xi/(10^9L).

The latter looser bound is used below. The classifier preserves rejected data rather than replacing it by erasure until the final receiver decision.

## 2. Received-component interfaces and conservative budgets

The ideal nine-projector receiver is analyzed in `nine_label_noise_adapted_ideal_receiver.md`: under e<=p/160, its genuine-code complete error is at most2340pt, its reset acceptance is at most30e, where t<=5e/(3p), and total ideal error is at most3960e<=19800epsilon_ent.

The candidate weighted interface is `noise_adapted_weighted_classifier_branch_lemma.md`. For one classifier write e_h=100000h exp(50000h), beta=eta+e_h. For the L-classifier retained-data binary instrument define

 eL=100000Lh exp(50000Lh),
 u=L[4sqrt(eta)+256h],
 kappa=eL+eta^L.

The chosen budgets give

 eL<=xi/9000, e_h<=xi/(9000L),
 u<=xi/20, beta<=1/16,
 beta^L<=p0xi/1000,
 kappa<=xi/4000.

The actual accepted branch A_j and rejected branch B_j, versus exact A0_j(X)=P_jXP_j and B0_j(X)=Q_jXQ_j, therefore obey

 ||(A_j-A0_j)(D)||1<=p xi/9,                         (3)
 +/-[(B_j-B0_j)(D)]<=kappa D+pR_j,
 R_j>=0, TrR_j<=xi/9.                               (4)

Their COMPLETE retained-data instrument has diamond error at most u. These are not inferred from uniform simulation alone; (3)-(4) use the CQ error cone and repeated acceptance coefficient contraction.

## 3. A coarse bound only for actual future suffixes

From(3), Tr A_j(D)<=p(1+xi/9)<=10p/9. Exact rejection obeys Q_j DQ_j<=D+pS_j with S_j>=0 and TrS_j<=4. Combining(4),

 B_j(D)<=(1+kappa)D+pS'_j, TrS'_j<=5.

Let F_k be the actual total acceptance effect of any suffix of k labels, with0<=F_k<=I. Induction then gives

 Tr(F_k D)<=7kp, for0<=k<=9.                         (5)

Indeed its recursion is at most10p/9+(1+kappa)Tr(F_(k-1)D)+5p, and kappa<=1/4000. This can exceed1 and is deliberately coarse. It is used only to charge SMALL signed D-weighted simulation errors, not to estimate the ideal reset baseline.

## 4. Ideal reset prefixes retain the small baseline

The reset marginal on the measured A,B registers, including its original source weight, is

 S0=q I_A/3 tensor tau=D/2-pQcode/6,
 Qcode=I_A tensor VV*, TrQcode=9.

After j exact ideal rejected labels, its positive marginal S_j can be written

 S_j=D/2+pZ_j, Z_j Hermitian,
 ||Z_j||1<=3/2+2j.

This follows from trace-norm contractivity of each Q_j(·)Q_j and ||Q_jDQ_j-D||1<=4p. For every prefix used in the nine-label comparison, ||Z_j||1<=18.

Crucially, S_j is the IDEAL prefix, not an arbitrary coarse reset domination. The ideal total reset acceptance is already at most30e.

## 5. Signed actual-versus-ideal telescoping on reset acceptance

Replace one label instrument at a time, using ideal prefixes and actual suffixes. At a prefix S_j, the total acceptance-probability discrepancy consists of

 Tr[(A_j-A0_j)(S_j)]
 +Tr[F_suffix (B_j-B0_j)(S_j)].

For its D/2 component, (3)-(5) bound the absolute discrepancy by

 pxi/18+(1/2)[7k kappa p+pxi/9], k<=8.

For its signed pZ_j component, the complete instrument bound u gives the conservative bound2pu||Z_j||1<=1.8pxi. The sum is less than2pxi per label. Nine labels therefore add at most18pxi to reset acceptance:

 actual reset acceptance<=30e+18pxi.                (6)

There is no unjustified absolute-value bound on a noncommuting Jordan component: (4) is a common positive order majorant, and the future acceptance effect is positive.

The accepted logical reset output may be arbitrary. Relative to erasure, its complete output error is exactly twice the accepted mass. Thus reset contributes at most60e+36pxi.

## 6. Genuine-code and complete-instrument receiving

For the genuine branch, generic complete-instrument telescoping across nine labels is sufficient because this branch has original mass p. Its additional learned error is at most9pu<=0.45pxi, uniformly over all external reference systems. Add the ideal code error2340pt.

Combining with(6),

 total<=2340pt+60e+36.45pxi
       <=3960e+37pxi
       <=19800epsilon_ent+37pxi,

which is(1). Accepted labels can be discarded after their known correction; all failed paths are replaced by a single erasure flag. This is a complete physical instrument, not only an accepted success-probability estimate.

## Relative accuracy corollary and scope

For0<nu<=1, choose xi=nu/74 and require

 epsilon_ent<=nu p/39600,
 equivalently Delta<=nu²p²/[7,840,800,000(p+3q)].

Then e<=5epsilon_ent<=p/160 and complete error is at most nu p. The sufficient noise scale is order p²; the large numerical constant is not asserted optimal. At fixed sufficiently small relative nu, the received exact-erasure Omega(p^-2) lower bound and this construction match the signal exponent up to logarithmic factors, now at full target throughput p.

The source promise is not itself experimentally certified by this theorem. Existing fixed-decoder holdout certificates can be applied with fresh batches; their validation overhead must be charged separately. Nothing here provides free multi-data amortization, a reusable decoder, unassisted capacity, a finite-block coding theorem, or a dimension-independent gate implementation.
