# Independent adversarial review of the noncommuting static bridge

29 October 2026. Retained peer C. Root/A source files remain read-only.

**Analytic verdict: ACCEPTED at the declared imported-input and smallness
scope, with the inverse-temperature convention recorded below.** This review
does not infer the static claim from the accepted zero-temperature result.
It independently reconstructs the new finite-temperature chain in
`a_independent/thermal_interface/STATIC_PEIERLS.md`, Sections 1--9. No finite
example or dynamics rerun was used.

## 1. Inputs actually used

The all-level check-soundness result in the frozen `RETRACTION_PROOF.md` is
an accepted input: a physical stabilizer of weight M has a supplied-check
representation of length <=F M^p, with size-independent F and an integer
p>=1. The bounded check geometry, growing code distance, exact corrected
logical Pauli algebra of one shared decoder, and primary valid-witness
counting/deletion statements are also imported inputs. This review neither
revalidates that retraction theorem nor substitutes a small constructed code
for the primary family and its spatial embedding.

The static Hamiltonian is H0=sum_j(I-S_j)/2. Thus a violated check costs one
unit. Throughout this review beta_c means the finite threshold in the
primary's explicit syndrome measure proportional to exp(-beta |sigma|),
namely the counting inequality in Theorem 5.13. The primary separately writes
the physical Hamiltonian -sum S_j; using that convention would rescale inverse
temperature by two. No physical-temperature identification is made without
this conversion. The producer incorporated this convention explicitly in
Section 1; no formula or numerical output changed.

## 2. Exact-label activities and factorization

Let D be stabilizer-group averaging. It is a contraction in the physical
Pauli coefficient l1 norm and fixes every syndrome projector. Since D(X)
commutes with every supplied check,

    T_J=e^(beta H0) D(e^[-beta(H0+V_J)])

is a positive Hermitian operator. There is no invalid claim that
e^(beta H0)e^[-beta(H0+V_J)] itself is positive.

Write V_i(s)=e^(sH0)V_i e^(-sH0). A Pauli term anticommutes with at most Dq
checks. Conjugation by one projector increases its coefficient l1 norm by
at most e^s. Hence ||V_i(s)||_P<=e^(beta Dq)||V_i||_P. Expanding T_J in the
local Dyson series and applying inclusion--exclusion retains exactly the
histories using all labels of J. For multiplicities n_i>=1, the ordered
time simplex and the number of label strings give the factor
product_i a_i^(n_i)/n_i!. Therefore

    ||W_J||_P <= product_i(e^(a_i)-1),
    a_i=beta e^(beta Dq)||V_i||_P.

This avoids an extensive e^(beta||H0||) estimate. The conversion
||V_i||_P<=2^q||V_i|| is valid by Pauli Parseval and Cauchy--Schwarz on a
q-qubit support, so arbitrary coherent local terms are genuinely included.

If two label components are nonadjacent, their native supports are disjoint,
and no check touches both. Every native operator of one component commutes
with the checks dressing the other component; all checks commute mutually.
Thus the two interaction-picture histories commute even at unequal times.
Time interleavings factor. Their check-charge characters have disjoint
supports, so a product has zero charge exactly when each component does.
This proves D-factorization and W_J=product_components W_component.
Redundant checks create no exception: zero charge is an assertion about
the full character, not independently assignable syndrome bits.

Möbius inversion consequently produces the stated exact hard-core operator
polymer gas. Compatible activities commute, even when incompatible large
activities need not. Each W_J is Hermitian as a real signed sum of T_K.

## 3. Centrality of every small polymer is justified

Moving stabilizer functions through native Paulis preserves the form

    native Pauli word times a function of stabilizers.

The native Pauli word uses only the union of the distinct labels' native
supports; repetition does not increase that support. Surviving stabilizer
averaging requires this word to be in the normalizer. For q|J|<d it must be
a stabilizer, up to its absorbed scalar phase, by the definition of quantum
distance. Hence W_J is in the central stabilizer algebra when |J|<ceil(d/q).
Multiplying small activities remains central even if the union of all labels
in the cluster has size above the distance. This is why scalar cluster tools
can be used without a noncommutative logarithm theorem.

