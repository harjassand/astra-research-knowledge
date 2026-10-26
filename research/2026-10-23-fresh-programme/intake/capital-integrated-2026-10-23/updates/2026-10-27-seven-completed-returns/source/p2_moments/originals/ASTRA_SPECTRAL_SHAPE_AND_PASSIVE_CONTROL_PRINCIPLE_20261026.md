# ASTRA foundational physics — spectral shape, passive moments and all-particle control

26 October 2026. Independent constructive continuation in the foundational-physics role. Scope: exact scalar Fano continuum Hamiltonians, positive-energy emitter-side auxiliaries, a separately declared finite-capacity memory and ideal lossless one-photon scattering. Mathematical results are source-local, not claims of historical priority, a Maxwell-compatible apparatus, or a new interaction of nature.

## 1. Scientific question and competing approaches

The previous continuum-impurity capacity work gave a scalar passive spectral construction with an exact quartic-flat scattering resonance, while microscopic Maxwell reconstructions exposed substantial geometric and independent-loss costs. Rather than further tuning a particular side resonator, this attack asks whether the **measured continuum spectral shape itself determines** which passive dispersion corrections can exist. The stronger alternative is directly switching a photon port or using a cavity/dark-state topology rather than conditioning only an emitter frequency; such an alternative can evade scalar moment restrictions but needs a distinct microscopic control interface. We kept both possibilities explicit.

Reference Hamiltonian, in one-particle excitation sector and binding energy units B=1:

    h=H|e><e| + sum_i Omega_i |i><i|
       +sum_i V_i (|e><i|+|i><e|)
       +int omega |omega><omega| domega
       +int sqrt(J(omega)) (|e><omega|+|omega><e|) domega.

All Omega_i>0, |V_i|^2>=0, and the continuum bath has nonnegative one-particle energies. Its complete zero-energy Schur positivity is

    H >= K+sum_i |V_i|^2/Omega_i,   K=int_0^infty J(omega)/omega domega,

when K is finite. This is a complete-square form criterion for the actual one-body Hamiltonian, not a conditioned emitter sector. The real on-shell reactance is

    D(E)=E-H+Sigma(E)+sum_i |V_i|^2/(Omega_i-E),
    Sigma(E)=PV int J(omega)/(omega-E)domega.

For one asymptotic lossless photon port the inclusive one-photon scattering amplitude is

    S(E)=[D(E)-i*pi*J(E)]/[D(E)+i*pi*J(E)].

The sign operation S(E0)=-1 requires D(E0)=0. One obtains fourth-order flat local error S(E)+1=O((E-E0)^4) when D^(j)(E0)=0 for j=0,1,2,3. A passive auxiliary pole at E0 is excluded; it produces an exact Fano zero and cannot serve as the selected -1 resonance.

## 2. General generative passive-moment criterion (proved)

Suppose J(omega)=g*j(omega), and define the real shape self-energy f(E)=Sigma(E)/g. At the chosen E0, assume f has three ordinary real derivatives. Define

    A=-f'(E0),  B=-f''(E0)/2,  C=-f'''(E0)/6.

Introduce for every coupled auxiliary

    s_i=1/(Omega_i-E0), w_i=|V_i|^2/(Omega_i-E0)^2>=0.

Exactly cancelling D',D'',D''' forces

    mu0=sum w_i=g*A-1,
    mu1=sum w_i*s_i=g*B,
    mu2=sum w_i*s_i^2=g*C.                       (2.1)

Thus necessarily mu0>=0, mu2>=0, mu0*mu2>=mu1^2. These follow by positivity and Cauchy–Schwarz and allow any number of auxiliary modes with energies on either side of E0, so long as no auxiliary pole lies at E0.

**Complete constructive converse for upper-side auxiliaries.** Let T=1/(Emax-E0)>0. If

    mu0>0, 0<mu1<T*mu0,
    mu1^2<=mu0*mu2<T*mu0*mu1,                     (2.2)

