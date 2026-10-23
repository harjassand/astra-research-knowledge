# Independent challenge of the adaptive coherent-history bound

Reviewer: `/root/feedback_incorporation`  
Date: 21 October 2026  
Construction owner: `/root`  
Scope: only the new adaptive weighted-history step for `V_s = cos(s) U + i sin(s) I`, together with its direct rank/error consequences. This does not repeat the old tree or recurrence audit.

## Verdict

**The proposed bound is valid.** The common-environment and common-Kraus-index obligations can be proved directly from the accepted frozen-transcript lemma. This avoids any reliance on an ordinary block diamond-distance estimate for an adaptive protocol, and avoids promoting classical feedback to a quantum communication resource.

For the fixed diagonal normal initializer and any allowed fixed-n feedback protocol transmitting a K-dimensional logical system, define `a = 2 sqrt(2)`, `M_j = floor(a^j)`, `alpha = |cos s|`, `beta = |sin s|`, and

`R_n(q) = sum_(0 <= k <= floor(qn)) binom(n,k) 3^k M_(n-k)`,

`T_n(q) = sum_(k > qn) binom(n,k) alpha^(n-k) beta^k`.

Then

`F_e <= min{1, (R_n(q)/K)(1+T_n(q))^2 + (2+T_n(q))T_n(q)}`.

The truncation is a coherent amplitude truncation, not a classical random-mixture approximation. The absolute amplitudes in T, rather than their squares, are necessary for the stated argument.

## 1. The perturbed interaction and its scope

Because `U = U*` and `U^2 = I`, the operator `V_s` is unitary. The inherited stationary product density commutes with U, hence also with `V_s`, so the same `eta tensor tau_pi` is stationary. No bath state or device parameter is adjusted with the horizon.

The claim concerns this explicit coherent one-parameter family. It does not prove stability for every small operator-norm perturbation of U. An arbitrary perturbing interaction can alter the vertex transition structure used below.

## 2. Freeze one physical feedback strategy

Fix its prescribed causal local maps, including its measurable dependence on the actual classical transcript. These maps are held fixed while considering different device histories. A replacement history h is a subset of the n slots: at the k slots in h the device uses I, and at all other slots it uses U. The same local strategy can be run on each such history; it remains a legal deterministic protocol, since its local maps and complete instruments are defined on their full input spaces.

The accepted transcript lemma applies to each history and to `V_s` itself. For a complete classical transcript t, it gives the **same** encoder `E_t` and receiver branch map/density `D_t`, independent of h. Only the device block operator changes.

Use the same measurable Kraus lists `E_(t,a)` and `D_(t,b)` for all histories. They can be chosen from columns of the positive square roots of the finite-dimensional Choi operators. For continuous outcomes, use the common dominating transcript measure obtained from Bob's receiver instrument. Pointwise CP densities need not be trace-nonincreasing; integrated physical completeness is what is used.

For a diagonal initial density `tau = sum_v pi_v |v><v|`, define

`A^h_(w,v) = <w| W_h |v>`,

`F_mu(h) = sqrt(pi_v) D_(t,b) A^h_(w,v) E_(t,a)`,

where the common environment index is `mu = (t,b,a,v,w)`. For continuous t, sums below mean the corresponding positive integrals. The root's main stationary initializer is a special case; stationarity is not required for this rank argument.

## 3. A common isometric dilation follows from completeness

Each replacement-history protocol is deterministic, so

`integral sum_(a,b,v,w) F_mu(h)* F_mu(h) dmu(t) = I_K`.

Consequently the map

`Z_h : psi -> (F_mu(h) psi)_mu`

is an isometry into one common direct-integral environment space, with final logical output Lhat. All histories have the same environment coordinates. This constructs the needed common dilation explicitly; no abstract comparison of separately chosen Stinespring dilations is being assumed.

For the actual device, expansion of only its n interaction gates gives

`A^(s)_(w,v) = sum_h c_h A^h_(w,v)`,

`c_h = (cos s)^(n-|h|) (i sin s)^|h|`.

The fixed transcript factors are unchanged, so

`F_mu(s) = sum_h c_h F_mu(h)`

and therefore, in the same environment,

`Z_s = sum_h c_h Z_h`.

This is exactly a Stinespring isometry of the actual adaptive logical channel. Each `Z_h` has norm one. If `Z_low = sum_(|h| <= qn) c_h Z_h`, then directly

`||Z_s-Z_low|| <= sum_(|h| > qn) |c_h| = T_n(q)`.

This is a uniform estimate for the fixed complete adaptive strategy, including its reference extension, and its right-hand side is independent of the strategy. The potentially difficult compatibility of purification and transcript indices is thus resolved by a single explicit Kraus representation.

No backward quantum wire is operationally introduced. The common environment is mathematical and traced out. In particular, actual classical transcripts remain mixed; only the unobserved move/stay amplitude histories interfere within each transcript.

For nonatomic outcomes one should not write literal uncountably many orthogonal pointer copies or assert a normal dephasing channel on all of `B(L^2)`. The direct-integral construction above is the appropriate statement. Measurability and normality ensure the relevant instrument integrals are defined. The classical-feedback invariant already supplies the finite-dimensional Choi cone closure needed for these integrals and for well-defined operational limits.

## 4. Individual ranks after coherent truncation

If h has k identity slots, those k ports pass through unchanged and do not move E. Up to input/output tensor-factor permutations,

`A^h_(w,v) = I_(3^k) tensor A^(n-k)_(w,v)`.

The inherited tree path bound therefore gives

`rank A^h_(w,v) <= 3^k M_(n-k)`.

Local multiplication cannot raise rank. The low-history Kraus operator is

`F_mu(low) = sum_(|h| <= qn) c_h F_mu(h)`.

