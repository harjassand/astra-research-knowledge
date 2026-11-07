# Final source and novelty review

Reviewer: machinery. 7 November 2026, Australia/Brisbane.

## Version and verdict

Reviewed `outputs/PHYSICAL_COOLING_THERMAL_SERVICE_RESEARCH_DOSSIER.md`, SHA256
`d7e25afde8da5874136adb99d0dd0ad7fbdb74329dabc7b756124423951e9a7e`.
The hash was checked before and after the reads. No dossier edits were made.
This is the reused machinery researcher's final source/novelty review, not an
independent external mathematical audit or a priority certification.

**PASS at the stated model scope, with the source/convention clarifications
below.** The dossier accurately claims a composite repeatable warm-basin
collision compiler and restricted paid encoded-port service. It does not claim
a new general principle of coherent fault tolerance, thermal computation or
measurement-free correction, historical first priority, a finite recycled
refrigerator, or a matched complete-cost advantage. I found no source-based
objection that invalidates the main compiler. Items 1–3 are small but necessary
for exact source/convention accounting; item 4 is a research-record omission.
The suggested additional comparisons do not commission a new literature round.

## 1. Align the reset energy basis with the collision basis

**Location:** dossier lines 533–540 and its use as a source/reset for Sections 2–4.

The collision convention is explicit: `H_a=Jd|1><1|`, with `|0>` ground and
`B tensor |1><0|` absorbing the lowered DATA energy. This convention is correct:

```
[JU,B]=-Jd B,
[Jd |1><1|,|1><0|]=+Jd |1><0|,
[H_0,V]=0.
```

The reset subsection instead writes `H_A=+(Delta/2)Z`. Under the standard
`Z=|0><0|-|1><1|`, this has `|1>` as ground. As a stand-alone Merkli import it is
fine, but its Gibbs reset is not the cold `|0>`-biased token used elsewhere.
Make the bridge explicit by replacing it with

```
H_A=Delta |1><1|,
equivalently H_A=-(Delta/2)Z up to an additive scalar,
G=X.
```

Alternatively explicitly relabel Merkli's two energy eigenvectors when the
source is connected to the collision module. The checked form factor, positive
gap, FGR condition, simple level-shift spectrum, rates and reset estimate are
unchanged under that basis permutation. This is a convention correction, not a
gap in the fixed-qubit reset theorem or in the collision proof.

I rechecked the partial-isometry convention in dossier lines 76–90:
`B=P_a Pi_(a,-d)`, `B†=P_a Pi_(a,+d)`, `B†B=Pi_(a,-d)` and
`BB†=Pi_(a,+d)` are mutually consistent. The ground full-exchange Kraus pair
`I-Pi_(a,-d), -iB` is correct. The interacting-pair source's marginal is explicitly
distinguished from the uncoupled Gibbs marginal, so there is no false detailed
balance inference from Section 8.

## 2. Retain Wang–Ding's derivative factor in the abbreviated statement

**Location:** dossier lines 752–754.

Theorem S2, equation (S21), of `2512.03457v4` has a leading error term proportional
to

```
t_mix * beta/sigma
 * (||gamma'||_(L1)+||(gamma e^(beta omega))'||_(L1)) log(sigma).
```

The current summary mentions integrability but drops the derivative-norm factor
when describing the bound. Its precision-choice corollary
`sigma=~Theta(beta t_mix/epsilon)` assumes that the sum of those norms is
`O(1)`. State that factor and this condition explicitly. This avoids silently
making the estimate uniform over arbitrary admissible spectral densities.

The other claims in this subsection are supported: fixed sufficiently small
coupling can be independent of target accuracy; Theorem S10 controls mixing
under `Gamma^2=O(lambda_gap)`, sufficiently wide filter and truncation window;
the thermal end-to-end example in Theorem 3 uses `Gamma=O(N^(-1/2))` and
`~O(poly(N)/epsilon^2)` total Hamiltonian evolution time. Its general
fixed-point theorem does not give a repeated arbitrary-logical-input service
or a free size-uniform joint reset. The dossier correctly avoids that transfer.

