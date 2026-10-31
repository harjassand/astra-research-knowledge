# Acquired random-map extension and multistep return: the shuffle example
31 October 2026. Constructive local work. This is not a whole succinct-source compiler or a novelty claim. This note develops the shuffle example and symmetry improvement, and checks the exact CP interface, acquired operations and a finite Lyapunov activity bound.

## 1. Random maps give a quantum extension, with a time-reversal convention
Let a finite row-stochastic matrix P have positive stationary pi. Suppose P is realized as E K_f, where K_f h(y)=h(f(y)) for a random deterministic map. Put psi_x=sqrt(pi_x), S=diag(psi), T_f=S K_f S^(-1).

Then T_f psi=psi, E T_f^dagger T_f=I by stationarity, and M=E T_f is a contraction with Mpsi=M^dagger psi=psi. Consequently
Phi(rho)=E T_f rho T_f^dagger
is CPTP and fixes the pure state P0=|psi><psi|.

Its adjoint on diagonal observables is the TIME REVERSE P_rev:
Phi^dagger(diag h)=diag(P_rev h),
(P_rev)_xy=pi_y P_yx/pi_x.
It is P itself only in the reversible case. This orientation cannot be silently dropped for card shuffles or noncommuting noise couplings.

For finite random-map outcomes f with probabilities p_f, dark jumps
L_f=sqrt(p_f)(T_f-I)
and Hamiltonian H_env=(i/2)(M-M^dagger)
give the generator Phi-I exactly. The cross commutator from the dark-jump expansion is canceled by this H_env. Moreover
C=sum L_f^dagger L_f=2I-M-M^dagger,
0<=C<=4Q, Q=I-P0,
and the no-jump generator is M-I.

These are direct algebraic identities, not a free circuit theorem. Random-map and stationary-amplitude operations must still be acquired. Exact diagonal-algebra preservation then gives the same stationary classical-source controlled process under system-only couplings through those diagonal observables, as in the earlier source-receiving argument.

## 2. Coalescence is a weighted CP statement, not just a probability
A product of T maps corresponds to a composed deterministic map. If that map is constant with value x, its matrix is |psi><x|/sqrt(pi_x).

Let E_good be a chosen coalescence event in the independent map sequence. Its CP contribution is
rho -> P0 sum_x a_x rho_xx,
a_x=Pr(root=x,E_good)/pi_x.
Thus a small ordinary failure probability does NOT by itself guarantee dimension-free quantum reset. One needs a pointwise bound on these stationary-normalized root probabilities. In general the residual CP effect is bounded only by failure/pi_min.

For uniform pi on d states this crude bound is d times failure. It can still be useful if an exponential coalescence tail makes log d affordable, but it is not a dimension-free identity. If conditional on E_good the root law is EXACTLY pi, then a_x=Pr(E_good) and the favorable branch is exactly Pr(E_good) times the reset channel. The remainder is a subnormalized CPTP component, giving a diamond reset bound of twice the failure probability. This is the important normalization seam.

## 3. Explicit exponentially large source: shuffle maps
Take d=n! permutations of n labeled cards and uniform pi. Let f_c move card c to the top, with c chosen uniformly. Its row kernel P is random-to-top. The quantum extension above therefore has classical diagonal restriction P^T, namely TOP-TO-RANDOM. This is the admitted classical source in this construction.

The map T_c has one unit entry per row and n preimages for every permutation whose top card is c. Its norm is sqrt(n). Nevertheless the full channel Phi=(1/n)sum T_c rho T_c^dagger has an elementary Stinespring isometry:
given input permutation x, retain c=x_top; remove c, then coherently reinsert it into a uniform position j=1,...,n; output the new permutation and private color c.
The pair (output permutation,c) reconstructs the input by moving c to the top; the position register is recoverable as c's output position. Thus scratch can be uncomputed coherently. This is exactly the Kraus family T_c/sqrt(n), not an amplitude postselection with probability1/n!.

It uses polynomial n and precision arithmetic on O(n log n) permutation bits. Invalid encodings have explicit extensions/flags. A controlled block for L_c=(T_c-I)/sqrt(n) is acquired by the color-selected Stinespring block minus I/sqrt(n), with normalization at most2 and actual polynomial selection overhead. There are n jump labels, not n! edges.

The uniform pure permutation state is also acquired: prepare independent uniform mixed-radix digits and reversibly unrank their permutation, uncomputing the digits by inverse ranking. This is a bijection between n! digit strings and permutations. Range-state preparation and arithmetic require polynomial n and precision work; no generic coherent stationary-distribution oracle is assumed.

A normalization-one block of P can be built from explicit uniform outgoing random-to-top and incoming top-to-random neighbor preparations by the usual row/column overlap. Its inverse supplies P^dagger, so the environmental Hamiltonian and C are acquired without enumerating d.

## 4. Symmetry earns dimension-free multistep reset
After every card label has appeared among k independent choices, the composed move-to-top map is constant, determined by the order of occurrences rather than the initial permutation. This remains true if the product convention reverses the sequence.

The event all labels appeared is invariant under arbitrary relabeling of the cards. The constant root transforms equivariantly. Card relabelings act transitively on all permutations, so the root conditional on this good event is exactly uniform. It is enough to use this sufficient good event; it need not be the exact coalescence event.

