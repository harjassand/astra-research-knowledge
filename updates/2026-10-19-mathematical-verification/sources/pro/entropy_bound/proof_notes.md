# Entropy forced by a reversible sampled Markov chain

Research notes written 19 October 2026. All statements below use row generators,
natural logarithms, and the ordinary time reversal in which every state is even.
These are proofs reconstructed independently in this run, not recovered prior files.

## 1. Setting and notation

Let P be an n by n stochastic matrix, reversible with respect to a strictly
positive probability vector p. Assume its eigenvalues are strictly positive.
Fix a sampling interval t>0. Write

    D=diag(p), R=D^(1/2) P D^(-1/2), H=t^(-1) log R,
    T=-t^(-1) log det(P), d^2=sum_(i != j) (max(-H_ij,0))^2.

Then R is real symmetric positive definite and H is real symmetric. The
quantity d is the Frobenius norm of the negative off-diagonal part of H.
Assume d>0 and that there exists at least one real Markov generator Q with
exp(tQ)=P. Thus Q_ij>=0 for i!=j and Q1=0. The irreducible case is simplest,
but the proof also works when P is reducible, provided p has full support.

Define the stationary entropy production

    sigma(Q)=sum_(i<j) (p_i Q_ij-p_j Q_ji)
                       log[(p_i Q_ij)/(p_j Q_ji)].

An edge with two zero fluxes contributes zero; an edge with exactly one zero
flux contributes +infinity. This is a statistical irreversibility rate; its
thermodynamic interpretation requires the usual local-detailed-balance model.

## 2. Main explicit bound

Let p_min=min_i p_i, and let s be the sum of the two smallest p_i. Every
compatible Q satisfies

    sigma(Q) >= max(12 p_min, 2s)/T * (d^2 + 8 pi^2/t^2).       (1)

The simpler constant 2s/T requires only elementary two-state traffic estimates.
The 12 p_min/T term uses circulation and is especially useful for uniform p.
For uniform p_i=1/n, it improves the simple constant by a factor of three:

    sigma(Q) >= 12/(nT) * (d^2 + 8 pi^2/t^2).                 (2)

All terms on the right can be computed from P and t alone. The feasible set
of generators is compact. The extended-valued entropy functional attains its
minimum on this set, and the minimum satisfies (1). If every embedding has an
irreversible one-way edge, this minimum may be +infinity.

The right side is not asserted to be the exact minimum. The point is a
strict positive, closed-form certificate that survives the continuous families
of logarithms associated with repeated observed eigenvalues.

## 3. Stationarity and compactness

First, p is stationary for every compatible Q. For irreducible P, Q is
irreducible: a directed path of positive rates makes the corresponding entry
of exp(tQ) positive, and exp(tQ) cannot create communication absent from Q.
The unique stationary distribution of Q is invariant for P and hence equals p.

For general reversible P with p>0, there are no transient classes and, after
permuting states, P is block diagonal over its communicating classes. A
positive rate crossing between two blocks would make the corresponding entry
of exp(tQ) positive (use the positive one-jump path weight), which is
impossible. Thus Q is block diagonal with the same classes, and the preceding
irreducible argument applies to p conditioned on each class. Therefore pQ=0.

The determinant identity gives

    tr Q=t^(-1) log det P=-T.

There is no logarithm ambiguity here: tr Q is real and det exp(tQ)=exp(t tr Q).
Consequently T=sum_i(-Q_ii), every exit rate is at most T, and every
off-diagonal rate is at most T. The generator constraints and exp(tQ)=P
define a closed subset of a bounded finite-dimensional set. It is compact.

The edge function (a-b)log(a/b), with the conventions above, is nonnegative
and lower semicontinuous on [0,infinity)^2. At (0,0), nonnegativity suffices;
at a positive/zero boundary, it diverges. Thus sigma is lower semicontinuous
and attains an extended-valued minimum on the nonempty compact feasible set.

