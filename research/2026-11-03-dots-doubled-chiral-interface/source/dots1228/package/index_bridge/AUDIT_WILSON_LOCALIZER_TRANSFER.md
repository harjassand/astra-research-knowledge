# Independent audit: actual Wilson slab / odd localizer bridge

2026-11-03. Verdict: the finite-volume inertia transfer is sound under the final explicit parameter ledger, including M>=pmin. No missing far state, UV integer, dimension factor, or cutoff-boundary error was found. This earns an existence-scale free-fermion index component, not an interacting interface theorem or practical simulator. One general-statement qualification and an explicit sign obligation are below.

## Primary theorem, independently checked

Loring–Schulz-Baldes, *Spectral flow argument localizing an odd index pairing*, arXiv1802.04518v2, theorem on pp.1–2: https://arxiv.org/pdf/1802.04518 . Apply with A=U, g=||A||=1, kappa=1/M, rho=Lambda. Its hypotheses become M>=12||[D,U]|| and Lambda>2M. Multiplying the localizer by M gives gap>=M/2 and half-signature equal to the Fredholm index. D=+sigma.p on the AP torus is invertible with compact resolvent; Lipschitz U preserves its domain and has bounded weak commutator. No eta expansion, smooth asymptotics, or closed-clutch transfer is needed.

## Actual normal chain and high sector

The code's Gamma_i=X tensor sigma_i, Gamma4=Y, Gamma5=Z and forward normal hopping T=-(Z+iY)/2 give near boundary ker(T dagger)=X-positive. Thus its near kinetic operator really is +sigma.sin(k)/a. The two low normal components, not just one eigenvector, must be retained: they are the left/right smallest-singular-vector spaces, each carrying spin and flavor. Their joint space is invariant under the free Hamiltonian, with offdiagonal singular value nu_min/a.

For b<1, perturbing the shift by bI gives nu_2>=1-b. The normalized geometric trial vector has residual <=b^L. Its component outside the smallest singular space is <=b^L/(1-b), so, after phase choice, its distance to that singular vector is <=sqrt(2)b^L/(1-b). This proves the required boundary estimates with ample room in delta=32b_*^(L-1), including L=2 and b=0 by continuity. In particular far boundary norm is at most b^(L-1)+sqrt(2)b^L/(1-b), and near amplitude differs from one by at most b^2+sqrt(2)b^L/(1-b).

All three high-momentum inequalities are valid: sum sin^2(k_i)>=b for b<=1; >=2b-b^2>=3/4 for 1<=b<=3/2; and nu_min>=b-1>=1/2 for b>=3/2. Together with excluded low-momentum nu>=1-b these give g_H>=.4 Lambda under a Lambda<=1/8. The high block stays gapped along tV and its doubled free signature is zero. This is the needed UV control, not merely convergence of low eigenvalues.

## Schur and the far boundary

Finite-dimensional inertia additivity applies without a spectral approximation: H is congruent to H_Q direct-summed with its exact Schur complement. The correction bound M^2/(g_H-M) is valid. The map from a normalized far low vector to the physical massed face has norm <=delta, uniformly over arbitrary superpositions of low momentum, because the Fourier transform diagonalizes its boundary-amplitude multiplier. Thus no number-of-modes factor occurs. Every Schur term with a far leg carries delta; the displayed E_far is conservative.

The free far kinetic gap is not literally pmin: it is >=(2/pi)pmin (and much closer in this parameter window). Its signature is zero. The displayed pmin/8 error budget is nevertheless safe.

**Qualification:** E_near<M/8 and E_far<pmin/8 alone, for arbitrary M, do not imply stability of the near-plus-far direct sum. One also needs E_far<3M/8 (with strict margin), e.g. E_far<min(pmin/8,3M/16). The final ledger's M>=pmin supplies this automatically and should be imposed from the start of the theorem statement.

With that condition the low Schur gap is at least min(3M/8,(2/pi)pmin)-E_far. Inverse congruence bounds give an actual full-H gap at least the minimum of this and g_H-M, divided by (1+M/(g_H-M))^2. There is no omitted gapless-in-volume face, but neither is there a volume-independent far-face gap.

## Sampling, aliasing, and normal mass factors

Choose cells centered at the sampled sites, with the same AP seam convention for the piecewise-constant embedding E and continuum Fourier embedding J. Restricted to momenta |p|<=Lambda, J dagger E is diagonal, with entries product_i sinc(ap_i/2). Distinct retained momenta are distinct modulo reciprocal-grid momentum because a Lambda<=1/8. Therefore

  ||E-J||^2 = max_p [2-2 product_i sinc(ap_i/2)] <= a^2 Lambda^2/12.

This is an operator-norm bound, not a modewise bound subsequently multiplied by dimension. Comparing multiplication by the sampled field to continuum U costs at most sqrt(3)B0 a (already conservative for centered cells). Consequently the note's 20aLambda allowance is ample. This directly controls aliasing, even when U is only Lipschitz. There is no assumed Fourier-tail oracle and no missing momentum-cutoff boundary term.

The near amplitude multiplier R is a positive contraction after a consistent real singular-vector phase choice. Thus ||R U R-U||<=2||R-I||, establishing the stated mass-profile contribution. The kinetic error a^2 Lambda^3 is conservative.

## Parameters, counts, and scope

For Lambda=1000M and aM<=10^-6, b_*<=5e-7 and b_*/a<=M/2. Hence

  E_far <= [0.5+128+128/399] M (5e-7)^(L-1) <130M(5e-7)^(L-1).

The stated L choice and near-error ledger follow; the delta contribution is tiny already at L=2. Grid dimensions must fit the physical torus (choose a commensurate cubic torus, or explicitly extend estimates to rectangular spacings). Counts are per the actual independent 16-orbital CAR model; they must not be reinterpreted as a redundantly doubled BdG count.

The exact conclusion independently certified here is

  N_negative(H)-dim(H)/2 = -Index(P_+ U P_+ +1-P_+).

There is one localizer, acting on spin times the two-dimensional flavor on each of its two blocks; flavor is not an additional multiplicative copy of an already flavor-valued index. The constant-texture reference is balanced. The existing code's near face is D=+sigma.p. Converting the Fredholm index into +s or -s requires a stated odd Chern-character/Dirac orientation convention. The earlier quaternion audit established that +(24pi^2)^-1 integral tr[(U^-1 dU)^3] is -degree(q) for this U matrix. An eta-derived sign should not silently substitute for this remaining convention calibration. Reversing the root orientation reverses the index.

The conservative >=10^21 sites-per-coarse-cell scale is correctly characterized as existence machinery. Nothing here proves a symmetric interacting gapped interface, removes the untreated far boundary in the thermodynamic limit, or supplies efficient preparation/simulation.
