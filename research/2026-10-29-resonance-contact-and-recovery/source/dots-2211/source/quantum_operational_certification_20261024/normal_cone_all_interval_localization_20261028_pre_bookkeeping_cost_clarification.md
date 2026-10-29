# Finite learned localization from disjoint-competitor oracle scores

28 October 2026. New candidate acquisition mechanism; separate internal review required. This replaces the FAILED inference that normal-cone channels have zero signed contrast on every disjoint interval. It uses simultaneous optimal-score comparisons from one common actual channel bank.

## 1. Structural and physical contract

A qubit-input source has n ordered physical output qubits. There is ONE fixed physical Pauli triple B_j on the full output, supported on an unknown nonempty interval I of length<=w, with w<=n known. At every exposed calibration history, the current reduced qubit-to-output channel N_t is CPTP, selected before the current private input/readout coins. Its three contrasts C_(t,j)=N_t(sigma_j/2) satisfy the full oracle normal cone of B:

 Y_(t,B)=sum_j C_(t,j)B_j is Hermitian,
 Q_(t,B)=I_2 tensor Y_(t,B)-sum_j sigma_j^T tensor C_(t,j)>=0.

The source may retain quantum memory and change with past observed history. Its actual conditional memory is positive; current probe inputs are freshly prepared independently of that memory. All local means in a comparison bank must arise from the SAME average global channel Nbar=(1/N)sum_t N_t. Private randomized settings below ensure this. Alternatively a fixed stationary independently restarted channel is a sufficient special case. Separate setting/interval banks with uncontrolled history-changing noise do NOT supply comparable scores.

This is a trusted qualitative source contract, not certified by finite data. The source need not have a positive operator-block factorization and may have gauge-only input contrasts. For eventual completion we separately assume a uniform positive full-output dual gap Q_(t,B)>=mu0(I-P_B), mu0>0 over the relevant histories; its numerical value is NOT an input to the observed acceptance guard. Finite funded caps can always abstain.

## 2. One actual ordinary bank supplies all local contrasts

Enumerate ALL nonempty intervals J of lengths1,...,w, not only intervals of lengthw. In each of N rounds choose a private input axis j uniformly from X,Y,Z and sign s uniformly from+-1; prepare (I+s sigma_j)/2. Measure every physical output qubit in an independently uniform Pauli axis. Retain input axis/sign, output axes and binary outcomes.

For a nonidentity Pauli word P on interval J, of weight k, and input label j0, the actual coefficient record is

 X_(j0,J,P)=3^(k+1) 1_(j=j0) 1_(readout axes match P on its nonidentity support)
                         s product_(support P) output_bit.

Conditionally on the prior full classical history its expectation is Tr[P C_(t,j0),J], with C_(t,j),J=Tr_notJ C_(t,j). Its absolute value is <=L=3^(w+1). The sample mean therefore estimates the corresponding coefficient of the SAME random predictable average Cbar_J for every interval and every input axis, even though the source memory evolves.

Let M=3 sum_(ell=1)^w (n-ell+1)(4^ell-1), a conservative count including duplicated coefficients. Conditional Hoeffding/Azuma for the bounded records and a union bound give, with probability>=1-beta,

 |chat_(j,J,P)-cbar_(j,J,P)|<=eta=L sqrt(2 log(2M/beta)/N)

SIMULTANEOUSLY. Reconstruct Chat_(j,J)=(1/d_J)sum_(P!=I) chat P, d_J=2^|J|; the identity coefficient is exactly zero by TP. Pauli orthogonality gives

 ||Chat_(j,J)-Cbar_(j,J)||_F<=sqrt(d_J) eta.                 (1)

The union event is about actual predictable means, not a guessed stationary distribution or postselected records. It permits later data-dependent interval selection. The conservative bound can be loose; it is stated to pay every required observation rather than assert practical sample efficiency.

There are N source calls, n physical output readouts per call, and O(n w 4^w) coefficient bookkeeping. Exact uniform ternary choices for the input axis and n output axes can use two-bit rejection with a fixed L_rng-attempt cap. Over N calls, cap-failure probability is <=N(n+1)4^(-L_rng); pay it as an abort/record-TV debit. At most N[2L_rng(n+1)+1] random bits are used. Readout/preparation/control inaccuracies require separate complete record-law allowances. No environment measurement or full2^n matrix tomography is performed.

