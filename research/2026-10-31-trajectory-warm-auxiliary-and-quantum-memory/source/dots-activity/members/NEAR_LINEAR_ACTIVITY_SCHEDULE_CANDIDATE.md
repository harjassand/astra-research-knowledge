# A fixed-window schedule with near-linear activity and Hamiltonian action
31 October 2026. Root candidate for independent review. This is a resource refinement of the frozen reviewed graded receiver, not a change to its physical model or an implementation claim.

## 1. Receiving premises
Receive the whole common-loss graded receiver (source SHA93731752d0d34c2fcfa1e7fb0b6812b88f90d301083d32ecd60525cee5b543c9, whole receipt SHA8aa67eda1b857be0fccb55e6c711ffc1e2c783787030e117266a159e3a9ccd65), its acquired marked bridge, and the reviewed uniform occupation bound (source136e1cf32b06eac6dbfba53f1e7c4a91783c607233779f2cf7ce55fa234509dd). All common-loss, initial-vacuum, private-clock, prescribed-control and actual-access restrictions remain.

Write G=g^2 T/lambda, ell=lambda T, mu=g^2/(4lambda^2). Choose the existing global cutoff L by the better of its two proved bounds. In particular the uniform bound permits

    L=O(1+mu+log(2+Tg)+log(1/epsilon)).

The system free Hamiltonian on the cutoff has an ACTUALLY ACQUIRED block encoding of normalization alpha_f(L). Assume standard controlled qubitization of that encoding, so a fixed physical duration t at error delta costs O(1+alpha_f(L)|t|+log(1/delta)) queries, with the actual selection/arithmetic cost per query paid. This refinement does not apply to an arbitrary opaque C_f promise without this resource property.

## 2. Choose a tighter known maximum duration
In normalized time define

    D=16G(L+1)+p+log(100/epsilon)+2,
    tau=1/D,
    M=ceil(G(e-1)+log(100/epsilon))+1,
    W=ceil(1/tau)+p+1, S=M+W+2.

Split the prescribed schedule into pieces of length at most tau. This is within the original row/column-normalization limit. The additional prescribed boundaries require at most p extra pieces. Both the actual-event cap and the number of no-event pieces are therefore covered by S. Directly,

    S=O(G(L+1)+p+log(1/epsilon)+1),
    S*tau=O(1).                                         (1)

These are worst-case deterministic bounds, not expectations over selected paths.

The existing complete first-event normalizer is A=O(sqrt(L+1)), with its safe fixed constants retained. Redefine e_step, beta, eta and sigma using this S exactly as in the frozen receiver. Their inverse logarithms are O(log(S/epsilon)+log(L+1)), up to fixed constants. The tighter tau only changes already priced scalar precision.

The mean candidate-immigration count is at most Gtau/2<=1/[32(L+1)]. Consequently the existing Chernoff cap is

    Hcap=O(1+log(S/epsilon)+log(L+1)),
    Kcap=2L+2Hcap=O(L+log(S/epsilon)).                     (2)

The acquisition/arithmetic of each scalar bridge and source list is polynomial in L, Kcap, register/input bit lengths and the required precision bits. It contains no further polynomial factor G; rate magnitudes enter precision logarithms. This follows from the explicit finite endpoint factorial lists, capped CDF scans and marked-source arithmetic in the received proof, not a new source oracle.

## 3. Actual bounded-duration circuit
Let every H_f interval have normalized duration t in[0,tau]. Store its fraction t/tau in B binary fractional bits, rounding to a declared representative. For every bit k execute a controlled fixed-time evolution with physical duration T*tau/2^k. There are B such calls, including ones whose controls are zero on a particular branch. Each gets operator error at most delta_slot/B.

For ONE interval slot, the sum of the fixed durations in this ACTUAL circuit is

    sum_(k=1)^B T*tau/2^k <= T*tau.

Hence the qubitization query cost of the slot is

    O(alpha_f(L) T tau + B[1+log(B/delta_slot)]).        (3)