## 3. Identify Ong et al.'s mixing-time channel

**Location:** dossier lines 738–748.

In equation (24) of `2605.03011v2`,

```
tau_mix(epsilon)=tau_(K_LS,mix)(epsilon),
t_(mix,J)=J^2 tau_(K_LS,mix).
```

The exact Hamiltonian/reset cycle implements the averaged channel `K`; `K_LS`
is its nearby Lindbladian-plus-random-unitary comparison. Equation (25)'s
condition

```
tau_(K_LS,mix)(epsilon/2) ||K-K_LS||_(1->1)<=epsilon/2
```

and Appendix A Lemma 2 give the comparison
`tau_(K,mix)(2epsilon)<=tau_(K_LS,mix)(epsilon/2)` in equation (26).
The present dossier's generic symbol `tau_mix` is not false, but should be
defined this way so it cannot be mistaken for a directly proved mixing time
of the microscopic cycle.

The source theorem/DOI/version, Gaussian randomization, pure reset ancillas,
fixed-point rather than logical-channel target, equation (77) size factors,
rescaled-mixing assumption `t_J=o(J^(-2))` and equation (44) total-time scaling
are otherwise recorded accurately. The failure of those global sampler bounds
to provide this service as a black box is not presented as a failure of the
samplers themselves.

## 4. Add the supporting research-record links

The dossier's existing relative Markdown links all resolve. However it gives
cache hashes without the actual cache paths, and does not link its new frozen
initials, source manifests or final reviews. The supporting files exist.
Add a compact supporting-record list or table, for example:

* `../work/physical-cooling-thermal-service-20261107/initial/principal.md`
* `../work/physical-cooling-thermal-service-20261107/initial/constructor.md`
* `../work/physical-cooling-thermal-service-20261107/initial/auditor.md`
* `../work/physical-cooling-thermal-service-20261107/machinery/initial/machinery.md`
* `../work/physical-cooling-thermal-service-20261107/machinery/sources/SOURCE_MANIFEST.json`
* `../work/physical-cooling-thermal-service-20261107/machinery/sources/FOLLOWUP_SOURCE_MANIFEST.json`
* `../work/physical-cooling-thermal-service-20261107/constructor/sources/COMPILER_SOURCE_MANIFEST.json`
* `../work/physical-cooling-thermal-service-20261107/machinery/followups/RESET_AND_COMPARATOR_AUDIT.md`
* the final version-bound constructive/source reviews.

The frozen machinery initial explicitly records the pre-freeze message timing
limitation: its derivation predates the principal's message, but the written
initial was not frozen before that scientific message arrived. The research
record must not describe all four written initials as fully uncontaminated.
Link and preserve that exact account; do not retroactively alter the initial.
This affects the independence accounting, not the subsequently checked proof.

## 5. Further verified source/convention checks

### Merkli

The fixed qubit import in lines 527–650 retains the correct model: static
coupling to a fresh independent infinite-volume free boson equilibrium
reservoir, positive temperature, the checked isotropic form factor, and
permanent no-return after tracing that reservoir. The four radial derivatives,
infrared/ultraviolet powers, FGR and simple level-shift hypotheses all hold.
The theorem is genuinely uniform in all times; the dossier does not deny that.

The finite-dimensional conversion to diamond norm and the conservative
`4C |lambda|^(1/4)+6exp(-lambda^2 r_beta t/2)` reset estimate are valid. The
positive/negative and real/imaginary decomposition plus the input-dimension-two
amplification bound explain the factor four. The generator-derived
`r_beta=c_hat_beta(Delta)+c_hat_beta(-Delta)>0` avoids the visible sign typo
in source equation (1.37). The boson interaction's unbounded full norm is
explicitly excluded from an automatic DATA local-complete-norm import.
The optional reset is an existence-level constant-accuracy construction;
the text accurately leaves numerical module constants, power and bath reuse
unestablished.

