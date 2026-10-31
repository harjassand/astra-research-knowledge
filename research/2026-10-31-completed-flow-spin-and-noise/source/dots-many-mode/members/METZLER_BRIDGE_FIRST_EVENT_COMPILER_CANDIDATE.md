# Metzler bridges and the complete first-event instrument

Root construction, 31 October 2026. Unreviewed whole compiler candidate. The exact damped-ancilla representation and its count bound have a separate mathematical review. No completed circuit implementation or novelty claim.

## 1. Restrict the difficult new case precisely
Take two independent telegraph modes, two arbitrary bounded Hermitian A1,A2 (not necessarily commuting), and H0. Use the exact amplitude-damped two-ancilla representation. Let ai be charged block-encoding normalizations, gi=sqrt(gamma_i lambda_i) ai, Gamma_i=gamma_i ai^2, Gamma=Gamma1+Gamma2. The no-jump propagator is

K(t)=exp[t(-iH0-i sum_i vi Ai Xi-2sum_i lambda_i Pi)].

The goal is not to postselect K alone. It is to implement the complete first-event instrument on a short window tau with Gamma*tau<=1:

K(tau), and {J_i K(t) sqrt(dt): 0<=t<=tau, i=1,2}.

Exactly K(tau)^dagger K(tau)+sum_i integral_0^tau K(t)^dagger J_i^dagger J_i K(t)dt=I. The no-event and first-event outcomes therefore form an isometry when their labels are retained. This identity holds for arbitrary system/ancilla input, not only ground ancillas.

## 2. A positive majorant for virtual no-jump paths
Remove H0 by its ordinary unitary interaction picture. Expand the remaining no-jump evolution into virtual flips of the two ancilla bits. A virtual flip of color i inserts -i Ai/ai on the system and toggles bit i; its scalar factor is gi. Between flips the scalar damping factor is exp[-2sum_i lambda_i*(occupied time of bit i)]. Products of the normalized system operators are contractions, although they do not commute.

All positive scalar path weights, summed for given initial and final ancilla sectors, equal entries of

exp(Mt), M=M1 tensor I+I tensor M2,
Mi=[[0,gi],[gi,-2lambda_i]].

This is a four-state matrix, used for source acquisition rather than an assumed system-sized matrix exponential. Its tensor factors have explicit formulas. Put omega_i=sqrt(lambda_i^2+gi^2), si=omega_i-lambda_i=gi^2/(omega_i+lambda_i), di=omega_i+lambda_i. Then si<=Gamma_i/2. Use the rationalized expression for stable numerical evaluation.

The positive Perron vector of Mi is ri=(1,si/gi) for gi>0. The Doob transform is the two-state row generator with rates 0->1 equal si and 1->0 equal di. A path of this Markov chain conditioned on its endpoints has exactly the normalized positive virtual-path weight for Mi. The Perron prefactor cancels under endpoint conditioning. If gi=0, Mi is diagonal and the only nonzero virtual paths have no flips; handle this case directly.

Conditional paths for the two colors are independent. Sort their virtual event times and apply the normalized system operators in the resulting chronological order, including ordinary H0 propagation. The sorting step is mathematically essential for noncommuting A1,A2.

## 3. Actually acquiring the conditional bridges
For rates s,d>0, nu=s+d, the transition probabilities are
P01(t)=s/nu*(1-exp(-nu*t)), P10(t)=d/nu*(1-exp(-nu*t)),
P00(t)=d/nu+s/nu*exp(-nu*t),
P11(t)=s/nu+d/nu*exp(-nu*t).

Given current bit i, terminal bit j and remaining duration t, the conditional probability that the first transition exceeds u<t is

exp(-q_i*u) Pij(t-u)/Pij(t), where q0=s,q1=d.

There is a no-transition atom at u=t when i=j. Invert this explicit monotone distribution by certified finite bisection; after a transition, flip the current bit and continue with the same terminal bit. There is no rejection loop waiting for a rare terminal endpoint.

The unconditioned number of transitions is pathwise at most twice the number of rate-s proposal up-clocks plus one initial down-transition. Thus it is bounded by 2Poisson(s*t)+1. Conditioning on an endpoint divides tail probabilities by Pij(t). For two colors and Gamma*t<=1, a virtual event cap of order log[1/(eta P1 P2)] suffices by an exponential Markov bound. This cap, not a loop over lambda*t, is used in the coherent circuit.