## 4. Exact branch identity

For any compatible Q put

    A=D^(1/2) Q D^(-1/2), S=(A+A^T)/2,
    K=(A-A^T)/2, U=S-H, B=A-H=U+K.

Both Q1=0 and pQ=0 imply A sqrt(p)=A^T sqrt(p)=0. In particular S and K
annihilate sqrt(p). Since off-diagonal entries of A are nonnegative,
S_ij>=0 for i!=j. Therefore

    ||U||_F^2 >= d^2.                                       (3)

A commutes with R=exp(tA), hence preserves each orthogonal eigenspace E_l
of the symmetric matrix R. On E_l, R=l I and H=(log l)/t I. Thus B
preserves E_l and exp(t B|E_l)=I. Its eigenvalues are 2 pi i k/t for integers
k. All eigenvalues of B have that form. They occur in conjugate pairs
because B is real. (In fact B is diagonalizable: a nonzero Jordan nilpotent
part cannot exponentiate to the identity.)

Using trace, not an assumption of orthogonal diagonalizability, gives

    tr B^2=-(4 pi^2/t^2) sum_l k_l^2.

On the other hand symmetry/skew symmetry give tr UK=0,
tr U^2=||U||_F^2, and tr K^2=-||K||_F^2. Hence the exact identity

    ||K||_F^2=||U||_F^2+(4 pi^2/t^2)sum_l k_l^2.              (4)

If all k_l=0, then exp(tB)=I and the nilpotent observation above imply B=0.
This would make A=H, impossible because H has a negative off-diagonal entry.
Therefore a nonzero conjugate pair occurs and sum_l k_l^2>=2. Combining
(3) and (4) proves

    ||K||_F^2 >= d^2+8 pi^2/t^2.                            (5)

This is the source of the discrete branch contribution. It is not an
approximation or a small-defect argument. The same branch floor applies to
any nonprincipal embedding of a reversible positive-spectrum P, even if
the principal logarithm happens also to be a generator.

Remark: Because any nonzero k must occur in conjugate pairs within one real
eigenspace E_l, a reversible positive-spectrum P with simple spectrum has
no nonprincipal real logarithm. Our setting necessarily involves repeated
observed eigenvalues. Eigenvalue one cannot carry nonzero branches of a
finite Markov generator (or use the blockwise stationary argument above).

## 5. Elementary entropy-to-skew estimate

For i<j let a=p_i Q_ij, b=p_j Q_ji, c=a+b, j=a-b. The scalar inequality

    (a-b)log(a/b) >= 2(a-b)^2/(a+b)                         (6)

holds for nonnegative a,b with the adopted limiting conventions. For
positive a,b this is 2x atanh(x)>=2x^2 with x=(a-b)/(a+b).
Also K_ij=j/(2 sqrt(p_i p_j)).

Define the activity-normalized maximum

    kappa=max_(i<j) c_ij/(2 p_i p_j).

Equation (6) yields the standard estimate

    sigma(Q)>=2||K||_F^2/kappa.                             (7)

This estimate, including stronger nonlinear forms, is prior work:
Kolchinsky, Ohga and Ito (2024), Appendix C.1.

Let x_i=-Q_ii. Stationarity makes total incoming and outgoing flux at i
both p_i x_i. Therefore c_ij<=2p_i x_i and c_ij<=2p_j x_j. It follows that

    x_i+x_j >= c_ij/(2p_i)+c_ij/(2p_j),
    c_ij/(2p_i p_j) <= T/(p_i+p_j) <= T/s.

Thus (7) implies sigma(Q)>=2s||K||_F^2/T. Together with (5), this proves
the first, simplest version of (1).

The exit-rate lower bounds x_i>=-log(P_ii)/t from Bauer et al. can improve
this constant. For instance, if l_i=-log(P_ii)/t, then

    kappa <= max_(i<j) [T-sum_(r not in {i,j}) l_r]/(p_i+p_j).

