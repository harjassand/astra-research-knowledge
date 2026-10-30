# Protected operations, microscopic sources, and a supplied accepted-resource factory

Working research, 31 October 2026. Previous source files are unchanged.
The new conclusions are mathematical/model results, not experimental
operating regions or a scalable fault-tolerance threshold. The primary
physical continuation is a fixed-rail charge code, a real capacitive
leakage instrument, and a symmetry argument for the entire accepted
operation. A complementary dressed-source theorem repairs an excessive
cost in the preceding star architecture. Ordinary controls and prior
encodings receive the same information and improvements.

## 1. The corrected source cost

The previous spinless-star gate has active Hamiltonian H_a=H_d+W,
P H_d Q=0, and an anti-Hermitian Sylvester generator S satisfying
[S,H_d]=-W. Let ||S||<=s and ||W||=w. The one-conjugation remainder obeys

\[
 e^S H_a e^{-S}=H_d+R_2,
 \qquad \|R_2\|\le s w e^{2s}.
\]

Include a retained source Hamiltonian H_G(t) that commutes with S and
preserves P, with gauge-only action on P. It may include an arbitrary
bath Hamiltonian and need not have bounded total norm. Let B(t) also
preserve P and act gauge-only on P, but not necessarily commute with S.
Let E(t) be the remaining perturbation. Assume the actual and comparison
propagators exist, and the displayed commutators and error actions are
bounded on the qualified domain. No bath derivative, stationary state,
Markov approximation, or initial system/source product state is assumed.

### Dressed-source theorem

The comparison Hamiltonian H_d+H_G(t)+B(t) implements a logical gate
times an arbitrary gauge/source evolution on P. Its difference from
the true gate is bounded by

\[
 \boxed{\epsilon\le 2s+
 {1\over\hbar}\int_0^T
 \left[swe^{2s}+\|[S,B(t)]\|+\|E(t)\|\right]dt.}
\]

Proof: conjugate the whole joint Hamiltonian by e^S. The large H_G is
unchanged. The source correction is exactly

\[
 e^S B e^{-S}-B
 =\int_0^1 e^{uS}[S,B]e^{-uS}du,
\]

so its norm is at most ||[S,B]||. Duhamel bounds the difference of the
two joint propagators; the two endpoint conjugations cost at most 2s.
Tensoring an arbitrary reference changes no operator norm. In particular,
if ||B(t)||<=beta(t), its contribution is at most
2s integral beta(t)dt/hbar. An identity component of a system coupling
can first be absorbed into the bath Hamiltonian to tighten beta.

The commutator form is more useful than a bound on the entire source
interaction. Arbitrarily large commuting terms have zero susceptibility.
For an incident sum B=sum O_j tensor B_j, use
sum ||[S,O_j]|| ||B_j||, with the actual source occupation/domain bounds.
The bath energy itself does not enter. This is a finite-dimensional
dressing argument, extended to a well-defined source by bounded
commutators; it does not assert a global bath spectral gap.

### Star specialization

For the balanced spinless entangler, c(NoA,NoB) is the midpoint of the
overlap-count range for D=sum_i n_iA n_iB. On the entire Fock space,
||D-c||<=1/2, not only on the code. Subtracting this commuting term for
the Sylvester construction gives g=Delta-|delta V| and

\[
 w=\sqrt2|\delta V|/3,\qquad
 s\le2|\delta V|/(3g).
\]

S preserves each No sector and commutes with c, so c may be restored in
H_d even when B changes No. Thus this construction covers bounded
center--bright hopping as a gauge-only source correction too.

At T=3pi hbar/(2|delta V|), the former bound f(r) is replaced by

\[
 \boxed{\epsilon\le f(r)+{2\pi\beta\over\Delta-|\delta V|}
        +{1\over\hbar}\int\|E(t)\|dt,\quad r=|\delta V|/\Delta,}
\]

where beta bounds a time-independent gauge-only remainder after any
harmless identity part is removed. In contrast, a true logical-breaking
term of norm sigma still contributes (3pi/2)sigma/|delta V|. The two
effects must not be merged into a single raw exposure parameter.

Here the explicit conservative intrinsic function is

\[
 f(r)={r\over3(1-r)}
 \left[4+\sqrt2\pi\exp\!\left({4r\over3(1-r)}\right)\right].
\]

The beta in this bound is an operator norm. In the example below the
coefficient multiplying (n_b-I/2) is .02 Delta, so the corresponding
remainder norm is .01 Delta.

The existing finite ramp and local-pulse costs remain. This theorem
does not manufacture a larger physical Delta or make orbital leakage
gauge-only in an encoding whose controls do not act uniformly there.

### Executable quantum-source witness

`dressed_source.py` includes a source spin with

\[
 H_B={\omega\over2}Z_B+
 \beta(n_{bA}-I/2)X_B.
\]

It evolves all 256 active Fock states and both source states, testing all
128 encoded/source input dimensions. At beta=.02 Delta and omega=Delta,
r=.005,.002,.001,.0005 give errors .04156,.04231,.04371,.04424. The raw
exposure estimate grows from9.42 to94.25 while the dressed analytic
bound stays between .07734 and .06427. At omega=0,2Delta,20Delta the
errors are much smaller. These are ordinary floating calculations.

