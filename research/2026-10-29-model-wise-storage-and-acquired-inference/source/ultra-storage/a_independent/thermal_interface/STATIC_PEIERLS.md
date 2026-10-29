# A quantum Peierls receiver from central small polymers

This file concerns **static decoder-bad probabilities** for a weakly noncommuting perturbed Hamiltonian. It does not replace the Gibbs state by its stabilizer twirl, does not prescribe a dephasing actuator, and does not infer memory from free-energy analyticity. The separate root quantum receiver owns the CPTP encoding and dynamical/coherence step.

## 1. Input and statement

Let `H0=sum_j (I-S_j)/2` be the even-level RX/RZ family in the frozen retraction proof. Import the primary bounded degree/range/density, corrected logical Paulis, and valid-witness Peierls construction. Write D for a bound on the number of supplied checks touching a qubit. Let `d` be the quantum distance. Let `F M^p` bound the number of supplied checks needed for **any** stabilizer of Pauli weight M; the accepted retraction result supplies `F=2K` and a fixed integer p.

**Temperature convention:** one violated supplied check has energy one. Here beta_c means the threshold of the primary Theorem 5.13 counting inequality for weights `exp(-beta|sigma|)`. A Hamiltonian written instead as `-sum S_j` has twice that defect energy and requires the corresponding beta rescaling; that convention is not silently transferred.

Assume the embedding satisfies `#qubits(B_R)<=rho(1+R)^3`, and the diameter of each supplied check is at most `r_c`. Consider

`H=H0+V`, `V=sum_{i in I} V_i`.

Each V_i is Hermitian, acts on a nonempty native support A_i of at most q qubits and bounded diameter, and each qubit belongs to at most nu such supports. These are arbitrary local coherent Hamiltonian terms, not assumed Pauli or commuting with H0. Remove scalar identity terms if convenient. In the physical Pauli expansion use the Banach norm

`||A||_P = sum_P |a_P|`, so `||AB||_P<=||A||_P||B||_P`.

Take `v=max_i ||V_i||_P`; a supplied operator-norm bound gives `v<=2^q max_i||V_i||`. This basis cost is explicitly charged.

Join native labels i,j if their supports overlap or one H0 check touches both supports. Let Delta bound this graph's degree. Define U_i to be A_i together with the supports of H0 checks touching A_i. Let `q_*` bound `|U_i|`, and let r_* bound the physical step/diameter constants of a connected union of these supports. All these constants are independent of code size for fixed native range, incidence and q; for example `q_*<=q(1+D w)` if supplied checks have weight at most w.

At a fixed beta>beta_c set

`a=beta exp(beta D q) v`, `w0=exp(a)-1`,

`B=(Delta+1)^2 exp(2) w0`, `b=B/exp(1)`.

We impose `B<=1/[2(Delta+2)]`. Let

`L=ceil(d/q)`, `delta=|I| b^L/(1-b)`.

The central effective interaction below has a computable check-incidence charge zeta tending to zero with v. If `beta_eff=beta(1-2 zeta)>beta_c` and `delta<=1/4`, then for the primary base bad projector Pbad0 (the union of the two syndrome-sector sufficient bad sets),

`Tr(Pbad0 exp(-beta H))/Tr exp(-beta H) <= 4 exp(4 delta) 2^(-2^(k-1))`.

More generally, section 8 constructs a **common** good projector for every operator on any supplied region X of q_R qubits, and proves

`p_bad(X) <= 4 exp(4 delta) 4^q_R exp[beta(1+2 zeta)D q_R] 2^(-2^(k-1))`.

At fixed beta and sufficiently small, size-independent v, delta tends to zero stretched exponentially with system size and the base exponent remains the primary's 2^k. The permissible v from the conservative bounds can be exceptionally small. No useful numerical tolerance is claimed.

## 2. Interaction-picture locality and exact-label activities

Let D_S be averaging over the stabilizer group, used only mathematically. It deletes Pauli coefficients outside the stabilizer normalizer and preserves every syndrome-diagonal expectation. Because H0 is a sum of commuting Pauli projectors,

