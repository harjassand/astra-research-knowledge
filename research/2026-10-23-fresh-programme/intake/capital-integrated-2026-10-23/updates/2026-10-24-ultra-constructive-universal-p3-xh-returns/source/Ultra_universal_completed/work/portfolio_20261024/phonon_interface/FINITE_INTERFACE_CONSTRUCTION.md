# Finite thermal ports, counted connectors, and a conventional competing realization

24 October 2026. This is an owned finite-interface construction and comparison,
separate from the proved periodic scalar optimum. The positive operation supplied
here is an explicit passive, finite single-TEM thermal two-port with a rigorous
Bose-weighted conductance bound. It is a conventional transmission-line filter,
not a new phonon mechanism or a manufactured device. The phonon calculations
below do not establish a multi-polarization device advantage.

## 1. What changes when the reservoir interface is included

The governing old normalized fixture is

\[
c=4.259874009292292,\quad K=(c^2-3)/4,\quad M=4-12/c^2,
\quad m_b=1,\quad m_s=M-1,\quad k_s=4m_s/M.
\]

Its infinite periodic, ideal-contact scalar integral at theta=1/2 is
`J*=1.133319342823405`, versus rigid `1.440176577374174`.
The owner's universal-family theorem permits other physical resource values;
neither theorem optimizes a finite specimen's contact scattering matrix.

For a finite device the actual linear-response functional is

\[
G(T)=\frac{k_B\omega_u}{2\pi}\int_0^\infty
g(u)\operatorname{Tr}[t(u)^\dagger t(u)]\,du,
\quad g(u)=(u/\sinh u)^2,
\quad \hbar\omega_u=2k_BT.
\tag{1}
\]

The trace includes every propagating port mode, with reflections and mode
conversion retained. A bulk passband indicator replaces it only under the
declared ideal-contact construction. A loss channel is another thermal
reservoir; it cannot be discarded merely because it reduces measured S21.

The corrected finite point-mass calculation is in
`lag_finite_contacts/FINITE_CONTACTS.md`. A rigid lead has mass M and spring K,
with `M omega^2=2K(1-cos q)`. Its physical endpoint has diagonal `K+Kc`, so

\[
g_s=(K_c-K+Ke^{-iq})^{-1},\qquad \Sigma=K_c^2g_s,
\quad \Gamma=2\operatorname{Im}\Sigma.
\tag{2}
\]

At `Kc=K`, the N=8 side chain has `J=.861707749387`, while the same-contact rigid
chain has `J=1.440176577374` and exactly unit transmission inside its lead band.
The lead cutoff is `c/2`: much of the optical band cannot enter these leads.
For nonmatched positive contact springs both devices have `T(omega)->1` as
omega tends to zero. The original off-match sweep incorrectly retained the
matched lead-end diagonal. Its bytes are preserved in the explicitly named
`*_pre_contact_correction` files; only the corrected sweep is used here.

## 2. Distributed connector inertia is charged

`trunc_connectors/COUNTED_INTERCELL_ROD.md` and `rod_transfer.py` replace each
intercell massless spring by a uniform axial rod. For length a, area A, modulus
E and density rho,

\[
c_L=\sqrt{E/\rho},\quad K=EA/a,\quad m_r=\rho Aa,
\quad m_r/m_b=K a^2/(c_L^2m_b).
\tag{3}
\]

The exact continuum transfer in displacement/axial-force coordinates is

\[
R_a(\omega)=\begin{pmatrix}
\cos z&\sin z/(EA\omega/c_L)\\
-EA(\omega/c_L)\sin z&\cos z
\end{pmatrix},\quad z=\omega a/c_L.
\tag{4}
\]

The side mass gives `m_eff=m_b+k_s m_s/(k_s-m_s omega^2)`. With the force-jump
matrix `P=[[1,0],[-omega^2 m_eff,1]]`, the cell discriminant is
`cos z-omega^2 m_eff sin z/(2EA omega/c_L)`. This includes the complete
longitudinal rod field and its higher bands. A finite N-module specimen uses
N-1 full rods and two half-rods, exactly N rod masses and length Na. Its rigid
control uses the same rods, leads, length, and total mass. The finite-lead
observable comes from `R_(a/2) P [R_a P]^(N-1) R_(a/2)` between bare rods.