### Coherent thresholds

Han et al.'s theorem numbering and perfect-check/recovery code-capacity scope
are correctly represented. The channel extension is a tensor-product-per-layer
local CPTP noise circuit, not an arbitrary persistent correlated environment.
The comparisons credit its `d=Omega(log n)` strength and do not imply that this
compiler supersedes it. Terhal–Burkard's explicit bath-locality restriction and
Aharonov–Kitaev–Preskill's unrestricted bath Hamiltonian with bounded per-qubit
system-interaction sum are distinguished correctly. Coherent fault-path
methods are credited as established machinery.

### Other physical samplers and autonomous computing

The statements for `2611.03422v1` retain fixed positive temperature, one dimension,
parallel ancillas, accuracy-dependent `alpha^2=c epsilon/n` and expected
Hamiltonian evolution cost `~O(n/epsilon)`. Rouze–Franca–Alhambra's polynomial
inverse-temperature computational model is not mislabelled as a fixed-noise
unknown-input service. The QCA `2601.20818v3` is credited for its proved
discrete-time autonomous universality and common-environment fault scope, while
its continuous-time threshold is correctly described as an outline left open
in that version. The older dissipative-memory and trickle-down predecessors
are credited without promoting effective physical approximations to theorems
at stronger microscopic scope.

### Powered elementary compilation

Barenco et al.'s cached primary text explicitly gives an ancilla-free
`Theta(q^3 4^q)` construction for arbitrary `q`-qubit unitaries through
two-level rotations and Gray-code/multiple-control gates. Thus the dossier's
loose fixed-patch gate-count bound is supported. Dawson–Nielsen Theorem 1 and
Definition 1 require a finite inverse-closed instruction set dense in `SU(d)`;
those library hypotheses are retained. No exact high-body energy-conserving
Hamiltonian is falsely obtained from the driven two-body circuit. The dossier
explicitly makes `U` diagnostic in that representation and charges drive and
source costs. Approximate fixed local synthesis is counted as local error,
rather than a fictitious exponentially accurate global simulator.

## 6. Two useful close primary additions

These are bounded source additions to the existing novelty discussion, not
new scientific premises.