The source penalty is real. `resonant_source.py` tunes
omega=sqrt(Delta²-beta²), so the conditional source splitting is exactly
Delta. In the r->0 interaction-picture averaging limit, the effective
interaction is the spectral pinching of D into degenerate eigenspaces
of Delta K+H_B. A two-dimensional resonant block is, up to a scalar and
basis signs,

\[
 {1\over3}\begin{pmatrix}2&\sqrt2 b\\\sqrt2 b&1\end{pmatrix},
 \qquad b=\beta/\Delta.
\]

Its leakage amplitude after the useful scaled time tau=3pi/2 is

\[
 {2\sqrt2|b|\over\sqrt{1+8b^2}}
 \left|\sin\left({\pi\over4}\sqrt{1+8b^2}\right)\right|
 =2|b|+O(b^3).
\]

The executable pinched-Hamiltonian calculation gives limiting isometry
errors .0019999996,.019999609,.039996872 for b=.001,.01,.02. This is a
resonant obstruction for this gate family, not a universal impossibility
for alternative controls or encodings. It rules out treating arbitrary
gauge-only source fluctuations as costing nothing.

Energy-penalty suppression and Schrieffer--Wolff theory are established.
The useful refinement here is the explicit logical/gauge source
classification, the commutator-sensitive finite-time bound, and its
actual microscopic input. Existing exponential suppression results can
be stronger when their local bath, equilibrium, and perturbative
hypotheses hold; those hypotheses cannot simply be assigned to this
arbitrary-history source. See arXiv:1602.03251 and 1105.0675.

## 2. Microscopic source input, including failures

The complementary derivation in `microscopic/DERIVATION.md` starts from
localized orbitals rather than an abstract bright shift. Three Gaussian
leaf orbitals of width ell on an equilateral radius R have overlap
s=exp[-3R²/(4ell²)]. Symmetric Loewdin orthogonalization gives the exact
projected potential of an axial point source as a No+beta(z) n_b, with

\[
 \beta(z)={3Ks\over(1+2s)(1-s)}
 \left[F_\ell(\sqrt{R^2/4+z^2})-
       F_\ell(\sqrt{R^2+z^2})\right],
 \quad F_\ell(x)={\operatorname{erf}(x/\ell)\over x}.
\]

The harmful coefficient has a z^-3 bound; the common monopole has a
z^-1 tail. A source-orbital matrix retains all f_k†f_l coherences.
Its centered second-quantized norm is one half of the matrix trace norm.
The supplied all-length estimate is independent of reservoir length and
includes these off-diagonal quantum-source terms. Actual infinite
electrostatics still needs its neutralization/screening convention.

A separate complete projected Coulomb calculation includes direct,
exchange and correlated hopping terms. A U(3) algebraic twirl extracts
the genuinely commuting part; it is not an added physical operation.
The remainder is gauge-only on E. At R=2ell and source z=6ell its norm
is .000598998 K/ell in the complete 16-state projected model.

Two decisive failures remain. The same source has an out-of-retained-
dark-orbital coupling .0178859 K/ell, much larger than its point-source
bright coefficient .000898473 K/ell. Also an explicit symmetric barrier
profile at R=2ell gives a gap increment .0739395 lambda but an
out-of-basis control coupling .402866 lambda. Increasing separation
can suppress hopping more strongly than the source correction.

Thus the improved source theorem has a real microscopic input, but no
complete device window follows. A confining spectrum, actual ramps,
loading and orbital-return qualification remain necessary. An off-axis
source displacement .01ell at z=6ell produces a direct logical
coefficient3.92875e-5 K/ell that still pays the full exposure time.

## 3. A different physical capability: fixed rails and a charge code

The stronger alternative uses the established square charge-qubit idea,
with controls and a leakage instrument made explicit. Four sites lie at
(a,0),(0,a),(-a,0),(0,-a). Set

\[
 |0_L\rangle=|13\rangle,\qquad |1_L\rangle=|24\rangle.
\]

In a polarized one-orbital model the full N=2 domain has six charge
configurations. A useful alternative qualification is one electron in
each of disjoint rails (1,2) and (3,4). Then the accessible charge domain
is |13>,|24>,|14>,|23>, while the two rail spins may be completely
unprepared. With spin-independent hopping and density interactions,

\[
 \mathcal H=\mathcal H_{charge}\otimes
 (\mathbb C^2_{spin,1}\otimes\mathbb C^2_{spin,2}),
 \quad H=H_{charge}\otimes I+I\otimes H_{spin,source}(t).
\]

Position-independent spin/source dynamics can remain arbitrary and
factor exactly. This removes spin polarization as a loading requirement
in this narrower rail-charge setting. It does not protect wrong-rail
populations, doublons, spin-orbit coupling, position-dependent magnetic
fields or substantial interrail exchange. The six-state polarized
instrument and the four-charge-state arbitrary-spin model are distinct
qualifications, not interchangeable descriptions.

