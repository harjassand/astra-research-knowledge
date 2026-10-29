# Convex channel fitting for the positive-operator Pauli certificate

28 October 2026. Root candidate upgrade. Separate receiving required. The received positive_operator_clifford_acquisition_20261028.md remains unchanged. This replaces its expensive global unitary search by a convex channel SDP followed by explicit Pauli rounding and the same acquired certificate.

## 1. Retained physical contract

Use exactly the received common-global-V, local-envelope, actual private three-axis probes, predictable-history means and positive operator-block contract:

    C_j=sum_k B_k T_kj,
    T_kj=T_jk Hermitian, [T_kj,B_a]=0, T>=0.

Unknown T entries may be noncommuting and vary with past history. Local B comes from the same fixed global mixer as other input-qubit algebras. The dimension d=2g is the containing envelope dimension. No new physical access, environment model, native reset or oracle for C is supplied.

## 2. An observable convex objective

Let Phi:M_2->M_d be any UNITAL completely positive map, with A_j=Phi(sigma_j). It is the adjoint of a physical trace-preserving recovery, although that recovery is used here to propose generators, not blindly sewn into a complete inverse. Define its Choi matrix in auxiliary-input/output order by

    K=(1/2)[I_2 tensor I_d+sum_j sigma_j^T tensor A_j].

Unital complete positivity is equivalent to K>=0 and Tr_aux K=I_d. Its trace is d. Set

    H=sum_j sigma_j^T tensor C_j.

Then Tr(HK)=sum_j Tr(C_j A_j)=F_C(A). The acquired optimization is the SDP

    maximize Tr(Hhat K), K>=0, Tr_aux K=I_d,
    Hhat=sum_j sigma_j^T tensor Chat_j.             (1)

The true physical embedding A_j=B_j is feasible.

## 3. Positive operator blocks give an exact SDP dual certificate

Put Y=sum_j T_jj, and D_j=sigma_j^T tensor I_d-I_2 tensor B_j. Because T entries commute with B and are symmetric in j,k,

    Q=I_2 tensor Y-H
     =(1/2)sum_jk D_j(I_2 tensor T_jk)D_k >=0.      (2)

Thus Y is a valid dual matrix. Antisymmetric Pauli cross terms cancel in both auxiliary and physical factors. At the true embedding the primal objective equals TrY, so it is globally optimal in the ENTIRE convex channel set, not merely on unitary Pauli triples.

If T>=tau I_(3d), then

    Q>=tau[3I_(2d)-sum_j sigma_j^T tensor B_j].

For any feasible K, unital positivity gives -I<=A_j<=I, hence Tr A_j^2<=d. Therefore

    F_C(B)-F_C(A)
       >=tau[3d-sum_j Tr(A_j B_j)]
       >=(tau/2)sum_j ||A_j-B_j||F^2.              (3)

No commutation of candidate A with unknown T is assumed. The dual is used for proof, not as a supplied computational oracle.

Let E=(sum_j||Chat_j-C_j||F^2)^(1/2). A feasible rational SDP output within zeta of its true empirical optimum then satisfies

    Dnorm=(sum_j||A_j-B_j||F^2)^(1/2)
       <=[E+sqrt(E^2+2 tau zeta)]/tau.             (4)

The proof is the same noisy-objective comparison as in the received variational theorem, now over a convex feasible set. In particular E<=sqrt(3d)a on the simultaneous ordinary-data event. A numerical value of tau need not be supplied: it is used to prove eventual completion, while the acquired positive fit checks actual accuracy.

## 4. Finite SDP interface

Parameterize the affine constraint exactly by the Hermitian matrices A_j, so approximate feasibility need only concern PSD. The known center K0=I_(2d)/2 is strictly positive, and every feasible K has trace d and Frobenius norm at most d. These give explicit inner/outer radii for the same rational PSD separation and finite weak-optimization machinery used in the separately received accessible endpoint source.

If an affine numerical output has K>=-eta I, repair it by

    Kphys=(K+eta I_(2d))/(1+2eta).

It remains exactly unital and becomes PSD; its Pauli images are A_j/(1+2eta). The repair changes the objective by at most6d(1+a)eta when every ||Chat_j||op<=1+a. Optimization and repair slacks must be budgeted together into zeta, not ignored after solving. The SDP step has the standard finite rational convex-optimization dependency on dimension, coefficient bits and requested precision; no hidden global unitary search remains. No production solver run is claimed by this derivation.

