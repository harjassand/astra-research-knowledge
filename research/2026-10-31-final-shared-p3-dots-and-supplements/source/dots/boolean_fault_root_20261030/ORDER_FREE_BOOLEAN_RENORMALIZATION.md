# Global Boolean fault renormalization without ordered local fault factorization
2026-10-30. Root algebraic theorem and proposed receiving contract. Independent review pending. The algebra is elementary inclusion/exclusion, not a claim of historical novelty. Its purpose is to avoid assuming an unnecessary causal factorization for the new physical cavity expansion.

## 1. Global signed maps are enough for the norm calculation
Let I be a finite set of primitive boxes. Let E_R, R subset I, be completely bounded linear maps from the full computation input to its full output, possibly with retained environment/reference. They need not be CP and need not factor into time-ordered local fault maps. Assume

 sum_R E_R = Lambda,
 B_F := sum_(R contains F) E_R,
 ||B_F||_diamond <= epsilon^|F|  for every nonempty F, 0<=epsilon<=1.  (1)

Lambda is the actual CPTP map. The native CP-cavity construction supplies a candidate of exactly this global form. No fault record in the actual noisy process is assumed.

Every Boolean function b on fault sets has a unique multilinear polynomial

 b(R)=sum_(F subset I) c_F product_(i in F) 1_(i in R).

Therefore the map selected by that Boolean property satisfies the EXACT identity

 Lambda_b := sum_R b(R) E_R = sum_F c_F B_F.             (2)

If b(empty)=0, its constant coefficient is zero and

 ||Lambda_b||_diamond <= sum_(F nonempty)|c_F|epsilon^|F|. (3)

This is an identity of global maps; it does not insert an unproved physical measurement of b.

## 2. A composable coarse noise theorem
For each coarse location j in a finite set J, let b_j be a Boolean badness criterion supported on a set I_j of lower-level variables. Suppose its multilinear polynomial has:

- no monomial of degree below d>=1;
- sum of absolute coefficients at most C;
- each lower-level variable belongs to at most R0 of the sets I_j.

All d,C,R0 are fixed independently of computation size. Define the exact coarse maps by regrouping:

 E'_A = sum_(R: {j:b_j(R)=1}=A) E_R.

They still sum to Lambda. For any set F of coarse locations,

 B'_F = sum_R [product_(j in F)b_j(R)] E_R.

Expand the product. Each selected tuple of monomials S_j has |S_j|>=d. Because a lower variable occurs in at most R0 coarse supports,

 |union_(j in F) S_j| >= d|F|/R0.

Boolean idempotence merges repeated variables; it does not invalidate this union bound. The sum of absolute product coefficients is at most C^|F|, even before collecting cancellations. Equations(1)-(2) imply

 ||B'_F||_diamond <= [C epsilon^(d/R0)]^|F|.             (4)

Thus epsilon'=C epsilon^(d/R0) is a valid GLOBAL inclusive coarse strength. No open-process/comb norm, local Kraus factorization or fixed causal order of bad maps is used in this norm theorem.

A nontrivial iterative threshold requires alpha=d/R0>1. If alpha<=1, this estimate does NOT supply one. For common constants across levels,

 epsilon_l <= epsilon_th (epsilon_0/epsilon_th)^(alpha^l),
 epsilon_th=C^(-1/(alpha-1)),

when epsilon_0<epsilon_th.

## 3. Exact threshold polynomial example
For a gadget with m lower boxes, badness meaning at least d faults has coefficients

 b(R)=sum_(j=d)^m (-1)^(j-d) binom(j-1,d-1)
                      sum_(|F|=j) product_(i in F)1_(i in R).        (5)

At a set of size n this is zero for n<d and one otherwise, by the finite-difference/binomial identity for the threshold step function. Its coefficient norm is the finite constant

 C_(m,d)=sum_(j=d)^m binom(m,j) binom(j-1,d-1).

This constant may be large, but m,d must remain fixed through the hierarchy. Merely declaring a long-lived module a single gadget does not make its entire waiting history a bounded-size input set.

## 4. Final bad-part bound
For L top-level locations whose joint inclusive strength is epsilon_l, the property that any one is bad has the OR polynomial. Hence

 ||Lambda_bad||_diamond <= (1+epsilon_l)^L-1 <=2L epsilon_l

when L epsilon_l<=1/2. This avoids an invalid positive-probability union bound on signed maps. More efficient witness-counting bounds may be available, but are not assumed here.

## 5. Correctness is a separate OPEN-TENSOR obligation
The norm theorem alone says nothing about what Lambda computes. For a unitary/isometric target U_L, suppose that whenever the top badness criterion is false, the decoded, encoded-input map E_R has the common factor

 D E_R Enc = c_R U_L,                                 (6)

or, before tracing a fixed initially logical-independent auxiliary state, the stronger retained-syndrome identity U_L tensor K_R. Coefficients/maps may be signed. An open-tensor fault-tolerant rectangle identity can supply(6) after contraction with arbitrary bad-region boundary tensors, but it MUST be proved for the actual marked ports and actual good open circuit.

Let Delta_bad=D Lambda_bad Enc. Then

 D Lambda Enc = c_good U_L+Delta_bad.

Trace preservation gives |1-c_good|<=||Delta_bad||_diamond. Therefore

 ||D Lambda Enc-U_L||_diamond <=2||Delta_bad||_diamond
                              <=4L epsilon_l.         (7)

Additional source/preparation errors are propagated through actual CPTP maps and added separately. This normalization argument does not condition on a rare good event. For a general target channel, one may retain a target Stinespring circuit before discarding its environment; an arbitrary outcome-dependent postselection is NOT silently replaced by a scalar c_R.

## 6. What the physical construction must still earn

1. The native cavity box family must satisfy(1) on the actual full physical channel, with exact compatible good-subprocess maps.
2. A deterministic coarse damage COVER must be expressible by the b_j with the required minimum degree and overlap. A statement about only expected classical output error or a marginal clock state is insufficient. If an actual damage event is contained in a Boolean cover, the cover may be used, but its polynomial costs must be counted.
3. Quantum correctness must hold with all bad quantum AND relevant classical port indices open. Boundary port count by itself is not(6). No copying or rewinding unknown DATA is allowed.
4. The actual good modules must execute the needed open circuit/cut. Missing, repeated, prematurely fired, or retimed gates must lie inside the marked-port cover.
5. Active-wire waiting exposure is a genuine scaling obligation. If one module can wait for O(D) physical windows and all of those become independent opportunities to corrupt its quantum input, its lower-level fan-in m grows with D and the stated constant threshold does not follow. Physical memory protection, safe overwriting of inactive future banks, or an earned waiting/cut theorem must resolve this.
6. The scheme still pays initialization, physical hardware, entropy-export/reset resources, readout and classical processing. Nothing here establishes a universal autonomous quantum architecture by itself.

## Primary comparison and receiving status
Inclusive common-environment fault-path norms and fault renormalization are established in Aliferis–Gottesman–Preskill (quant-ph/0504218). The proposed role here is to retain the GLOBAL signed Boolean channel family supplied by the new CP cavity, rather than first forcing its bad-region combs into an ordinary ordered gate-noise model. The complementary worker's OPEN_TENSOR_CORRECTNESS_V1.md cites the retained-syndrome factorization and Pauli-linearity structure in AGP Sections5.2.2 and11.4. Neither that application nor an historical novelty claim is imported without its actual proof review.
