# Passive planar-cavity equilibrium control: a sensitivity bound

**Result:** increasing the photon-mode count with cavity area can evade
single-mode dilution, but it does not supply useful bulk equilibrium control
in the independent-additive, fixed-metal-mirror model at a micrometre gap.
The obstruction is a bound on the chemical-potential derivative followed by
an oscillator-strength ceiling. At T=300 K and L=5 micrometres,

\[
 \beta|\delta\mu_{B-A}|\le 4.4310\,10^{-13} Z_{AB},               \tag{R}
\]

where the coefficient evaluates the exact series below and
\(Z_{AB}=(m_e/e^2)\sum_{a\in A,B}q_a^2/m_a\) includes **all** electronic and
nuclear charges/masses in both stable species. For every pair satisfying
\(Z_{AB}\le1000\), the bound is below \(4.5\,10^{-10}k_BT\).
No actual species, molecular response, kinetic rate or device was acquired.
This is an equilibrium chemical-potential bound, not a maximum local
activation-barrier or kinetic theorem.

New physical operation: **NOT_ACHIEVED**. Priority: **UNKNOWN**. The internally
derived proof and executed computations are retained; simulations do not
establish physical validity, novelty or mission completion.

## Governing existing operation and provenance

Kotov, Feist, Garcia-Vidal and Shegai, *PRL* **135**, 263601 (24 Dec 2025),
[DOI 10.1103/v79d-tty5](https://doi.org/10.1103/v79d-tty5), already derive
the full multimode, bulk-subtracted Lorentz/Hopfield energy as a Lifshitz
expression. Their calculation establishes nonresonant static screening and
the metallic-mirror zero-frequency cancellation. These belong to prior work.
Their per-molecule energy estimate does not replace the composition derivative
below. [arXiv:2509.05156v2](https://arxiv.org/html/2509.05156v2) supplies the
supplemental Fresnel and material formulas. The final PDF, rendered governing
pages, supplemental HTML, source bytes and hashes are retained in `sources/`.

The previous local `opportunity_collective_cavity` endpoint is a
Tavis-Cummings elimination/ensemble audit; `opportunity_cavity_dynamics`
is a classical nonlinear finite-time path bound. Neither is reused as a
quantum spatial theorem. This seed was locked before reading them.
Current archive entrypoint was read at
`afc382b341e69ccb7af08d1cdb6efb5744ae71f9`; initial supplied pin was
`728fca98c6a28bb290cb78a07df7de91f483ad5a`. Selective current chemistry,
Casimir and thermodynamic-control routes supplied no governing result used
here. This does not claim corpus-wide absence.

## Exact contract and observable

The planar gap L, area A, temperature T>0 and total convertible-site density
n=N/(AL)>0 are fixed. Fraction f is in stable species B, the rest in A.
The homogeneous, local, scalar passive gap permittivity satisfies
\(\epsilon(i\xi;f)\ge1\), with finite static value. Two fixed passive,
nonmagnetic dielectric halfspaces have scalar
\(\epsilon_b(i\xi)\ge1\); metallic limits are allowed. Changing f does not
change the mirror constitutive functions, gap, host, temperature, external
charge, pump or mechanical pressure constraint. Spatial nonlocality, phase
transitions, adsorption and omitted local-field corrections are excluded.

The established interplate free energy is

\[
 \mathcal F/A=\frac{k_BT}{2\pi}\sum_{j=0}^\infty{}'
  \int_0^\infty q\,dq\sum_{\lambda=s,p}
   \log(1-r_{1\lambda}r_{2\lambda}e^{-2\kappa L}),                \tag{1}
\]

where \(\xi_j=2\pi jk_BT/\hbar\),
\(\kappa=(q^2+\epsilon\xi_j^2/c^2)^{1/2}\),
\(\kappa_b=(q^2+\epsilon_b\xi_j^2/c^2)^{1/2}\), and

\[
 r_{bs}=\frac{\kappa-\kappa_b}{\kappa+\kappa_b},\qquad
 r_{bp}=\frac{\epsilon_b\kappa-\epsilon\kappa_b}
                 {\epsilon_b\kappa+\epsilon\kappa_b}.           \tag{2}
\]

Converting one site gives df=1/(nAL), so the interplate contribution to the
one-for-one chemical-potential difference is

\[
 \delta\mu_{B-A}=\frac1{nL}\partial_f(\mathcal F/A).              \tag{3}
\]

Increasing area cancels from this quantity. Bulk reference contributions
are subtracted in (1). Single-interface self energies, adsorption, the
largest tagged-molecule shift and kinetic rates are not bounded. A small
mean energy does not control an exponential average of local rates.

## Proof of the Fresnel-response bound

For fixed q,xi>0 put theta=log epsilon and
\(v=\partial_\theta\log\kappa\in[0,1/2]\). With mirror response fixed,

\[
 \partial_\theta r_{bs}=(1-r_{bs}^2)v/2,\qquad
 \partial_\theta r_{bp}=(1-r_{bp}^2)(v-1)/2.                    \tag{4}
\]

Their magnitudes are bounded by (1-r^2)/4 for s and (1-r^2)/2 for p.
For R=r1*r2 and a=abs(r1),b=abs(r2), the numerator in the product
derivative is (a+b)(1-ab), and a+b<=2. Hence

\[
 |\partial_\theta R_s|\le(1-|R_s|)/2,\qquad
 |\partial_\theta R_p|\le1-|R_p|.                              \tag{5}
\]

Writing u=exp(-2 kappa L), the denominator obeys 1-Ru>=1-abs(R)u.
The reflection part of abs(partial_theta log(1-Ru)) is therefore at most
u/2 for s and u for p. Each propagation part is at most
\(L\kappa/(e^{2\kappa L}-1)\). Summing and applying the triangle inequality,

\[
 \left|\partial_\theta\sum_\lambda\log(1-R_\lambda e^{-2\kappa L})\right|
 \le\tfrac32e^{-z}+\frac{z}{e^z-1},\qquad z=2L\kappa.           \tag{6}
\]

This includes dissimilar mirrors, either sign of R and the changing Fresnel
coefficients. The factor 1-abs(R) in (5) controls the apparent denominator
singularity near perfect reflection. No linewidth or detuning is omitted.

Let \(C_j=|\partial_f\epsilon(i\xi_j)|/\epsilon(i\xi_j)\). The envelope
in (6) decreases with z. Since epsilon>=1 it can be evaluated at
\(z_0=2L(q^2+\xi_j^2/c^2)^{1/2}\), where
\(q\,dq=z_0\,dz_0/(4L^2)\). Define

\[
 \tau=4\pi Lk_BT/(\hbar c),\qquad
 A(t)=\tfrac32(t+1)e^{-t}+\int_t^\infty\frac{x^2\,dx}{e^x-1}.    \tag{7}
\]

Equations (1),(3),(6) give

\[
 \beta|\delta\mu_{B-A}|\le\frac1{8\pi nL^3}
          \sum_{j=0}^\infty{}' C_j A(j\tau).                   \tag{8}
\]

The same summable envelope justifies differentiating the sum/integral, for
example if C_j<=C. At j=0, fixed Drude halfspaces have kappa=q, r_s=0,
r_p=1, independent of finite static gap epsilon. PEC mirrors have r_s=-1,
r_p=1, also independent. **The zero-frequency chemical derivative is zero.**
Consequently,

\[
 \boxed{\beta|\delta\mu_{B-A}|\le\frac1{8\pi nL^3}
            \sum_{j=1}^\infty C_j A(j\tau).}                   \tag{9}
\]

A conducting gap or a reaction-dependent mirror/charge boundary changes
this contract. A nonzero-frequency polarizability bound must not be applied
to j=0 before establishing its cancellation.

For orientation, a uniform C gives the zero-temperature bound

\[
 |\delta\mu_{B-A}|\le\frac{C\hbar c}{nL^4}
    \left(\frac3{32\pi^2}+\frac{\pi^2}{480}\right).             \tag{10}
\]

Its coefficient is 0.0300605368021, since integral A(t)dt=3+pi^4/15.
This is a conservative upper bound, not the actual nonretarded scaling of
a fixed Drude material. At 300 K and L=5 micrometres, (9) gives
\(\beta|\delta\mu|\le0.001060549664 C/(nL^3)\). A thermodynamic bias of
\(k_BT\log10\) therefore requires \(C/n\ge2.7139\,10^{-13}\rm\,m^3\).
This necessary response-volume condition does not supply a physical C.

## F-sum corollary: a density-free ceiling including soft modes

Make the additional independent-additive response assumption

\[
 \epsilon(i\xi;f)=\epsilon_h(i\xi)+
       n[(1-f)a_A(i\xi)+fa_B(i\xi)],\qquad a_s=\alpha_s/\epsilon_0. \tag{11}
\]

The host is fixed. Each species is a stable passive molecule with full
nonrelativistic canonical kinetic energy and a coordinate-dependent
potential. Molecular interactions that invalidate (11) are excluded.
Arbitrary internal potentials and soft modes are allowed if passive linear
response exists. For one Cartesian dipole component d_s=sum(q_a x_a),
thermal Kubo spectral positivity and the f-sum rule give a nonnegative
measure d_sigma_s for the response at xi>0 such that

\[
 a_s(i\xi)=\int_0^\infty\frac{d\sigma_s(\omega)}{\omega^2+\xi^2},\qquad
 \int d\sigma_s=
 \frac{\langle[d_s,[H_s,d_s]]\rangle}{\epsilon_0\hbar^2}
 =S_s:=\frac1{\epsilon_0}\sum_{a\in s}\frac{q_a^2}{m_a}.         \tag{12}
\]

For continuous absorption, d_sigma_s=(2/(pi epsilon0))*omega*
Im(alpha_s(omega))*d_omega; delta lines are allowed. The double commutator
follows from canonical position/momentum commutation. All electronic and
nuclear charges/masses enter; using only a convenient IR line would not
prove this bound. A truncated effective Hamiltonian needs its own valid
sum rule. Standard ancestry is explicit in
[Savasta, Di Stefano and Nori (2020)](https://arxiv.org/html/2002.02139v2).
Only positive imaginary frequencies are needed here. A strictly static
diagonal/Curie contribution, if present, has already dropped out of the
metal-mirror chemical derivative before (12) is used.

For xi>0, 0<=a_s(i xi)<=S_s/xi^2. Thus
\(C_j/n\le a_A(i\xi_j)+a_B(i\xi_j)\le(S_A+S_B)/\xi_j^2\), using
epsilon>=1 and (11). Substitution into (9) proves

\[
 \boxed{\beta|\delta\mu_{B-A}|\le
    \frac{S_A+S_B}{8\pi L^3\xi_1^2}
         \sum_{j=1}^\infty\frac{A(j\tau)}{j^2}.}                \tag{13}
\]

TRK and Lifshitz theory are standard. The work here is their explicit
composition-derivative bridge, not a claim to invent them or the prior
nonresonance conclusion. Priority for (9) or (13) is unestablished.

At 300 K, \(e^2/(m_e\epsilon_0\xi_1^2)=5.2259658952\,10^{-26}\rm\,m^3\).
Approximate coefficients multiplying Z_AB in (13) are:

| Gap | Bound on beta abs(delta mu), per unit Z_AB |
|---|---:|
| 100 nm | 1.231168423e-5 |
| 1 micrometre | 5.604514719e-9 |
| 5 micrometres | 4.430980874e-13 |
| 10 micrometres | 4.890425276e-17 |

At 5 micrometres a factor-ten one-for-one equilibrium quotient change would
require Z_AB at least about 5.1966e12. Attaining that condition is not
asserted. Softening internal oscillators, adding modes, increasing ensemble
area or narrowing passive resonances cannot evade (13) while its assumptions
continue to hold.

## Computation, ordinary alternative and costs

`python3 calculate.py` writes `results.json`; it needs numpy and mpmath.
It evaluates the full positive-Matsubara Fresnel derivative in 18 declared
Lorentz/Drude cases. The source form is Kotov et al Eq. 1 and SI Eq. 18.
Au parameters are omega_p=8.9 eV, gamma_D=0.0357 eV. Water uses
epsilon_D=77.46, tau=11800 fs, f=0.843, omega_0=18.4 eV, gamma_0=13.5 eV.
Declared variations are Au halfspaces, a lossless added oscillator, static
susceptibilities 0.04, 1 and 4, and bare resonant gaps 100 nm or 5 micrometres.
These are model scans, not measured molecules or reproductions of the
source's 30-nm-film figures.

The 20,000 pointwise samples include dissimilar mirrors, dielectric matching
and either sign of R. Maximum derivative/envelope ratio: 0.9969566. All
18 integrated cases obey (9) with C=1. One analytic derivative agrees with
central free-energy differences to relative 7.24e-8; quadrature/cutoff
refinement changes it by 7.22e-15. These checks supplement the proof, not
physical or formal verification.

The ordinary Lifshitz alternative receives the same gap, material functions,
response direction, temperature, modes and bulk subtraction; it computes
exactly the same physical effect. Naming its modes polaritons adds no
operation. The source's ordinary static-screening approximation receives
the same host/mirror data. In the selected high-frequency model its derivative
differs by 0.578% at 100 nm, 0.015% at 1 micrometre and 0.100% at
5 micrometres. This is model-specific approximation accuracy, not measured
process advantage.

The corollary's positive series is truncated after argument 65. A tail bound is

\[
 A(t)\le e^{-t}\left[\tfrac32(t+1)+
             \frac{t^2+2t+2}{1-e^{-t}}\right].                 \tag{14}
\]

For J*tau>=65 the weighted tail is at most
K*exp(-(J+1)*tau)/(1-exp(-tau)), with
K=1.5*(tau+1)+(tau^2+2*tau+2)/(1-exp(-65)). This is negligible at displayed
precision. Outputs are approximate floating-point calculations, not interval
certificates. Bound (R) is rounded upward.

An actual application must justify the model and acquire the A/B response
or valid full charge counts, host and mirror responses, geometry, temperature
and composition. None was acquired for an actual reaction. Collective Rabi
splitting does not supply these inputs. The f-sum rejection needs fewer
spectral inputs only after the additive model and charge inventory are justified.

For volume V, mirror area per face is A=V/L. A 1-mL fill at 5 micrometres
needs 0.2 m^2 per face; at 10 nm it needs 100 m^2, a factor 500 increase.
At A=1 cm^2 the capacities are 0.5 microlitre and 1 nanolitre. These are
geometric identities, not manufacturability/throughput evidence. Gap uniformity,
surfaces, mass transport and continuum validity at nanogaps remain unacquired.

Both interpretations charge fabrication/replacement, preparation, loading,
equilibration/thermal control, residence time, unloading, separation/recovery,
cleaning, retuning and measurement. Useful production scales as n*V*y divided
by the whole cycle time, with acquired useful yield y. Times, yields, energy,
lifetime and money costs are UNKNOWN for both. No production or economic
advantage is claimed; the same ordinary surface-dispersion operation and
cost boundary apply to both.

An escape must change a stated premise: nonadditive response, phase/structural
change, conducting gap, altered mirror/charge boundary, local surface mechanism
or nonequilibrium operation. None is constructed or excluded here. This
closes the passive independent-additive multimode bulk equilibrium rescue
at its actual scope. Dynamical/rare-event rates and the broader reaction-control
mission remain UNKNOWN.