The bounded worker's synthetic fixture (`E=125 GPa,rho=5000 kg/m^3`) gives
13.12% suppression with matched periodic leads but only 6.99% with its specified
finite bare-rod contacts. These are numerical model diagnostics, not sourced
material measurements.

For a sourced bulk-constant *scale check*, use the SiN constants employed by
Williams et al., `E=280 GPa,rho=3140 kg/m^3`. With `30nm x 30nm` rods,
`a=300nm`, and `omega_u/(2pi)=1GHz`, equations (3) give
`T=23.996mK`, `K=840N/m`, `m_b=5.61910e-18kg`,
`m_r=.8478e-18kg`, `m_s=12.29367e-18kg`, total `18.76057e-18kg`.
`interface_checks.py` gives N=10 finite bare-rod integrals
`.507107816` versus `.512816537` at 320000 Simpson panels; 80000-panel values
are `.507053067` and `.512816537`. Thus this axial fixture has only about
1.1% suppression with those contacts. The bulk constants do not acquire a
30nm SiN specimen. The internal spring and point bodies remain idealizations;
this calculation does not silently charge them as finite continuum objects.

A physical free beam also has torsion and two flexural gapless branches.
Even the old intrinsic scalar decrement, with three unchanged ideal acoustic
bypasses, reduces the total by only 4.813%. This is not an actual FEM result.
`mark_polarizations/EXTRA_POLARIZATION_GATE.md` retains the full mode ledger.
An experimental baseline smaller than an ideal decrement only invalidates
transplanting that decrement; it says nothing by itself about measurement
resolution.

## 3. A finite distributed electrical realization, with real reservoir ports

The same positive scalar network has a conventional mass-to-capacitance,
spring-to-inverse-inductance realization. We use it to supply an independently
calculable single-channel interface rather than infer a four-mode phonon device.

For angular frequency omega, an exact lossless TEM segment with characteristic
impedance Z and transit time t has ABCD matrix

\[
L(Z,t)=\begin{pmatrix}
\cos\omega t&iZ\sin\omega t\\
i\sin\omega t/Z&\cos\omega t
\end{pmatrix}.
\tag{5}
\]

Its integrated capacitance is t/Z and inductance Zt. An open finite stub with
integrated capacitance Cs has input admittance
`Y=i tan(omega Zs Cs)/Zs`; its integrated inductance is **Zs^2 Cs**, not zero.
Every internal stub resonance is present. For a shunt, use `[[1,0],[Y,1]]`.
For equal positive resistor ports R, a cascade `[[A,B],[C,D]]` has

\[
\mathcal T(\omega)=\frac4{|A+B/R+CR+D|^2}.
\tag{6}
\]

Lossless passivity gives `|S11|^2+T=1`. The code independently checks this,
the scalar closed formula below, and the low-frequency limit. No continuum
line is replaced by a massless inductor or ideal capacitor in the calculation.

For reference, the periodic realization uses normalized `R0=1/sqrt(KM)`,
`ZL=3R0`, `Zs=.1R0`, main line integrated `Lb=1/K`, side line `Ls=1/ks`.
The line capacitances `Lb/ZL^2` and `Ls/ZL^2` are subtracted from the backbone
and side stub budgets. The resulting positive stub capacitances are
`.629031509` and `1.837376765`. Total C per cell is exactly M. Total integrated
L, including both open stubs, is `.622934081`, not just `.620983193`.

At 100mK, choose `R=50ohm`, so `omega_u/(2pi)=4.167323827GHz` and
`Cunit=.214820924606pF`. The complete periodic per-cell resource ledger is

| segment | impedance | integrated C (pF) | integrated L (nH) | delay (ps) |
|---|---:|---:|---:|---:|
| main line | 150ohm | .0796917943 | 1.793065373 | 11.95376915 |
| side series line | 150ohm | .1076982489 | 2.423210600 | 16.15473734 |
| backbone open stub | 5ohm | .1351291303 | .0033782283 | .6756456513 |
| side open stub | 5ohm | .3947069755 | .0098676744 | 1.973534878 |

For N=8, this is `Ctotal=5.737809192pF`, `Ltotal=33.8361750nH`,
main-path delay `95.63015320ps`, summed segment delay `246.0614962ps`.
The finite numerical J is `1.058680426627`. The same-C rigid-node version
gives `1.404297697918`; its total L is smaller, so this is not an equal-L test.
A central-stub conventional layout keeping the same 150ohm main line has
`J=.297057183773` with the same total C and still less aggregate L. Its
different concentration/routing is explicitly allowed only in a global-budget
comparison, not the periodic theorem's per-cell class.