## 3. Certified LOCAL full-CPTP scores, including solver error

For each J define v_J as the actual entanglement-fidelity optimum of the marginal channel Nbar_J over ALL CPTP decoders from J to one qubit. Solve the known local SDP with Hhat_J=sum_j sigma_j^T tensor Chat_(j,J), primal K>=0, Tr_aux K=I_(d_J). Obtain an EXACTLY FEASIBLE or rigorously repaired primal value p_J and dual value u_J, so p_J<=empirical optimum<=u_J. Numerical feasibility residuals and rounding costs must already be paid in these bounds; an optimizer's unverified objective is not an interval.

For any feasible decoder its Pauli images have Frobenius norm<=sqrt(d_J). Equation(1) therefore changes its fidelity objective by at most h_J=3d_J eta/4. Hence the actual score satisfies

 L_J=max(0,(1+p_J)/4-h_J)<=v_J,
 U_J=min(1,(1+u_J)/4+h_J)>=v_J.                             (2)

Use the usual0<=v_J<=1 only when clipping a valid interval. A certified solver gap u_J-p_J<=zeta is sufficient for eventual shrinking intervals. The full-CPTP SDPs are the standard recovery optimization; fixed small output width, not complete environment dimension, determines their local matrix size. Known strict primal/dual centers and finite PSD separation can use the separately received endpoint machinery. Hardware and full arithmetic runtime are not asserted inexpensive.

## 4. A finite margin-free overlap witness

Accept any interval J whose actual computed bounds satisfy

 L_J > max_(K disjoint J, 1<=|K|<=w) U_K.                  (3)

Define max over an empty family as minus infinity. Then every nonempty candidate support interval intersects J, so that vacuous case is sound.

On the simultaneous event, any accepted J MUST intersect the true support I. Indeed the decoder B is globally oracle-optimal and acts entirely on I, so v_I equals the global optimum. No decoder on another interval can exceed it. If I were disjoint from J, it would be a listed competitor in(3), and

 L_J<=v_J<=v_I<=U_I

would contradict the strict guard. This proof needs NO numerical gap and NO disjoint-zero signed contrast premise. Gauge input information may be arbitrarily visible; the certified score order, not its mere presence, determines acceptance.

Enumerating all lengths is essential. For example on n=5 with w=3, a proposed J=[3,5] has no disjoint length3 interval, although a true support I={2} is disjoint. A fixed-width-only guard would falsely pass vacuously. The all-length family includes I and prevents this error.

If J=[l,r] passes, expand to E=[max(1,l-w+1),min(n,r+w-1)]. Overlap and |I|<=w imply I subset E, and |E|<=3w-2. This is an actual acquired support envelope, not an assumed localization oracle.

## 5. Why the guard eventually passes under a strict true margin

For any interval K disjoint from I and any decoder supported on K, extend its unital-CP Pauli images to the full output. Because B_j is traceless on its support and K is disjoint, Tr(B_j A_j)=0. The exact leakage identity from the normal-cone source is therefore3d/4, d=2^n. A full-output dual gap mu gives

 global optimum-v_K >=3mu d/16=:gamma.                     (4)

For the common bank, averaging Q_(t,B) preserves the cone and the uniform margin mu0. Taking J=I in(3), sufficiently narrow intervals separate its score from every disjoint K. More explicitly, if every empirical solver gap is<=zeta, then L_I>=v_I-2h_I-zeta/4 and U_K<=v_K+2h_K+zeta/4. Thus4h_max+zeta/2<gamma is sufficient.

This is a completion analysis, not a supplied gamma in the guard. Staged larger common banks, smaller solver errors and simultaneous failure budgets can eventually pass under a persistent positive gap; a caller-funded finite cap may still return ABSTAIN. A conservative sufficient N scales as O(3^(2w+2) 4^w log(M/beta)/gamma^2), not as an asserted optimal sample law. The full d and mu in(4) have reciprocal dimension scaling in many product-gauge examples, but that must be checked for the actual source family rather than assumed.

## 6. The acquired envelope inherits the exact normal cone

