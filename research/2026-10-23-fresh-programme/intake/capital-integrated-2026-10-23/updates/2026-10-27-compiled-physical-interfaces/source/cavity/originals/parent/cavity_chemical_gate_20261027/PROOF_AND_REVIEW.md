# Completed scoped mathematical acceptance and exact chemical-potential gate

Root whole-read the fresh worker's completed296-line RESULT.md and independently
reconstructed its Fresnel derivative bounds, integration prefactors and charge
sum rule. The mathematical result is accepted at the actual scope below. Root
also constructed/executed a separate exact series certificate without importing
worker code. The18 floating model scans remain producer-reported diagnostics;
root does not claim an independent replay/audit of that entire driver.

## Model and exact observable

Use the equilibrium interplate Lifshitz free energy AFTER subtraction of the
same material's unbounded electromagnetic reference. The planar gap L contains
a local, isotropic, nonmagnetic passive dielectric epsilon(i*xi,f)>=1, finite
at zero frequency. Total convertible-site density n is fixed, with fraction f
in stable speciesB and the restA. The two halfspace mirrors have fixed passive
constitutive functions; their Fresnel dependence on gap epsilon is INCLUDED.
For zero-mode cancellation use fixed metallic Drude mirrors (PEC also works).
Define the interplate chemical-potential contrast

    delta_mu=(1/(nL))*partial_f(F_interplate/area).

This is not a tagged molecule's maximum barrier. Single-interface self/adsorption
energies, spatial nonlocality, phase changes, conducting gap, altered mirrors,
omitted local-field effects and kinetic rates lie outside this model. A tenfold
chemical-ACTIVITY-quotient change from this term alone requires
|delta_mu|/(kB*T)>=log10. This does not assert a concentration/rate change in a
critical or nonideal medium. Area cancellation does not supply usable throughput.