## 4. A simpler conventional finite-port winner and analytic certificate

An even simpler complete scalar-TEM circuit is

```text
50ohm resistor -- matched50ohm finite line -- T -- same line --50ohm resistor
                                             |
                                      finite5ohm open stub
```

Use total matched-throughline delay `95ps`, one open stub `Zs=5ohm`,
`Cs=3.8pF`, and resistor temperatures near `100mK`. Its exact resources are

\[
C_{\rm main}=95\mathrm{ps}/50\Omega=1.9\mathrm{pF},\qquad
L_{\rm main}=50\Omega\,95\mathrm{ps}=4.75\mathrm{nH},
\]
\[
C_{\rm total}=5.7\mathrm{pF},\quad
L_{\rm stub}=25\Omega^2\,3.8\mathrm{pF}=.095\mathrm{nH},\quad
L_{\rm total}=4.845\mathrm{nH}.
\tag{7}
\]

All are below the N=8 periodic network's aggregate C/L and main-delay budgets.
There is one finite stub, not eight independent zero-size junctions. These
budgets do not constrain every lithographic category or every per-cell mass;
this circuit is a conventional competitor for the finite-port problem, not a
counterexample to the periodic optimum.

Matched throughline sections change scattering phases, not |S21|. Therefore

\[
\mathcal T(u)=\left[1+
\left(\frac{R}{2Z_s}\tan(\omega_u Z_s C_s u)\right)^2\right]^{-1}.
\tag{8}
\]

Put `a=R Cs omega_u/2=2.487486445`, and let the first stub pole be
`U=pi/(2 omega_u Zs Cs)=3.157396757`. On `[0,U)`, `tan x>=x`, so
`T<=1/(1+a^2u^2)`. With `g<=1` there and `T<=1` everywhere,

\[
J\le\frac\pi{2a}+\frac{e^{-2U}(2U^2+2U+1)}{(1-e^{-2U})^2}
=.680968384<.682.
\tag{9}
\]

The second term charges **all** higher-frequency pass windows and stub
harmonics; none are discarded to get the bound. Numerical integration gives
`.476087197255`, but the positive result is the analytic upper bound (9).
Since a full single channel has `JQ=pi^2/6=1.644934067`, this supplied model
provides at least 58.5% photonic-conductance suppression relative to a matched
plain line. The conservative upper conductance is about `3.92e-14W/K`, against
`GQ=9.4643e-14W/K` at 100mK. This is a stationary passive scattering operation;
there is no cyclic-work or active-refrigeration claim.

The exact-same-C, exact-same-main-delay variant in `tem_twoport.py` uses
`Cs=3.825206128pF`, `delay=95.63015320ps`, `Ctotal=5.737809192pF`,
`Ltotal=4.877137813nH`. It has numerical `J=.473522549` and analytic
`J<=.678343300`. The rounded values above make an independent concrete contract.

## 5. Finite uniform-segment dimensions and the unclosed junction interface

For a vacuum PEC coax TEM segment with inner radius a and outer conductor's
inner radius b,

\[
C'=2\pi\epsilon_0/\log(b/a),\quad L'=\mu_0\log(b/a)/(2\pi),
\quad Z=\frac{Z_{\rm vac}}{2\pi}\log(b/a),\quad v=c.
\tag{10}
\]

Take `a=10um`. The required b are `10.8697um` (5ohm), `23.0230um` (50ohm),
and `122.036um` (150ohm). The rounded conventional circuit has throughline
length `28.4803mm` and stub length `5.69606mm`. These are finite segment
dimensions, not an acquired superconducting fabrication process. Choosing a
1um outer-shell thickness explicitly counts segment metal volume; it is not
a certified superconducting surface-loss specification.

A conservative uniform-coax non-TEM cutoff bound is

\[
k_c\ge\min\{1/b,\ \pi\sqrt{a/b}/(b-a)\}.
\tag{11}
\]