there is a finite positive-residue auxiliary network with Omega_i>Emax that exactly cancels all three derivatives, using **at most two oscillators**. At determinant equality, set s=mu1/mu0 and w=mu0, giving one oscillator at Omega=E0+1/s. Otherwise choose any sufficiently small 0<s1<mu1/mu0 and define

    s2=(mu2-mu1*s1)/(mu1-mu0*s1),
    w2=(mu1-mu0*s1)/(s2-s1), w1=mu0-w2.

The strict conditions ensure 0<s1<s2<T and w1,w2>0. Put Omega_i=E0+1/s_i, |V_i|^2=w_i/s_i^2. Choosing H=E0+g*f(E0)+sum_i w_i/s_i cancels D(E0) as well. The full positive-energy Schur condition remains a **separate** condition to check; moment solvability alone does not prove it. The result is a finite-order Hausdorff moment theorem specialized to a physical source contract, not a claim to invent moment theory.

If A,B,C are all positive and AC>B^2, cancellation with upper-side positive poles is possible (without a prescribed upper pole range) iff

    g>=C/(AC-B^2).                               (2.3)

For g>the threshold the two-atom recipe can use s1 arbitrarily small; at equality its unique atom is s=mu1/mu0=C/B. If AC<=B^2 and C>0, cancellation is impossible at every g>0. If C<0 then mu2<0 is already impossible. For arbitrary other signs, use the full moment test rather than (2.3).

## 3. Sharp optimality for the hard-band Ohmic source (proved)

Set E0=3/2 and j(omega)=omega on (0,2), zero above. Then

    f(E)=2+E*log[(2-E)/E],
    A=4+log 3, B=16/3, C=160/27,
    mu0=g(4+log3)-1, mu1=16g/3, mu2=160g/27.

A direct exact factorization gives

    mu0*mu2-mu1^2=(32g/27)*[(5log3-4)g-5].

Therefore every positive-residue network cancelling D' through D''' has

    g >= g*=5/(5log3-4)=3.3488240033933843... .

At equality the measure has rank one, s=10/9, all nonzero auxiliary couplings share Omega=12/5, and the unique total squared coupling is 486/[25(5log3-4)]. The previous fourth-order achromat is thus **minimum-coupling**, not just one feasible point.

A complete all-g constructive extension is also explicit. For g>=g*, put

    a=mu1/mu0,
    v=mu2/mu0-a^2=a(10/9-a)>=0,
    s_-=a-sqrt(v), s_+=a+sqrt(v), w_-=w_+=mu0/2.

Indeed 1<a<=10/9 and v=a(10/9-a)<=1/9, so 2/3<s_-<=s_+<13/9<2. These are two positive off-band poles Omega=E0+1/s>2; they collapse at g=g*. The zero-energy Schur margin has the exact Jensen lower bound

    M=H-2g-sum_i |V_i|^2/Omega_i
     =E0[1-g log3+sum_i w_i/(1+E0*s_i)]
     >=6g[((4-log3)g+1)]/[(12+log3)g-1]>0.

This proves the entire two-auxiliary family stays nonnegative in its full Fano one-body space. It does not prove that arbitrarily increasing g is cheap or beneficial; the off-sector memory detuning scales at least linearly with g.

At selected center D=0, changing *only* H by chi gives exact off-sector error

    |S_un(E0)-1|=2*pi*g*E0/sqrt(chi^2+(pi*g*E0)^2).

For error <= epsilon, necessarily

    chi>=pi*g*E0*sqrt(4/epsilon^2-1).

The proven minimum g* therefore yields the **sharp joint lower bound** chi>=3156.1528135 when epsilon=0.01. It is specific to emitter-energy-only conditional control. A memory-controlled auxiliary coupling or different port can evade it; no universal device bound is asserted.

### Quantitative fourth-derivative obstruction without in-band poles

Assume the chosen auxiliary system has no coupled pole in [5/4,7/4], so every s_i=1/(Omega_i-E0) satisfies s_i<=4 (positive poles above 7/4, negative s for modes below 5/4). Integrating the nonnegative polynomial (4-s)(s-x)^2 against the auxiliary moment measure and optimizing x gives

    mu3<=4mu2-(4mu1-mu2)^2/(4mu0-mu1),
    mu3=sum_i w_i*s_i^3.