The square encoding and its Coulomb computation are established
(arXiv:quant-ph/0206075); charge-quadrupole noise protection and composite
controls are also established (arXiv:1605.01797). The new working
combination is full-path error detection, a supplied meter, robust
accepted filtering, and incident bounds for actual allowed source
histories.

### Finite transverse and diagonal gates

Opening only the two rail hoppings gives, after a scalar subtraction,

\[
 H_c=\begin{pmatrix}0&0&-t&-t\\0&0&-t&-t\\
 -t&-t&\Delta&0\\-t&-t&0&\Delta\end{pmatrix},
 \quad \Delta={K\over a}(1/\sqrt2-1/2).
\]

The formula for Delta is for point charges; real profiles/screening use
their acquired integrals. At t=sqrt3 Delta/4 and T=pi hbar/Delta,
the coupled charge doublet returns exactly and the logical gate is
exp(i pi/4)exp(i pi X/4). No weak-tunneling approximation is used. A
signed quadrupole bias nu Q/2, Q=n1+n3-n2-n4, supplies nu Z_L on code.
This quarter-X plus continuous Z supplies arbitrary local control.

Fully symmetric four-edge hopping fails for polarized fermions by
destructive interference. The two open rail links are a real operation.
The finite transverse path has adjacent-state population and a dipole;
endpoint quadrupole neutrality is not full-path immunity.

A finite smooth control is also supplied. With Delta=hbar=1, use a
positive hopping pulse with sin-squared rise and fall of duration .25,
peak .4330442742541, and total duration3.3914207260784. Two ordinary
numerically acquired parameters impose the return and quarter-X phase.
The maximum hopping slew is2.72089742135 in these units. The full
four-state isometry residual is5.38e-12. At dipole strength .01 Delta
and source frequency Delta/hbar, its raw error is .0163472 and its
ideal-check accepted error is .000144391. The corresponding sufficient
accepted bound is .000575087. Thus finite ramps preserve the mechanism
in the fixed-orbital Hamiltonian. The calculation neither fixes Delta
during a real barrier deformation nor qualifies omitted orbitals.

For coaxial squares at separation R,

\[
 J={K\over R}+{K\over\sqrt{R^2+4a^2}}
       -{2K\over\sqrt{R^2+2a^2}},\qquad
 H_{LL}=JZ_AZ_B+\text{scalar}.
\]

This is an exact charge-preserving interaction in the density model.
At R=2a, J=.03705681K/a and a pi/4 ZZ gate takes
21.19444 hbar a/K. Its distant tail is3Ka^4/R^5. The intended coupling
is weakened by quadrupole geometry too.

### A calibrated non-density correction can preserve the gate

With real separable rail orbitals, the spin-independent projected direct
Coulomb terms allowed by the rail symmetry include

\[
 C I+J_{zz}Z_1Z_2+J_x(X_1+X_2)+jX_1X_2.
\]

The common X term renormalizes t. The j term commutes with ZZ and
X1+X2, so it need not be charged as an uncontrolled error if acquired.
For H=Delta/2(I-ZZ)-t_eff(X1+X2)+jXX, an exact quarter-X return is
obtained when

\[
 \Omega=2(\Delta+4j)>|\Delta|,\quad
 t_{eff}={1\over4}\sqrt{4(\Delta+4j)^2-\Delta^2},\quad
 T={\pi\hbar\over\Delta+4j}.
\]

This is an ordinary informed controller repair. Its parameter relation
must be verified for the actual orbitals and controls; it does not
certify the retained-band approximation. Transverse rail separation
provides an independent suppression direction for exchange, unlike
reducing longitudinal overlap while demanding the same hopping.

The projected microscopic calculation uses one common orbital family,
with longitudinal Gaussian width d/4 and transverse/vertical widths d/9,
where d is the rail separation and longitudinal site spacing. All four
orbitals are orthogonalized together, and all Coulomb matrix elements
are retained. In units K/d it gives

\[
 \Delta=.2664002212152,\quad J_x=.000778106523892,
 \quad j=.0000161751967502.
\]

The repaired bare hopping is .1161701396022 K/d, and the quarter gate
takes11.7898920052 hbar d/K. Matching this hopping to the same projected
longitudinal confinement determines d/a_B*=2.842462961, with
a_B*=hbar^2/(mK); hopping and Coulomb energy were not assigned
independently. The corresponding transverse hopping is1.16135e-7 K/d,
the complete wrong-rail Coulomb block norm is3.91938e-9 K/d, and the
calculated quarter-gate transfer-plus-exchange action is2.785e-6.
These are results in the orthogonalized orbital model. The longitudinal
and transverse oscillator scales are21.13 and106.97 times Delta, but
that fact alone is not an interacting continuum leakage certificate.

The nonzero j persists during a charge hold unless its profile is changed
or its evolution is controlled. It therefore cannot be omitted from a
microscopic implementation of the ideal meter in the next section.
Off-diagonal cross-cell Coulomb integrals can also perturb that meter.
This projected local-gate fixture and the density-only circuit example
are separate models; combining their most favorable numbers would be
an invalid device claim.