This refinement is optional; all proofs above use only T and p.

## 6. Circulation improvement

Choose one orientation for every undirected pair and retain signed current
j_e. Its divergence at every vertex is zero. Put

    h_e=(p_i+p_j)/(2p_i p_j),
    L=sum_e |j_e| sqrt(h_e),
    N=sum_e j_e^2/(p_i p_j)=2||K||_F^2.

Stationarity eliminates the gradient term in the total rate:

    T=sum_e [a_e/p_i+b_e/p_j]
     =sum_e h_e c_e + (1/2)sum_e j_e(1/p_i-1/p_j)
     =sum_e h_e c_e.

Cauchy-Schwarz and (6) give

    sigma >= 2 sum_e j_e^2/c_e >= 2 L^2/T.                  (8)

Every divergence-free current decomposes into sign-compatible directed
simple cycles with nonnegative amplitudes. Let C be one such cycle and

    l_C=sum_(e in C) sqrt(h_e),
    n_C=sum_(e in C) 1/(p_i p_j),
    rho=min_(simple cycles C of length >=3) l_C^2/n_C.

No cycle of length two occurs because a nonzero net current cannot point in
both directions on the same undirected edge. Since L is linear on the
current's fixed sign pattern, j/L is a convex combination of unit-cycle
currents divided by their l_C. Convexity of the squared weighted norm N
therefore gives

    N <= L^2/rho.

Combining with (8) proves the more precise inequality

    sigma >= 4rho ||K||_F^2/T.                              (9)

To get a closed form, write a_i=p_min/p_i in (0,1]. On any simple cycle,

    rho_C/p_min = [sum_(ij in C) sqrt((a_i+a_j)/2)]^2
                         /sum_(ij in C) a_i a_j
                 >= [sum_(i in C) a_i]^2/sum_(ij in C) a_i a_j
                 >=3.

The first inequality uses sqrt(x)>=x for x in [0,1] and the fact that every
cycle vertex occurs twice in the edge sum. The last is the clique bound
for a cycle: (sum_i a_i)^2>=3sum_edges a_i a_j.

For completeness, the clique bound needs no external theorem. Normalize
sum_i a_i=1. If two positive-mass vertices are nonadjacent, hold their
total mass fixed and move all mass to whichever has the larger weighted
neighbor sum. The edge quadratic is linear in this redistribution and
does not decrease. Repeating reduces positive support to a clique. A simple
cycle has clique size at most three. On a clique of size r<=3 the quadratic
is (1-sum_i a_i^2)/2<=(1-1/r)/2<=1/3. This proves the claim.

Consequently rho>=3p_min and (9) yields

    sigma>=12p_min ||K||_F^2/T.                             (10)

For uniform p=1/n, rho_C=|C|/n, so rho=3/n when all edges are allowed.
The constant 12/(nT) is optimal for the entropy-to-skew inequality among
uniform stationary generators: approach equilibrium on an isolated
three-state cycle, with other states isolated or coupled by arbitrarily
weak reversible edges. This does NOT assert sharpness of the final bound
(1), which also used negative-log and branch estimates.

## 7. Correctness and originality are separate

Established sources used in the derivation:

* Jia (2016), A solution to the reversible embedding problem for finite
  Markov chains. Reversible embedding is unique and characterized by the
  principal logarithm being a rate matrix. https://arxiv.org/abs/1605.03502

* Kolchinsky, Ohga, Ito (2024), Thermodynamic bound on spectral perturbations,
  with applications to oscillations and relaxation dynamics, Physical
  Review Research 6, 013082. Their Appendix C.1 supplies (7) and a stronger
  atanh inequality. https://arxiv.org/html/2304.01714v4