For nonzero s, every Pij(t) is at least c*(s/nu)*min(nu*t,1) for an absolute c>0. Hence log(1/Pij) has polynomial bit complexity in the encoded parameters and log(1/t), not in lambda*t. Small couplings must be represented with their actual input bit length; zero couplings are handled separately.

## 4. Precision seams that must be priced
Recursive bridge durations can become arbitrarily short, and two different colors' near-coincident events can reverse order when rounded. A scalar integrated-path error bound cannot justify changing that order.

Fix an original bridge duration tau and its endpoint probabilities P1,P2. Let qmax bound all transition rates. Under the unconditioned chains, an event within zeta of either endpoint has probability at most O(qmax*zeta), and an ordered event pair within zeta has probability at most O(qmax^2*tau*zeta). Divide by the original endpoint probabilities for the conditioned bridge laws. Choose zeta sufficiently small in eta, P1P2, qmax and tau. Declare the near-endpoint and near-coincidence paths bad. Their total conditioned probability is at most eta.

On the remaining paths, every recursive residual time is at least zeta and all actual event orders are separated. This supplies one uniform denominator bound Pmin(zeta) for all recursive inverse-CDF calls. It does not recursively worsen the arithmetic precision. Approximate every event time within zeta/(10(Kcap+1)); then all terminal bits and cross-color orderings are preserved.

For a monotone quantile Q:[0,1]->[0,tau], coupling U to its B-bit left endpoint gives E|Q(U)-Q(U_B)|<=tau*2^-B. Markov's inequality prices the desired time tolerance without assuming an inverse-CDF Lipschitz constant. Certified bisection has a fixed depth. Its potentially ambiguous comparisons are charged by a union over the finite set of possible grid thresholds; that set can be large, but only its logarithm enters the required arithmetic precision. The no-event atom is a separate branch and is not counted as an event near the terminal boundary.

Away from bad paths, perturbing the ordinary H0 intervals changes the selected operator product by at most a constant times alpha0 times the summed timing error. Every Ai/ai remains a contraction. Bad-path probability changes the mean operator by at most twice that probability. These are block-encoding errors, not claims that the original and rounded continuous path measures have small total variation.

## 5. Matrix-entry LCU without an optimal matrix oracle
For r=2, ||exp(Mt)||<=exp(Gamma*t/2), so each of its 16 entries is at most that scalar. Select the 16 initial/final ancilla pairs uniformly, accept with probability exp(Mt)ji/exp(Gamma*t/2), and conditionally acquire the virtual bridges. The selected block is the ancilla matrix unit |j><i| tensored with the chronological product of normalized system blocks and its phase. A matrix unit has a simple norm-one unitary block encoding; fresh work registers for products prevent cross terms. On rejection select a zero block.

Prepare and unprepare the inner random-word registers coherently. The resulting mean block is K(t)/alpha0_event(t), with alpha0_event(t)=16exp(Gamma*t/2). This intentionally loose constant is harmless for short windows. The virtual sampler's finite random words are coherent LCU work, not a physical classical trajectory record; they are unprepared. No unlimited random oracle or global limited-independence seed is required here.

## 6. An integrable normalizer for actual first jumps
For one factor, write E_i(t)=exp(Mi*t). Its off-diagonal entry is
b_i=gi/(2omega_i)*(exp(si*t)-exp(-di*t)).
Therefore 2sqrt(lambda_i)b_i<=sqrt(Gamma_i)exp(si*t).

Its excited diagonal entry is
d_entry=si/(2omega_i) exp(si*t)+di/(2omega_i) exp(-di*t).
The first coefficient after multiplication by 2sqrt(lambda_i) is at most sqrt(Gamma_i), and the second term is at most 2sqrt(lambda_i)exp(-2lambda_i*t). Multiplying by the bounded other-factor row sums gives an explicit constant C such that all matrix-entry LCU weights for J_iK(t) are bounded by
C exp(Gamma*t/2)[sqrt(lambda_i)exp(-2lambda_i*t)+sqrt(Gamma_i)].

It is simpler to use a squared envelope

w_i(t)^2=C0 exp(Gamma*tau)[lambda_i exp(-4lambda_i*t)+Gamma_i], 0<=t<=tau,

with C0 a sufficiently large absolute constant including all 16 entry branches. Its integral is
C0 exp(Gamma*tau)[(1-exp(-4lambda_i*tau))/4+Gamma_i*tau],
which is bounded by an absolute constant on Gamma*tau<=1. Its normalized law is a mixture of a truncated exponential and a uniform, not a free arbitrary-density sampler. Square roots and inverse exponential CDFs are finite-bit arithmetic operations with their errors charged. A controlled entry/bridge LCU implements J_iK(t)/w_i(t).