## 4. The physical meter and its stronger coarse-area use

Use a second square as a meter. Project only the meter into its code.
The actual coaxial capacitance on all six N=2 data configurations is

\[
 H_{DM}=a_0N_D I_M+\chi Q_D Z_M,\qquad \chi=J/2.
\]

Q has values +2,-2 on code and zero on all four adjacent configurations.
The first term is scalar because N_D=2. Prepare the meter in +X and
read it in X after alpha=integral chi dt/hbar. The data Kraus operators
are, without imposing a precise alpha,

\[
 \boxed{M_0=P_{adj}+\cos(2\alpha)P_{code},\qquad
 M_1=-i\sin(2\alpha)Z_LP_{code}.}
\]

The yes outcome is an exact, coherence-preserving code filter at every
scalar area alpha for which it occurs. Track its known Z Pauli frame,
or apply the supplied quadrupole phase. There is zero false acceptance
of adjacent-charge states in this ideal instrument. A no outcome also
preserves all logical coherence inside either sector. The two logical
charge orientations are not revealed.

At alpha=pi/4 this is the earlier exact two-outcome Lüders measurement
up to the known code Pauli. The more general formula means fine gain
calibration is unnecessary for the accepted filter. It does not remove
local-control or detector qualification.

For successive qualified scalar areas alpha_j, the first yes at m has
Kraus operator

\[
 -i\sin(2\alpha_m)\prod_{j<m}\cos(2\alpha_j)Z_LP_{code}.
\]

After M no outcomes the operator is
P_adj+[product_j cos(2alpha_j)]P_code. If each area lies in
[pi/8,3pi/8], the probability that valid code has not been verified is
at most2^-M and expected probe count is at most2. Such an area interval
can be selected from a qualified positive gain box with chi+/chi-<=3.
The box and stability must be acquired from the device; they are not
obtained by naming them. A gain operator correlated with logical
information would not inherit this scalar-probability guarantee.

There is an explicit counterexample. Let logical and gain registers
initially be in (|00>+|11>)/sqrt2, and let their gain-dependent areas be
pi/8 and pi/4. On acceptance, after the known logical Pauli correction,
the reduced logical weights become1/3 and2/3 instead of1/2 and1/2.
Their trace distance is1/6. The same issue occurs for an unobserved
classical gain correlated with the logical input. The scalar-gain
promise is a uniform statement conditioned on the available record;
an operator-valued or hidden correlated gain is a different resource.

Meter preparation and analysis use the actual quarter-X Uq and a finite
Z+=exp(i pi Z/4): preparation Z+ Uq, analysis Uq Z+. A meter starting
in known charge bit1 instead of0 is equally usable; acceptance means
the output bit differs from the input bit. Thus accepted meter outcomes
do not require a physical X reset. Adjacent meter failures need an
actual reset, and the detector and record need renewal.

The meter must be read sufficiently fully to distinguish its code
patterns from its adjacent patterns. The instrument does not diagnose
N=1/3 charge loss, wrong-rail doublons, or arbitrary orbital excitation.

## 5. Why the short gate can be better than a long correction pulse

Let S_c be the charge-only inversion. In the four-state rail model it
is -I on both code states and swaps the two adjacent states with a
minus sign. The rail hopping, quadrupole bias and symmetric finite
ramps commute with S_c. Electric dipole operators anticommute with it.
They annihilate the held-charge code but can cause leakage during X.

For unprepared rail spins, physical spatial inversion also swaps the
spins and is not scalar on the full gauge. The proof uses S_c acting
only on the charge tensor factor. No implementation of S_c is needed;
the factorization of the actual Hamiltonian is what is required.

### Accepted-gate theorem

Let U0(t) be the ideal charge control with U0(T)P=U_LP, and with
[U0(t),S_c]=0 throughout. Include arbitrary retained source dynamics
that act only on spin/gauge/source and commute with charge. Decompose
the remaining error into E_-(t), odd under S_c, and E_+(t). Define

\[
 a={1\over\hbar}\int\|E_-(t)\|dt,\qquad
 b={1\over\hbar}\int\|E_+(t)\|dt.
\]

In the interaction picture of ideal control and source,
P E_-(t) P=0 exactly. The first Dyson term vanishes in PUP. An exact
second-order Duhamel expansion, retaining a unitary propagator in the
remainder, therefore gives

\[
 \boxed{\|P U(T)P-U_LP\|\le a^2/2+b.}
\]

More explicitly, first omit E_+ and write its interaction-picture
propagator as V_-. In units hbar=1 the exact identity is

\[
 V_-(T)-I=-i\int_0^T E_I(t)dt
 -\int_0^Tdt\int_0^t ds\,E_I(t)E_I(s)V_-(s).
\]

Sandwiching with P kills the first integral. Unitarity of V_- bounds
the second by a^2/2 without an exponential Dyson-series estimate.
Restoring E_+ changes the full propagator by at most b by Duhamel.

