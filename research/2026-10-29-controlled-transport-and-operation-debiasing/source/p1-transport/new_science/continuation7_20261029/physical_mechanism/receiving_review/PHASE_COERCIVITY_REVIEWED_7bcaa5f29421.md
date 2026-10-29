# Phase energy supplies an exchange-form bound at zero native rates

**Date:** 2026-10-29. **Status:** proved complementary lemma, not a full action theorem.

Use the model and notation of `ORDINARY_ENTROPY_HYDRODYNAMICS.md` and `WEAK_TILT_PHASE_REPLACEMENT.md`. In particular `V=N^d`,

\[
c_b=\frac{s}{2}(1+\alpha_b(\eta,z)\cos\theta_b),\qquad |\alpha_b|\le1,
\]

and the amplitudes are phase independent and invariant under their own swap. Let

\[
D_{\rm ex}(f)=\frac12\sum_b\int|f^b-f|^2d\mu_N,
\quad D_{\rm vis}(f)=\frac12\sum_b\int c_b|f^b-f|^2d\mu_N,
\quad D_\theta(f)=\sum_b\int|\partial_bf|^2d\mu_N.
\]

## 1. The form comparison

For every form-domain function,

\[
\boxed{D_{\rm ex}(f)\le\frac4sD_{\rm vis}(f)+8D_\theta(f).}
\tag{1}
\]

Consequently,

\[
D_{\rm vis}(f)+\kappa_ND_\theta(f)
\ge\min\{s/4,\kappa_N/8\}\,D_{\rm ex}(f).
\tag{2}
\]

For `kappa_N>=2s`, the constant is `s/4`, independent of volume, nonlocal amplitude dependence, and frozen disorder. This is a bound on the joint form. It does not say that every instantaneous native rate is positive.

### Proof

Fix a bond and put `h=f^b-f`. Periodic integration by parts gives

\[
\int\alpha_b\cos\theta_b|h|^2d\mu_N
=-2\operatorname{Re}\int\alpha_b\sin\theta_b\,\overline h\partial_bh\,d\mu_N.
\]

Write `I_b=int|h|^2`, `J_b=int|partial_bh|^2`, and `W_b=int(1+alpha_b cos theta_b)|h|^2`. Then

\[
I_b\le W_b+2\sqrt{I_bJ_b}
\le W_b+\tfrac12I_b+2J_b,
\]

so

\[
I_b\le\frac4s\int c_b|f^b-f|^2d\mu_N+4J_b.
\tag{3}
\]

The swap commutes with phase differentiation and preserves the reference visible measure. Thus

\[
J_b\le4\int|\partial_bf|^2d\mu_N.
\tag{4}
\]

Sum (3) over bonds and divide by two to obtain (1). Equation (2) follows. The proof permits complex `f`, and it differentiates no amplitude. ∎

## 2. Weak comparison tilts

For `|q_b|<=K/N`, the companion note proves

\[
\operatorname{Re}\langle f,L_N^qf\rangle
\le-N^2[\tfrac12D_{\rm vis}(f)+\kappa_ND_\theta(f)]
+C_KV\|f\|_2^2.
\]

Equation (1) implies

\[
\tfrac12D_{\rm vis}(f)+\kappa_ND_\theta(f)
\ge\min\{s/8,\kappa_N/8\}D_{\rm ex}(f).
\tag{5}
\]

Hence `kappa_N>=s` supplies an exchange-form constant `s/8` under the weak tilted law, up to its fixed `O(V)` numerical-range cost. Reserve part of the phase form first if a simultaneous phase-potential estimate needs it; only the constants change.

## 3. Exact transfer interface for occupation replacement

For any phase-independent potential `U_N(eta)`, (2) yields

\[
\sup_{\|f\|_2=1}
\{\gamma V\langle U_N,|f|^2\rangle+\langle f,L_Nf\rangle\}
\le
\sup_{\|g\|_{L^2(\mu_{N,\eta})}=1}
\{\gamma V\langle U_N,|g|^2\rangle-c_*N^2D_{{\rm ex},\eta}(g)\},
\tag{6}
\]

where `c_*=min{s/4,kappa_N/8}`. For the last step, apply the visible variational bound separately to the possibly unnormalized vector `f(.,theta)` at each fixed phase configuration, and integrate its squared norm. No factorization of the full density is asserted.

The right side is the ordinary symmetric exclusion Feynman–Kac problem at a fixed positive rate once `kappa_N>=2s`. Therefore a standard one-block/two-block superexponential estimate transfers whenever its proof supplies this variational estimate. This includes the occupation-pair replacement needed to replace `(eta_x-eta_{x+e_j})^2` by `2 rho(1-rho)`. The receiving proof must still specify the block observable and order of limits.

Under weak tilts, (5) supplies the same transfer with an added `C_KVT` in the logarithmic moment bound. This fixed cost does not obstruct a superexponential conclusion when the Chernoff parameter is sent to infinity after the block limits. Alternatively use the likelihood `L2` transfer in the companion note. The active phase heat layer supplies an `exp(hV)` initial density bound from arbitrary initial correlations; a bounded occupation potential has a deterministically negligible initial-layer integral.

The classical occupation-pair estimate is Theorem 3.2 of Bertini–De Sole–Gabrielli–Jona-Lasinio–Landim, [Large deviations of the empirical current in interacting particle systems](https://arxiv.org/pdf/math/0512394). Equation (6) is the explicit connection to its ordinary reversible-form proof.

## 4. Scope correction

The sufficient condition `a_0<1` identified in the first two companion notes is convenient but is not necessary for this architecture's occupation Dirichlet comparison. The phase energy itself repairs its endpoint `a_0=1`. This lemma does not remove the common mean, phase independence of amplitudes, actual autonomous phase access, or swap invariance. It does not by itself prove current exponential tightness or a full macroscopic action theorem.