The source interfaces for this finite step are ACCESSIBLE_ENDPOINT_RATIONAL_SDP_AND_COMPILER.md and its separate receipt in cross_foundation_bridge_20261028/. Its generic Choi/PSD/finite-arithmetic machinery is used, not any claim that it already proved the present dual certificate.

## 5. Explicit rounding to a physical Pauli triple

The feasible SDP images need not be reflections or anticommute. Do NOT substitute them as unitary gates. Form the following known matrix functions:

    X=sign(A_X),
    Zodd=(A_Z-X A_Z X)/2,
    Z=sign(Zodd), Y=i X Z.                        (5)

Only proceed when A_X and Zodd have certified strict spectral gaps around zero. Zodd is Hermitian and anticommutes exactly with X. Its invertible sign therefore anticommutes with X. Thus (X,Y,Z) is an exact physical Pauli triple on an even-dimensional space, with X necessarily balanced because an invertible anticommuting Z pairs its two eigenspaces.

For completion, if the SDP images tend to true B_X,B_Z, spectral continuity gives X->B_X, Zodd->B_Z and Z->B_Z. The singular-value/sign gaps approach1. For example the odd projection difference obeys

    ||Zodd-B_Z||op <= ||A_Z-B_Z||op+||X-B_X||op,

because the projection onto X-odd operators is an operator-norm contraction and the difference of the two X-conjugations of B_Z is at most2||X-B_X||op. Known sign perturbation bounds then give quantitative convergence. No empirical appearance of approximate anticommutation is treated as exact physicality.

These matrix functions are known finite matrices, not source operations. Exact algebraic descriptions or certified outward interval computations with separately compiled controls are permitted. Actual physical reflection gates can be synthesized with a paid operator-norm error. One explicit finite exact representation is to diagonalize X, write Zodd in its off-diagonal block form, and use the unitary polar factor of its invertible off-diagonal block; this gives Z with exact anticommutation. Rational-unitary approximations and spectral residuals can then implement the gates with the original whole-process allowance. Symbolic field size, conditioning and control synthesis are not declared free or practically efficient; the new polynomial convex optimization claim concerns the SDP candidate stage, not an unqualified end-to-end hardware runtime.

## 6. Acquired accuracy, not reliance on unknown tau

Apply the RECEIVED positive-fit certificate to the rounded physical triple (X,Y,Z). Compute its Pauli conditional expectation, symmetrized own-commutant coefficient block S, and known model Ctilde. Certify S>=kappa I for a rational kappa>0. Compute a rational upper bound e on the full observed fit residual plus sqrt(3d)a, including matrix-function/certificate arithmetic errors. Accept only when

    2e/kappa <= desired delta.                    (6)

This soundness certificate needs no global optimality claim from a numerical solver. Any physical candidate satisfying it is valid under the source promise. The SDP proof provides an efficient convex WAY TO GENERATE candidates and an eventual-completion argument: under a persistent positive local true gap, shrinking a,zeta forces A->B by(4), rounding is continuous, S->T, the fit shrinks, and(6) eventually passes. Finite funded stages can still abstain; no generic source-membership test follows.

All finite confidence unions, actual source blocks, acquired support, current-coin privacy and global-V compatibility remain as in the received parent construction. Once every X/Z error is at most delta, the literal3n-block coherent extraction circuit has operator error at most3n delta. The same complete-memory future comparison, known-code composition, finite causal reuse and physical implementation debits follow. A local recovery Choi matrix was a computational proposal, not an assumed noiseless logical subsystem or an erased gauge output that could destroy other qubits.

## 7. Actual advance and remaining work

This closes a specific algorithmic obligation in the positive operator-block representation: a tractable-size convex channel fit replaces nonconvex global Pauli-algebra search, while a separate positive residual certificate protects soundness and absorbs numerical search failure. The local dimension remains exponential in envelope width, source sample/control budgets may remain large, and efficient acquisition of the source promise is not claimed. A real sampled pilot and strong equally informed comparison are still required for any practical advantage. Standard quantum recovery SDPs and local-unitary sewing are prior machinery; novelty of this operator-block dual and acquired certificate has not been established externally.