The flag probability is at most min[1,(a+b)^2], by the ordinary
full-unitary Duhamel bound on leakage amplitude. These bounds apply to
arbitrary source/reference states and time dependence; no quasistatic
approximation or bath bandwidth is used. The accepted quantity is
subnormalized. Conditional normalized-state error must account for
success probability; if the accepted isometry differs by e from an
ideal isometry, e<1, a safe pure-state/reference distance bound is
2e/(1-e). Instrument and detector imperfections add their actual
channel/isometry error, with the appropriate normalization factor.

In this notation U_L includes the comparison gauge/source propagator
when acting on the joint input space: the target is U_logical tensor
V_gauge,source. Its source factor need not be a reset or an identity.
For repeated accepted operations the subnormalized maps telescope;
normalized error estimates must retain the acceptance probability of
the relevant record. No independence of retained-source states follows
from the single-operation bound.

### The complete flagged instrument, including retained memory

For an exact-area endpoint check, keep both the accepted quantum output
and the failure flag. Compare this instrument on code inputs with the
ideal gate that always accepts. Let

\[
 D_\diamond(\mathcal I,\mathcal I_0)
   ={1\over2}\|\mathcal I-\mathcal I_0\|_\diamond,
\]

where the joint source is part of the input/output system and an
arbitrary additional reference is allowed. Then

\[
 \boxed{D_\diamond(\mathcal I,\mathcal I_0)
       \le\min\{1,a^2+b\}.}
\]

Proof: first set b=0. The accepted Kraus map A=PUP differs from its
ideal isometry by e<=a^2/2. Since both A and the ideal isometry are
contractions, their completely positive maps differ in diamond norm
by at most2e<=a^2. The rejected completely positive map has diamond
norm ||P U^dagger Q U P||<=a^2. The two classical outcome blocks thus
have total diamond norm at most2a^2. Restoring the even perturbation
changes the preceding unitary channel by at most2b, and the instrument
cannot increase that distance. The same argument applies to a finite
meter sequence when its accepted single-insertion amplitude vanishes
and its ideal record accepts with certainty; readout and other modeled
imperfections add their actual instrument error.

This supplies a uniform bound for the whole operation, including rare
rejected branches; it is not a conditional-fidelity statement. Legal
adaptive compositions telescope on the joint source and outcome
records. A failed unknown data block still needs an actual recovery or
abort operation, and a reload must return the next input to the
qualified rail-number domain. The bound supplies neither independence
of errors nor an outer fault-tolerant code. Coarse-area checks have
ideal stochastic records; their accepted-map and retry statements
above remain valid, but this always-accept comparison must not be
applied to a single coarse probe without changing its ideal instrument.

With a perfect coarse-area meter, every accepted record applies P
followed by a known Pauli, times a scalar. Hence the code filter retains
the same conditional gate guarantee even without precise meter gain.
The weaker measurement changes expected time and rejection rate, not
the ideal accepted logical operation.

This is an application of error detection to a supplied control path
and meter, not a claim that postselection or quantum error detection is
new. The consequential feature is that the *leading physical dipole
interaction* has exactly the required path property, while the check
is generated by the same capacitance rather than assumed as an oracle.

### Actual finite-meter sequence

For leading electric dipole density errors, the complete modeled
sequence also detects every single error insertion:

1. A data-quarter error reaches adjacent data; the subsequent meter
   rejects that sector.
2. A meter-preparation error reaches adjacent meter; the diagonal hold
   preserves that charge sector and final full-pattern readout rejects it.
3. A meter-analysis error reaches adjacent meter at readout.
4. During held-code diagonal intervals the dipole density operator
   annihilates the ideal charge code.

All ideal transverse pulses have a true endpoint return on both code
and its orthogonal complement. These facts remain valid with arbitrary
retained source operators multiplying the dipole errors. They do not
extend automatically to arbitrary hopping errors late in the check.

`flagged_gate.py` explicitly executes data quarter-X, finite meter
preparation, actual full charge capacitance, data phase correction,
finite meter analysis and charge projection with a retained source spin.
The first derivative of the accepted map is below4e-16 for the tested
source frequencies. For dipole/gap=.01 and source frequency=gap, the
raw data-quarter error is .0163296. An ideal check gives accepted error
.000144147 and flag probability .000266635. Including noisy finite meter
preparation/analysis gives accepted error .000334233 and rejection
probability .000533167. These are joint-source isometry calculations,
not average fidelities or a device noise fit.

An ordinary twelve-window static-dipole-corrected pulse was also
constructed. It is six times longer. At dipole/gap=.01 it reduces raw
error .01633 to .001790, but it need not beat the short checked gate
after measurement and holding costs are paid. At dipole/gap=.1 the
long pulse is slightly worse than the short pulse. Static derivative
cancellation is not a substitute for this arbitrary-history proof.

### Charge holds can be treated exactly, rather than charged perturbatively

