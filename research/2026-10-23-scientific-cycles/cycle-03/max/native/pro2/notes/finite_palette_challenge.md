# Finite-palette compression: a universal obstruction and a local-frame repair

Contributor: `/root/compression_challenge`, 22 October 2026 Brisbane.
This is a scoped lemma/challenge for the owner's stable-recovery programme.
No original-input benchmark, incoming proof replay, optimization, or new scientific target was run.

## 1. Contract

Let G be a known finite simple graph. Allowed matrices D are real symmetric,
supported on E(G) and all diagonal positions. A proper star coloring
kappa:V(G)->{1,...,c} means each two-color induced graph is a disjoint union of
stars. Let P have c row vectors p_a in R^q, each of Euclidean norm at most one.
The query matrix is X_v=p_{kappa(v)}. Error in the complete action block is
absolute Frobenius error; the principal target is operator error. Statements
below also give, when positive, the stronger Frobenius output guarantee.

## 2. All-palette obstruction on one fixed family of colored forests

**Theorem 1.** Fix c>=2 and N>=1. Form a forest H_{c,N} consisting of c disjoint
stars. The center of the i-th star has color i, and that center has exactly N
leaves of each color j!=i. Thus n=c[1+(c-1)N]. This is a valid c-star-coloring.
For EVERY c-by-q palette P with q<c and row norms at most one,

    sup_{0 != D in S_H} ||D||_2 / ||DX||_F >= sqrt(N/(c-1)),

with the ratio infinite if a nonzero supported D annihilates X. The palette
may depend on N, and may be dense, signed, or have short/zero rows.

**Proof.** Since q<c there is a nonzero alpha with sum_j alpha_j p_j=0.
Scale it so max_j |alpha_j|=1 and choose i with |alpha_i|=1. Restrict D to the
star centered at color i. Put D_00=alpha_i, each edge from its center to a
color-j leaf equal to alpha_j/N, and all other coefficients (including every
leaf diagonal) equal to zero. The center action is

    alpha_i p_i + sum_{j!=i} N*(alpha_j/N)*p_j = 0.

Each color-j leaf action is (alpha_j/N)*p_i. Consequently

    ||DX||_F^2 = ||p_i||^2 * sum_{j!=i} alpha_j^2 / N <= (c-1)/N.

Meanwhile ||D||_2>=|D_00|=1. The asserted ratio follows whenever action is
nonzero; otherwise it is infinite. The graph and its coloring were fixed
before P, so this is a uniform all-palette statement, rather than a bad
example of one selected simplex. QED.

**Consequence.** A compression operation that must preserve an arbitrary
supplied c-star-coloring cannot lower its c-coordinate palette to q<c and
retain a uniform operator/Frobenius-action inverse bound over all such colored
graphs. This remains false even on forests (degeneracy one), even when the
palette is optimized for the particular colored graph. Therefore a bound
such as c-1>2*degeneracy cannot repair unrestricted palette compression.
This is not an all-design lower bound for H_{c,N}: it has a three-query stable
forest decoder after recoloring, already supplied in the owner's checkpoint.
The hypothesis that rows depend only on the supplied color is load-bearing.

For a fixed palette P, universal safety over all c-star-colored graphs is
therefore characterized exactly by full row rank. Necessity is the preceding
proof. If sigma_min(P)>0, every row subpalette has smallest singular value at
least sigma_min(P), and Theorem 2 below gives the uniform bound sqrt(2)/sigma_min(P).
This full-row-rank condition requires q>=c. The statement is about fixed
palette compression, not about the best design on each underlying graph.

### Simplex specialization and the first rejected conjecture

For a regular unit simplex p_1,...,p_c in R^(c-1), sum p_j=0. Already ONE
star with center color1 and N leaves of every other color suffices: take
D_00=1 and every edge1/N. Its center action is zero and

    ||DX||_F^2=(c-1)/N,   ||D||_F^2=1+2(c-1)/N,   ||D||_2>=1.

For c=6 this rejects five-query simplex compression of an arbitrary six-star
coloring, with inverse amplification at least sqrt(N/5), despite degeneracy1.
The failure is coherent center cancellation whose residual is distributed
over increasingly many leaves. It is not loss of exact identifiability on
a fixed finite example.

## 3. Local-frame theorem: an actual bounded-error decoder

For each vertex v, let T_v be the set of colors in its closed neighborhood,
including kappa(v). Let P_T denote the rows of P with those labels.

**Theorem 2.** Suppose the coloring is a star coloring and every P_{T_v} has
full row rank with sigma_min(P_{T_v})>=s>0. Then q actual actions followed by
an explicit local decoder give, for every supported symmetric D and every
arbitrary action perturbation E,

    ||Dhat-D||_2 <= ||Dhat-D||_F <= (sqrt(2)/s) ||E||_F,
    where observed Y=DX+E.