**Elementary thermal operations.** Cite Lostaglio–Alhambra–Perry,
[*Elementary Thermal Operations*, arXiv:1607.00394v3](https://arxiv.org/html/1607.00394v3),
Sections 2 and 3.1, near Section 2 or in Section 12. The two-level thermal
exchange and its Jaynes–Cummings/collision realization are established physical
machinery. The dossier says this in general, but a direct primary citation would
make the attribution concrete. The local-code sweep, contraction and joint
fault closure remain the stated composite contribution.

**Shtanko–Sharma.** The inspected primary version is
[*Complexity of Local Quantum Circuits under Nonunital Noise*,
arXiv:2411.04819v1](https://arxiv.org/abs/2411.04819v1), cached at the workspace-relative
`work/physical-cooling-thermal-service-20261107/constructor/sources/shtanko-sharma-2411.04819v1.{pdf,txt}`.
Theorem 1 (formal version in Section 2.4) considers identical contracting
single-qubit CPTP noise after the geometrically local unitary layers, including
idle noise. With fixed-point polarization `eta>0`, sufficiently small strength
`kappa` permits arbitrary-depth computation without intermediate measurements
through a noise-enabled reset/refrigerator construction and measurement-free
FT; the overhead is polylogarithmic for fixed noise parameters. This is a close
mandatory capability comparator for the powered version of the present device.

It should not be silently upgraded to the present unknown-state quantum ports:
the proof initializes the logical circuit in `|0>^N` [equations (117)–(118)]
and concludes through final encoded `Z` measurements and majority-vote error
analysis [equations (131)–(135)]. Its hypotheses are product contracting
nonunital noise rather than the arbitrary bounded retained common bath here.
Its formal reset/threshold theorem does not supply a complete correlated
quantum-port interface. A one-paragraph comparison with exactly these scopes
would reinforce the dossier's existing conclusion that powered thermal-ancilla
QEC and universality are established, while its complete unknown-input wrapper
remains restricted.

## 7. Final novelty and status assessment

The strongest defensible wording is already present: this is a **specific
finite-collision local-contraction/coherent-module compiler for the supplied
dense-descent code**, plus inherited selected gate and restricted encoded-port
operations. The explicit thermal-pair reserve is a finite paid realization of
the delivered-source premise, not an indefinitely operating recycled bath.
The small-body version is powered measurement-free active error correction.

The active-class inclusion argument is correct: a matched active controller
can run the identical schedule, with the identical channel and resources.
Therefore the compiler alone establishes no strict advantage over that class.
The `NOT_ACHIEVED` affordability/new-regime and `UNKNOWN` priority entries should
remain. No source inspected here forces a stronger novelty or practical claim.

The final review is limited to the pinned dossier bytes and source claims
above. Routine clarification of items 1–4 preserves the main mathematics;
newly introduced substantive claims would need their own checking.

## 8. Settled final-hash delta review

The principal requested a delta check of the settled dossier SHA256
`92cd3cf466b669f39ae9bab6e845330d46470a7280d7519fcc4d9a00216ceb1b`.
I recomputed that hash, read the changed source/convention passages and research
index, and checked their local links. No new broad literature search was made;
no dossier bytes were edited.

**Final verdict: PASS for that exact final dossier hash at its stated scientific
and physical-model scope. No required source/novelty correction remains from
this review.**

The requested clarifications are resolved:

1. Section 11 now takes `H_A=Delta|1><1|` and explicitly relabels the source basis
   so `|0>` is ground. This matches the collision/reset energy convention while
   preserving all previously checked Merkli hypotheses.
2. Section 12.3 retains
   `A_gamma=||gamma_prime||_1+||(gamma exp(beta omega))_prime||_1` in the leading
   error and accuracy-choice scaling, and says that omitting it requires a
   uniform bound. No unearned uniformity over spectral densities is asserted.
3. Section 12.2 identifies the rescaled mixing time with the reference channel
   `K_LS` and includes equation (25)'s condition for transfer to the actual `K`.
4. Section 16 links the actual record index. That index names the four initial
   files, primary manifests and follow-ups, and transparently records the
   timing/independence limitation. The dossier and index's relative Markdown
   links resolve.

The added Shtanko–Sharma v1 paragraph correctly names Lemma 7's RESET,
Theorem 4's threshold wrapper and formal Theorem 1/equation (136), while retaining
contracting local noise and classical final-readout limitations. It does not
import an unknown-state quantum-port factorization or an exact overhead exponent.
My earlier optional elementary-thermal-operation citation suggestion is not a
condition of this final PASS: the elementary collision is proved explicitly and
the dossier already credits the ingredient as established without claiming
priority.

I also checked the small added accounting/contract clarifications visible in
the settled revision. Independent source-preparation trace error plus private
fixed-point waiting and permanent exclusion of waiting-environment outputs gives
the stated per-delivery error by contractivity; it is not generalized to a
returning reservoir. The powered synthesis budget now explicitly includes the
thermal/source-state term `mu_src`. Total-duration/source accounting now names
`K_tot`, gate time and paid port time. These refinements preserve rather than
weaken the actual source/no-return and local-error premises.

The source/novelty conclusion is unchanged: the earned result is the supplied
code's composite finite-collision warm service, with restricted encoded ports
and selected compatible gates. Practical constants, economical renewal,
general noisy quantum ports, a new computational regime, matched full-cost
advantage, and first priority are not awarded. This PASS is an internal
version-bound source/novelty review, at precisely that scope.