Since D''''(E0)=24[mu3-704g/81], and the right hand side divided by g is maximized as g->infinity, the whole class obeys

    D''''(E0)/g <= -17.9835695524099... .

This is a strictly quantitative curvature floor for a pole-free fourth-order achromat: extra passive modes cannot make its next Taylor coefficient arbitrarily small while retaining exact cancellation of the first three derivatives, with the specified hard-band source. It strengthens the earlier pole-placement no-go. It is a *local derivative* bound and does not alone certify a global wavepacket error.

## 4. New global shape no-go: exponential Ohmic ultraviolet tails (proved)

Change only the source to

    J(omega)=g*omega*exp(-omega/Lambda), omega>0,

with any g>0, Lambda>0. The exact PV transform is

    f(E)=Lambda-E*exp(-E/Lambda)*Ei(E/Lambda).

Put t=E0/Lambda and q=exp(-t)*Ei(t). Differentiation gives

    A=1+(1-t)q,
    b:=2E0*B=1-t-t(2-t)q,
    c:=6E0^2*C=t^2(3-t)q-(1+2t-t^2).

The source shape determinant is

    AC-B^2 = [2Ac-3b^2]/(12E0^2).

As a polynomial in the real variable q, its numerator has q^2 coefficient

    -t^2[(t-2)^2+2]<0

and discriminant

    4(t^2-10t+1).

**Interior t in [1/8,9].** The discriminant is negative everywhere (convex quadratic, both endpoint values negative); therefore AC-B^2<0 independently of q. If C>=0 the required auxiliary moment determinant

    mu0mu2-mu1^2=g^2(AC-B^2)-gC<0,

and if C<0 then mu2=gC<0. Both contradict passive positivity.

**Low t in (0,1/8].** The elementary series Ei(t)=gamma+log t+sum_{k>=1}t^k/(k k!) and bounds gamma<0.58, log8>2.07, sum_{k>=1}(1/8)^k/(k k!)<1/7 give Ei(1/8)<-64/49. Since exp(1/8)<8/7, q(1/8)<-8/7 and A(1/8)<0. Ei(t)<0 below 1/8 and A'(t)=(1-t)/t-(2-t)q(t)>0 there; hence A(t)<0 throughout. Thus mu0=gA-1<0.

**High t in [9,infinity).** Set R(t)=q(t)-1/(t-1). The exact differential equation q'=1/t-q gives R'=-R+1/[t(t-1)^2]. At t=9, q(9)>1/8 follows from exact rational bounds:

    Ei(9)>S15=sum_{k=1}^{15}9^k/(k*k!)>8110/8,
    exp(9)<8110,

where the exponential bound comes from its first 36 nonnegative series terms plus a rational geometric remainder. Therefore R(9)>0, and the positive forcing in its ODE implies R(t)>0 for all t>=9. Hence A=1-(t-1)q<0, again contradicting mu0>=0.

Together the three arguments cover every t>0. **No finite positive-residue passive auxiliary network with no exact pole at E0 can cancel D',D'',D''' for the exponentially tailed Ohmic source, at any cutoff and coupling strength.** The proof does not require h>=0: the impossibility precedes the physical stability test. It does not rule out active elements, different coupling topology, genuine additional open channels, or all other smooth spectral densities.

## 5. Constructive contrast: C2 compact-edge source and C-infinity robustness (proved)

The preceding failure is not a no-go for spectral smoothness. Define W0(omega)=1 below 19/10, W0=1-r(u) on [19/10,2] with u=10omega-19 and r(u)=10u^3-15u^4+6u^5, and W0=0 above 2. Let J(omega)=4omega W0(omega). This is a nonnegative, C2 upper-edge spectral density, fully equal to 4omega around the operating photon band.