Subadditivity of matrix rank, with the same mu on every summand, yields

`rank F_mu(low) <= R_n(q)`.

It would be incorrect to average history ranks by squared amplitudes or to use a mixture of history channels: either operation would erase cross-history interference. The actual low map retains all of those cross terms because its Kraus operators are the coherent sums above.

## 5. The low map need not be trace preserving

The operator `Z_low` defines a CP logical map. It generally does not define a trace-preserving map. However,

`||Z_low|| <= ||Z_s|| + ||Z_s-Z_low|| <= 1+T_n(q)`.

For the normalized maximally entangled logical input, let `rho` and `rho_low` be the actual and low decoded Choi operators. Then

`Tr rho_low <= (1+T_n(q))^2`.

The individual-rank fidelity estimate remains valid for a subnormalized positive Choi operator:

`<Phi_K|rho_low|Phi_K> <= (R_n(q)/K) Tr rho_low`.

For completeness, this follows from `|Tr F|^2 <= rank(F) Tr(F*F)` without invoking trace preservation.

Let the two corresponding global vectors be psi and psi_low. Their norms are at most 1 and `1+T`, and their difference has norm at most T. For any effect P of norm at most one,

`|<psi|P|psi> - <psi_low|P|psi_low>| <= (2+T)T`.

Take P to be the decoded maximally entangled projector tensored with the identity on the mathematical environment. Combining the last three bounds proves the displayed fidelity inequality. No normalization of the low map is performed, so there is no missing denominator or success probability.

## 6. Exponents and the numerical example

Write `c = log2(a) = 3/2`, `r = 3/a > 1`, and binary entropy `H2`. For

`0 < q < r/(1+r)`,

the function `H2(x)+x log2 r` increases over `[0,q]`, so the standard binomial coefficient bound gives

`R_n(q) <= (n+1) 2^[n(c+H2(q)+q log2 r)]`.

If

`q > beta/(alpha+beta)`,

the function `H2(x)+(1-x)log2 alpha+x log2 beta` decreases for `x >= q`. Therefore

`T_n(q) <= (n+1) 2^[n g(q)]`,

`g(q) = H2(q)+(1-q)log2 alpha+q log2 beta`.

When `g(q)<0`, every communication rate strictly greater than

`c + H2(q) + q log2 r`

has entanglement fidelity decaying exponentially. Polynomial prefactors do not alter the threshold.

For `q=1/100` and `0 < beta <= 1/512`, the tilt condition holds and

- Rank exponent: `1.5816427609031227`.
- Full qutrit rate: `log2(3) = 1.584962500721156`.
- Gap: `0.0033197398180333515` qubits per forward slot.
- Safe tail exponent, dropping the nonpositive alpha term: `H2(.01)-.09 = -0.009206864104088816`.
- Tail exponent at the largest beta, retaining alpha: approximately `-0.009209588314474507`.

The strict rank comparison can be verified with integers rather than floating-point logarithms: it is equivalent to

`8^99 * 100^200 < 9^99 * 99^198`.

This exact inequality holds. For tail negativity, `H2(q) <= q log2(e/q)` and `100e < 512` already give a fully analytic strict bound. At beta=0 the original exact device bound applies directly.

## 7. Upper semicontinuity along this family

A convenient analytic choice for `0 < beta <= 1/512` is `q=3 beta`. It exceeds the tilt and tends to zero with beta. Since `H2(q) <= q log2(e/q)` and `log2 alpha <= 0`,

`g(3 beta) <= 3 beta log2(e/3) < 0`.

Thus one may also state the explicit upper bound

`Q_backward-classical(V_s) <= 3/2 + H2(3 beta) + 3 beta log2(3/(2 sqrt(2)))`.

It implies `limsup_(s -> 0) Q_backward-classical(V_s) <= 3/2`, with an upper modulus of order `beta log(1/beta)`. This concerns each fixed s followed by its long-block limit. It is not lower semicontinuity, an exact perturbed capacity formula, or a positive-rate achievability proof for every nonzero s.

## 8. Optional initializer extension and scope limits

The same argument for a finite vertex-coordinate cutoff of an arbitrary fixed normal initializer inserts a factor r_F in R. Contractivity of the full fixed-horizon adaptive protocol then adds `sqrt(1-Tr(P_F tau))`. Fixing F before the horizon limit preserves the capacity upper bound. No uniform exponential rate over unrestricted coherent tails is established.

The principal result here is for fixed n, or a physical protocol with a maximum n padded to n. It does not itself provide a new unbounded-stopping converse. That operation requires its separately developed cost argument. The proof does not assume IID device noise, resets, independent outputs, or a measured history.

## Evidence and resource record

The proof challenge used the already read feedback trial and its accepted-scope correction, plus the exact inherited tree rank certificate. A short Python calculation evaluated the exponents and checked the displayed exact integer inequality; it was an arithmetic check of constants, not a test of the universal adaptive theorem. No old capacity replay was rerun.

A focused primary-source lookup checked the type-I normal-instrument dilation background: Kazuya Okamura, *Measuring processes and the Heisenberg picture*, arXiv:1511.09228v3, Theorem 1 on page 6, states the CP instrument/measuring-process correspondence and attributes it to Ozawa's dilation theorem. The paper also explicitly distinguishes general non-atomic von Neumann algebras, where unrestricted dilation statements can fail. URL: https://arxiv.org/pdf/1511.09228 . The original AIP page attempted in that lookup was inaccessible. The final direct common-Kraus proof above avoids relying on a blanket dilation claim for classical nonatomic registers.

No paid computation, hardware experiment, external outreach, sharing change, subdelegation or inferred energy/monetary total was used. Internal agreement does not establish external certification or historical priority.