## 7. Complete isometry amplification
Prepare an outer superposition of no-event and event branches with weights alpha0_event(tau)^2 and integral w_i^2. Within an event branch coherently acquire its time with density proportional to w_i^2. Retain this OUTER time/type/random-word register as the private Kraus record. Unprepare only the INNER virtual-path LCU registers.

The good block is the complete first-event isometry divided by
alpha=sqrt(alpha0_event(tau)^2+sum_i integral w_i^2),
an absolute constant for short windows. Its squared singular values on the input subspace are all 1/alpha^2. Pad to a fixed larger constant if helpful. Robust oblivious amplification can therefore produce the entire instrument; it would not generally amplify a lone nonunitary K(t) with its correct probability. Do not measure the outer register before this amplification.

Finite outer-time sampling must be coupled and analyzed in isometry norm. Exclude tiny uniform tails and price them; on the retained domain inverse truncated-exponential sensitivity is polynomial in lambda and cutoff inverses. Analytic K/w sensitivity and finite-bit inner block error are charged separately. Conservative squared or fourth-power internal accuracy suffices to keep all final trace-norm errors within budget. The precise complete error ledger remains a whole-review obligation.

## 8. Iteration, memory and remaining work
Measure or retain the private first-event record only after completing the instrument. On an event apply the returned J_iK(t) state, preserving both damping ancillas, and continue to the fixed end of the current short window. On no event advance to that window end. Split windows additionally at prescribed system-control times. Never reset the damping ancillas at a control or a no-event boundary.

The accepted jump MGF bounds the actual total event count from initially ground ancillas; cap it at O(Gamma*T+log(1/epsilon)). The number of no-event windows is O(1+Gamma*T+p). A uniform per-instrument error and a hybrid through this deterministic cap compare the approximate finite procedure to the exact stopped process; use the exact process's count tail, not an unproved tail for the approximate implementation.

Very short remaining windows can be advanced by identity with error bounded by their duration times a known norm bound on the full Lindblad generator. Choose the cutoff inversely proportional to that norm and the deterministic call cap. This costs logarithmic rate precision. Very early event-time tails need a corresponding isometry-error budget; they cannot simply be omitted as impossible.

The intended completed theorem is polynomial in physical resources and log switching rates/inverse error for TWO noise modes, with arbitrary noncommuting A1,A2. The 16-entry construction grows exponentially with a variable number of modes; no efficient arbitrary-mode extension is asserted. All source acquisition, bridge sorting, first-event normalization and timing error claims above remain subject to independent whole-chain review. This is a serious candidate mechanism, not yet an accepted completed algorithm.

## 9. Binding finite constants and duration-stability completion
For two modes one may take alpha0_event(tau)=16exp(Gamma*tau/2) and the deliberately generous squared event envelope w_i(t)^2=4096 exp(Gamma*tau)[lambda_i exp(-4lambda_i t)+Gamma_i]. Their total squared mass is at most 256e+4096e(1/2+1)<256^2 when Gamma*tau<=1. Thus a fixed amplitude normalizer A=256 is sufficient, with a zero good-block arm supplying unused mass. Known-success-amplitude isometry amplification uses only a constant number of base calls (plus accuracy-dependent gate synthesis); this is not an optimal constant or a practical resource claim.

The outer branch preparation can itself use a uniform seed and threshold comparisons: choose the no-event arm with probability alpha0_event^2/A^2, event arm i with probability integral(w_i^2)/A^2, and the zero arm otherwise. Within event arm i, map a separate uniform to the normalized mixture of truncated exponential and uniform. Retain these outer uniforms as part of the private output record. Their ideal good block obeys B^dagger B=I/A^2 because the branch probability and time density cancel w_i(t)^2. Inner virtual-path registers, in contrast, must be unprepared to form the desired operator mean.

For recursive virtual bridges, not only sampling error but remaining-duration perturbation must be bounded. On t>=zeta/2, let pmin bound all conditional transition denominators. The first-event density is q_i exp(-q_i u)P_(1-i),j(t-u)/Pij(t), plus a separate no-event flag when i=j. Its derivative in t, the no-event flag derivative and the moving-endpoint strip yield a TV Lipschitz constant bounded by an explicit polynomial in 1+qmax, 1+tau and 1/pmin; for example a sufficiently large constant times (1+tau)(1+qmax)^2/pmin^2 suffices. This bound concerns distributions, not a pointwise inverse-CDF derivative.

