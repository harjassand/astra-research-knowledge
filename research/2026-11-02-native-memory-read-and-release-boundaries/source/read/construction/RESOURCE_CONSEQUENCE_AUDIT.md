# Resource/consequence audit: robust native memory versus usable write–store–read

2026-11-02. Read `ROOT_ROBUST_NATIVE_MEMORY_JOIN.md`, the exact clock algebra, both native rod bounds, mixed-source KP admission, and previous ideal preparation joins. This audit accepts those internal joins conditionally as stated; it does not independently re-prove Delivery83 or claim external validation.

## Decision first

**The strongest established consequence is presently foundational retention in an open Hamiltonian region, not a demonstrated usable memory.** The next decisive gate is a noise-tolerant, physically charged route into and out of the admitted equilibrium logical subsystem. There is also a separate finite-size/energy-hierarchy obstacle: the available sufficient certificates can be enormous. These are independent gates; improving either alone does not establish practical advantage.

A useful next theorem would specify an allowed write/read control set, accessible spins, initialization resource, error model, and target `(hold time T, total error epsilon)`, and prove

    error_total <= error_write + error_store(T) + error_read,

with explicit preparation time, live ancilla/reset cost, coupling range/strength, and control faults. The target must include reference-entangled inputs. One should not demand exact equilibrium if a quantitatively sufficient weaker admission can be proved.

## 1. Actual source-family assembly certificate—not a universal lower bound

