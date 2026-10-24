# Common-real POVM pairs admit an exact Liouville boundary lift

24 October 2026. Parent's proposed extension checked independently. The conclusion is a relative comparison between two measurement channels sharing one real basis. It is not, without another argument, a contraction theorem comparing one measurement channel against the identity.

Let P and Q be POVM measurement channels on the same finite quantum input A. Assume every effect of both POVMs is real in one common orthonormal basis of A. Fix a faithful sigma_AR with dim R=r and a Hermitian H_AR satisfying H_R=0.

Use a copy R' of R and define the positive definite top state on A tensor R tensor R'

    G = [sigma_AR tensor I_R' + Swap_(R,R') (sigma_AR^T tensor I_R') Swap_(R,R')]/(2r).

The transpose is the FULL transpose on A,R in their fixed bases. It preserves positivity. The swap only exchanges R and R'. Each summand has trace r, so G is a density.

On the enlarged reference (R tensor R') direct-sum C|vac>, choose any faithful input density a0_A and define

    Gamma_epsilon = diag((1-epsilon)G, epsilon a0_A).

This is a faithful state. Define a rectangular top-to-bottom operator X by its physical A matrix blocks

    X_ab = |H_ab>> in R tensor R',

where H_ab is the R-valued (a,b) block of H. Let Z be the Hermitian reference-offdiagonal operator with blocks X and X*. Then

    Tr_A X = sum_a |H_aa>> = |H_R>> = 0,

so Z has zero reference marginal exactly.

For any nonzero real POVM effect E_i, put sigma_i=Tr_A[(E_i tensor I) sigma] and H_i=Tr_A[(E_i tensor I) H]. Realness gives

    Tr_A[(E_i tensor I) sigma^T] = sigma_i^T.

The output top block is consequently

    [sigma_i tensor I + I tensor sigma_i^T]/(2r) = Omega_(sigma_i)/r.

The output offdiagonal vector is exactly |H_i>> because

    sum_ab (E_i)_ba |H_ab>> = |Tr_A(E_i H)>>.

The bottom scalar is epsilon q_i with q_i=Tr(E_i a0)>0. Therefore the same finite-resolvent boundary formula as in the classical-input construction yields

    g^B_(P Gamma_epsilon)(P Z)/log(1/epsilon)
       -> 2r g^S_(P sigma)(P H),

and simultaneously the identical statement for Q. Both outputs are cq block algebras.

A uniform complete equal-reference Umegaki comparison between P and Q therefore implies the corresponding complete SLD comparison by taking infinitesimal pairs, then epsilon to zero. The universal conditional-SLD equivalence gives the reverse conditional implication, while conditional comparisons trivially include equal-reference pairs. Thus the three uniform relative orders coincide for any pair of POVMs with a common real basis.

## Exact scope limitation

The construction does not realize g^S_sigma(H) at the INPUT. Its input top state is G, not the full arithmetic-mean operator on HS(A tensor R). Already for r=1 and real sigma, G=sigma and the leading input cost is proportional to Tr H sigma^-1 H, not generally g^S_sigma(H). Therefore replacing Q by the identity is not justified by this lift. The current theorem needs both comparison outputs to be measurement channels with the stated common-real structure.

Any two binary qubit POVMs have a common real basis: their two Bloch directions span at most a plane, which a common physical unitary rotates into the XZ plane. Hence the relative-order conclusion covers arbitrary pairs of binary qubit POVMs. It does not automatically cover a generic informationally complete qubit POVM whose Bloch vectors span three dimensions.

## Sufficient shared-antiunitary extension

The common-real assumption can be weakened as follows. Suppose one fixed physical unitary U satisfies

    U E_i U* = E_i^T,    U F_j U* = F_j^T

for every effect of both POVMs. In the second top summand, replace sigma^T by (U* tensor I_R) sigma^T (U tensor I_R), then swap the two reference copies as before. The term stays positive. Cyclicity of the partial trace gives

    Tr_A[E_i U* sigma^T U]
      = Tr_A[E_i^T sigma^T]
      = (Tr_A[E_i sigma])^T,

and identically for F_j. All output and tangent identities in the proof are therefore unchanged.

Equivalently, the antiunitary J=K U, where K is conjugation in the fixed basis, commutes with all effects. The construction does not require J^2=+I; a symmetry with square -I need not admit a common real basis. This is only a sufficient compatibility hypothesis. It does not claim every POVM pair has such a symmetry, give a classification algorithm, or remove the generic complex orientation obstruction. The identity-input limitation remains unchanged.
