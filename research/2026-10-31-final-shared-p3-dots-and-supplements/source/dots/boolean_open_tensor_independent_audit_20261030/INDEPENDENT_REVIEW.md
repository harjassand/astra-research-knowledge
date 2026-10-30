# Independent receiving-lemma audit: global Boolean norms and open-tensor correctness

2026-10-30. Reviewer: `producer-workspace/challenge_live_busy_energy`.

## Verdict and exact scope

**PASS as two conditional algebraic receiving lemmas.** The global signed-map Boolean renormalization, its overlap exponent, the final OR estimate, and its trace-preserving normalization are correct. The full retained-amplitude open-tensor premise is genuinely sufficient to separate an ideal logical isometry from an arbitrarily signed, correlated, even circuit-order-acausal boundary contraction. No small open-comb norm or ordered local fault factorization is required for these two deductions.

This is **not** a physical one-way/autonomous architecture theorem. No physical good open-DAG realization, controller damage cover, clean partial-transaction semantics, online-record correctness, or active-wire waiting theorem is supplied here. In particular, the current norm receiver does not itself give a threshold when its exponent is at most one, or when waiting makes the lower-level support size grow with the computation. All prior cavity, actual-service, weighted-incidence, memory, activity and readout receipts remain unchanged.

Acceptance of the open lemma uses the source's FULL retained-amplitude identity on every allowed input sector and every actual marked quantum/classical/dilation port. We do not replace it by a claim about a measurement distribution, one noisy implementation, an unproved extra port, or one auxiliary initialization. General-channel Stinespring retention is a reformulation requiring its own isometric identity, not an automatic inference from marginal channel correctness.

### Frozen sources

1. `producer-workspace/ORDER_FREE_BOOLEAN_RENORMALIZATION.md`
   SHA-256 `b0d69747a063ef37e6763e1571a682e0cddc2f17f2ce3f687e43e7248a38775c`.
2. `producer-workspace/OPEN_TENSOR_CORRECTNESS_V1.md`
   SHA-256 `598e20f61cbd909d8febc8060a3bda646abdec137d203e07342c59c4e1362b99`.

Byte-identical copies are in `reviewed_sources/`. This receipt neither edits those sources nor upgrades other notes in their directories.

## 1. The global Boolean identity uses precisely the supplied inclusive norm

Let the finite primitive label set be I. Write `B_empty = Lambda`, with

    B_F = sum_{R containing F} E_R,
    sum_R E_R = Lambda,
    ||B_F||_diamond <= epsilon^{|F|}  (F nonempty),  0 <= epsilon <= 1.

All maps have common full input/output spaces. The norm is the completely bounded trace norm, including arbitrary finite reference amplification (and the stated normality/regularity if an infinite bath is retained). Lambda is CPTP. Individual E_R and B_F need not be positive, Hermiticity preserving, or factorized.

For a Boolean function b, its coefficient is explicitly

    c_F = sum_{S subset F} (-1)^{|F|-|S|} b(S).

Finite Möbius inversion gives `b(R)=sum_{F subset R} c_F`. Consequently,

    sum_R b(R) E_R = sum_F c_F sum_{R containing F} E_R
                  = sum_F c_F B_F.

No map has been reordered or composed. This is a finite linear equality, so chronology of the individual signed summands is irrelevant. If b(empty)=0, the constant term vanishes and the triangle inequality gives the stated coefficient-weighted inclusive bound. There is no physical measurement of b and no assumed fault record.

A useful equivalent way to check the minimum-degree hypothesis: `b(S)=0` for every `|S|<d` implies `c_F=0` for `|F|<d`; the converse follows from polynomial evaluation. Thus a deterministic localized damage COVER whose occurrence needs at least d distinct lower labels supplies the degree condition. For an m-variable Boolean function, a crude universal bound is

    sum_F |c_F| <= sum_F 2^{|F|} = 3^m.

A much smaller exact coefficient norm can of course be used. Neither this observation nor the source requires b to be monotone.

**Signed-cover precision:** containment of a real damage event in a Boolean cover licenses declaring the ENTIRE cover bad, provided everything outside it is correct. It does not license norm monotonicity between sums selected by nested events. One must bound and retain the whole signed cover sum, including any semantically benign terms it contains. Dropping such terms can destroy cancellations.

## 2. Coarse regrouping and the exact overlap exponent

Define `f(R)={j:b_j(R)=1}` and `E'_A=sum_{R:f(R)=A}E_R`. This partitions the original summands, hence `sum_A E'_A=Lambda` exactly, and

    B'_F = sum_{A containing F} E'_A
         = sum_R product_{j in F} b_j(R) E_R.