* Bauer, Seifert, van der Meer, Stroboscopic measurements in Markov networks:
  Exact generator reconstruction vs. thermodynamic inference.
  https://arxiv.org/html/2412.15642v2
  Section 3.3 enumerates logarithms in the nondegenerate case and explicitly
  notes continuous families in degenerate cases. In Section 4.1 the
  estimator is formally set to zero when observed eigenvalues are degenerate.
  The present bound handles a special but consequential degenerate case.

* Shiraishi (September 2026), Second largest eigenvalue does not bound
  stationary entropy production. https://arxiv.org/html/2609.34352v1
  This disproves proposed bounds using only the second generator eigenvalue.
  Our dependence on the full observation determinant and stationary p_min
  is essential; there is no conflict with that counterexample.

The finite-generator logarithm machinery and the entropy-to-skew relation
are not novel. The specific combination (4)-(5) with observation-only
constants, and the circulation refinement above, have not been located in
the sources checked. This is a scoped originality assessment, not a claim
of an exhaustive literature search or a certified first discovery.

## 8. Independent audit of the root agent's hidden-state extension

Let a finite equilibrium CTMC with positive stationary measure mu have the
symmetric positive definite lag operator M=exp(t A), A self-adjoint in the
weighted representation. A deterministic partition into observed states
induces an isometry V of normalized indicator functions. Define

    R=V^* M V, Z=V^* M^2 V,
    Delta=Z-R^2, a=lambda_min(R)>0.

The letter T used above for total exit rate is deliberately not used here.
An orthogonal block decomposition relative to range V writes

    M=[[R,B^*],[B,C]],   Delta=B^*B>=0.

For 0<alpha<1, the root agent's proposed estimate is correct:

    0 <= R^alpha - V^* M^alpha V,
    ||R^alpha - V^* M^alpha V||_op
       <= (1-alpha) a^(alpha-2) ||Delta||_op.               (11)

Proof: M>0 implies C-BR^(-1)B^*>=0. The lower Schur complement of M+sI,

    C+sI-B(R+sI)^(-1)B^*,

is at least sI. The block inverse formula makes

    V^*(M+sI)^(-1)V-(R+sI)^(-1)

positive semidefinite and bounded in norm by

    ||B||^2/[s(a+s)^2] = ||Delta||/[s(a+s)^2].

Use the integral formula

    X^alpha=(sin(pi alpha)/pi) int_0^infty s^(alpha-1)
                                         X(X+sI)^(-1) ds.

The difference is the positive integral of s^alpha times the resolvent
gap. Its norm is bounded by

    (sin(pi alpha)/pi) ||Delta||
           int_0^infty s^(alpha-1)/(a+s)^2 ds
     =(1-alpha)a^(alpha-2)||Delta||.

This verifies the sign, exponent and coefficient in (11).

Because M^alpha is the hidden transition operator at time alpha t, its
compressed observed kernel has entrywise nonnegative entries. Therefore

    max_(i!=j) max(-(R^alpha)_ij,0)
       <= (1-alpha)a^(alpha-2)||Z-R^2||.                   (12)

This gives a quantitative witness against every finite hidden equilibrium
realization from two lag matrices, with no hidden dimension or hidden
spectral-gap parameter. If Z=R^2 exactly, all fractional powers R^alpha
must be entrywise nonnegative, and differentiating at alpha=0 shows that
log R has nonnegative off-diagonal entries.

The qualitative zero-defect rigidity is classical in spirit, and essentially
in Kemeny and Snell, Finite Markov Chains, Section 6.4.8: weak lumpability
of a reversible regular chain implies lumpability. Their proof uses the
same squared-defect identity. Primary scanned source:
https://www.math.pku.edu.cn/teachers/yaoy/Fall2011/Kemeny-Snell_Chapter6.3-4.pdf

The quantitative fractional-power remainder needs its own originality
search against operator Jensen/remainder inequalities. Equation (12) is
an equilibrium-incompatibility witness, NOT by itself a positive numerical
entropy-production bound over arbitrary hidden nonequilibrium models.