The missing spectral moments are exact rational-plus-log(5/4) expressions:

    Delta_j = int_{19/10}^2 omega*r(10omega-19)/(omega-3/2)^j domega,
    f(E0)=2-(3/2)log3-Delta_1,
    A=4+log3+Delta_2,
    B=16/3+Delta_3,
    C=160/27+Delta_4.

These follow by expanding the polynomial in z=omega-3/2, integrating each z^(k-j) term exactly. Their positive moment determinant at g=4 is enclosed by outward interval arithmetic around 42.13222647822 (>0). The two-atom construction with equal w_i gives

    Omega_1=2.6360244168232523,
    Omega_2=2.169658569804541,
    |V_1|^2=13.664599111833748,
    |V_2|^2=4.748193676095431,
    H=21.18976862396349.

All auxiliaries sit above the bath band. The exact whole-Hamiltonian Schur margin is enclosed around 6.01752580896 (>0).

### Complete lossless wavepacket certificate, not a frequency grid

The polynomial strip integral I(x) with x=E-E0 has an exact algebraic-logarithmic primitive:

    I(x)=Q(x)+P(x)*log[(1/2-x)/(2/5-x)],
    P(z)=(z+3/2)*r(10z-4),
    Q(x)=sum_{k>=1} p_k sum_{j=0}^{k-1}
            x^j * [(1/2)^(k-j)-(2/5)^(k-j)]/(k-j),

where p_k are the rational coefficients of P(z). It determines the exact D(E),D'(E) on [1.26,1.74]. An analytic global second-derivative estimate gives |D''(E)|<490 throughout the interval. At 1200 rational cell centers, 80-digit outward interval arithmetic encloses D(c),D'(c), and Taylor's theorem encloses **all** intermediate E, with |D(E)-D(c)| <= r|D'(c)|+490*r^2/2 for cell radius r. The complete lossless one-photon scattering satisfies

    sup_[1.26,1.74] |S_selected(E)+1|<0.00860377,
    sup_[1.26,1.74] |S_unselected(E)-1|<0.00874636,

with a memory-only emitter detuning chi=5000. The on-shell photon density J(E)=4E remains unmodified within that band. These are full normalized photon-wavepacket operator-norm bounds, including untouched references, for the stated single-port lossless scattering asymptotics. They exclude independent output losses because none is present in the Hamiltonian.

### C-infinity, compact-support realization remains viable without retuning

Extend the monotone envelope W0 as 1 below its taper. Let rho_tau be any nonnegative normalized C-infinity mollifier with support in [-tau,tau] and choose tau=10^-5. Then W_tau=W0*rho_tau is C-infinity, 0<=W_tau<=1, equal to 1 throughout [1.26,1.74], and zero above 2+tau. The BV translation inequality gives

    ||W_tau-W0||_L1 <=tau.

The entire bath self-energy perturbation in the photon operating band is bounded by

    |Delta Sigma(E)|<=4(2+tau)*tau/(0.16-tau) < 0.000500034.

Because S(D) is 2/(pi J(E))-Lipschitz in D, the previous certificate extends with **the same controls** to

    selected error <0.00866694,
    unselected error <0.00874637.

The Schur-margin shift is at most 4tau, leaving margin >6.01748. This is a theorem for all such C-infinity mollified spectral envelopes, not one sampled smoothing function. Thus an ideal mathematical passive broadband operation can be robust to infinitely differentiable smoothing of the spectral edge while retaining all-particle spectral capacity.

### Independent full finite-band Hamiltonian check

An independently implemented ordinary finite-mode Fano matrix (the emitter, both auxiliaries, and Gauss–Legendre bath modes) was diagonalized for 24, 48, 96, 192 and 384 bath modes. The minimum energies were respectively 0.00477284, 0.00122641, 0.00031033, 0.0000780209 and 0.0000195582 in B units, always positive and decreasing toward the genuine soft-continuum threshold. The finite-mesh Schur margin converged to 6.0175258. This is a diagnostic consistency check, not the all-particle proof. Script `astra_smooth_compact_full_fock_audit_20261026.py` and JSON with the same prefix preserve actual values.

## 6. Exact all-particle capacity interface