`T_J = exp(beta H0) D_S(exp[-beta(H0+sum_{i in J}V_i)])`

is Hermitian and positive: the twirled positive operator commutes with H0. The interaction-picture expansion is the time-ordered exponential of `V_i(s)=exp(sH0)V_i exp(-sH0)`, integrated over s in [0,beta].

A Pauli anticommuting with a supplied check picks up a hyperbolic two-term factor under this conjugation. Its Pauli-l1 norm increases by at most exp(s) per touching projector. Hence

`||V_i(s)||_P <= exp(beta Dq)||V_i||_P`.

The support is within U_i. A nonadjacent pair of labels has disjoint native supports and no common touching check. Their interaction-picture operators commute at all times (even if the enlarged geometric supports happen to overlap), and their Pauli charge patterns use disjoint supplied-check sets.

For a nonempty label set J define its exact-label activity

`W_J=sum_{K subset J} (-1)^(|J|-|K|) T_K`.

Dyson histories in W_J use every label in J at least once and no label outside J. Summing repetitions and orderings with the integral factorial gives the explicit Banach bound

`||W_J||_P <= product_{i in J}(exp[a_i]-1) <= w0^|J|`,

where `a_i=beta exp(beta Dq)||V_i||_P`. This bound is obtained from the local Dyson series, not the exponentially large norm of exp(beta H0).

If J has graph components J1,...,Jm, then `W_J=product_l W_Jl`. Time interleavings factor, operators of different components commute, and stabilizer averaging factorizes: a product of Pauli words with disjoint check-charge sets can be a normalizer only when each component already is. The last assertion remains valid with redundant checks, because it is an assertion about equality of the complete charge characters, not independent syndrome bits.

Möbius inversion therefore gives an **exact operator-valued hard-core polymer gas** for T_I, with polymers the connected label subsets, compatibility meaning no common or adjacent labels, and activity W_J. Compatible activities commute. Each W_J is Hermitian, because it is a real signed sum of the Hermitian T_K.

## 3. Why small polymers are central

Expand a Dyson history in physical Pauli words. Conjugation by H0 multiplies each native Pauli by a function of stabilizers. Moving those functions past other native Paulis preserves this form. Thus every history is

`P_native * f(stabilizers)`,

where P_native is supported on the union of the native supports of its distinct labels. Repetition of a label does not enlarge that union. If the history survives D_S, P_native is in the normalizer. If `q|J|<d`, code distance implies P_native is itself a stabilizer (with its fixed group sign). Hence W_J belongs to the **stabilizer algebra**, the center of the complete stabilizer commutant.

This proves centrality for all `|J|<L`. It does not suppose all normalizer activities commute: large activities can contain logical operators. A central small activity, however, commutes with **every** twirled activity, including the large ones. This is the resource that avoids invoking a general noncommutative logarithm expansion.

## 4. Ordinary scalar polymer estimates, with the actual norm budget

Use the hard-core Kotecky–Preiss cluster expansion, e.g. Ueltschi, **math-ph/0304003v3**, Theorem 1/equations (3)–(5). Its scalar complex-activity statement is the ordinary imported tool. Products of the small activities are commutative; the coefficient formulas therefore hold in their finite-dimensional commutative Pauli algebra. Absolute coefficient estimates are dominated by the scalar gas with activities `||W_J||_P`.

There are at most `(Delta+1)^(2m)` connected m-label sets containing a fixed label, by the elementary depth-first traversal bound. An incompatible polymer must contain a label in the closed neighbourhood of the reference polymer. With the weighted activities `exp(|J|)||W_J||_P` and KP size function `a(J)=|J|`,

`sum_{J incompatible G} exp(2|J|)||W_J||_P <= |G|(Delta+1) B/(1-B) <= |G|`.