For azimuthal order m!=0, the angular Rayleigh term gives `m^2/b^2`.
For the nonconstant m=0 Neumann mode, weighted mean zero and ordinary
Poincare give
`int r|f|^2 <= b(b-a)^2/(a pi^2) int r|f'|^2`; the Dirichlet case obeys the
same bound directly. This proves (11), excluding the TEM zero mode. The
lower cutoff frequencies are 4.39THz, 2.07THz, and .383THz for the three
impedances, respectively. This validates the uniform-segment scale separation
from the 0--62.5GHz window used for numerical checks. It proves **no** junction
mode-conversion or finite-device error bound. Higher-mode ports, real surface
impedance, bends, support paths, and finite T-junction geometry still require
their own scattering/noise accounting.

For a practical conditional performance contract, if a completed physical
single-channel device has amplitude error at most delta from (8) on `[0,W]`,
with both amplitudes <=1, then

\[
|J_{\rm physical}-J_{\rm model}|\le 2\delta\int_0^Wg(u)du+
\int_W^\infty g(u)du
\tag{12}
\]

for this channel. Other propagating channels and thermal reservoirs have
separate nonnegative heat budgets; (12) does not set them to zero. Thus a
measured multiport S matrix plus calibrated parasitic heat paths can complete
the contract. A reduction of S21 caused by absorption is not by itself a
closed two-reservoir heat reduction: the absorber emits noise at its own
temperature.

## 6. Source and competing-operation check

The NIST supplied paper was read in its author full source, including methods:
[Spann et al.](https://arxiv.org/html/2301.04769). It experimentally establishes
localized-resonance effects in room-temperature suspended Si/GaN membranes,
with up to 21% conductivity reduction and a coalescence failure control. It
does not supply a cryogenic finite single-channel device or fixed-resource
optimum. Its conductivity observable is distinct from (1).

[Williams et al.](https://arxiv.org/html/1805.09783) supplies the stronger
relevant phonon interface baseline: fabricated four-leg few-mode TES links,
full elastic modes, and measured island-to-bath power. Their three-ring
devices give `G=.51pW/K`, versus `1.36pW/K` for the 3IC straight reference;
their transition temperatures differ slightly. The reported 19% is normalized
power relative to their ballistic comparator, not a universal linear-G ratio.
This achieved multimode conventional filter is preserved as the winner over
any unsupported extrapolation of our scalar number. Its material constants
motivate only the bulk-constant calculation in section 2.

[Partanen et al.](https://arxiv.org/html/1510.03981) supplies a demonstrated
single-photon thermal-port and measurement ancestry: superconducting CPW
between normal-metal islands with NIS thermometry/control, and a full thermal
balance including nonphotonic paths. It demonstrates near-quantum transport;
it does not fabricate our impedance values or certify the filter. Actual
island resistances there are not the exact matched50ohm assumption here.

[Slichter et al.](https://arxiv.org/html/0903.1895) supplies an important
conventional absorptive thermal-filter comparator. Its thermal-emission
calibration is the appropriate extra accounting when loss matters; it is not
a proof that a reactive network's two-terminal heat current follows from S21
without further reservoirs. No priority claim for any filter here is made.

## 7. Reproduction, independent checks, and current decision

Run `python3 tem_twoport.py` and `python3 interface_checks.py` in this folder.
The first evaluates full distributed lines and stubs, resource totals, the
analytic finite-stub bound and coax scale. The second independently compares
the closed scalar transmission with ABCD, checks lossless unitarity, and
replays the sourced-bulk-constant axial scale. The 80k/160k/640k N=8 TEM
quadratures agree for the side J to about 1.2e-8; this is convergence evidence,
not an interval-arithmetic proof of each numerical integral. The strict
positive bound (9) does not depend on those quadratures.

Bounded support receipts were independently inspected: Lag checked finite
contacts and TEM passivity and caught missing open-stub inductance in the
first resource display; Trunc derived distributed rod transfer and checked
the coax cutoff; Mark checked polarization budgets and the finite-stub
inequality; Irregular reopened the full governing experimental comparators.
All earlier wrong-contact and missing-stub-L bytes remain as named
predecessors. The complete mathematical derivation is owned here.

**Decision:** the finite scalar phonon interface is calculated but a whole
elastic-device advantage is **not established**. The concrete positive
competing operation is the finite conventional TEM thermal filter with real
resistor-port contract and bound (9). Full physical implementation, loss/noise
calibration, total heat-leak comparison and fabrication are **unacquired**.
No proof of periodic spectral optimality is promoted to a finite-port optimum,
and no additional hardware capability or novelty is inferred.
