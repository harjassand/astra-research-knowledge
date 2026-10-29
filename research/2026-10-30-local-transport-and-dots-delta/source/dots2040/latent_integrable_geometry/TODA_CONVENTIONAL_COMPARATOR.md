# Raw-coordinate periodic Toda recognition: constructive comparator verdict

**Verdict (2026-10-29): the tested C−4D recognition construction has no demonstrated capability or complexity advantage over an equally informed elementary algebra/Darboux comparator.** Its exact coordinate acquisition works, but its central hidden a/b split can be replaced by a linear self-adjointness kernel. This is an independently derived specialization of ordinary methods, not a claim that the identical algorithm was previously published. It does not settle novelty of any broader project.

## Interface and shared acquisition

Both programs receive only a rational homogeneous quadratic field f in 2N raw coordinates and an initial point x0. N≥3; the test family consists of invertible rational linear conjugates of periodic Toda:

    a_i' = a_i (b_(i+1) − b_i),
    b_i' = 2(a_i² − a_(i−1)²).

Both acquire the one-dimensional linear first-integral space and the one-dimensional annihilator of the polarized multiplication T(u,v)=(f(u+v)−f(u)−f(v))/2. They remove the central b-translation direction, use the invariant hyperplane W as a concrete quotient model, and solve the same linear coefficient equations for a positive definite quadratic conserved form G on W. The implemented admission check requires that form to be unique up to scalar. Thus the comparator is not given the physical a/b split, a hidden chart, cofactors, or a metric unavailable to the proposed recognizer. The public fixture constructor is used only to create inputs; neither recognition function receives its matrix.

## Exact split proof

Let D be oriented cyclic incidence, (Db)_i=b_(i+1)−b_i, so f=(diag(a)Db,−2D^T(a∘a)). On the zero-mean b-space the physical conserved metric is G=c diag(2I,I), c>0. Multiplication by z=(a,b) is

    L_z = [ (1/2)diag(Db)       (1/2)diag(a)D ]
          [ −2D^T diag(a)             0      ].

Consequently

    G L_z − L_z^T G = c [ 0                  3 diag(a)D ]
                                [ −3D^T diag(a)        0      ].

Every row of D is nonzero even restricted to zero-mean b. Hence this vanishes **if and only if a=0**. In any acquired basis of W, solve the linear coefficient system

    B = {z ∈ W : G L_z − L_z^T G = 0}.

It gives exactly the hidden b-space (dimension N−1). Its G-orthogonal complement A is the hidden a-space (dimension N). Congruence of G and similarity of L prove coordinate invariance. Scaling G changes neither space. No fourth-order contraction, C−4D, nonlinear algebraic solve, or Jordan theorem is required.

## Reconstruct the complete chart, not merely the split

For β∈B, L_β restricted to A is diagonal in the physical a-lines with eigenvalues (Dβ)_i/2. The N distinct root functionals have pairwise unequal values for a generic β. Choose β(t)=Σ_(j=0)^(N−2) t^j β_j in any acquired basis of B. Each difference is a nonzero polynomial of degree ≤N−2; at most (N−2)N(N−1)/2 parameter values are bad. Testing integers from zero through that bound guarantees a simple spectrum. The implementation uses the square-free characteristic-polynomial test, then exact eigenspaces.

For each acquired eigenline vector u, form its G-dual coordinate p, extended to vanish on B and the central direction. It is proportional to a physical a_i. Verify the linear Darboux identity

    ∇p · f = p c_i

by exact polynomial division. Its cofactor c_i is b_(i+1)−b_i, unaffected by rescaling p. Normalize p(u)=1. For u in the corresponding raw a-line,

    c_i(f(u)) = −4 a_i(u)².

Thus multiply p by sqrt(−c_i(f(u))/4), orienting its sign using x0. This recovers positive-sector physical amplitudes. The dual-metric Gram matrix of the cofactors has equal positive diagonal, −1/2 times that diagonal on cycle neighbors, and zero otherwise (for N=3 every other vertex is a neighbor). This acquires cycle order. Solve the cofactor difference equations plus the acquired linear invariant as the mean to obtain b. Freedom to scale the central invariant is harmless because adding a constant multiple of the central coordinate to every b preserves the field.