## 4. The two cluster estimates have enough budget

I read Ueltschi, [math-ph/0304003v3](https://arxiv.org/abs/math-ph/0304003),
Theorem 1, Equations (3)--(5), in the acquired primary text. The following
application uses its ordinary scalar hard-core criterion and rooted bounds;
the theorem itself is not a new contribution.

Give polymer J weighted activity y_J=e^(|J|)||W_J||_P and KP size |J|.
The connected-set count rooted at one native label is at most
(Delta+1)^(2m). With B=(Delta+1)^2 e²w0,

    sum_(J incompatible G) y_J e^(|J|)
      <= |G|(Delta+1) B/(1-B) <= |G|.

The stated B<=1/[2(Delta+2)] has slack. Removing any small polymers preserves
the criterion. The formal coefficients are products in a commutative finite
Pauli algebra, and their norms are bounded termwise by the scalar majorant.
No pointwise scalar bound is silently converted into a Pauli l1 bound.

For completeness, the precise rooted-label estimate follows by rooting each
cluster at a polymer J containing the given label i. Ueltschi's rooted bound
gives the remaining cluster sum <=e^(|J|), so

    sum_(C whose union contains i) ||Phi_C||_P e^(m_C)
      <= sum_(J contains i) e^(2|J|)||W_J||_P
      <= B/(1-B).                                           (S1)

Overcounting clusters with more than one eligible root is harmless. This
supplies exactly the multiplicity-weighted decay later used for incidence.

The difference between log Z_s and the logarithm with polymers incompatible
with a fixed large family removed consists only of clusters touching that
removed set. The primary's rooted incompatibility inequality bounds its
absolute norm by sum_(J in Gamma)|J|. Exponentiating in the central algebra
proves

    ||Z_s^(avoid Gamma) Z_s^(-1)|| <= exp(sum_(J in Gamma)|J|).

The real scalar syndrome values of Z_s cannot cross zero along tV,
0<=t<=1, because KP convergence is uniform along this path and the cluster
exponential never vanishes. They start at one, so Z_s is positive. This
argument also applies to every avoided gas.

## 5. The large-polymer error is genuinely relative

Every small activity commutes with all twirled activities. Grouping the full
gas by its compatible large families is therefore exact. With b=B/e and
L=ceil(d/q),

    sum_(large J) e^(|J|)||W_J||_P <= |I| b^L/(1-b)=delta.

Ignoring compatibility only enlarges the positive majorant, giving
||T_I Z_s^(-1)-I||<=e^delta-1. T_I and Z_s are Hermitian commuting positive
operators. For delta<=1/4,

    (2-e^delta)Z_s <= T_I <= e^delta Z_s.

Multiplying by e^(-beta H0), tracing with any positive syndrome projector,
and dividing by the actual partition functions costs at most

    e^delta/(2-e^delta) <= e^(4delta).                         (S2)

The last inequality follows, for example, by integrating
d/dx[x-log(2-e^x)]=2/(2-e^x)<4 on [0,1/4]. This pays normalization and
avoids dividing an extensive absolute error by a tiny partition function.
It is only a statement about syndrome expectations of the full coherent
Gibbs state; it is not a physical dephasing step.

## 6. Check-incidence charge survives long stabilizer representations

Every physical Pauli coefficient of Phi_C is a stabilizer. Choose the
accepted representation with at most F M^p supplied generators. In the
check-overlap graph, distinct connected components have disjoint physical
supports. A component whose output is supported away from the monomial's
support must have identity output, and can be deleted. A stabilizer group
has no -I, so no residual sign obstruction occurs in this pruning.

Each remaining component touches the monomial support. Its length bounds
the graph distance of each retained generator from that support. Combining
the polynomial filling bound with the connected native-cluster diameter
gives R(m)<=R0 m^p. Thus for a fixed supplied check only clusters anchored
within this radius can contribute. Bounded density and native incidence give
at most C_geo m^(3p) possible anchors.

Apply (S1) separately at each anchor and total multiplicity m. This proves

    zeta <= (C_geo/beta) B/(1-B) sum_(m>=1)m^(3p)e^(-m)
          <= (C_geo/beta) B/(1-B) e(3p)! .                    (S3)

For the last inequality, on [m,m+1] use
x^(3p)e^(-x)>=m^(3p)e^(-(m+1)), then integrate and sum. Identity monomials
are constants and need no generator representation or incidence charge.
The bound is independent of volume but extremely conservative. An
operator-norm bound alone would not have justified this step; the physical
Pauli l1 budget in (S1) does.

Writing H_eff=H0-beta^(-1)log Z_s with these representations, flipping a
valid set tau of check bits changes the effective perturbation energy by
at most 2zeta|tau|. Cross-sector monomials and arbitrary coefficient signs
do not alter that conclusion.

## 7. Valid witness deletion, rather than arbitrary bit deletion

I read the primary 2605.10943v1 Sections 5.3--5.4, in particular Lemma 5.8
and Equations (218)--(236). Lemma 5.8 constructs an actual coboundary for
each witness. The witness is a subset of the originating syndrome. For a
fixed valid witness tau, sigma->sigma+tau is injective on the event
tau subset sigma and remains in the valid syndrome space. It drops the
unit-check H0 energy by |tau|.

By (S3), the perturbed effective energy drop is at least
(1-2zeta)|tau|. The primary's counting argument only needs the resulting
bound exp[-beta(1-2zeta)|tau|], so it repeats at beta_eff=beta(1-2zeta).
The untouched CSS sector may be held fixed; no independence assumption is
needed. Constant logical-sector multiplicities cancel because H_eff is
central. Combining the two sectors and (S2) gives exactly the displayed
4e^(4delta)2^(-2^(k-1)) bound for the primary sufficient bad-set union.

## 8. A common projector really covers the full support algebra

Let Pbad0 be that syndrome-diagonal sufficient bad projector, and define

    PbadX = OR_(U in Pauli(X)) U†Pbad0 U.

All projectors commute and their complement PgoodX obeys
Pbad0 U PgoodX=0 for every U on X. Every prefix of an ordered Pauli word
is among these same 4^q words, so every intermediate syndrome is in the
single-site good sector. Telescoping the corrected-logical commutators
therefore gives [O,U]PgoodX=0 for the full word. By linearity this holds
for every coherent operator supported on X, without a coefficient penalty.
The same common sector handles X,Z and their product Y.

Pauli conjugation is a bijection on the valid syndrome sectors even with
redundant checks. It flips at most Dq bits and changes effective energy by
at most (1+2zeta)Dq. Apply the classical translated-weight bound first, then
the 4^q union bound, then (S2). This recovers

    Tr rho_H PbadX
      <= 4e^(4delta) 4^q exp[beta(1+2zeta)Dq] 2^(-2^(k-1)).  (S4)

No unsupported comparison between e^(-beta H) and its Pauli conjugate was
used. Noncommuting Gibbs coherences are handled by the earlier syndrome
expectation comparison, while the logical kinetic receiver retains them.
For bounded three-dimensional density, q<=rho(1+R)^3; selecting a sufficiently
small fixed multiple of 2^(k/3) makes the positive volume term in (S4) smaller
than its negative 2^k term. This is the required growing-support input for
the exact quasilocal CKG class, not an assumption of finite-range Davies jumps.

## 9. Consequence and exclusions

At fixed beta above the specified counting threshold and sufficiently small
size-independent native Pauli l1 strength, the static bridge is mathematically
sound under the stated accepted source inputs. The smallness depends strongly
on beta, filling constants and geometry; no useful experimental threshold or
uniform low-temperature wedge has been acquired.

This review accepts neither a microscopic bath nor thermal initialization,
controlled native interactions, or the preparation of the encoder's ancilla.
It also does not establish world priority for the central-cutoff composition.
Ordinary quantum low-temperature/cluster-expansion antecedents remain relevant;
the exact new internal application is the relative central-small/large split
and its incidence-to-decoder bridge for this supplied recursive family.