**Decoder and proof.** At row v the noiseless action has the form

    (DX)_v = a_v P_{T_v},

where a_v's own-color entry is D_vv (proper coloring), and its other entries
are sums of incident edge coefficients over the corresponding color.
Recover the vector of row aggregates by

    ahat_v = Y_v P_{T_v}^T (P_{T_v} P_{T_v}^T)^(-1).

Then ||ahat_v-a_v|| <= ||E_v||/s. Each edge {u,v} is isolated at some endpoint:
in its bichromatic star, take a leaf endpoint. For a K2 component either end
works. Recover its coefficient from that leaf's aggregate at the other
endpoint's color. Recover every diagonal from its own-color aggregate.
All selected aggregate cells are distinct. Indeed the selected edge cell
contains only that one edge; diagonals have their own-color slots. Therefore

    ||Dhat-D||_F^2
       = sum_selected_diagonal error^2 + 2 sum_selected_edge error^2
       <= 2 sum_v ||ahat_v-a_v||^2
       <= 2 ||E||_F^2/s^2.

Symmetric copying explains the factor2; no independence, sign, cancellation,
or noise-structure assumption is made. The decoder is linear in the measured
action. It does not require recursive error propagation or a floating solver's
success status. QED.

**Checkable hypotheses.** Compute for each vertex v and color a its number
of neighbors of color a. Properness is checked on every edge. The star-color
condition is equivalent, for a proper coloring, to requiring that each edge
{u,v} has at least one endpoint satisfying
count(u,kappa(v))=1 or count(v,kappa(u))=1. If some bichromatic component were
not a star it would contain an edge with both endpoint degrees at least2;
conversely the displayed test says every edge belongs to a star component.
This same check supplies the exact selected endpoint for the decoder. Local
singular-value lower bounds require an exact or outward certificate for the
actual palette used; a numerical rank flag is insufficient.

**Costs.** With c,q fixed, assembling counts, validating the coloring, selecting
edge cells and decoding costs O(n+|E|) real-arithmetic work and storage, plus
q matrix actions. In explicit dimensions, row aggregate decoding uses at most
O(n q c) multiplies/adds once the at most 2^c distinct subpalette right inverses
are cached. A naive noncached preparation is O(n(q c^2+c^3)); the palette-only
cache costs O(2^c(q c^2+c^3)), independent of n. The graph/color pass can use
O(nc+|E|) storage or sparse dictionaries, and measured actions require O(nq)
storage if held all at once. The theorem does not assume action acquisition
is free. Reading a supplied graph or obtaining its coloring is additional
input/preprocessing work; no claim is made that discovering a coloring with
the extra local rank property is easy. Exact-real arithmetic and certified
finite precision are distinct implementation contracts.

The guarantee above is for the actual supplied X and absolute E. If intended
and applied directions differ by DeltaX, the term D*DeltaX belongs in E and
has norm at most ||D||_2 ||DeltaX||_F when an operator bound is supplied. No
relative-action-error interpretation or free input-conversion claim follows.

## 4. Missing-color sufficient condition for simplex compression

For the unit simplex, the Gram matrix on s0 selected palette rows is

    G_T = [c/(c-1)] I - [1/(c-1)] 11^T.

Its eigenvalues are c/(c-1) on the orthogonal complement of 1, and
(c-s0)/(c-1) along 1. Thus if every closed neighborhood omits at least r>=1
palette colors, then s0<=c-r, and sigma_min(P_T)^2>=r/(c-1). Theorem 2 yields

    ||Dhat-D||_F <= sqrt(2(c-1)/r) ||E||_F

with c-1 queries. In particular an additional one-omitted-color condition on
a six-star-coloring yields five queries and factor sqrt(10). The obstruction
above proves that this local condition cannot be removed indiscriminately.

This is a conditional representation theorem, not a proof that every
treewidth-two graph admits the strengthened six-star-coloring. Another scoped
contributor is investigating that separate combinatorial existence question.
No such existence is assumed here.

## 5. Comparison and novelty scope

The star leaf-cell mechanism is classical sparse-Hessian direct recovery.
Theorem 2 is an explicit conditioning/linear-frame extension of that mechanism,
not a historical priority claim. The exact universal finite-palette obstruction
and its application to the owner's compression proposal are new relative to
this checkpoint; historical originality has not been established.

One primary source was read in this local task:
Albertson et al., *Coloring with no 2-colored P4's*, EJC11(2004)R26,
https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v11i1r26/pdf/.
It supplies the classical star-color/in-orientation relationship. This read
cost one web-tool call, observed3.3s latency. The local proofs above are
self-contained; no external theorem is needed for their conclusions.

Source/check authoring and model service cost are unmetered additional work.
The accompanying exact script validates representative algebraic identities
and decoder selection on small rational inputs. It is supplementary; universal
proof is the argument above. No scientific scope is inferred from finite tests.
