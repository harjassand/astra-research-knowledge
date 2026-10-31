# Independent whole refinement review: near-linear activity schedule
31 October 2026. Reviewer: independent internal mathematical review.

## Verdict and source binding
PASS as a resource refinement of the already reviewed common-loss graded compiler, with the final explicit access-cost qualification. This is not a new physical model, implementation, practical-advantage or novelty claim.

I read the complete 7,283-byte initial source SHA-256 0fd4262be5e318479f4b968976ac1e968828925681d79f6c1e62e11f383e5ab5. I then read the actual added Section 4 query-versus-gate paragraph and independently verified the FINAL binding source:
graded_reservoir_consequence_audit_20261031/NEAR_LINEAR_ACTIVITY_SCHEDULE_CANDIDATE.md
7,899 bytes, SHA-256 69e4c59079c426c0a047b21995c94f4afa420496c9df29011fd56c46324285bd.

The received whole compiler is source 93731752d0d34c2fcfa1e7fb0b6812b88f90d301083d32ecd60525cee5b543c9 with receipt 8aa67eda1b857be0fccb55e6c711ffc1e2c783787030e117266a159e3a9ccd65. The normalized uniform occupation source 136e1cf32b06eac6dbfba53f1e7c4a91783c607233779f2cf7ce55fa234509dd and its receipt a799f1564926c5d0033771cf174257470078eca5831a77d646b2ee369c384430 remain binding. No frozen earlier proof is altered.

## 1. Deterministic windows and caps
For positive G, D=16G(L+1)+p+log(100/epsilon)+2 and tau=1/D satisfy the original scalar row/column limit. The original global g=0 branch remains separate and does not evaluate source expressions with vanishing G.

The no-event pieces number at most ceil(1/tau)+p+1. The exact physical-emission cap is O(G+log(1/epsilon)+1). Consequently
S=O(G(L+1)+p+log(1/epsilon)+1)
and S*tau=O(1).
These are deterministic worst-case call bounds, including jumps and prescribed boundaries. They do not use expected durations of sampled paths or an approximate-algorithm emission MGF.

The complete-isometry normalizer remains O(sqrt(L+1)). Replacing S in the existing e_step, beta, eta and sigma definitions enlarges their inverse logarithms only by log(S/epsilon) and log(L+1). All earlier finite physical-error budgets continue to apply.

## 2. No hidden activity-sized work per source call
On every shortened window, candidate immigration mean is at most Gtau/2<=1/[32(L+1)]. The direct bridge's candidate cap is therefore O(1+log(S/epsilon)+log(L+1)), and its total virtual-event cap is O(L+log(S/epsilon)).

The finite survivor-posterior lists and endpoint factorial sums have length O(L). Capped Poisson CDF scans run only through the declared candidate cap. Marked-event arithmetic, sorting, retention cuts and coherent stack/removal use polynomial work in the displayed caps, register lengths and precision bits. There is no loop over G or ell=lambda T.

Large or small positive rates enter the existing error tolerances through logarithms of explicit sensitivity bounds. The time floor and tie cuts become smaller as S grows, but their bit lengths increase only logarithmically in S and the encoded rate/norm scales. Thus the source analysis does not hide an extra polynomial G factor per call.

## 3. Actual binary-duration circuit
Each H_f interval lies in [0,Ttau]. Store its duration as a binary fraction of this KNOWN maximum, rather than of the full T. A B-bit circuit executes controlled fixed-time evolutions of lengths Ttau/2^k for k=1,...,B.

The sum of the durations of the actual compiled operations is at most Ttau for EACH slot, even though all controls and all B operations are present. Therefore controlled qubitization of the acquired normalization-alpha_f block costs
O(alpha_f Ttau+B[1+log(B/delta_slot)])
queries per slot.

This is a deterministic circuit accounting identity, not an assertion that stochastic durations along one branch sum to T. There is no lookup over 2^B possible durations. Binary rounding contributes at most alpha_f Ttau 2^(-B) in operator norm, and B can simultaneously satisfy all earlier source-time and private-clock tolerances.

