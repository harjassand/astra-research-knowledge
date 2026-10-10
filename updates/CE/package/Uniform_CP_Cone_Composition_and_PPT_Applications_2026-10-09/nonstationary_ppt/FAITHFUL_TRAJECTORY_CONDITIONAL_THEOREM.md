# Exact nonstationary EB under a uniformly faithful trajectory

9 October 2026. Complete conditional proof candidate. The lower-dimensional hypothesis is essential and is not silently replaced by the bistochastic theorem. This is a genuine nonunital extension of the two-sided anchor mechanism. No priority claim is made.

## Statement

Fix d>=2 and a>0. Assume that every product of R arbitrary PPT CP maps on M_(d-1) is EB, for some finite R.

Then there is a finite N(d,a,R) such that every sequence of N(d,a,R) PPT CPTP maps Phi_i:M_d -> M_d is EB whenever there are density matrices sigma_0,...,sigma_N satisfying

 Phi_i(sigma_(i-1))=sigma_i,        sigma_i>=a I            (1)

at every intermediate time, including the endpoints.

The matrices sigma_i may vary. In particular the statement applies when all factors fix a common faithful density matrix sigma with lambda_min(sigma)>=a. No unitality of the factors is required.

Using the known arbitrary two-map PPT composition theorem on M_3, this gives an unconditional result for d=4 (and the already-understood lower dimensions). In dimensions beyond that, this record asserts only the stated conditional implication. The qutrit input is Christandl–Mueller-Hermes–Wolf, When Do Composed Maps Become Entanglement Breaking?, arXiv:1807.01266v2, https://arxiv.org/abs/1807.01266v2 .

## 1. Tagged compact boundary

Use EXACT_UNRESTRICTED_GATE_REDUCTIONS.md, Section 2, with

 B=2R+1,        Q=(R+1)B.

For a Q-block T of arbitrary PPT CPTP factors, let f_tag(T) be the maximum strict-output margin among its contiguous B-subwords. The precise underlying tuple, not merely the resulting linear map, is part of the tag data. On the full compact tuple space,

 f_tag=0 ==> T is EB.

The Kraus lift and Lojasiewicz inequality consequently supply common A,alpha>0 such that each T admits a Kraus representation with

 b(T)=sum_j ||wedge^2 K_j|| <= A f_tag(T)^alpha.           (2)

The estimates are uniform before the trajectory restriction (1) is imposed.

## 2. The forward interior anchor

Suppose a tagged block has a strict-output-positive subword Psi of margin s, and suppose U is a product of preceding whole Q-blocks. Write L for the part of the tagged block between U and Psi. Thus the relevant chronological segment is Psi L U.

Let E be an EB approximation to U with delta=||J(U-E)||_F. Since L is TP,

 (L E)*(I)=E*(I)>=I/2

whenever delta<=1/(2sqrt(d)). As in the one-sided anchor lemma,

 Psi L E >=_EB (s/2)D,
 ||J(Psi L U-Psi L E)||_F <= sqrt(d) delta.

Therefore this segment is EB when delta<=s/(2d^2 sqrt(d)). The anchor may sit inside its tagged block; no extra approximation of L or Psi is needed.

## 3. The reverse interior anchor from a faithful trajectory

Now suppose U is a product of later whole Q-blocks, and R_0 is the part of the tagged block between Psi and U. The relevant segment is

 U R_0 Psi.

Let sigma_mid be the trajectory state entering U, and let sigma_out be the state leaving U. If sigma_after is the state immediately after Psi, then

 R_0(sigma_after)=sigma_mid,
 U(sigma_mid)=sigma_out.

Every density matrix is <=I, so R_0(I)>=sigma_mid. For an EB approximation E to U,

 E R_0(I)>=E(sigma_mid)>=sigma_out-delta I>=a I/2         (3)

provided delta<=a/2. The middle inequality follows by contracting J(E-U) with sigma_mid^T; its operator norm is at most delta because ||sigma_mid||_F<=1.

For any EB map F, strict output positivity Psi(rho)>=sI implies

 F Psi >=_EB [X -> s tr(X) F(I)].                        (4)

To see this, write F(X)=sum_j tr(F_j X) tau_j. The adjoint bound Psi*(F_j)>=s tr(F_j) I makes the difference in (4) explicitly measure-and-prepare.

Apply (4) to F=E R_0 and use (3). Then

 E R_0 Psi >=_EB (a s/2)D.

Since the combined map R_0 Psi is CPTP,

 ||J(U R_0 Psi-E R_0 Psi)||_F <= sqrt(d) delta.

The separable ball gives EB of U R_0 Psi whenever

 delta <= a s/(2d^2 sqrt(d)).                            (5)

Because s<=1/d, (5) also guarantees delta<=a/2. This is the previously missing reverse direction. It uses a uniformly faithful actual trajectory, rather than unitality or a claim that arbitrary CPTP adjoints are TP.

## 4. Weak tagged runs

Choose m with alpha m>1. Choose epsilon>0 small enough that

 c_d A^m epsilon^(alpha m-1) <= a/(2d^2 sqrt(d)),
 c_d=sqrt(d^2-1).

Let W=2m+1. In any W-block run with all tags at most epsilon, select a block with maximal tag s. If s=0, that block is EB. Otherwise, one side of it contains at least m whole blocks.

Rank-one truncation of the m-block product U on that side yields an EB E satisfying

 delta <= c_d product b(T_j) <= c_d A^m s^(alpha m)
       <= a s/(2d^2 sqrt(d)).

Use the corresponding forward or reverse interior-anchor lemma. Both apply to the subword that attains the selected tag. Exterior CP factors preserve EB. Thus every W-consecutive weak tagged run is EB.

## 5. Strong tags and total length

The strictly-positive filtered-word theorem supplies a finite H(d,epsilon) such that H strict-output-positive CPTP anchors of margin at least epsilon, separated by arbitrary CP maps, force EB.

Each strong Q-block contains such an anchor. Thus H strong blocks force EB. Fewer than H strong blocks, with no W-consecutive weak run, give at most H W-1 total blocks.

Therefore

 N(d,a,R)=Q H(d,epsilon) W

is a valid uniform bound under (1). This proves the statement.

## What remains

This theorem does not prove the unrestricted dimension induction. In a hypothetical smallest dimension where unrestricted finite-word uniformity fails, arbitrarily long nonEB words must evade every fixed lower bound a on a faithful trajectory. Starting from the maximally mixed state, their evolving outputs must become arbitrarily close to singular somewhere along the word.

The exact compactness issue has thus been narrowed to concentration of intermediate states. The theorem does not say that a merely faithful trajectory, with no common quantitative lower bound, is sufficient for a uniform length.