Expand each b_j using its multilinear polynomial. Before collecting repeated monomials, a selected tuple has coefficient product `product_j c_{j,S_j}` and Boolean monomial supported on `U=union_j S_j`. By the degree and incidence assumptions,

    d |F| <= sum_j |S_j|
           = sum_{i in U} #{j:i in S_j}
           <= R0 |U|.

In particular U is nonempty. Boolean idempotence replaces repeated variables by one copy, not by a new norm product. Summing absolute coefficients of all selected tuples costs at most `C^{|F|}`. Since epsilon is at most one,

    ||B'_F|| <= sum_tuples |product_j c_{j,S_j}| epsilon^{|U|}
              <= C^{|F|} epsilon^{d|F|/R0}.

The sharper integer power `ceil(d|F|/R0)` is available for each F, but the uniform inclusive parameter

    epsilon' = C epsilon^{d/R0}

is correct and composable as a GLOBAL family. Cancellations when equal unions are collected only improve this upper bound. No assumed commutation, tensor product of local fault maps, independence, CP property of E'_A, or open-process norm occurs.

Take `R0>=1` when any predicate is nonzero. If all predicates vanish, the theorem is trivial. For a nonzero Boolean predicate, its coefficient l1 norm is at least one, so one can take `C>=1`. These conventions remove irrelevant degeneracies in the threshold formula.

### The loss cannot simply be omitted

Let R0 coarse predicates be the same AND of d primitive variables. Under an ordinary independent Bernoulli fault distribution, all R0 coarse locations are simultaneously bad with probability `epsilon^d`. Their common inclusive strength must therefore be at least `epsilon^{d/R0}`. This is already a positive classical example, so signed maps cannot improve the general overlap exponent.

For `alpha=d/R0>1`, set `epsilon_th=C^{-1/(alpha-1)}`. If `epsilon_0<epsilon_th`, then every iterate remains below one and

    epsilon_l <= epsilon_th (epsilon_0/epsilon_th)^{alpha^l}

follows by induction from `C epsilon_th^alpha=epsilon_th`. For `alpha<=1`, this bound supplies no nonzero attracting threshold. In particular d=2 and R0=2 do NOT establish contraction. A more economical disjoint-witness/truncation argument may improve the receiver, but it is not hidden in this theorem. Bounds uniform over the hierarchy are necessary; one cannot absorb O(depth) waiting opportunities into a supposedly fixed m without paying their coefficient cost.

## 3. Threshold-polynomial and final OR checks

For `b(R)=1{|R|>=d}` on m variables, symmetry makes c_F depend only on j=|F|. Möbius inversion gives

    c_F = sum_{r=d}^j (-1)^{j-r} binom(j,r)
        = (-1)^{j-d} binom(j-1,d-1)  (j>=d),

and zero otherwise. This proves source equation (5) and its exact l1 constant. No positive-probability estimate is substituted for this coefficient count.

For OR on L top labels, coefficients are `(-1)^{|F|+1}` for nonempty F, so

    ||Lambda_bad|| <= sum_{F nonempty} epsilon_l^{|F|}
                    = (1+epsilon_l)^L-1.

Using `(1+x)^L<=exp(Lx)` and `exp(y)-1<=2y` for `0<=y<=1/2` proves the source's `2 L epsilon_l` bound.

The ordinary probability union bound `L epsilon_l` is not valid for arbitrary signed families. It can fail sharply already with scalar multiples of the identity channel: choose `B_empty=Id` and `B_F=(-1)^{|F|+1}epsilon^{|F|}Id`, and obtain E_R by inverse Möbius transformation. The total is the CPTP identity, every inclusive bound is met, and the signed OR sum equals `[(1+epsilon)^L-1]Id`, strictly larger than L epsilon for L>1 and epsilon>0. The source correctly avoids this mistake.

## 4. Full open-tensor identity: a complete sufficiency proof

For precision, let L be the logical input space, A an allowed auxiliary/syndrome input subspace, L' the logical output, and B the retained auxiliary output. Let U:L->L' be the intended isometry. Let V_s be the finite vector space of amplitude tensors for hole s, containing EVERY actual local input/output leg of that hole. Fix product bases in the V_s.