The same criterion holds after deleting any subset of small activities. Let Z_s be the gas containing only `|J|<L`. It is central, invertible, and positive for real perturbations: every scalar syndrome value is real, starts at 1 as V is turned on from zero, and cannot cross zero under the uniform KP condition.

Write its convergent logarithm as a sum of connected cluster terms Phi_C. If `m_C` is the total number of labels counted with polymer multiplicity, the rooted KP bound gives, for every native label i,

`sum_{C whose union contains i} ||Phi_C||_P exp(m_C) <= B/(1-B)`.

Each Phi_C is a stabilizer-algebra operator supported on a connected union of at most m_C enlarged native supports. This bound controls **Pauli coefficient l1**, not only operator norm. There is no free passage from an operator norm to arbitrarily many stabilizer monomials.

Deleting all small polymers incompatible with a fixed family Gamma has partition-ratio bound

`||Z_s^(avoid Gamma) Z_s^(-1)|| <= exp(sum_{J in Gamma}|J|)`.

This follows by subtracting the two convergent cluster logarithms; Ueltschi's rooted incompatibility estimate bounds the removed terms. The ratio is central and positive for real parameters.

## 5. Large logical activities: a relative, not absolute, error

Group the exact full polymer sum by its compatible family of large polymers. All small activities are central, so

`T_I = sum_{Gamma large compatible} [product_{J in Gamma}W_J] Z_s^(avoid Gamma)`.

The empty family contributes Z_s. The partition-ratio estimate and activity bound imply

`||T_I Z_s^(-1)-I|| <= exp(delta)-1`,

because `sum_{|J|>=L} ||W_J||_P exp(|J|) <= |I| b^L/(1-b)=delta`. Ignoring compatibility in the final positive majorant only enlarges the sum.

T_I commutes with Z_s, and both are Hermitian. If delta<=1/4, the preceding bound yields positive operator comparison with factors `2-exp(delta)` and `exp(delta)`. Since H0 also commutes with both, the **twirled** Gibbs operator is bounded relative to `exp(-beta H0) Z_s`. Consequently every positive syndrome projector P satisfies

`Tr(P rho_H) <= exp(4delta) Tr(P rho_eff)`,

where `rho_eff` is the normalized operator proportional to `exp(-beta H0) Z_s`. This comparison includes the normalization ratio. It never bounds an extensive absolute remainder and then divides by an exponentially small partition function.

This is an expectation identity/comparison. The full rho_H generally has coherences outside the stabilizer commutant and is not replaced by rho_eff for a physical quantum-memory argument.

## 6. Pay the effective check-incidence charge

Define the central effective Hamiltonian

`H_eff=H0-beta^(-1)log Z_s`.

Expand each Phi_C in its **physical Pauli** coefficients. Every monomial is a stabilizer. Choose its supplied-generator representation using the accepted uniform check-soundness construction, and prune any connected component of chosen checks whose product is identity. Every remaining component must touch the support of that monomial: different check-graph components have disjoint qubit support, so they cannot cancel each other's nonidentity output. Thus every chosen check lies within at most `F M^p` check-graph steps of the monomial's support. This is a constructive pruning operation, not a minimum-cardinality representation oracle.

For `M<=q_* m`, all such generators therefore lie within physical distance

`R(m)<=r_* m+r_c[F(q_*m)^p+1]<=R0 m^p`,

where `R0=r_*+r_c(F q_*^p+1)`. A fixed check can receive a coefficient only from a cluster with some native anchor in that ball. There are at most `C_geo m^(3p)` possible anchors, with the conservative explicit constant

`C_geo=nu rho (1+R0)^3`.

The rooted Pauli-l1 budget from section 4 now gives a uniform bound on the total absolute effective coefficient incident on any supplied check:

`zeta <= [C_geo/beta] [B/(1-B)] sum_{m>=1} m^(3p) exp(-m)`

`       <= [C_geo/beta] [B/(1-B)] exp(1) (3p)!`.