Finally verify the entire polynomial identity K f(x)=Toda(Kx), nonsingularity, and both inverse compositions. These checks provide sound certification even outside the promised class; preliminary rank/Gram tests alone do not. The implementation rejects zero a-coordinates at x0 because it uses x0 to select the positive sector. Arbitrary real conjugacy can require algebraic numbers; rational fixtures here have rational reconstructed charts. General bit complexity of symbolic eigenvalue algebra is not benchmarked.

## Reproducible evidence

Run from this workspace:

    python -u latent_integrable_geometry/audit/toda_selfadjoint_comparator.py
    python -u latent_integrable_geometry/audit/toda_paired_replay.py

The comparator module imports no producer code. The paired *test driver* imports both implementations to provide identical fields and x0. Its JSON stores raw fields, initial states, input hashes, acquired charts, component identities, timings, software version, and source hashes. Exact mixed N=3,4,5 acquisitions pass both methods; they verify 6,8,10 raw component identities respectively and both inverse compositions. The chart transition is independently checked to be an exact Toda symmetry. Chart coefficient bit maxima match: 6,6,4. One paired run took 0.73/2.45/2.11 seconds for the tensor method and 0.30/1.56/1.74 seconds for the comparator. These tiny serial, cache-affected tests establish feasibility, **not** a speed theorem.

A connected four-edge/four-vertex noncycle (triangle plus pendant edge) preserves the elementary center/energy setup. Both methods reject it unmixed and after the same public mixing, with exact rejection assertions saved. This is a useful negative control, not exhaustive adversarial testing. Assertions must remain enabled (do not run Python with `-O`).

## Source-checked prior art and limits

* **Quadratic field → commutative nonassociative algebra** is classical: Markus explicitly identifies linear equivalence of quadratic systems with algebra isomorphism. The original paper's indexed opening and theorem text were accessible; direct PDF extraction failed because of file size. [Markus (1960), original scan](https://rainbow.ldeo.columbia.edu/~alexeyk/QDS/Markus1960.pdf).
* **Darboux computation for Toda** is a concrete comparator, not a vague appeal to “known integrability.” Tsiganov §2.1 defines the polynomial/cofactor coefficient solve; §3.1, Eq. (3.9), explicitly solves a bilinear system for a linear polynomial and cofactor. He acknowledges using known diagonal coordinates as implicit information. His system is the **full symmetric/Kostant Toda** family, not the cyclic nearest-neighbor raw conjugacy problem here. The periodic field has zero divergence, so his divergence-based cofactor guide does not simply recover this hidden split. His abstract is not an end-to-end theorem for the present interface. Our self-adjointness solve supplies the split without the nonlinear generic Darboux search. We do not endorse a general polynomial-time claim for solving bilinear systems. [Tsiganov (2025), full primary text §§2.1, 3.1](https://arxiv.org/html/2501.14251v1).
* **Jordan spectral theory is not directly applicable to the Toda polar algebra.** Orlitzky assumes a unital Euclidean Jordan algebra, including the Jordan identity and an associative positive inner product. The Toda product is not Jordan: take z=(e_i,0). Then z²=(0,−2D^Te_i), z²*z=−2z, so z*(z²*z)−z²*(z*z)=−2z²≠0. This counterexample lies in W and is exactly replayed for N=3,4,5. Therefore invoking Jordan classification/frames without constructing a different valid Jordan algebra would be a category error. Ordinary self-adjoint matrix diagonalization is all the comparator needs. [Orlitzky (2022), Definition 1 and Theorem 1](https://michael.orlitzky.com/documents/papers/rank_computation_in_euclidean_jordan_algebras.pdf).

## What obstacle remains?

The tensor construction does avoid a blind nonlinear Darboux-coefficient search, but **that is not an obstacle faced by the strongest equally informed comparator**: the same acquired G makes the relevant subspace a linear kernel, followed by conventional spectral/Darboux reconstruction and the same cycle test. No acquisition barrier uniquely removed by C−4D survives this comparison. Neither method by itself supplies a new periodic Toda decoder, certified long-time numerical accuracy, robust noisy recognition, or treatment of unknown nonlinear coordinate changes. No historical identity or priority claim is established by this bounded literature check.