For any m finite memory qubits with charge K_m=0,...,m, choose H_memory=-K_m+T, T>=0, [T,K_m]=0, with a T=0 state in every charge sector. In memory charge k, set the signal one-body Hamiltonian to the positive calibrated h+chi(m-k)|e><e|. The total excitation-number N Hamiltonian is block diagonal in k, with signal block dGamma_(N-k)(h_k), giving

    H_N >= -min(N,m).

When the memory has k=min(N,m) zero-T reference states and the bath admits arbitrarily soft continuum wave packets, the reverse bound is attained as a dissociation threshold, so

    inf spec H_N=-min(N,m), every finite N.

The memory lower-sector reference preparation, arbitrary-photon-source generation, independent loss, finite-temperature corrections, implementation of chi, and any Maxwell-native interpretation remain **additional resource conditions**. Spectral capacity is not a demonstrated reversible multi-photon loader or a full quantum memory device.

## 7. What has been ruled out, what is now known and next physical target

- **Proved:** An exact source-shape/moment criterion for passive derivative cancellation, with a two-resonator generative converse under strict support inequalities.
- **Proved:** For hard-band Ohmic baths, a sharp minimum coupling, a forced unique auxiliary pole at equality, and a sharp on-shell memory-detuning resource bound within the emitter-only control architecture.
- **Proved:** A quantitative nonzero fourth-jet curvature floor for every pole-free high-order hard-band design.
- **Proved:** Complete impossibility for *all* exponential Ohmic cutoff scales and couplings, without invoking numerical optimizer failure.
- **Proved and interval checked:** C2 compact-taper source, positive passive synthesis, uniform complete wavepacket error and all-particle capacity; a C-infinity mollification family retains the result without retuning.
- **Decisive limits:** The exponential no-go is not a no-go for all smooth baths. Conversely, source-spectrum feasibility does not establish a realizable Maxwell structure, an advantage over conventional cavity gates, a loaded memory, or practical tolerance of independent radiation. The high detuning cost is unavoidable only when memory control acts through one bare emitter frequency.

Natural next research: identify physically local passive band-edge mechanisms with actual port-accessible modes and independent-loss costs; or change control topology to memory-conditioned auxiliary coupling, which could evade the newly sharp detuning floor. The original homogeneous Jacobi-chain all-N capacity-two problem remains distinct and unresolved.

## Ordinary executed records (new workspace only)

- `astra_passive_moment_frontier_20261026.py` and `ASTRA_Passive_Moment_Frontier_20261026.json` — sharp Hankel coupling threshold, explicit positive two-pole family, Jensen margin, quantitative D4 floor, detuning cost and labelled grid diagnostics.
- `astra_exponential_ohmic_passivity_nogo_20261026.py` and `ASTRA_Exponential_Ohmic_NoGo_20261026.json` — exact discriminant, rational endpoint bounds, complete t>0 proof, and independent sample values.
- `astra_smooth_compact_spectral_synthesis_20261026.py` and `ASTRA_Smooth_Compact_Spectral_Synthesis_20261026.json` — exact rational-log missing moments, interval nonnegative Hamiltonian, and photon-grid diagnostics (not claimed as a certificate).
- `astra_smooth_compact_wavepacket_certificate_20261026.py` and `ASTRA_Smooth_Compact_Wavepacket_Certificate_20261026.json` — exact algebraic/log primitive, analytic curvature bound and continuous-band interval certificate.
- `astra_Cinfty_mollified_bath_robustness_20261026.py` and `ASTRA_Cinfty_Mollification_Robustness_20261026.json` — all-C-infinity-mollifier robustness via BV and resolvent estimates.
- `astra_smooth_compact_full_fock_audit_20261026.py` and `ASTRA_Smooth_Compact_Full_Fock_Audit_20261026.json` — independent complete finite-mode Hamiltonian spectra and Schur convergence.

Background antecedents: classical Markov/Hausdorff/Stieltjes moment problems, Foster positive-real reactance synthesis, Fano scattering and Bode–Fano matching. This derivation establishes neither historical novelty nor an experimentally new natural law.