There is a stronger exposure statement for this physical density model.
During a transverse pulse, call only the rotating cell active. Put the
dipole/source interactions of every held cell into a comparison
Hamiltonian H_*. During diagonal gates and holds, put all dipole/source
interactions into H_*. These terms may be large, time dependent and
noncommuting on the retained source. They preserve every held charge
pattern and annihilate the ideal code of that cell. The comparison
therefore still performs the same logical factory on its qualified input.

Let E_act contain the dipole interaction on the rotating cell only, and
let

\[
 a_{act}={1\over\hbar}\sum_{\text{transverse pulses}}
       \int\|E_{\text{rotating cell}}(t)\|dt.
\]

Every single E_act insertion is rejected, even with the large held-cell
terms left inside H_*: an adjacent data pattern stays adjacent until
its exact check rejects it; an adjacent meter remains outside its code
through the capacitive hold and is rejected by full-pattern readout.
Source entanglement and arbitrary phases on these leakage paths do not
change those statements. Subsequent ideal quarter pulses return both
charge subspaces exactly. The argument uses this actual circuit, not
independent inversion symmetry of the unrestricted two-cell capacitance.

Consequently the exact-area accepted factory obeys

\[
 \|A-A_0\|\le a_{act}^2/2+b,\qquad
 D_\diamond(\mathcal I,\mathcal I_0)\le\min(1,a_{act}^2+b),
\]

where b charges the remaining error over the full operation. A coherent
description of the charge records makes the entire ideal/check circuit
an isometry. The first accepted Duhamel term is zero by the insertion
argument, the second-order remainder is bounded by a_act^2/2, and the
rejection amplitude is at most a_act. This proves the displayed bounds
without bounding the held dipole strength or the retained bath bandwidth.

This is an exposure law for the useful operation: leading dipole noise
must be small during transverse motion; merely waiting in the qualified
charge code does not enlarge its action. It is not a statement that
all holding is harmless. Even electric terms, position-dependent spin
terms, orbital excitation, unwanted hopping and charge-changing source
operations remain in b or require a larger qualified model. Persistent
jXX during a meter hold violates the pattern-preservation premise unless
it is controlled. The proof does not absorb that correction for free.

The executable `activity_bound.py` checks the entire Bell factory with
active dipole strength .01 Delta, source frequency Delta/hbar, and held
dipole strengths0, .1 and3 Delta. Its six quarter pulses give
a_act=6pi(.01), independently of hold duration. At held strength3 Delta,
the accepted error is .000451767 for coherent time219.7393 hbar a/K.
Adding five extra complete logical periods to each diagonal hold gives
time1491.4054 with accepted error .000454256. Worst rejection probability
remains about .000799636. The first active-error derivative remains below
2.1e-15. The sufficient bound a_act^2/2=.0177653 is conservative but
unchanged by the stronger and longer held noise. The retained source is
never reset. These numerical cases are checks of the theorem's regime,
not a model of arbitrary charge disturbances or a device certificate.

For a single quarter gate with an exact endpoint code projection, an
additional sharpened bound depends on coupling out of the ideal moving
code. If P(t)=U_0(t)P U_0(t)^dagger, P(t)E(t)P(t)=0 and

\[
 a_{path}={1\over\hbar}\int\|E(t)P(t)\|dt,
\]

then accepted error is at most a_path^2/2 and rejection probability at
most a_path^2. Use the exact two-sided Duhamel remainder

\[
 -{1\over\hbar^2}\int_{s<t}
 U_0(T,t)E(t)U(t,s)E(s)U_0(s,0)\,ds\,dt.
\]

Both endpoint factors on code have norm ||E(t)P(t)||; the interior
actual propagator is unitary. For the bare quarter pulse with a bounded
quantum dipole coefficient of magnitude delta, the ideal adjacent-state
amplitude is (sqrt3/2)sin(Delta t/hbar). Thus a_path<=sqrt3|delta|/Delta,
giving accepted error at most1.5(delta/Delta)^2. At delta/Delta=.01 this
is .00015, close to the computed .000144147. This sharper endpoint
projector bound is not assigned to a noisy physical meter without its
own instrument analysis; the full finite-meter/factory statement above
uses a_act and includes all its transverse pulses.

## 6. Conservation controls the full incident interaction

The code is quadrupolar at held endpoints, but the X path has a dipole.
This would give a marginal R^-2 norm tail against independently varying
source monopoles in two dimensions. A real source constraint changes
that conclusion: closed cells have fixed total charge even on their
internal leakage states.

For actual confined particles in two cells of radii a_A,a_B and fixed
numbers N_A,N_B, subtract the known reference one-body fields and use

\[
 f(R+x-y)-f(R+x)-f(R-y)+f(R),\quad f(r)=K/|r|.
\]

The mixed derivative is bounded by 2K|x||y|/(R-a_A-a_B)^3. Thus the
operator norm of the uncertain cross-cell interaction is at most

\[
 \boxed{{2K N_A N_B a_A a_B\over(R-a_A-a_B)^3}.}
\]