The assumption on H_f access is essential. This estimate applies to the supplied acquired block encoding with ordinary controlled qubitization, not to an arbitrary opaque evolution-cost function without the stated time/precision resource bound.

## 4. Safe dyadic replacement
A dyadic lower window can be selected without an exact comparison of transcendental expressions to powers of two. For example, certify a positive rational Dhat in [D,9D/8], choose a dyadic grid spacing h<=1/(8Dhat), and round 1/Dhat downward to that grid. The result tau' obeys tau/2<=tau'<=tau.

Such relative enclosures require only the declared finite scalar precision. Recompute the no-event count, S and all subsequent budgets using tau' consistently. Candidate means only decrease, S grows by at most a constant factor, and S*tau' remains bounded. Thus the replacement does not create an unpriced timing or cap error.

## 5. Summed Hamiltonian and coupling costs
Each base word has at most Kcap+1 free-evolution slots. Complete amplification calls the base construction and inverse O(A) times. There are at most S calls. Summing the ACTUAL circuits and using S*tau=O(1) gives
Q_H=O(A(Kcap+1)alpha_f T
 + S A(Kcap+1)B[1+log(B/delta_slot)]).
The extensive free-Hamiltonian action is additive here; there is no unnecessary multiplication by G.

Coupling queries satisfy Q_F=O(S A(Kcap+1)) with the actual selected-encoding overhead paid. The remaining finite source, arithmetic and removal costs are polynomial in their caps, r and precision lengths.

The final source explicitly distinguishes query and gate accounting:
Q_H C_H(delta_H)+Q_F C_F(delta_F)
+ S A poly(arithmetic/input/precision lengths)
+ actual consumer costs.
This is the correct general access statement. An opaque query oracle does not automatically provide an elementary-gate bound.

Envelope (5) follows as an elementary-gate bound only when the supplied encoding circuits themselves have polynomial costs in the declared circuit/input sizes and precision lengths. That condition is now explicit in the frozen final source. An arbitrarily expensive encoding cannot be hidden in a constant-cost query.

## 6. Bounded-mu and interacting subclasses
The optional uniform occupation estimate gives
L=O(1+mu+log(2+Tg)+log(1/epsilon)),
mu=g^2/(4lambda^2).
For bounded mu, Tg=sqrt(Gell), so L is polylogarithmic in the displayed action/rate/accuracy scales. The finite source and amplification factors then remain polynomial in r and those logarithms.

The resulting statement is near-linear in G, p and alpha_f(L)T after separating the displayed L, input and logarithmic factors. It does not mean small constants or a rate-independent gate count.

For the acquired Bose–Hubbard/Kerr block, alpha_f(L) is a polynomial in L times the ordinary coefficient-action scales. Those noncommuting Hamiltonian costs remain paid. The special known diagonal-polynomial phase routine can improve its own cost, but is not needed to justify this general schedule. If mu is not bounded, the theorem still keeps its polynomial L dependence; it does not silently replace that dependence by logarithms.

## 7. Exact lower-bound comparison
The separate source dd9648df785e7a22fbdd7ec7452a20f383ae86d6d97d4d6bd87e2b562652abb0 has now been independently accepted in receipt 45c3a56734dd4df9b4ad9d4ad7b2cd52dee9f5bca44f219ccce34e20233e4e0e. Its hard-core clock/parity construction proves Omega(G) supplied-coupling queries at constant trace-norm error when lambda>=Gamma. This range has mu<=1/4.

It is therefore legitimate to say that linear accumulated-activity dependence cannot generally be removed in that oracle model. The lower bound counts acquisition/preprocessing and does not establish optimal mode, precision, free-action or gate dependence of the full upper bound. Nor does it prove practical superiority or novelty. The upper and lower statements are compared only on their common access/model domain.

## Final scope
The original vacuum, common-loss, compatible grade-preserving H_f, private reservoir, prescribed-control, finite-input domain and unconditional-error restrictions remain unchanged. The refinement uses earned source/cap/clock operations and the real bounded-duration qubitization circuit, not postselected good paths or generic fast-forwarding.

This source-bound PASS is a mathematical resource theorem. No implementation, benchmark, generic optimality or practical crossover is inferred.