This is not an assertion that realized source-path durations add to T. Every slot pays the same complete controlled binary circuit. The known scale tau is compiled into its fixed durations; there is no2^B lookup table or free variable-time oracle. Rounding error is bounded by alpha_f(L)Ttau2^{-B}, and all earlier source/outer-time constraints can be enforced by increasing B.

The required B is polynomial in input description lengths and logarithms of S/epsilon, ell, 1+alpha_f(L)T, plus the finite small-positive-parameter conditioning bits already required by the receiver. For rational finite-description parameters the elementary sums/products defining D and tau can be computed to the same budgets. One may select a dyadic lower value tau' in[tau/2,tau] to make its digital representation exact; (1)-(3) change only by constants. Use that tau' consistently in all scalar windows and budgets.

## 4. Sum the paid calls
A no-jump/event source word has at most Kcap+1 free-evolution slots. Complete-isometry amplification costs O(A) applications of the base construction and its inverse. There are at most S first-event calls. Combining (1)-(3), the total number of calls to the acquired H_f block encoding is bounded by

    O(A(Kcap+1) alpha_f(L) T
       + S A(Kcap+1) B[1+log(B/delta_slot)]).           (4)

Inverses and control flags change only constants. This sums the actual fixed-duration circuits, not the chosen stochastic durations.

Coupling-block queries and acquired removal/stack operations cost O(S A(Kcap+1)), up to their polynomial-in-r selection overheads and their already priced synthesis. Each finite source/list/arithmetic operation costs polynomial in r,L,Kcap,B and input/precision lengths. Thus a safe total elementary-gate envelope has the form

    [1+G+p+alpha_f(L)T]
       * poly(r,L,input lengths, log(2+G+p),
              log(2+ell), log(1/epsilon),
              log(2+alpha_f(L)T), conditioning bits),  (5)

Here (5) is an elementary-gate bound ONLY when the supplied H_f and coupling encoding circuits have gate costs polynomially bounded by the displayed circuit/input sizes and precision lengths. An opaque query oracle does not supply that gate-cost guarantee. In the general access model retain the explicit bound

    Q_H C_H(delta_H) + Q_F C_F(delta_F)
      + S A poly(r,L,Kcap,B,input/precision lengths)
      + actual consumer costs,

where Q_H is (4), Q_F=O(S A(Kcap+1)) up to the actual selection overhead, and C_H,C_F are the REAL per-query gate implementation costs at the allocated accuracies. The polynomial's degree in the non-oracle arithmetic is fixed by the explicit arithmetic and state-preparation choices. Formula (5), when its circuit-cost premise holds, means near-linear dependence on the extensive action scales after the displayed polynomial L and bit factors are separated; it does not mean small constants.

For bounded mu, L is logarithmic in Tg and inverse error. Since Tg=sqrt(G ell), this makes L polylogarithmic in G,ell,1/epsilon. For the explicit Bose–Hubbard/Kerr encoding, alpha_f(L) is itself a polynomial in L times the ordinary coefficient action scales. The resulting bound is near-linear in accumulated activity, prescribed-control count and ordinary free-Hamiltonian action, with polynomial factors in r and logarithmic magnitude/precision/input costs. A free diagonal-H_f phase routine can improve its own term, but is not required for (4).

## 5. Limits and lower-bound comparison
The refinement uses the reviewed time-uniform occupation theorem plus an explicitly bounded-duration qubitization schedule. It does not rely on an expected jump cap for the approximate algorithm, conditioning on good trajectories, an unpriced source operation or generic fast-forwarding of H_f.

The separate exact hard-core clock/parity construction, if independently accepted, gives an Omega(G) supplied-coupling query lower bound at constant error and lambda>=Gamma (hence bounded mu). That would make linear activity unavoidable in this oracle sense, while leaving precision factors, mode dependence, constants and gate complexity open. It would not show that the entire upper bound is optimal or practically superior. No numerical implementation or benchmark is established here.
