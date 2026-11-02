# Proved scalar dynamic-flux rod lemma

2026-11-02. **Exact scalar auxiliary influence lemma under the previously audited rod representation and KP hypotheses.** This is substantive but does not yet prove generic full-Gibbs memory stability. It replaces the candidate's scalar prescribed-flux gate; arbitrary clock/bath matrix insertions and the normalized data excursion gas remain separate.

## 1. Setup and explicit scope

Take the exact prefix-gauged native clock Hamiltonians H_a(s) of `native_thermal_interactions_20261101/root_rod_audit.md`, with the resonant/heterogeneous activities of `resonant_clock_compiler_20261102/resonant_rod_bound.md`. Prescribe, for each check a, a periodic piecewise-constant function s_a(t) in {+1,-1} on the beta circle. Define

  Z[s] = Tr_clock T exp[-integral_0^beta H_clock(s(t)) dt].

This is a scalar clock trace with prescribed flux; there are no additional clock matrix-unit insertions. The clock overlap signs are exactly the previously audited, flux-independent scalar pair factors. Let

  D_a={t:s_a(t)=-1}, L_a=|D_a|, N_a=number of jumps of s_a.

Each ordinary rod has length ell<beta and time origin u; wraps never visit clock vacuum. Assume the common uniform KP charge a(rod)=a0+b ell and a(wrap)=a0+b beta, with absolute ordinary density rho_a(ell), winding density rho_w,a(ell), and

  J_a,beta = integral_0^beta rho_w,a(ell)dell,
  R_a = integral_0^beta rho_w,a(ell)[exp(a0+b ell)-1]dell,
  E_a = exp(a0) integral_0^beta ell rho_a(ell) exp(b ell)dell.

Then Z[s] is real and strictly positive, and

  | log(Z[s]/Z[+]) + 2 sum_a J_a,beta L_a |
     <= 2 sum_a R_a L_a + 2 sum_a E_a N_a.             (DF)

In particular

  log(Z[s]/Z[+]) <= -2 sum_a (J_a,beta-R_a)L_a
                             + 2 sum_a E_a N_a.

No beta multiplier appears in the endpoint coefficient E_a.

## 2. Exact dynamic rod multiplier

The dressed closing edge has label S_a in either orientation; other individual clock-edge flux labels are identity. A first-return ordinary rod can use the closing edge only at its exit from or entry to vacuum. Consequently:

- A winding rod has different nonzero entry/exit endpoints and uses the closing edge once. Its multiplier is s_a(u) or s_a(u+ell), according to orientation.
- A nonwinding rod using the closing edge twice has multiplier s_a(u)s_a(u+ell).
- A nonwinding rod using it zero times has multiplier 1.
- A wrap never reaches vacuum and cannot traverse the closing edge, so its individual multiplier is 1.

The pair factors depend on clock trajectories but not s. This follows directly from the explicit dressed hop formula, not from assuming a static Fourier potential applies dynamically.

## 3. Positivity, despite signful clock histories

All activities and pair factors are real. The unchanged absolute KP majorant proves nonvanishing of the partition function for every activity multiplier of modulus at most one. Interpolate each dynamic multiplier k_s(rod) by k_z=(1-z)+z k_s, 0<=z<=1. This remains in [-1,1]. The finite-volume gas partition function is real, continuous, and nonzero throughout this interpolation. At z=0 it equals the ordinary positive trace Z[+]. Therefore Z[s]>0 and its real logarithm is the branch obtained by the convergent cluster expansion.

This is not an assertion that arbitrary traces of products of positive operators are positive; positivity here is a consequence of the particular real convergent rod gas.

## 4. Singleton winding term

The two winding orientations have equal internal density. More generally, each orientation's endpoint location is a translation of u, so integration over the time circle gives

  integral_0^beta [s_a(u+c)-1] du = -2 L_a,

for c=0 or ell. Summing singleton winding rods gives exactly -2 J_a,beta L_a. There is no beta-ell factor: the audited rod convention has full circle start measure beta.

## 5. All remaining clusters

For a cluster of rods gamma_i with flux multipliers k_i, the elementary telescoping inequality gives

  |product_i k_i - 1| <= sum_i |k_i-1|,

because |k_i|<=1. Mark a rod paying the right side. The absolute rooted cluster theorem bounds the remaining sum by exp(a(root)); if the singleton is removed, the bound is exp(a(root))-1.

A winding root has |k-1|=2 exactly when its marked endpoint is in D_a. Integrating its start gives 2L_a. Its nonsingleton rooted contribution is therefore at most 2 R_a L_a.

For a nonwinding closing-link backtrack, k differs from 1 only when the endpoint signs differ. Such a rod contains at least one jump on its circular arc. For fixed ell, the start set has measure at most ell N_a, by covering it with the ell-long start interval associated with each jump. Hence its rooted contribution, including its singleton, is bounded by

  2 N_a integral_0^beta ell rho_backtrack,a(ell) exp(a0+b ell)dell
       <= 2 E_a N_a.

Other backtracks and wraps have no individual flux multiplier and never need marking. They remain included as unmarked cluster decorations in the rooted theorem. Summing these bounds proves (DF). Multiple marks overcount only, so no independence or positivity of each history has been assumed.

## 6. Actual resonant constants

With common K, `resonant_rod_bound.md` gives

  E_a <= exp(a0) M1,a(b) <= 8 g^2(K-1)/t^2,

using exp(a0)<=2. The endpoint penalty in (DF) is at most 16 g^2(K-1)/t^2 per syndrome-bit jump.

For the heterogeneous equal-J choice with M=max K_a,

  E_a <= 8 eta^2/M,
  J_a,beta-R_a >= J[1-tail-(exp(32x)-1)],
  tail <= exp[2/9-beta JM/(2eta^2)], x=Dbar eta^2.

Thus for the previously imposed small x and cold beta, J_eff=inf_a(J_a,beta-R_a)>0 is uniformly a fixed fraction of J, while endpoint cost is at most 16 eta^2/M per bit jump. A local data Pauli changes boundedly many syndrome bits, so it incurs a bounded multiplicative endpoint renormalization exp(C eta^2), not exp(C beta J).

## 7. What this closes and does not close

**Closed:** exact native auxiliary response to an arbitrarily switching prescribed flux history has a positive defect-time mass and beta-independent jump cost, including all thermal clock wraps and all signed overlap clusters.

**Not closed:** generic native perturbations contain clock and bath matrix units, and a quantum data history carries nontrivial Pauli/logical amplitudes. Converting (DF) into normalized data contour contact bounds still requires a quantum excursion representation with correct vacuum cancellation and treatment of zero-energy/logical trajectories. One must not divide an absolute numerator path sum by a crude denominator and reintroduce a volume-exponential error.

For a perturbation that is data-only in the dressed frame, the prescribed-flux clock functional is exactly the clock factor along a fixed data history. This special restriction makes (DF) immediately applicable inside that history expansion, but does not by itself solve its normalization or logical-matrix summation.