Once E contains I, B_j=B_(E,j) tensor I_notE and P_B=P_(B_E) tensor I_notE. Partial trace gives EXACTLY

 Y_(B_E)=Tr_notE Y_B,
 Q_(B_E)=Tr_notE Q_B.

Hence global oracle optimality implies local oracle optimality on E, and a global gap mu gives

 Q_(B_E)>=mu d_notE(I-P_(B_E)), d_notE=2^(n-|E|).           (5)

The local full-CPTP optimum equals the global optimum because B factors through E. A later fine bank can have a different actual source mean, but it must retain the SAME B and the same qualitative normal-cone contract at every relevant history. Estimate that fine bank's three contrasts using one private common bank again, not separately history-biased input settings. Its own data error event and any margin used for completion are paid separately.

## 7. From support to a finite physical generator fit

On E, use the empirical full-CPTP SDP to propose images A'_j. Under a positive true local gap and shrinking data/solver errors, the normal-cone curvature forces A'_j->B_(E,j). Construct a PHYSICAL triple by the received exact rounding: X=sign(A'_X), Zodd=(A'_Z-X A'_Z X)/2, Z=sign(Zodd), Y=iXZ. Proceed only after certified nonzero sign gaps. This supplies exact Hermitian unitary anticommuting generators; arbitrary approximate SDP images are not used as gates.

For the resulting fixed physical candidate A, fit known Hermitian Ctilde_j with

 Y_A=sum_j Ctilde_j A_j Hermitian,
 Q_A(Ctilde)>=kappa(I-P_A), kappa>0,
 r^2>=sum_j||Ctilde_j-Chat_j||_F^2.

The equality constraints enforce the forced kernel EXACTLY. Compress onto P_A-perp for the PSD inequality. For fixed A this is a convex residual fit (SOCP/SDP); Ctilde_j=alpha A_j gives Q=4alpha(I-P_A), providing a known relative-interior baseline for alpha>kappa/4. A finite residual radius comes from the baseline's residual and the known data. Exact algebraic A and certified finite convex arithmetic are required; global nonconvex unitary search is not silently supplied.

If e is the verified fit residual plus the fine bank's simultaneous contrast-tuple Frobenius error and arithmetic allowances, accept the generators only if8e/kappa<=delta. The acquired normal-cone certificate then gives sum_j||A_j-B_(E,j)||_F^2<=delta^2. The numerical true gap is not an input to this guard. All coefficient-fit constraints/solver residuals are verified, not inferred from a small unverified objective.

For completeness, close physical triples admit an explicit intertwiner

 L=(I+sum_j A_j B_j)/4, A_j L=L B_j.

When A->B, L->I and is invertible. Its polar unitary W intertwines A_j=W B_j Wdagger, because Ldagger L commutes with B. Then Ctilde_j=W C_j Wdagger is a feasible candidate model with the SAME positive dual gap and residual tending to zero. It establishes eventual fit feasibility without knowing W or B algorithmically. Thus an ordinary SDP proposal, exact rounding and convex fixed-candidate fit complete the acquired local mechanism under the stated promises. Finite stages/trial kappas can still abstain; no noisy source-membership inference is made.

## 8. What physical recovery follows, and what does not

The certified local X/Z matrices can be used in the literal three-controlled-reflection subsystem extraction circuit. A deterministic operator-norm telescope gives per-use complete-reference error<=2||A_Z-B_Z||op+||A_X-B_X||op<=3delta relative to the PARTICULAR exact extraction B, with actual ancilla initialization, routing and synthesis errors paid. This comparison can be composed after arbitrary future coherent source memory because the circuit bound is state-uniform; it is not a generic identity-channel or optimal-future-noise guarantee.

For multiple logical inputs, their true triples must come from ONE compatible global algebra/unitary. Independent locally optimal triples are not enough. Learning joint encoders, preserving all other assignments, global compatibility, complete source control, sample scaling and a practical advantage over equally informed conventional methods remain separate obligations.

This source's added mechanism is the finite disjoint-competitor score guard and its normal-cone transfer. It does not reuse the false disjoint-zero proof, assume unchanged noise across separate history-dependent banks, or infer a physical compiler from a floating SDP result. Standard full-CPTP recovery SDPs and dual certificates are prior machinery; historical novelty is not established.