Primary source: [Balasubramanian–Davydova–Lin, arXiv:2605.10943v1](https://arxiv.org/html/2605.10943v1), §§3.2–3.4, 5.4, 6 and initialization outlook.

Its numerical random-embedding choice has alpha=1000, lambda approximately 5.4×10^24 and density bound 6.6×10^10. The definition ell>(2 alpha+1)lambda therefore literally gives ell approximately 1.08×10^28; the later informal ell≈10^24 summary should not replace that arithmetic. Local refinement patches have O(ell²) cells. These are sufficient construction choices, not proved resource minima. The same paper presents explicit ell=8 geometry but leaves its quantum lifetime proof incomplete. It also does not establish efficient passive initialization; its metachecks prevent direct use of the cited logical-sector mixing theorem.

The physical importance is not whether one can shave a factor of two from these numbers. Fixed-ell preprocessing, lookup tables, layout, signal routing and minimum patch size are hidden constants in every subsequent polynomial algorithm. A theorem polynomial in n with ell fixed is not a finite-machine resource estimate. The verified n=1336 small-ell algebra fixtures are valuable correctness tests but do not certify the random-embedding theorem at those practical dimensions.

### Actual Peierls admission

Use the robust join's tension

    a = 2 beta J0 (1-epsilon0) - Lambda_beta(v).

Let D_dec be the full decoding-graph degree, D_level its within-level degree, and M_ell the maximum local patch size. The inherited sufficient witness admission is

    2(D_dec+1)^2 * [(1+exp(-a/4))^M_ell -1]^[1/(1+D_level^4)] <= 1/2.

This is the explicit test to use, rather than only saying 'low temperature'. An algebraically equivalent condition is

    exp(-a/4) <= (1+u)^(1/M_ell)-1,
    u = [4(D_dec+1)^2]^[-(1+D_level^4)].

Evaluate the right side numerically with log1p/expm1, not direct subtraction. The sufficient tension behaves like 4[log M_ell +(1+D_level^4)log(4(D_dec+1)^2)] when u is small. This is an inference from the displayed criterion, not a lower bound on the true critical temperature.

## 2. Native energy hierarchy: a seventh-order scale

For K=7 and r=t/Delta, the existing construction uses

    J0=2 Delta r^7,
    Delta/J0=1/(2r^7),
    t/J0=1/(2r^6).

The real-parameter rod certificate has, with B=beta Delta and Dbar=D exp(mu),

    epsilon0 <= Q6(B) + 128r²/(1-4r²) +57344 Dbar r²,
    Q6(B)=exp(-B) sum_(j=0)^5 B^j/j!.

Its KP conditions also include

    64 Dbar r² <= log 2,
    2r+32 Dbar r² <=1/2,
    6 exp[-B(1-2r-32Dbar r²)+64Dbar r²] <= r².

The robust mixed gas strengthens some rod charges; `MIXED_KP_PARAMETER_ADMISSION.md` uses, for example, `2r+128Dbar r²<=1/2` plus the corresponding stricter wrap condition. Using only the earlier native conditions is insufficient for the robustness certificate.

Every quantity can be fixed once for all n. That is the existence achievement. But if a physical maximum coupling is E_max and Delta is the dominant onsite scale, then the certified protecting scale is only J0=2E_max r^7. Fixing J0 instead requires the reciprocal hierarchy above. One cannot quote a fixed J0 and a modest maximum hardware coupling simultaneously without charging r.

For illustration only, r=10^-3 gives Delta/J0=5×10^20 and t/J0=5×10^17. This is not asserted to meet the actual degree/tension conditions, and is not a physical lower bound. It shows why bounded-in-n need not mean usable.

## 3. Robustness certificate: the full-column exponential

Let x=beta J0. Then beta t=x/(2r^6). The source activity actually used is

    q(v)=7^b_c d_B^b_B exp(x b_c/r^6)
          [exp(beta C_local v)-1].

If the mixed KP consumer requires q(v)<=q_star, the direct sufficient choice is

    v <= [beta C_local]^-1 *
         log[1+q_star 7^-b_c d_B^-b_B exp(-x b_c/r^6)].

For a small argument this gives the certificate scale

    v/J0 approximately at most
      q_star/[x C_local 7^b_c d_B^b_B] * exp(-x b_c/r^6).

Moreover q_star is not generally order one: the source charge A must pay the ordinary-rod contacts of an entire time column, of order beta t²/Delta per owned clock, and source KP pays exp(2A). Since beta t²/Delta=x/(2r^5), this is another severe fixed-parameter cost.

**Interpretation:** this is a conservative sufficient upper limit on admissible perturbation strength in the current proof. It is NOT a necessary fabrication tolerance, a physical fragility theorem, or an upper bound on the model's true robustness radius. To claim practical tolerances one needs a qualitatively normalized response/control theorem or independently validated finite-size regime, not rhetoric that the constant is nonzero.

The retained Schatten-Hölder history bound may help avoid full-column absolute-weight penalties, but does not presently provide the required local connected factorization. Substituting it without a new connected-source proof would reopen the gate. Merely improving 57344 is not the main issue.

## 4. Endpoints: what the actual-H storage theorem assumes

The theorem receives the actual joint Gibbs state of the SAME coupled memory–clock–environment Hamiltonian and overwrites its decoder logical factor, leaving its gauge/environment marginal intact. It assumes neither a constructive thermalizer nor a noisy physical implementation of that overwrite or readout. Its bath may be large and inaccessible. Waiting until a laboratory system equilibrates is not a proved preparation algorithm or time bound.

Previous constructive machinery is useful but narrower:

- The recursive positive-polymer sampler prepares the commuting code's syndrome ensemble with a supplied encoded logical ground state. Strong established polymer samplers can replace the conservative dictionary enumeration when their computational contracts hold. This does not sample generic interacting quantum bath correlations.
- The filtered-parent encoder targets a known weakly noncommuting Hamiltonian with an ACCESSIBLE finite engineered bath and a commuting reference. Its reference argument does not automatically transfer to the noncommuting clock reference. Nor does an ideal quantum preparation algorithm prove fault-tolerant release into the physical memory.
- Full global equilibrium mixing is not necessary in principle. Logical-sector mixing or direct preparation can bypass long logical mixing times. Thus 'long memory implies exponentially slow preparation' is not a justified obstruction.

### Accuracy is less demanding than an exp(T) simulation requirement

If a physically prepared joint state is within trace distance delta of an admitted ideal encoding, exact joint evolution and decoding increase that discrepancy by at most zero: delta adds once, not T delta. Consequently fixed target error epsilon needs initial error O(epsilon), not exp(-T). A physically useful local-noise admission may be weaker still than global trace distance. Proving such an admission for generic native imperfections is a consequential endpoint target.

The caveat is accessibility: a memory-only reduced-state guarantee is not automatically a joint memory–environment guarantee in a non-Markovian model. Correlations with an inaccessible bath can matter. Any substitute admission must be phrased at the level required by the actual dynamical consumer.

## 5. Strong conventional alternatives under an honest resource ledger

### Active fault tolerance

[Terhal–Burkard](https://arxiv.org/abs/quant-ph/0402104) proves a threshold for local non-Markovian Hamiltonian noise, controlled by gate time times interaction spectral width. [Svore–Terhal–DiVincenzo](https://arxiv.org/abs/quant-ph/0410047) addresses local architectures. These are relevant stronger operational baselines than independent-Pauli toy noise: non-Markovian environments do not by themselves force passive storage.

If repeated local gates, fresh/reset ancillas, entropy export and classical processing are allowed throughout storage, use a standard active fault-tolerant memory as the baseline before building this hierarchy. At fixed noise below an applicable threshold, required protection can grow with target spacetime/accuracy rather than using the enormous certified passive assembly. One must still verify the particular Hamiltonian noise and geometric architecture satisfy the cited threshold hypotheses; the two references cannot be combined into an unchecked universal claim.

At the hardware level, [Google Quantum AI's below-threshold surface-code experiment](https://www.nature.com/articles/s41586-024-08449-y) demonstrated size-improving error suppression with repeated error correction. This is not proof for our adversarial environment class or arbitrarily long lifetimes, but it is an actual operational benchmark, unlike a passive existence certificate.

**Same resources means same controls:** active QEC consumes continual reset/control resources absent from the passive hold interval. It is not a substitute if that interval must be autonomous. Conversely, granting a full fault-tolerant computer to implement write/read does not justify ignoring what that same computer could do by remaining active during hold. Compare integrated spacetime, reset energy and control uptime, not physical-spin count alone.

### Passive and preparation comparators

Ocko–Yoshida, HPWL, universal Hamiltonian simulation and thermal-phase transfer were audited in `ocko_yoshida_shielding_audit.md` and `independent_constructor.md`. None supplies the same actual-family, fixed-ratio, full-spectrum robust passive write–store–read guarantee. Their existing low-energy engineering must still be credited.

[Bergamaschi–Gheissari–Liu](https://arxiv.org/html/2507.10976v1), Theorems 1.7–1.8, supplies logical-sector Gibbs preparation under structural assumptions, with efficient two-qubit block updates specifically for 4D toric code. It starts from a ground state. General block implementations can be quasipolynomial; neither the actual hierarchical metachecks nor its generic noncommuting native environment is automatically covered. It cannot currently replace the missing endpoint theorem at the same resources.

## 6. A materially different next construction

**Prefer the existing explicit ell=8 sheaf/defect-network geometry as the next foundational construction test—not another numerical improvement to the random-layout constant.** Its geometry changes the dominant assembly mechanism. Required concrete deliverables:

1. Extract the finite local refinement/doubling rules into exact chain maps and a bounded-stencil decoder, including terminal sectors.
2. Prove independently removable valid syndrome witnesses with amplification in both CSS sectors, bounded connected witness entropy, and polynomial local filling.
3. Check bounded check weight/incidence and physical density at every step.
4. Only then apply the already general native clock/rod machinery, adjusting K if the verified check weight demands it, and rebind the robustness consumer.

Success would replace the astronomical geometric certificate and potentially improve the storage exponent. Failure should produce a concrete bad configuration or failed witness identity. It would NOT alone fix seventh-order energy suppression, the full-column robustness majorant, or endpoint preparation. Its value is eliminating a distinct dominant assembly obstacle, rather than marginal constant polishing. The primary source already proposes the geometry; no novelty claim belongs to that proposal.

For an immediately usable device under continual-control resources, the materially different mechanism is instead conventional active error correction, with initialization and readout handled within its threshold protocol. The passive construction's distinctive potential benefit is reduced control/entropy-export demand during long hold intervals. That benefit cannot be quantified until the two endpoint operations and a nonprohibitive finite-size parameter point are admitted.

## 7. Stop/go criterion

Do not call the result a usable quantum hard drive until at least one explicit finite-size point includes all of: attainable maximum coupling and temperature; a defensible calibration/contact tolerance; a realizable assembly; reference-safe write/read under charged noise; and a total-error bound outperforming the strongest permitted active alternative on an identified resource, such as control uptime or reset cost.

The present work can still be a significant existence result without meeting that gate. Extreme sufficient certificates do not prove the physics must be extreme, and efficient ideal algorithms do not prove hardware interfaces are available.

## 8. Concrete allocation decision and native-output release

The consequence of Delivery83 is an internally certified autonomous retention region, not a finite-resource write–store–read implementation. Allocate the next work to TWO independent mechanisms, not to cosmetic constant reductions:

1. **Assembly:** independently prove the actual explicit ell=8 family's witness contraction and filling. Its local geometry cannot inherit the old random-layout decoder theorem for free. A positive constructor is now testing its exact collar and vertex incidences.
2. **Interface/robustness:** construct a quotient thermalizer or noisy basin of admissible gauge states for the actual native Hamiltonian. Require reference-safe logical loading and readout while charging faults at the final physical native-output boundary. Seek a normalized connected-source estimate before interpreting the tiny q certificate as an engineering tolerance.

A fault-tolerant compilation of an ideal N-spin Gibbs preparation channel is NOT by itself a solution to (2). If the output must be released as N unencoded physical native spins, independent local final faults at rate p can put O(Np) faults on that output. The probability of at least one fault is 1-(1-p)^N; this fact does not alone lower-bound its distance to a mixed Gibbs state, but it does show why a no-fault/global-accuracy argument is not uniform in N. A valid endpoint theorem must admit the resulting local error distribution, prove it correctable in the actual coupled bath setting, or physically retain protection without changing the promised native hold model. Demanding p=O(epsilon/N) is one conservative workaround, not a physical necessity and not an automatically available constant-overhead FT release theorem.

For a proposed finite parameter point, the decision ledger is:

- Fix N,T,epsilon and maximum implementable two-spin norm G, rather than only dimensionless existence parameters.
- Verify Delta<=G and t<=G; J0=2Delta r^7 and x=beta J0 then fix the necessary temperature for the chosen sufficient regime.
- Evaluate the actual witness admission and mixed KP inequalities, including graph degrees, patch size and source charges. Compare the obtained certified v allowance to the stated fabrication/contact model. Failure of these sufficient tests means 'not certified here', not 'physically impossible'.
- Bound preparation/control time, accessible bath size, reset/ancilla cost, final native release faults and readout error, and combine with the exact-H retention bound. No useful-device claim without all entries.
- Compare a continually active implementation at the SAME permitted controls/noise and target error, charging its hold-period resets and controller uptime. If continuous control is forbidden, label this explicitly; a passive advantage is then autonomy, not an established lower spin count or easier preparation.

**Current decision:** continue foundational construction and the quotient/noisy-interface target; do not claim an operational advantage or invest in reducing the rod prefactors alone. Even a successful ell=8 witness proof would not remove the seventh-order energy suppression or full-column source penalty. Conversely those penalties are upper-bound artifacts until a lower-bound or physical instability argument is supplied.