The infinite-mode/bulk-subtracted operation is established:
[Kotov et al., PRL135,263601(2025)](https://doi.org/10.1103/v79d-tty5), Eq4 and
finite-temperature extension. Root checked the final publisher-version PDF via
Chalmers. Its static-screening/nonresonance conclusions are prior results.
Priority for the new explicit sensitivity/sum-rule bridge is UNKNOWN.

## Independent reconstruction of the bound

Let kappa=sqrt(q^2+epsilon*xi^2/c^2),x=2L*kappa. At each positive Matsubara
frequency xi_j=2*pi*j*kB*T/hbar, halfspace reflections obey

    |partial_lnepsilon r_TE|<=(1-r_TE^2)/4,
    |partial_lnepsilon r_TM|<=(1-r_TM^2)/2.

Write r=(u-1)/(u+1); |partial_lnepsilon ln u|<=1/2 forTE and<=1 forTM,
while partial_lnu r=(1-r^2)/2. For two-mirror productR,
|partial R|<=2*c_pol*(1-|R|), using
(|r_minus|+|r_plus|)(1-|R|)<=2(1-|R|). This factor controls apparent perfect-
reflection divergence in ln(1-R*exp(-x)); |1-R*exp(-x)|>=1-|R|exp(-x).
Summed reflection derivatives are bounded by(3/2)exp(-x). Since
partial_lnepsilon kappa<=kappa/2, the two propagation terms sum to at most
x/(exp(x)-1). This also covers dissimilar mirrors and negativeR.

Put C_j=|partial_f epsilon(i*xi_j)|/epsilon(i*xi_j). Fixed Drude mirrors have
r_TE=0,r_TM=1 at zero frequency, independent of finite static gap epsilon;
the zero-mode chemical derivative vanishes EXACTLY. Apply the bound only to
j>=1. Use q*dq=x*dx/(4L^2) and epsilon>=1 to get

    beta*|delta_mu| <= 1/(8*pi*nL^3) *sum_(j>=1) C_j*A(j*tau),
    A(t)=(3/2)(t+1)exp(-t)+integral_t^infinity x^2/(exp(x)-1)dx,
    tau=4*pi*L*kB*T/(hbar*c).

A is positive/decreasing. If C_j<=C, use a uniformC. Dielectric mirrors or a
conducting/nonlocal gap need a different zero-mode calculation.

In the NARROWER independent-additive model
epsilon=epsilon_host+n[(1-f)a_A+f*a_B],a_s=alpha_s/epsilon0, passivity gives
C_j/n<=a_A+a_B. For full canonical molecular charges and position-dependent
potentials, [D,[H,D]]=hbar^2*sum_l q_l^2/m_l. Positive-frequency thermal Kubo
weights are nonnegative, so a_s(i*xi)<=S_s/xi^2, with
S_s=sum_l q_l^2/(m_l*epsilon0), including ALL electronic/nuclear charges.
The static diagonal/Curie term, if any, has already canceled with the metal
zero mode. Thus

    beta*|delta_mu| <= S_total/(8*pi*L^3*xi_1^2)
                         *sum_(j>=1) A(j*tau)/j^2.

Arbitrarily soft modes are allowed at positiveT. Truncated effective charge
models, nonadditivity and invalid local-field approximations are not included.
This is a standard sum rule used in a scoped bridge, not a new force theory.

## Root exact numerical certificate

exact_gate.py uses exact SI h,kB,c and rational arithmetic. Alternating series
and Machin's identity prove compact pi bounds. tau and xi1 are rounded DOWN.
A positive Taylor partial sum for exp(tau_lower) supplies an upper bound for
exp(-tau_lower), rounded UP to q_u. For t>=tau_lower,

    integral_t^infinity x^2/(exp(x)-1)dx
      <=exp(-t)*(t^2+2t+2)/(1-q_u).

Geometric moments sum the unweighted envelope. For the j^-2 envelope,
sum q_u^j/j and sum q_u^j/j^2 are bounded by sum q_u^j. MonotoneA permits
the lower tau; all certificate decisions are exact. A positive atanh-series
partial sum supplies a LOWER log10 bound.

At L=5micrometres,T=300K, the retained rational bounds imply

    beta*|delta_mu| <=0.001060685106292*C/(nL^3),
    beta*|delta_mu| <=1.392489440339e-16*S_total.

A tenfold activity-quotient change necessarily requires
C/n>2.71355876420e-13m^3 or S_total>1.65357454519e16m^3/s^2 in the respective
models. These are response REQUIREMENTS, not acquired/sufficient designs.
EXACT_GATE.json stores exact fractions; display decimals are not decision inputs.

For a conservative all-charge example, adopt the very loose empirical constant
enclosures m_e>=9.1e-31kg,epsilon0>=8.85e-12F/m, consistent with the live
[NIST electron-mass](https://physics.nist.gov/cgi-bin/cuu/Value?me) and
[permittivity](https://physics.nist.gov/cgi-bin/cuu/Value?ep0)2022CODATA pages.
With exact SIe these imply e^2/(m_e*epsilon0)<3200m^3/s^2. Hence for
Z_AB=(m_e/e^2)*sum_(chargesA,B)q_l^2/m_l<=1000, root independently certifies
beta*|delta_mu|<4.456e-10. The empirical enclosures are declared premises,
not exact SI definitions. No actual molecular charge inventory is claimed.

The first root version propagated unrounded Machin fractions into high-degree
polynomials: mathematical assertions passed but JSON conversion exceeded
Python's4300-digit limit. failed_unrounded_v1.py preserves it. Compact outward
rounding repaired representation growth while retaining rigorous inequalities.

For gap-volumeV, plate area is V/L before supports/manifolds, residence and
turnover losses. Neither equilibrium bias nor this geometry supplies useful
production. Root accepts the scoped mathematics and independent exact gate;
physical model validity, reaction inputs, rates, useful cycles and practical
advantage remain NOT_ACQUIRED/UNKNOWN. The original mission remains open.