For the last inequality integrate x^(3p) exp(-x) over intervals [m,m+1]. Every factor is explicit in admitted source/native constants. This extremely conservative bound tends to zero with v, independently of code size. It pays both the basis expansion and the possible spatial spread of a check representation.

Writing the effective perturbation as a sum of supplied-check monomials with these representations, flipping a set tau of syndrome bits changes its energy by at most `2 zeta |tau|`, regardless of signs or X/Z-sector cross couplings.

## 7. The primary witness deletion still works

Use the primary source **2605.10943v1, Lemma 5.8**: the witness tau is itself a valid coboundary, and it is a subset of the syndrome configuration sigma. Therefore sigma+tau remains an admissible syndrome and the map sigma -> sigma+tau is injective for fixed tau. No assumption that arbitrary subsets of syndrome are admissible is made.

The base projector energy drops by |tau| under this deletion; section 6 changes that drop by at most `2 zeta|tau|`. Hence

`Pr_eff(tau subset sigma) <= exp[-beta(1-2zeta)|tau|]`.

The primary's witness counting and all subsequent estimates can thus be repeated with beta replaced by beta_eff. The other CSS sector is left untouched in this injection, so the argument also allows effective cross-sector interactions; it does not assume independence of the two syndrome sectors. If beta_eff>beta_c, its two-sector bad-set bound is `4 * 2^(-2^(k-1))`. Section 5 supplies the stated quantum Gibbs bound with exp(4delta).

## 8. A common good projector for a whole physical support

Let X have q_R qubits. The primary corrected logical X/Z commute with a one-site Pauli on the primary good sector. Define

`Pbad^X = union_{U in Pauli(X)} U^dagger Pbad0 U`.

All these projectors are syndrome-diagonal and commute with the corrected logical algebra. Their complement is a **common** good sector for every operator on X. Indeed every prefix of an ordered Pauli word on X is itself one of these 4^q_R words; all intermediate syndromes are one-site stable. Telescoping proves commutation with the whole word on the common sector, and Pauli linearity proves it for every operator on X. This coefficient-free operator statement is stronger than assigning a separate good sector to each term of a Pauli expansion.

A word U on X flips at most D q_R supplied-check syndrome bits. In the effective classical model its energy shift is at most `(1+2zeta)Dq_R`. Syndrome translation is a bijection on the admissible syndrome set. The union bound over 4^q_R words and section 5 therefore yield

`Tr(Pbad^X rho_H) <= exp(4delta) 4^q_R exp[beta(1+2zeta)Dq_R] * 4 * 2^(-2^(k-1))`.

This is the actual static input for a whole-jump quantum receiver. For a radius-R physical patch the source density gives `q_R<=rho(1+R)^3`. Taking R to be a sufficiently small constant times `2^(k/3)` still leaves a stretched-exponentially small bad probability. The constant must pay rho, beta, D and zeta. It is not a free bounded-radius conclusion.

## 9. Scope, comparators and remaining dynamics

The smallness contains `beta exp(beta Dq) v` and the very large check-filling constants; it does not claim the stronger linear-in-temperature robustness wedge in Thorngren's classical gauge-averaging theorem. Thorngren's result is a classical-memory prior, Sengoku–Cao–Watanabe's quantum extension is a static free-energy prior, and neither is identified with a physical logical-coherence recovery map here. The scalar KP theorem is credited ordinary machinery.

The new operation here is the **central-small-polymer cutoff**, relative treatment of the remaining logical activities, and the check-incidence/growing-support decoder bridge for this recursively constructed quantum code. It supplies static input to the separately derived logical-twirl/quantum-generator receiver. No claim follows for an arbitrary nonstationary coherent noise process. Exact stationarity, the actual generator's locality/tails and full jump truncation must be paid there. In particular microscopic local coupling does not automatically make exact Davies frequency-resolved jumps local for the perturbed noncommuting Hamiltonian.

This is a theoretical sufficient route; preparation of rho_H or its logical-sector encoding, native interactions, bath parameters and useful physical tolerances remain unacquired. Historical priority of this composition is not established by a search miss.