At step k couple the exact kernel at its true remaining duration to the exact kernel at the rounded duration by maximal coupling. Conditional on agreement, numerical sampling contributes at most another h to the absolute event-time discrepancy. Thus the discrepancy after k steps is at most kh, and the accumulated duration-induced mismatch is at most O(L Kcap^2 h), not an exponential product of Lipschitz constants. Choose h<=min(zeta/[10(Kcap+1)], eta/[C L(Kcap+1)^2]) and price the separate fixed-duration quantile/CDF error. This closes the changing-duration seam as well as preserving cross-color order.

## 10. Common-uniform isometry comparison, not timestamp total variation
A finite timestamp distribution is mutually singular with a continuous timestamp law. The first-event approximation is therefore not justified by total-variation distance between timestamps. Use the outer uniform coordinates and mixture labels as the common private record space. An ideal event-time arm has operator amplitude J_i K(t(u))/sqrt(q_i(t(u))) in L2(du), where q_i=w_i^2/integral(w_i^2), together with its outer branch weight. Embed finite uniform bins as their normalized indicator functions in that same L2 space. On retained uniform tails the inverse exponential sampling map and analytic normalized Kraus amplitudes have polynomial sensitivity in the encoded rates and cutoff inverses; the integrated squared amplitude error controls the isometry norm uniformly over inputs. Removed uniform tails contribute their bounded squared-amplitude mass. Choose these tail budgets conservatively as powers of the desired instrument error.

The representative timestamp is then used for the finite remaining-window computation. Its effect on subsequent propagation is charged separately by finite-time generator bounds and the previously stated duration stability. The private record may be measured only after the complete isometry amplification. This common-coordinate comparison is a mathematical analysis device, not an infinite-precision output register required by the circuit.

## 11. Intended theorem and explicit unresolved status
For fixed two modes, finite rational rates and prescribed control times, exact or precision-capable controlled block encodings of H0,A1,A2 with their precision costs paid, the candidate targets an unconditional controlled-process trace-norm approximation epsilon with total gates, space and random-word lengths polynomial in

1+alpha0*T+Gamma*T+p, input bit lengths and register widths,
log(2+lambda1*T+lambda2*T), and log(1/epsilon).

The construction is digital and keeps two damping ancillas between calls. It does not expose their state or jump records to the consumer. The primitive rate-dependent numbers can be large, but all loops are bounded virtual-event counts, actual-event/chunk caps, bisection depths and bit-arithmetic lengths. The proposed proof must verify this claim from the explicit source/instrument bounds above; a low expected count alone does not establish it.

No full-chain acceptance has been recorded for this candidate yet. In particular, the finite common-uniform isometry and conditional-source preparations must be read as constructions requiring their stated error ledger, not an invitation to assume a sampler, a Kraus oracle, a free matrix exponential or an efficient inverse CDF. The earlier exact dilation and jump-count theorem remain valid separately if this implementation join fails.

## 12. Exact outer amplitude convention
Let I_i=integral_0^tau w_i(t)^2 dt and q_i(t)=w_i(t)^2/I_i. The preparation probability I_i/A^2 and inner block J_iK(t)/w_i(t) combine to the good-block amplitude J_iK(t(u))/(A sqrt(q_i(t(u)))) in the normalized conditional uniform coordinate du. After amplification the event-arm amplitude is exactly J_iK(t(u))/sqrt(q_i(t(u))). Do not multiply it by another sqrt(I_i) factor. The outer branch weight has already canceled the denominator's normalization. The no-event amplitude is K(tau). This formula supersedes any ambiguous reading of Section10's phrase about an outer branch weight.

The subsequent global comparison must also retain the private timing convention. Compare exact and finite records through their common uniform coordinates, not timestamp TV. At a representative-time error Delta t, use the exact remaining-window Markov channel's diamond continuity bound at most ||L_ext||_diamond*|Delta t| (with conservative additional factors for finitely many prescribed windows). The consumer cannot inspect private times or apply a discontinuous strategy to them. Controls are at fixed window boundaries. Charge this continuation error, the L2 Kraus-amplitude error, and near-window-endpoint/very-early-event tails in the total hybrid. An unqualified diamond comparison of channels exposing their continuous versus digital time records would be false.
