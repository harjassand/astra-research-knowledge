# Actual witness transfer under nonfactor syndrome free energy

2026-11-01, 23:50 UTC. Independent binding of the THERMAL TAIL implication, not a proof of the clock free-energy premise. Read ROOT_CONDITIONAL_THERMAL_TRANSFER.md, the audited actual full-trace binding, and the primary actual-code source https://arxiv.org/html/2605.10943v1 Sections 5.1–5.4, especially Lemma 5.8 and Theorem 5.13.

## Verdict

**PASS conditional on the stated exact influence bound.** The original actual-code witness surgery remains valid. Neither X/Z factorization of the probability law, positivity of effective interaction coefficients, spatial short range of R, nor independent clock excitations is needed. The source's original witness entropy argument applies with its dimensionless inverse temperature replaced by

 B = 2 beta J0 (1-epsilon).

The full-trace representation gives an independent, potentially more conservative proof. No missing correction surgery was found. Clock free-energy control and dynamical-consumer conditions remain separate prerequisites.

## 1. Precise measure and sign convention

Write x_a=(1-s_a)/2. Let Omega_X and Omega_Z be the valid syndrome vector spaces for the two CSS sectors; valid joint syndromes form Omega_X times Omega_Z. This is an ALGEBRAIC product of allowed sets, not an assertion that their thermal law factorizes. CSS X- and Z-type Pauli errors generate the two sectors independently. All valid joint stabilizer sectors have the same dimension, namely two in the actual family.

Assume exactly

 F(s)=c-J0 sum_a s_a+R(s),
 R(s)=sum_(A nonempty) r_A product_(a in A) s_a,
 sup_a sum_(A containing a) |r_A| <= epsilon J0, 0<=epsilon<1.

Then the syndrome law after tracing ALL clock states is

 mu(s)=exp[-beta F(s)]/sum_(u valid) exp[-beta F(u)].

Equal logical multiplicity cancels. No factorization of Tr_clock exp[-beta H_anc(s)] is used. If the native Hamiltonian is related by the exact unitary U, this is the probability of the dressed syndrome projector U(P_s tensor I_clock)U† in its Gibbs state.

For any two valid sign strings differing on D,

 |R(s)-R(s')|
 <=2 sum_(A:A meets D) |r_A|
 <=2 epsilon J0 |D|.

The first inequality is conservative: only odd intersections actually contribute. It remains valid for mixed-sector, disconnected and system-spanning A. No geometric support condition is required for this static estimate.

## 2. Actual source witness surgery, not assumed polymer removal

For one CSS sector, source Section 5 uses the SAME modified decoder stopping at level 2. Lemma 5.2 says vanishing level-2 residual implies stability under the relevant single-qubit errors. Thus unstable configurations are contained in B_X={x: x_2!=0}, and analogously B_Z for the dual sector. The source's text sometimes informally reverses implications; only the sufficient stable criterion and its contrapositive are needed here.

For every x in B_X, the selected root-connected decoding history has a top-level witness tau with:

 1. tau is contained in the occupied top syndrome x;
 2. tau is itself a VALID syndrome (a coboundary), proved by source Lemma 5.8 using the actual correction lifts and the terminal level-2 syndrome;
 3. its history has at least 2^(k-1) nodes for the level-2k family;
 4. its entropy and total multilevel syndrome mass satisfy source Lemmas 5.9–5.12.

Fix any such top witness tau, and fix the OTHER sector y. The map

 T_tau:(x,y) -> (x+tau,y)

is an involutive syndrome translation and is injective on the event tau subset x. Both endpoints are valid because x,tau are coboundaries. On this event it deletes exactly |tau| negative signs and creates none. It need not preserve which witness the decoder chooses after deletion. Injectivity for a FIXED witness is enough; no globally injective map across all possible witnesses is claimed or required.

The energy difference obeys

 F(x,y)-F(x+tau,y) >=2J0(1-epsilon)|tau|.

Consequently, for every y,

 mu_X(tau subset x | y)
 <= exp[-B|tau|] sum_(x:tau subset x) mu_X(x+tau | y)
 <= exp[-B|tau|].

The conditional partition function cancels. Every transformed term belongs to the SAME conditional normalization sum. This is the decisive reason cross-sector R couplings do not obstruct the proof. The ratio is uniform in y, so averaging over y after the witness union bound preserves it.

## 3. Same actual witness entropy estimate

Let Delta be the source decoding-graph degree, Delta_level the same-level degree, M_ell the maximum local syndrome-block size, and C_seed the fixed level-2 root-count prefactor. Define

 W(B)=(1+exp(-B/4))^(M_ell)-1,
 z(B)=2(Delta+1)^2 W(B)^[1/(1+Delta_level^4)].

The source's counting lemmas imply, uniformly in the other-sector condition y,

 mu_X(B_X | y) <= C_seed sum_(m>=2^(k-1)) z(B)^m.

This bound copies only the COMBINATORIAL sum after replacing the fixed-witness probability by exp[-B|tau|]. The product of local sums W_v in that counting argument is an upper bound obtained by dropping witness-consistency constraints. It is NOT an invocation of factorization of the actual Gibbs measure. Thus the proof survives arbitrary X/Z couplings in R.

For z(B)<=1/2,

 mu(B_X) <=2 C_seed 2^[-2^(k-1)].

Use the corresponding dual constants for B_Z and take a union bound. Hence

 mu(B_X union B_Z) <= C exp[-c 2^k]
                    <= C' exp[-c' n^nu]

