# Charged-component minimum-of-two decoder lemma

Root proposed this route. The following independently checked algebraic lemma shows exactly what the actual construction must supply. It replaces an unnecessarily strong pointwise cleaning demand, but is not a completed stability/witness theorem.

## Hypotheses

Let D be the fine syndrome map, d the coarse syndrome map, J a fixed coarse-to-fine syndrome lift. Suppose two linear bounded-row/column-support pairs (f_A,p_A),(f_B,p_B) and a similarly local K satisfy, for every valid fine syndrome σ,

    σ = D f_A σ + J p_A σ = D f_B σ + J p_B σ,
    p_A σ + p_B σ = d K σ.

Suppose p_A,p_B are actual cochain syndrome projections, hence each maps globally valid fine syndromes to globally valid coarse syndromes. Suppose also their input supports lie in disjoint sheet sectors and

    |p_A x| ≤ |x restricted to sheet A|,
    |p_B x| ≤ |x restricted to sheet B|

for arbitrary x. Parent-face parity projections have this property; arbitrary HPL maps need not.

If the two initial lifts differ, a bounded chain homotopy between them may be used to put both identities into a COMMON J; that extra map must be supplied, not silently assumed.

## Dependency components and local residual identities

Form a bounded-degree graph on fine syndrome coordinates, joining coordinates whose influence neighborhoods overlap in any of f_A,f_B,p_A,p_B,K, or in a row of the residual operators

    R_A=I+D f_A+J p_A,
    R_B=I+D f_B+J p_B,
    R_K=p_A+p_B+dK.

All these operators must have uniformly bounded support. Restrict the graph to occupied coordinates of σ. For each connected component C let σ_C be its restriction.

Since R_Aσ=R_Bσ=R_Kσ=0 and a residual row cannot see occupied coordinates from different components, the same three residual identities hold on every σ_C. This uses only local linear constraints; σ_C need not itself be a globally valid syndrome.

## Componentwise choice and exact global validity

On each C choose t_C∈{A,B} minimizing |p_t σ_C|, with deterministic ties. Set

    f(σ)=Σ_C f_{t_C}σ_C,
    p(σ)=Σ_C p_{t_C}σ_C.

Then σ=D f(σ)+J p(σ). Moreover

    p(σ)=p_Aσ+d Σ_{C:t_C=B}Kσ_C,

so p(σ) is a valid coarse syndrome. This is the precise reason independently selected components do not break coarse admissibility.

Finally,

    |p(σ)| ≤ Σ_C min(|p_Aσ_C|,|p_Bσ_C|)
            ≤ (1/2)Σ_C(|σ_C|_A+|σ_C|_B)
            ≤ |σ|/2.

The same inequality holds on each component before summing. No weight-nonincreasing fine correction is required: corrections may have bounded-size but nonzero syndrome output, and the entropy bookkeeping charges their support to input defects.

## What locality means here

The choice on a component can depend on an arbitrarily large connected set. It is therefore **not** a constant-radius decoder. Its support is confined to the union of bounded influence neighborhoods of the component, of size at most c|σ_C|. Connected shape counting can charge this support linearly to occupied syndrome mass.

A single-qubit update can merge/split components and change the chosen copy throughout a large component. Such influence must be counted as a large connected witness; it cannot be declared bounded-radius. A full lifetime proof still needs the logical class identity, distance/local filling as appropriate, and a proof that a logical decoder change forces a polynomial-size occupied witness across the recursive history. The product-Gibbs occupancy bound supplies the eventual commuting probability estimate only after that witness statement is established.

## Actual-family gaps

The explicit ell=8 family has not yet supplied all the bounded alignment homotopies, common lift, and exact parent projections used in this lemma. The shifted rib inclusions and recursive parent-boundary atlas are the specific outstanding algebraic/geometric joins. Thus this is a reusable positive decoder mechanism with an explicit contract, not a theorem that ell=8 already satisfies it.