The completed good network is a multilinear map in the hole assignments. Equivalently, its uncontracted object is an element of

    Hom(L tensor A, L' tensor B) tensor (tensor_s V_s^*).

After encoding and the same fixed retained decoder, the premise is that every product-basis component is

    T_a = U tensor W_a,

as an operator on the ENTIRE allowed L tensor A, not just one test state. Uniqueness of expansion in the product basis then gives exactly

    T_open = U tensor W_open.

This is an equality of finite-leg tensors. It is stronger than reduced channel equality and contains all ket-level phases. It is not a norm estimate and has no dimension penalty.

In a doubled network, the ket and bra hole labels need not coincide. Let C_ab be arbitrary retained operator-valued coefficients, or more generally arbitrary linear contractions on the remaining auxiliary/bath legs. A representative term is

    (U tensor W_a) rho_LA (U^dagger tensor W_b^dagger)

contracted with C_ab. Factoring U and U^dagger out of the sum yields exactly the superoperator factorization

    Ad_U tensor Gamma_C

on L tensor A (with other retained references untouched). This is simply distributivity of tensor contraction. C need not be CP, Hermitian, positive, normalized, causal in the target circuit order, or small coefficientwise. Correlations among multiple holes and a retained shared bath are allowed. No transpose/sign convention in the chosen tensor contraction changes the conclusion, because U has no contracted hole index.

Two qualifications are essential:

1. C must contract only the exposed hole/auxiliary legs. A connection to an unmarked external logical leg, hidden classical control, or missing dilation output is NOT covered. The chosen full network, not a schematic port count, must be exactly the physical coefficient map under study.
2. For an initially independent auxiliary state sigma_A, the output is `U rho_L U^dagger tensor Gamma_C(sigma_A)` as written schematically in source equation (2.3). For initially correlated L,A, the correct statement is `(Ad_U tensor Gamma_C)(rho_LA)`, not a product-state output. The logical map factor remains exact and reference-stable, but pre-existing correlations do not disappear. The source's final scalar normalization expressly uses a fixed logical-independent initialization.

An infinite retained bath introduces no new finite-basis algebra. Its normal maps and contractions must still exist with the stated completely bounded/trace-class regularity. This lemma does not define an arbitrary divergent formal tensor contraction or validate an unbounded postselection operation.

## 5. Exactly what Pauli-word correctness supplies, and what it does not

Suppose a fixed Pauli/operator word P produces a physical completed circuit whose chosen dilation F_P obeys, for every logical input and every allowed auxiliary input, the reduced logical channel Ad_U. For each pure auxiliary vector a, purity of the logical output implies

    F_P(|i> tensor |a>) = U|i> tensor |w_{P,i,a}>.

Applying the same equality to logical superpositions forces `w_{P,i,a}` to be independent of i. Linearity in a then supplies a linear W_P with `F_P=U tensor W_P` on the allowed span. The same argument is stable under external reference amplification. It is the same decoder/dilation for all words; choosing a different logical correction or decoder for each word would not supply the common factor.

If those Pauli/operator words span every local hole amplitude space, the identity extends to all matrix units by multilinearity, including coherent ket-bra cross terms. It is NOT enough merely to know that a Pauli *mixture* has correct output probabilities.

For a rectangular hole `B:H_in->H_out`, a fixed local isometry V with `V^dagger V=I` gives

    B = (B V^dagger) V.

Thus all rectangular replacements can be represented as output-operator insertions after V, and an operator basis (Paulis on padded qubit spaces, or another complete matrix basis) spans them. This observation is legitimate only if the actual fault-tolerance premise covers the WHOLE output space on which `B V^dagger` acts, including exposed reset/measurement dilations and classical-control registers. A theorem tolerating a data-qubit Pauli does not automatically tolerate an arbitrary operator on additional record ports, nor an operator on a larger-than-counted support. The marked-location enlargement must preserve the actual correctability budget.

For initialization, preparation and discard tensors, retain a definite Stinespring isometry first and include all its relevant legs. Non-isometric maps cannot be treated as arbitrary invertible local tensors. Allowed auxiliary sectors may be a theorem's explicitly restricted syndrome subspace; this review does not enlarge them to the entire apparatus Hilbert space without proof.

### Concrete weaker-premise failures

- A controlled-X from auxiliary A to logical L acts as the ideal identity on every logical input when A starts in |0>, but flips L for A=|1>. Therefore fixed-ancilla correctness cannot justify leaving that auxiliary input open to an arbitrary boundary tensor.
- Complete dephasing reproduces every computational-basis measurement distribution of the input, yet destroys an unknown superposition. Distribution correctness is insufficient for a retained quantum logical factor.
- For the non-isometric reset channel, a dilation `|psi> -> |0>_out tensor |psi>_env` has the correct reduced channel for every input. Contracting the retained environment with `<0|` gives success weight `<0|rho|0>`, not a logical-input-independent scalar. Thus one cannot infer a common factor for a GENERAL target channel merely by mentioning a Stinespring representation. One must prove the stronger isometric retained-target identity itself before arbitrary contractions. This is the governing interpretation of the root source's Stinespring remark.

None of these counterexamples satisfies the full source premise (2.1); they delimit possible incorrect applications rather than refute the lemma.

## 6. Final normalization is valid for signed good maps

Let Enc be the fixed CPTP encoding/initialization map and let D_out be the fixed CPTP decoding followed by the desired auxiliary marginal. Isometric decoding with retained outputs is also CPTP; when comparing only the logical target, take the indicated marginal. Suppose every globally good summand has the SAME channel factor

    D_out E_R Enc = c_R Ad_U.

The scalars can be complex; no positivity, probabilistic interpretation, or lower bound on their sum is required. The strong tensor factor gives this scalar statement for fixed auxiliary initialization after the appropriate trace. Let `c=sum_good c_R` and `Delta=D_out Lambda_bad Enc`. The actual decoded channel obeys

    Phi_actual = c Ad_U + Delta.

For any density operator rho,

    1 = Tr Phi_actual(rho) = c + Tr Delta(rho).

Consequently `|1-c|<=||Delta||_diamond`. Since `||Ad_U||_diamond=1` and CPTP pre/post-composition is contractive,

    ||Phi_actual-Ad_U||_diamond
      <= |c-1| + ||Delta||_diamond
      <= 2 ||Delta||_diamond
      <= 2 ||Lambda_bad||_diamond
      <= 4 L epsilon_l,

under the source's small-L epsilon condition. This handles even a nonpositive good part and does not condition on or divide by a rare event. If a physical source/preparation error is added, propagate it through the actual CPTP total map. Do not propagate it termwise through a possibly large signed good map, or compare exponentially large observables by trace-distance continuity.

A factor `Ad_U tensor Gamma` with arbitrary retained auxiliary output is not automatically close to `Ad_U tensor` a fixed physical bath channel: Gamma may be signed. The claimed bound concerns the desired decoded logical marginal, exactly as in the source. It does not promise bath reset or disappearance of pre-existing correlations.

## 7. Primary-source comparison: specific, not a transplanted theorem

Inspected the local primary PDF/text for Aliferis–Gottesman–Preskill, *Quantum accuracy threshold for concatenated distance-3 codes*, arXiv:quant-ph/0504218v3. Official version metadata was independently opened at [the arXiv version page](https://arxiv.org/abs/quant-ph/0504218v3).

- Section 5.2.2, especially equation (14), gives the retained-syndrome logical/syndrome separation associated with good rectangles. The allowed syndrome/input conditions and the preceding rectangle hypotheses remain essential.
- Section 11.4 extends good-part correctness to nonphysical fault sums through Pauli expansion and linearity. Its final reliability statement retains a reliable classical-decoding qualification. The current full diamond-map/isometric receiving lemma is proved above; AGP's amplitude-norm/final-measurement formulation is not silently relabelled as this stronger physical-interface assertion.
- Section 9, Lemma 5, proves higher-distance exRec correctness from explicit gadget properties 0–3. It does not license choosing a code distance while omitting those gadget properties, leading/trailing rectangle semantics, or independent-badness/truncation bookkeeping.

These are primary antecedents for the algebra, not evidence that the native apparatus already executes their gadgets or admits their physical timing/control model. No novelty claim for inclusion/exclusion, common-environment fault paths, syndrome retention, or Pauli linearity is accepted here. A strong ordinary scheduled adversarial fault-tolerant quantum computation is the relevant comparator.

Primary local hashes:

- `sources/agp-2006.pdf`: `2df9a42e5094dac7bfc8356ceacd6e1ca9b777d7458efa75cc5120c0031fedea`.
- `sources/agp-2006.txt`: `8b04c3f52f77d266c07a18b51eb7ca4f4a8245a07526071a188c5678e39ef6ed`.

## 8. Independent diagnostics and remaining action

`check_boolean_and_open_scope.py` checks 8,194 threshold truth-table inputs; reconstructs a signed global superoperator family by inverse Möbius transformation; verifies 15 coarse inclusions with overlapping supports and nonmonotone predicates; saturates the overlap loss and signed OR cost; and contracts arbitrary non-Hermitian operator-valued boundary coefficients with an entangled logical/auxiliary input. It also checks the three weaker-premise counterexamples above. The largest open-contraction residual is approximately `1.20e-14`; the global Möbius residual is `1.05e-15`.

The author's separate `[[5,1,3]]` ideal-recovery-cut diagnostic was also read and rerun. Its complete correctable-error frame and all one-qubit matrix-unit checks are consistent with the stated common-correctable-span lemma. It is not a native fault-tolerant recovery circuit, and no such inference is made.

**Remaining exact interface:** exhibit the physical coefficient network for each declared-good global term, with every bad quantum/classical boundary and every damaged partial transaction marked; prove the resulting retained circuit obeys the full open identity within a uniform correctability budget; construct the localized Boolean cover with fixed degree/coefficient/overlap constants; and bound active-wire waiting without computation-size-growing fan-in. Until those actions succeed, the two receiving lemmas are available but a whole architecture remains OPEN. No access denial blocks this audit; the unresolved issues are mathematical/physical premises, not permissions.