with the actual family's fixed size/depth exponent nu>0. Keeping a harmless fixed C_seed is conservative: source Lemma 5.9 displays |V_2|, which is suppressed in a later displayed sum. No claim about its exact prefactor 2 is needed. The source's threshold is retained after the explicit effective-temperature substitution B; no new factorization assumption or extensive free-energy error is introduced.

## 4. Independent positive full-trace proof

The banked actual full-stencil trace representation supplies individually valid components gamma, total marked mass m_gamma<=A |x_gamma|, O(n) host objects and at most K^m rooted mass-m candidates. Deleting a fixed gamma is valid by the exact splitting/recombination theorem. Its occurrence probability under the NONFACTOR law is at most exp[-B |x_gamma|], by the same injective deletion argument; factorized polymer activities are unnecessary.

If the actual level-2 residual is nonzero, at least one trace component has nonzero isolated residual there. Every-two-level halving forces its top syndrome weight at least 2^(k-1); in particular its marked mass is at least that large. Therefore

 mu(B_X) <= C n sum_(m>=2^(k-1)) [K exp(-B/A)]^m.

Choose B>A log K with fixed slack. This independently yields poly(n) exp[-c 2^k]. It may have much worse constants than the original source entropy bound, but confirms that the trace-component surgery mentioned in the root is sufficient. A mere global large-syndrome-weight argument would NOT suffice, because typical syndrome weight is extensive; the connected witness/component is essential.

## 5. Enlarged bounded-contact stable set: all prefixes, both sectors

Let z_inc bound the number of actual checks incident to any data qubit. For any data Pauli P of weight at most b, its syndrome translation d(P) flips at most z_inc b checks and is a bijection of the valid joint syndrome space. Unlike witness deletion, some flips can create defects. The general estimate gives

 |F(s+d(P))-F(s)| <=2J0(1+epsilon) z_inc b.

Hence for any event E,

 mu(E+d(P)) <=exp[2 beta J0(1+epsilon) z_inc b] mu(E).

Let B=B_X union B_Z, and define the enlarged bad event

 B_b = union_(Pauli P:wt(P)<=b) [B+d(P)].

The number of phase-free Paulis here is at most sum_(j=0)^b 3^j binom(n,j)=O_b(n^b). Thus

 mu(B_b) <= O_b(n^b) exp[2 beta J0(1+epsilon)z_inc b]
              C exp[-c 2^k].

For fixed b, beta, J0 and epsilon, this remains stretched exponentially small. This deliberately conservative enlargement covers all Pauli prefixes in any ordering: each prefix of a product supported on at most b data qubits is another Pauli of weight at most b, even when Y is split into X and Z. There is no additional factorial over orders. Including both CSS bad events protects both decoded logical generators, and linear expansion then handles the entire bounded-contact data operator algebra on the enlarged stable subspace.

If a bounded-depth finite-range native conjugation U enlarges each admitted native contact to at most b DATA qubits plus clock operators, b must be fixed after that conjugation. The static argument bounds the dressed projector P_bad,b tensor I_clock exactly. It does not itself prove a Davies-frequency-resolution or clock-operator algebra claim; that belongs to the dynamics audit. Arbitrary unbounded-support native contacts are not covered.

## 6. Exact premises and limits

- The required premise is a UNIFORM per-check influence bound for the EXACT finite-temperature conditional free energy. A ground-energy approximation or O(epsilon n) total free-energy error does not imply it.
- Clock excitations are already included in F. No assumption that the clock Gibbs state is globally close to vacuum enters.
- Long-range/mixed-sector r_A are allowed for this thermal tail. They may create separate locality/dynamics problems, which this result does not resolve.
- If an approximation leaves additional error in a syndrome deletion ratio, it must be included explicitly and checked against witness size. An arbitrary additive bad-probability floor could destroy the stretched tail.
- Stability here is the actual fixed decoder's original stable criterion enlarged to bounded-contact prefixes. No replacement logical frame, generic physical perturbation robustness, loading/readout theorem, or automatic dynamical lifetime is inferred.

**Decision:** the thermal-witness transfer is not an additional missing premise once the exact free-energy influence bound is earned. The decisive remaining clock construction gate is proving that bound at finite temperature with fixed volume-independent native parameters; dynamical contact/rate control is independent.
