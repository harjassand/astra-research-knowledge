# Exact clock-loop algebra receipt

Independent audit, 2026-11-01. This receipt uses no thermal-expansion lemma.

## Assumptions

Data consist of bounded-dimensional spins (qubits suffice). The target checks S_g are mutually commuting Hermitian Pauli products, of weight at most w and bounded geometric diameter. Each data spin lies in at most d checks. Spin density is bounded. Choose a fixed K>=max(w,3), and write S_g=P_{g,1}...P_{g,K}, using distinct-site single-qubit Hermitian Paulis and identity padding. An overall minus sign can be included in one label. Consequently the factors within each check commute. The physically relevant target here permits K=7.

Checks need not be independent, CSS, translation invariant, or of identical support geometry. Mutual commutation IS necessary for the simultaneous syndrome/logical conclusion below.

## Native Hamiltonian

One K-level ancillary spin g is placed within bounded distance of check g. For q=0,...,K-1,

    H = sum_g Delta_g (I-|0><0|)_g
        - sum_g sum_{i=1}^K t_{g,i}
          [ |i mod K><i-1|_g tensor P_{g,i} + h.c. ].

All nontrivial contacts act on one ancilla and one data spin. Identity labels give onsite ancillary hopping. Strengths may be arbitrary bounded constants for the algebra below; no t/Delta smallness is required.

Physical spin dimension is max(2,K), ancillary degree at most w, and data degree increases by at most its original check incidence. At fixed density and bounded check diameter, inserting these spins preserves bounded density and interaction range. This assertion permits arbitrary individually addressable matrix elements between a K-level spin and a qubit. It does not prove realizability within a narrower interaction class such as isotropic exchange only.

## Local dressing and its depth

Set F_g(q)=product_{j=1}^q P_{g,j}, with F_g(0)=I. Color the check-overlap graph; it has degree at most w(d-1), so a constant number c<=w(d-1)+1 of colors suffices. Order checks by color and then arbitrarily within a color.

    U_g = sum_q |q><q|_g tensor F_g(q),
    U = ordered product_g U_g.

Each F_g(q) is Hermitian unitary and each U_g is unitary. Disjoint-color-class checks have disjoint data supports and distinct ancillas, so the corresponding U_g commute and can be applied in parallel. Hence U has depth c in bounded-support gates. Moreover U_g itself is a product of at most w controlled-Pauli gates, one ancilla–data gate for each nonidentity factor; the control condition is q>=j. Thus U also has constant depth in two-spin unitary gates if desired. The storage Hamiltonian does not require dynamically executing this circuit.

In a clock basis configuration q, write

    W(q)=F_1(q_1)...F_M(q_M),
    U=sum_q |q><q| tensor W(q).

The order is indispensable when check prefixes anticommute. U is generally not Hermitian even though each U_g is.

## Exact transformed edge formula

Let an oriented hop of gadget g have source q_g=i-1, destination q'_g=i mod K, and data label P=P_{g,i}. Define b_i=0 for i<K and b_K=1. For Pauli operators A,B, let chi(A,B)=+1 if they commute and -1 if they anticommute.

Then

    W(q')^dagger P W(q)
      = sigma_{g,i}(q) S_g^{b_i},

where

    sigma_{g,i}(q)
      = product_{h<g} chi(P_{g,i}, F_h(q_h))
        * product_{h>g} chi(S_g,F_h(q_h))^{b_i}.

Proof: factor W=L F_g R and W'=L F'_g R. Conjugating P by L gives the first scalar sign. The middle factor (F'_g)^dagger P F_g is I for a nonwrap hop and S_g for a wrap hop. Conjugating the latter by R gives the second sign. No series, limit, or spectral projection is used. Reverse hops follow by Hermitian conjugation.

Only gadgets sharing data support can contribute nontrivial chi. Every sign is a product of functions of the hopping clock's current edge and ONE neighboring clock label. Nevertheless the full transformed hopping operator can involve multiple clocks simultaneously; the two-body claim applies to H before dressing, not to U^dagger H U.

The penalty terms commute with U. Therefore

    U^dagger H U = sum_s P_s tensor H_a(s),

with the sum over allowed joint syndrome values s and P_s their data projectors. H_a(s) is a bounded-range ancillary Hamiltonian whose hopping signs are sigma and whose wrap fluxes are s_g.

## All-Hilbert-space logical decoupling

If the stabilizer rank is r on n qubits, every nonzero P_s has dimension 2^(n-r). On each such sector, the transformed H acts as the identity on the entire data sector and acts only on ancillas. Equivalently, after an abstract syndrome/logical decomposition,

    U^dagger H U is isomorphic to direct_sum_s [I_logical tensor H_a(s)].

This includes all ancillary excitations and all allowed syndrome sectors. Any data logical operator commuting with all stabilizers commutes with the transformed H; its dressed version U L U^dagger commutes with the native H. Thus Hamiltonian-only evolution cannot rotate or split this dressed logical subsystem. The algebra does NOT prove that the all-positive syndrome minimizes energy, that a desired thermodynamic phase exists, or that a bath preserves the subsystem.

The isomorphism identifying the code's logical factor need not itself be geometrically local; the only newly introduced encoding circuit U is local. No extra local-code-decoding property is assumed.

## Pairwise trajectory sign factorization

For any sequence of elementary ancillary hops, multiply the exact edge signs. Because each edge sign is a product over neighboring gadgets, the complete sign can be regrouped as

    sign(history)=product_{unordered pairs {g,h}} Phi_{gh}(history_g,history_h),

where each Phi is +/-1 and is determined by the two clocks' time-ordered paths. For a closed history the syndrome factor is

    product_g s_g^(number of wrap crossings modulo 2).

Thus arbitrary-order shared-data effects are retained as pairwise SIGN functionals of trajectories. This does not imply a positive classical measure, pairwise spatial free energy, absence of higher connected clusters, or an independently established cluster convergence bound. Configuration-space square holonomy can be -1.

## Error locality

For any microscopic operator supported in a bounded region, conjugation by U expands support only within the constant-depth circuit light cone. Consequently a bounded local physical error remains bounded local on dressed data plus ancillas. This includes ancillary error operators, not merely data Pauli errors. A finite-density or long-time noise claim needs the correct state-level domain and bath theorem; this support statement alone does not supply it.

## Audit verdict

PASS: exact native two-body construction; bounded local resources under stated geometry/density assumptions; exact bounded-depth dressing with explicit ordering; exact full-spectrum logical decoupling; local pairwise factorization of trajectory signs; bounded support expansion of bath operators.

NOT EARNED BY THIS RECEIPT: uniform syndrome free-energy interaction bounds; thermal witness ratios; positive contour tension; finite-temperature initialization in the required state domain; rare logical-fault/lifetime theorem; robustness to arbitrary added native perturbations.