The constant in (11) is optimal for general positive-operator compression.
Take M=[[a,b],[b,b^2/a+epsilon]], let epsilon decrease to zero, and then
let b decrease to zero. At epsilon=0, M has rank one and

    (M^alpha)_11=a(a+b^2/a)^(alpha-1).

Hence [a^alpha-(M^alpha)_11]/b^2 tends to
(1-alpha)a^(alpha-2). This proves sharpness for positive operators only;
sharpness within hidden Markov semigroups with deterministic partitions
has not been established here. Qualitative operator Jensen is classical:
Hansen and Pedersen, Jensen's Operator Inequality (2003),
https://arxiv.org/abs/math/0204049. Focused searches did not locate the exact
mean-spectrum/variance norm remainder (11); that absence is not proof of
novelty.

## 9. Scope and limitations

* Bound (1) assumes the specified finite observed state space is the actual
  homogeneous CTMC state space; it does not transfer its constant to larger
  hidden models. A hidden minimum stationary probability may vanish and
  hidden rates may diverge while the observed P stays fixed.
* Equation (12) covers arbitrary finite hidden equilibrium models under a
  deterministic partition, using TWO lag matrices. Pairwise information at
  one lag alone does not justify Z=R^2; coarse observations of an equilibrium
  model need not be Markovian.
* Isometry of V matters. Independent randomized emissions at observation
  times are not automatically covered by a deterministic-partition theorem.
* Time-homogeneity and the known fixed sampling interval matter. A driven
  protocol or non-Markov dynamics belongs to a different inverse problem.
* All states are even under ordinary time reversal. Models with momenta or
  other odd variables require the correct time-reversal involution and can
  invalidate a naive identification of self-adjointness with equilibrium.
* Exact reversibility, positivity of the spectrum and matrix entries must
  be certified with uncertainty margins before applying to measured data.
  Repeated eigenvalues are fragile as exact algebraic conditions. The
  hidden two-lag inequality (12), rather than exact branching alone, is a
  possible route to robustness.

## 10. Independent audit of the four-state calculation

Read and checked /workspace/scratch/8ec4cd763ba5/markov_family/
reconstructed_markov_proof.md, Sections 2--4, independently of its author.
All decisive steps passed: exhaustive real logarithms; all rate signs;
the two monotone feasibility functions and their common minimum; the exact
entropy prefactor including repeated edges; reduction to equal magnitudes
of off-diagonal block entries; reduction to winding one; strict convexity
by the perspective argument; the derivative at zero; and infinite entropy
at the nonprincipal embedding boundary. No decisive gap was found.

For its rational example a=8log2, b=18log2, one has p_i=1/4,
T=44log2 and d^2=(log2)^2/2. The general bound (1) becomes

    sigma >= 3/(44log2) * ((log2)^2/2+8pi^2)
          = 7.790264194785... .

This is below, and therefore consistent with, the separately optimized
minimum 26.1789116783... . The general bound does not purport to recover
the exact family-specific minimum.

## 11. Reproducible targeted checks

Run `python entropy_bound/verify.py`. Results are recorded in
`entropy_bound/verification.json` and use random seed 20261019.

* 800 random stationary generators: no violation of the strengthened
  entropy-to-skew inequality; smallest random sigma/bound ratio 1.2782.
* Uniform almost-equilibrium three-cycle: sigma/bound approaches one,
  reaching 1.0000003333 at the final tested parameter.
* 45 nonprincipal real-generator constructions: branch-identity residual
  at most 4.3e-14; no entropy-bound violation.
* 960 general positive compression examples: no violation of (11), and
  the Jensen gap was positive semidefinite to numerical precision.
* Sharp two-by-two positive compression construction: gap/bound approaches
  one, reaching 0.9999575 at the final tested parameter.

These checks are supplementary. The exact proofs above carry the claims;
floating-point tests do not establish universality or novelty.