A union bound gives failure delta_k<=n exp(-k/n). Hence
Phi^k=(1-delta_k)Reset_psi+delta_k Xi_k,
with Xi_k CPTP and fixing P0, where delta_k here denotes the actual chosen-event failure probability. In particular
||(Phi^k)-Reset_psi||diamond<=2delta_k,
(Phi^dagger)^k Q<=delta_k Q.
There is NO d=n! factor.

Choose K=ceil(n log(2n)). Then delta_K<=1/2. Define
W=sum_(j=0)^(K-1) (Phi^dagger)^j Q.
It satisfies Q<=W<=KQ and (Phi^dagger-I)W<=-Q/2. This gives an explicit finite multistep potential despite the one-jump return obstruction.

## 5. A checked high-rate activity bound using that potential
Scale the source generator to lambda(Phi-I), use its dark jumps sqrt(lambda)L_f, and couple to a system by sqrt(lambda)A with ||A||<=b. System-only drift and prescribed instruments commute with W. An accessible centered coupling may be imposed for a later compiler; the moment argument itself only needs the norm bound.

Let kappa=exp(theta)-1<=1/(32K), and take V_theta=I+32kappa W. The tilted dissipative/environmental part obeys
lambda[32kappa L0^dagger W+kappa C+32kappa^2 sum L_f^dagger W L_f]
<=-8kappa lambda Q,
using L0=Phi-I, C<=4Q and W<=KQ.

The Q/Q block of i32kappa sqrt(lambda)[A,W] has norm at most64kappa sqrt(lambda)bK. If sqrt(lambda)>=16bK, it consumes at most4kappa lambda Q. The P0/Q cross block has norm at most32kappa sqrt(lambda)bK. Completing the remaining square against -4kappa lambda Q gives
L_theta^dagger V_theta<=256kappa b^2K^2 P0<=256kappa b^2K^2 V_theta.

The initial source state is P0, so its V_theta moment is one. Thus
E exp(theta N_T)<=exp[256 b^2K^2 T(exp(theta)-1)]
for lambda>=256b^2K^2 and the stated theta range. Differentiation at zero gives mean count at most256b^2K^2T; a Chernoff bound gives a cap of order b^2K^2T+K log(1/error).

This proof explicitly handles the Q A Q commutator. Ignoring it would invalidate the finite-potential substitution. The alternative potential I+16kappa W with the stronger sufficient threshold sqrt(lambda)>=64bK gives the same rate constant and is also valid.

Below the threshold, ordinary supplied-block Lindblad simulation has source action lambda T bounded by a polynomial in n and b^2T. H_env and the n dark jumps have polynomial acquired normalizations. This observation is not yet a full high-rate no-jump compiler.

## 6. A basic acquired fast contraction, and its limitation
The random-map coupling also bounds classical P powers. Compare a fixed starting state with an independent uniform starting state under the same maps. On the all-labels-seen event they agree. Thus ||P^k-P0||_infinity<=2n exp(-k/n). Double stochasticity gives its induced1-norm at most2, so
||P^k-P0||_2<=2sqrt(n)exp(-k/(2n)).
Poissonization yields
||exp[t(P-I)]Q||<=2sqrt(n)exp(-t/(4n)).

For t below a polynomial n/log-error cutoff, positive Poisson sums of powers of the acquired contraction P give a normalization-one block with polynomial degree. Above that cutoff, P0 plus zero on Q approximates the full unscaled contraction. P0 itself is acquired from the uniform permutation preparation. Time arithmetic depends on log t rather than a microscopic event loop.

This is an UNscaled contraction operation. A later two-sector compiler may require an exponentially rescaled hidden contraction or a different norm/phase interface. That stronger operation must be earned separately; the displayed decay estimate alone is not a circuit for it.

## 7. Exact small checks and comparison
The script check_shuffle_extension.py verifies, in exact SymPy arithmetic for n=2,3, trace preservation, the dark-generator/Hamiltonian identity and the reversed diagonal restriction. It also exhaustively checks constant maps and uniform conditional roots for (n,k)=(2,3),(3,3),(3,5),(4,4),(4,5). All tests pass. They are diagnostics, not substitutes for the proofs above or an implemented simulator.

Coupling from the past is established prior machinery, not a new concept here. The primary Propp–Wilson paper describes coupled-chain exact sampling: https://www.stat.berkeley.edu/~aldous/206-RWG/RWGpapers/propp_wilson.pdf . Quantum extensions preserving classical algebras are likewise prior machinery; see Bardet https://arxiv.org/html/1509.04849 . Their existence statements do not automatically provide the particular pure return, normalization and coherent-access conjunction used above.

Coherification and quantum perfect-sampling literature is separately relevant. Those comparisons must remain part of any later originality assessment; no claim of first quantum coupling, first extension or first rank reduction is made here.

The concrete outcome is a succinct nonreversible source with d=n! classical states, polynomial acquired pure-state/channel/jump operations, a dimension-free symmetry-normalized multistep return, and a polynomial-in-n high-rate activity potential. It does not yet establish the complete source-plus-system compiler, eliminate actual system/coupling acquisition costs, grant a free classical mean subtraction, or prove advantage over direct classical shuffling and ordinary quantum/classical process simulators.