This is a continuum multiplication-operator bound, uniform over
arbitrary confined spin/orbital states and correlated source histories.
It does not assume a diagonal occupation model. The known reference
fields must be included in/acquired for the actual control Hamiltonian;
their subtraction is not a physical cancellation supplied for free.
In particular, including a known symmetry-breaking reference field
in an ideal Hamiltonian does not preserve the odd-error theorem: the
actual compensated control path must still have its stated inversion
symmetry. The symmetric central-cell array example below has that
geometric symmetry; a general boundary cell requires its own control.

More generally, if the target response starts at multipole order p_d
and the source *operator fluctuation* starts at p_s, the Coulomb tail
is R^-(p_d+p_s+1). Absolute incident strength on a d-dimensional packed
array is summable when p_d+p_s+1>d. Source order is an operator identity
on every allowed history, not the vanishing of an ensemble average.

For fixed-N source cells, p_s>=1 after subtraction. Even a dipolar
target path then has a summable R^-3 tail in two dimensions. In the
finite occupation-diagonal model, held code has p_d=2; its even
response to arbitrary fixed-N leakage starts at R^-4, and code-code
coupling at R^-5. Those faster exponents do not automatically apply
to full continuum leakage: P dipole P=0 does not imply dipole P=0.

The displayed continuum bound assumes confinement to the stated bounded
regions. The Gaussian orbital fixtures have infinite tails. Applying
the same bound to them requires an additional tail/localization estimate;
one cannot silently replace Gaussian support by a compact region.

The charge-domain qualification is operational. One electron per
isolated rail is preserved by all supplied coherent gates. Loading,
particle loss, detector currents and an open reservoir require their
own incident bounds. A schedule can keep data in its held-charge code
while sources are renewed, but its longer holding time is charged.
For unrestricted orbital excitations or unconfined charge sources,
screening/localization and actual source regularity remain necessary.

### Geometric finite-mode fixture, not an assigned residual

All six N=2 source charge patterns were included in an absolute
incident sum on a square array. At pitch40a and radius64 cells,

\[
 B_{odd}=.0004563500 K/a,\quad
 B_{even}=.00001057754 K/a.
\]

Safe tail enclosures are approximately1.57e-5 and1.84e-8 K/a,
respectively. The quarter-X time is15.16895 hbar a/K. These values give
the ideal-check sufficient accepted bound a²/2+b about1.86e-4 for the
whole fixed-charge incident model. This number excludes meter,
readout, control, orbital, loading and transport errors. It is not a
complete device error or an experimental parameter claim.

The spatial price is explicit: the chosen pitch is forty cell radii.
Increasing distance also weakens intended remote Coulomb gates. A
near coaxial interaction site and a distant parking site must have an
actual routing/holding budget, or an ordinary joint controller must
handle their always-on interaction.

## 7. A concrete computational consumer and all remaining costs

The immediate consumer is an offline entangled-resource factory. Load
fresh fixed-rail charge configurations, prepare two +X logical states
with the supplied quarter-X and Z controls, apply the physical pi/4 ZZ
gate, and verify both charge-code sectors with the supplied meter.
The resulting two-qubit graph state is a maximally entangled resource
with known local Clifford/Pauli frames. No additional purification
oracle is assumed.

The root executable `bell_factory.py` performs this consumer with three
four-charge-state cells and a retained source spin, a128-dimensional
joint system. It includes finite preparation and analysis gates and
the actual near-site Coulomb matrix. The meter is reused in the charge
state produced by its first readout; the source is never reset. The
ideal output has Schmidt coefficients1/sqrt2,1/sqrt2. For source
frequency Delta/hbar, the ordinary numerical results are:

| Dipole strength / Delta | Accepted joint-isometry error | Minimum acceptance probability |
|---:|---:|---:|
| .01 | .000444165698 | .999200391025 |
| .003 | .000039986698 | .999928003169 |

The first derivative of the entire accepted map vanishes algebraically
by the insertion argument; its numerical residual is below2e-15 in the
tested source cases. The norm comparison includes every source input,
not just a thermal or average source state. The accepted errors in the
table are subnormalized; conditional state distances are bounded only
after accounting for acceptance. These figures exclude orbital,
spin-dependent, detector, loading, transport and remote-tail errors.

Every single leading dipole error during a preparation pulse is
rejected by the later check; the ZZ dwell preserves charge patterns.
Finite meter errors are included as in section5. Even errors, physical
loading mistakes and detector mistakes retain their actual bounds.
Failed resource attempts can be discarded and reloaded. A flagged gate
on unknown computational data cannot simply be repeated; it is an
erasure location for a separately supplied outer correction scheme.

Uniform conditional success bounds hold for each allowed retained-source
history, so expected attempts are at most1/p_min without assuming
independent attempts. The accepted error must include success
normalization. For ideal coarse checks, M probes per block give valid
verification probability at least(1-2^-M)^2 for two blocks, and mean
probe count at most2 per valid block. Additional probes consume real
meter operations, sensing time, detector renewal and data holding.

For one checked quarter-X, exact-area near dwell, signed bias amplitude
|nu|, and the phase correction overlapped with the diagonal dwell,
the coherent base time is

