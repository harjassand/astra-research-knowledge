# Exact obstruction to replacing return histories by a logical Hamiltonian

2026-11-02.

## 1. Projected return propagators are not semigroups

Let P project onto the bare code/vacuum sector and Q=I-P. Define W(t)=P exp(-tH)P, regarded as an operator on ran(P). Then

  W(0)=I_P, W'(0)=-PHP,
  W''(0)=PH^2P=(PHP)^2+PHQHP.

Therefore

  W''(0)-[W'(0)]^2=PHQHP >=0.

If PHQ is nonzero, this differs from the identity required by W(t)=exp(-tK) for a time-independent Hermitian K acting on the logical/vacuum space. Summing closed excursions exactly produces a memory kernel, not automatically a local-in-imaginary-time Hamiltonian. This is already true for one excited mediator and does not depend on topology, sign problems or volume.

A ground-band spectral flow supplies an invariant **dressed** P and hence an exact low-band semigroup. It does not place the extensive finite-temperature excited spectrum into that low band. The thermal numerator cannot be replaced by its ground-band restriction without a separate Gibbs estimate.

## 2. Positive compression and logarithms do not close the bound

At each beta, W_beta=P exp(-beta H)P is positive, so K_beta=-beta^{-1}log W_beta exists on its support. This is a useful definition, but it does not imply quasi-locality, beta-uniform source derivatives, or a small bad-observable insertion. In particular an inverse W_beta can amplify different logical directions by exp(beta delta_L), even if the logical splitting delta_L is exponentially small in distance.

Likewise, scalarity of every spatially small closed Pauli word only controls its completed action. It does not establish factorization of overlapping/interleaved return histories, nor convert their retarded kernel into a Hermitian generator.

## 3. A less demanding sufficient logical interface

Introduce H(h)=H+h B, with B the bad-event projector, and let

  F_beta(h)=-beta^{-1}log Tr exp[-beta H(h)].

Then F'_beta(0)=Tr(B rho_beta). If an exact contour resummation produced

  F_beta(h)=f_beta(h)-beta^{-1}log Tr_L exp[-beta K_beta(h)]

and proved

  |f'_beta(0)|+||K'_beta(0)|| <= epsilon_L,

then p_bad<=epsilon_L uniformly in beta. The derivative of the finite-dimensional pressure is a Gibbs expectation of K'_beta, bounded by its operator norm even when beta||K_beta|| is large. This is weaker than full operator domination of marked versus unmarked partition matrices.

However, merely defining K_beta from a logarithm makes the displayed representation tautological. The **quantitative source derivative** is the unproved content. No such estimate has yet been derived from the actual data excursion gas.

## 4. Ground-stability machinery: precise useful structure and missing transfer

The Bravyi–Hastings–Michalakis construction (arXiv:1001.0344, Sections 3–4) does more than assert a gap: after a quasi-local change of frame it produces interactions individually preserving the bare ground space, plus a system-size-small residual. Local topological consistency can turn short ground-annihilating terms into terms annihilating an enlarged local vacuum projector. This suggests a thermal expansion without spontaneous vacuum bubbles: dressed interactions require an existing local defect.

But the actual paper explicitly retains an error Hamiltonian E from supports beyond the local-topological scale. Its small global norm alone cannot be discarded uniformly for beta->infinity. The decomposition is used there for spectral stability, not a normalized thermal-contour theorem. Even with exact local vacuum annihilation, thermally seeded excitations can propagate and branch; one must prove their time-slice cluster distribution, not just their energy gap. The original native Hamiltonian is moreover not itself a commuting-projector model, so a separate native transfer would be required.

Primary source: https://arxiv.org/html/1001.0344 , notably the block-diagonal hierarchy around Eqs. (4.2)–(4.3), error term discussion, and Eq. (4.29). No finite-temperature claim is attributed to this ground-stability result.

## 5. Sparse-impurity diagnostic is not a new thermal-memory principle

The restricted-trace comparison in SPARSE_TRANSVERSE_IMPURITY_THEOREM.md is valid. However, if total impurity support is correctable, conventional logical cleaning can often choose bare logical representatives avoiding it and commuting exactly with the full perturbed reference. This stronger alternative makes a fixed-island theorem low consequence. It is not promoted as the desired extensive-disorder advance.

## Current honest boundary

The scalar native dynamic-flux and time-point-pin lemmas are constructive progress. An extensive normalized data-excursion theorem remains open. The exact obstruction above rules out the tempting but invalid shortcut 'small closed words are scalar, therefore the large words exponentiate into a logical Hamiltonian.' A successful next step needs either an exact positive enlarged transfer representation with controlled marked insertions, or a genuine operator/source-derivative cluster theorem compatible with the stabilizer syndrome constraints.
