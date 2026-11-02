# Exact candidate reduced mapping-cylinder gate for Section 6 X doubling

This records a representation justified locally by the source's actual blue attaching incidences and checked independently by the native parallel reader. It is a reduced complex after degree-2 subdivision transports, **not** equality of raw physical vector spaces or a Hamming isometry.

Let A and B denote the refined sheet complexes. Let R be the abstract compatible-rib graph with its inherited sheaf, with actual endpoint inclusion maps i_a:R→A and i_b:R→B. R must not identify distinct free-cross vertices because their images coincide. A T vertex retains the inherited seam code; a glued-cross vertex carries repetition code on its four incident bands. The maps i_a and i_b use distinct rib preimages: compatible physical planes 4,5 in the original sheet correspond to preimages 3,4 in the translated copy. The two restriction maps must not be set equal by fiat.

After collapsing ordinary degree-2 subdivisions in the cylinder strips, the X-doubling complex has the mapping-cylinder syndrome block form

    C¹_new = C¹(A) ⊕ C¹(B) ⊕ C⁰(R),
    C²_new = C²(A) ⊕ C²(B) ⊕ C¹(R),

    D(x,y,z) = (δ_A x, δ_B y, r_a x + r_b y + δ_R z).

Here r_a,r_b are the actual cochain restrictions to the two attaching subcomplexes. An attaching-rib edge's original two-face repetition column becomes a three-face repetition column, producing its sheet δ component and its one cylinder component. A vertical cylinder-edge correction is a stalk element at an R vertex; its band syndrome is δ_R z. These are exactly the local X-doubling rules. The T polygon subdivisions in Example6.8 can be reduced by actual degree-2 pair columns; lifting remains necessary when estimating physical weights.

This formula is not asserted for Z doubling without rebuilding the appropriate parity-sheaf complex.

## Matrix test for actual admissibility, avoiding assumed balance

Let a,b,c be the reduced face-syndrome blocks. The full exact metacheck space is the kernel of D transpose. Its elements (λ_a,λ_b,μ) satisfy

    δ_A^T λ_a + r_a^T μ = 0,
    δ_B^T λ_b + r_b^T μ = 0,
    δ_R^T μ = 0.

Therefore (a,b,c) is a valid syndrome iff

    <λ_a,a> + <λ_b,b> + <μ,c> = 0

for every solution of those three equations. This is necessary and sufficient finite GF(2) linear algebra, not a local-acyclicity heuristic. For the central hashtag cycle μ, its two sheet fillings λ_a,λ_b give precisely the six-face central-cube metacheck already proved.

A cylinder trace at a single T star is not generally constrained to have W=0: the associated relative cycle may not close until neighboring ribs and both sheet fillings are included. These equations give a decisive test for any proposed balance rule and for any proposed coarse image F: construct actual matrices, solve this kernel, and verify the claimed rule lies in its row space. Merely computing a vertex stalk F_v from edge codes does not establish a syndrome constraint.

## Geometric correction to an overly simple transport plan

Section6.2.5/Table1 puts no ribs in W0 (the coarse-vertex regions). Cylinder contacts lie in W1 and W2. Thus cylinder defects cannot simply travel along cylinder cells into W0 and cancel there. They must circulate through the W1/W2 rib network or first convert into correlated sheet-side carries. The five-edge T flow representation retains the necessary correlations; splitting its charges independently can double the weight.

## Exact remaining constructive target

Provide the actual bounded subdivision transports for every endpoint gadget and a finite relative complex for the complement of R in the two sheets. Use the above metacheck equations to prove the required carry compatibility only after a complete bounded local circuit, then establish a weight-controlled map to a specified coarse complex. A useful sufficient structural route would identify the kernel cycles of R→A and R→B with bounded complementary-region boundaries and explicitly control both sheet fillings. That identification is NOT yet proved for inherited recursive T gadgets.

## Lower-degree consistency and an exact logical test

The compatible degree-zero differential in the reduced representation is

    D0(u,v) = (δ_A u, δ_B v, r_a u + r_b v).

It satisfies D D0=0 because each r is a cochain map. This gives a concrete test of any reconstructed incidence matrices before a decoder is attempted.

The associated long exact sequence has the segment

    H0(A)⊕H0(B) → H0(R) → H1(new)
       → H1(A)⊕H1(B) → H1(R),

where the two horizontal restriction maps are sums of the actual endpoint restrictions. Hence preservation of logical dimension is a checkable kernel/cokernel statement, not an implication of the drawing. For example, surjectivity at H0 and injective, equal-image endpoint maps at H1 would identify H1(new) with a diagonal copy of old H1. Those hypotheses are stated as a future matrix test, not assumed for every inherited gadget here.