\[
 T_{base}=3\pi\hbar/\Delta+\pi\hbar/(2|\nu|)
                   +\pi\hbar/(2J).
\]

At |nu|=Delta and R=2a it is95.4802 hbar a/K. Add the complete
loading/qualification time, ramps, roundtrip motion, sensor integration,
record renewal and any leakage reset. During meter local rotations the
interaction is not zero: use an actual remote-tail action bound or
jointly compile the known conditional Hamiltonians. Coaxial motion
keeps all diagonal phases commuting, so its acquired area can be
included and a positive near wait reaches an allowed filter interval.
Motion forces and orbital return are not supplied by that phase fact.

The executable Bell factory uses six quarter-X pulses, six finite
Z phases, one pi/4 ZZ hold, two capacitive checks, and two full charge
readouts. At the same model parameters its coherent base time is
219.739311525 hbar a/K. It initially loads six electrons, two per cell;
their rail spins are arbitrary under the spin-independent qualification.
The reported simulation uses rectangular transverse pulses. The smooth
quarter pulse above is an independently supplied replacement in the
same fixed-orbital model, not a claim that this entire numerical schedule
already includes physical motion or barrier-ramp deformation. Initial
loading and rail qualification, ramp/transport time, both detector
integration times, record renewal, and resets after rejection must be
added. Residual interactions act during all these intervals.

The coarse filter reduces the precision needed for its capacitive area;
it does not remove local pulse calibration, the spin/orbital domain,
charge isolation, or detector fidelity. At fixed detector time the
new dominant budget may be even electric noise during holding. The
physical resource improvement is therefore conditional, not a claim
of a completed high-fidelity device or automatic fault tolerance.

## 8. Alternative controller retained, with its actual narrower scope

The control branch found a positive smooth-return and gauge-echo
construction for the previous star at fixed total charge2/module:
one dark particle plus one unprepared center/bright gauge particle.
A physical central--bright swap complements that gauge and cancels the
complete second-order logical/gauge Hamiltonian. The bare abrupt echo
still has linear endpoint leakage with coefficient2/3, so cancellation
of virtual phase alone fails.

Smoothly reducing the coupling to a finite floor r²Delta before a
finite smooth gauge swap supplies the missing return. The complementary
proof gives an intrinsic bound at most42r² for r<=.1 in its stated
control model, before source, orbital and incident-array corrections.
Full point-charge capacitance simulations give errors .0016380,
.00037123,.00015235 at r=.04,.02,.01, with durations228.007,463.508,
934.686 hbar/Delta. The required moving geometry and source closure
are resources. Long-held spectator tails must be small over the entire
1/r duration, not merely at the mid-gate pulse. This result is retained
as a stronger ordinary controller on a smaller gauge domain, not used
to claim the full-gauge or active-source promise for free.

## 9. Comparisons and evidence boundary

The square/rail encoding, error detection, Schrieffer--Wolff dressing,
quadrupole protection and composite control each have established
precedents. The working contribution is their physically supplied
combination and the source/path-sensitive guarantees. Singlet-only,
charge-quadrupole and optical alternatives may use the same calibration,
finite-bandwidth optimization, fixed-charge incident law and accepted
instrument improvement wherever their native operations support them.

The star results retain the original unprepared charge gauge but pay
an orbital/control qualification. Fixed rails trade that generality for
direct charge gates, arbitrary rail spins, and a native leakage meter.
Optical heralding retains its genuine loss-to-retry benefit; comparisons
must include local operations, detectors and waiting memory on both sides.

All new code is ordinary executable Python using NumPy/SciPy, except
the exact algebra check in the control branch, which uses rational
arithmetic in Q(sqrt2,sqrt3). Floating residuals are not certified
rounding enclosures. No new threshold or globally novel discovery is
asserted merely because a model check passed.

Primary research consulted:
* Noiseless subsystem control: https://arxiv.org/abs/quant-ph/0004064
* Schrieffer--Wolff: https://arxiv.org/abs/1105.0675
* Energy penalties and local baths: https://arxiv.org/abs/1602.03251
* Bounded-control corrected gates: https://arxiv.org/abs/0906.0525
* Two-electron square qubits: https://arxiv.org/abs/quant-ph/0206075
* Charge quadrupole: https://arxiv.org/abs/1605.01797
* Microscopic barrier versus tilt control: https://arxiv.org/abs/1704.07975
* p-orbital quadrupole: https://arxiv.org/abs/2411.06058
* SAGE: https://arxiv.org/abs/2501.18589
* Optical double heralding: https://arxiv.org/abs/quant-ph/0408040

Root scripts: dressed_source.py, resonant_source.py, flagged_gate.py,
smooth_return.py, coarse_filter.py, bell_factory.py, activity_bound.py. Each writes a
same-stem results JSON. Run from this directory with Python; dependencies
are NumPy and SciPy. The scripts import only their companion local files.
Complementary proofs and executable microscopic/control/alternative
constructions are in their named subdirectories. All prior p2_continuous,
p2_physical_bridge and p2_neutral_blocks files remain unchanged.
