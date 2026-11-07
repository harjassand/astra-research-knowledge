# Initial machinery report: finite thermal collisions in place of a system Lindblad primitive

Researcher: machinery. Date: 7 November 2026, Australia/Brisbane.

## 0. Provenance, independence and exact capital

I read `AGENTS.md`, `outputs/RESEARCH_TO_PUBLICATION_WORKFLOW.md`, the governing protected-processing dossier and the load-bearing thermal-service proof before this extension. I did not read peers' notes. The governing proof has SHA256 `bb4e12ae7cc82ed68f94d4b162f6c9a85e08671fd88b805a510ee47058666b40`; the dossier inspected here has SHA256 `b94faadf5e396a54566414b0889bb45286080a47512701f032795c8e10fb8c00`.

**Independence limitation:** my finite mixed-thermal-ancilla collision construction, sweep mean/moment argument, backward-observable noise estimate, and positive whole-round repair were developed in this turn before receiving any scientific summary. However, the principal sent a summary of a related ground-collision/Dyson/positive-repair construction before this written initial was frozen. I read that automatically delivered message. The principal acknowledged the timing error. Consequently this is an independently developed construction with a late pre-freeze exchange, not a fully uncontaminated written initial satisfying the strict protocol. The received summary is not used below; its proposed coherent-threshold references are left for post-freeze work. This timing cannot be repaired by rewriting provenance.

The exact capital used is: a commuting integer syndrome energy `U`, linear code distance, the fixed minimum-syndrome canonical frame, low-radius confinement `U >= h r`, and at least `kappa U` improving bounded-support catalogue moves. The stable two-sector normal form and selected CCZ gates remain as established in the dossier. This is not an extension of the old N1694 microscopic three-body bath.

## 1. Strongest route and earned scope

The strongest transfer I found is to analyze a **finite-depth sweep of finite-angle energy-preserving collisions directly**. Each local energy-changing Pauli component exchanges one quantum with a thermal qubit of the matching gap. Neither a Davies weak-coupling limit nor exponentially accurate global simulation is used. A sweep has fixed duration, bounded local coupling strength, `O(n)` thermal-qubit contacts and an exponentially contracting energy moment in a warm basin. Small fixed local reset/control/retained-bath errors can be included through a local backward-observable estimate and a signed fault expansion followed by positive CP/TNI repair.

The derivation below establishes a mathematical route under explicit resettable-ancilla and high-body local-control contracts. Its novel candidate content is the **repeatable warm-basin compiler**, not the elementary thermal exchange, autonomous error correction, coherent fault tolerance, or thermal computation in general. It has not yet faced the team's hostile challenge. No practical advantage, small-body geometric hardware, common-bath noisy encoder threshold, or native universal gate set is earned by this initial.

## 2. Exact physical collision

Write `H=J U`. For a Hermitian catalogue Pauli `P_a`, and positive integer gap `d`, put

```
A = A_(a,-d) = P_a Pi_(a,-d),
Pi_h=A†A,  Pi_l=AA†,  [H,A]=-Jd A.
```

These are bounded full-support operators because only the energy terms meeting `supp P_a` enter the change `d`. They are partial isometries pairing syndrome sectors; `Pi_h Pi_l=0` for `d>0`. Use one ancilla with Hamiltonian `h_R=Jd |1><1|` and thermal state

```
tau_d=p0 |0><0|+p1 |1><1|,
p0=1/(1+e^(-beta Jd)),  p1=e^(-beta Jd)/(1+e^(-beta Jd)).
```

Apply for fixed time `t_col` the bounded interaction

```
K=g(A tensor |1><0|+A† tensor |0><1|),
g t_col=pi/2.
```

It commutes with `H+h_R`. All gaps, strengths, durations and support sizes are independent of `n` and requested service accuracy. Tracing this ancilla gives four local Kraus operators

```
sqrt(p0)(I-Pi_h),  -i sqrt(p0) A,
sqrt(p1)(I-Pi_l),  -i sqrt(p1) A†.
```

For every real `s`, with `V_s=e^(sU)`,

```
Phi_(a,d)^*(V_s)
 =V_s[I+p0(e^(-sd)-1)Pi_h+p1(e^(sd)-1)Pi_l].       (2.1)
```

It is exactly Gibbs-preserving: the paired population fluxes obey `p0 e^(-beta E_h)=p1 e^(-beta E_l)`. It need not mix the logical sectors or be a unique-fixed-point sampler. On syndrome populations it is an exact heat-bath exchange: a downhill move succeeds with probability at least `1/2`; an uphill move with probability at most `e^(-beta J)`; all other inputs remain unchanged. Coherences do not enter (2.1).

The finite-angle exchange is established thermal-operation machinery, close to partial level thermalizations and collision models. See Lostaglio–Alhambra–Perry, *Elementary Thermal Operations*, [arXiv:1607.00394v3](https://arxiv.org/html/1607.00394v3), Sections 2 and 3.1. No novelty is assigned to (2.1).

## 3. A full sweep contracts a moment without a Lindblad limit

Assume at most `m<=M n` positive-gap labels, gaps at most `D`, bounded catalogue incidence, and colour the full collision supports into `chi=O(1)` disjoint layers. Each label acts once in the sweep; each layer runs in parallel. Keep all ancillas for the sweep, then discard/reset them. The nominal global sweep is a constant-depth circuit on system plus `O(n)` thermal ancillas.

Let `C` bound how many initially improving labels one successful update can deactivate by changing their read syndromes. Let `L` bound the change in final energy caused by changing one independent collision coin. Both are constants: a changed coin has a causal cone through only `chi` layers of a bounded-degree interaction graph; at most a fixed number of final energy terms are affected. For example, if the conflict degree is `Delta`, a conservative `L` is `D_E q_cat sum_(j=0)^chi (Delta+1)^j` after enlarging the incidence constants. An entire system-wide random colour per round would not give this argument.

For an initial syndrome `sigma` in the promised basin, let `S` and `B` count successful downward and upward transitions in the sweep. At least `A0>=kappa U(sigma)` labels improve at the start. An initially active label is either still downhill when its turn arrives, or an earlier successful local update has changed its read pattern. Hence pathwise

```
A0 <= A_still + C(S+B).
```

Conditionally on reaching a still-active label, success has probability at least `1/2`; thus `E A_still <= 2 E S`. Also `E B <= M n e^(-beta J)`. Therefore

```
E U_out <= (1-c)U(sigma)+b_beta n,
c=min{ kappa/(C+2),1/2 },
b_beta=(D+C/(C+2))M e^(-beta J).                    (3.1)
```

Every successful downhill event decreases `U` by at least one; every upward one adds at most `D`. Importantly, this proof uses descent density only at the **initial** syndrome. Later transitions always have their exact signed energy change, even if an unfiltered path leaves the basin.

Expose the `m` independent random variables generating the collision outcomes. Bounded differences for the final energy, proved by the Doob martingale and the scalar Hoeffding lemma, gives

```
E exp[s(U_out-E U_out)] <= exp[s^2 m L^2/8].
```

Combining with (3.1), and using that the nominal dual preserves the syndrome-diagonal algebra,

```
Phi_sweep^* V_s
 <= exp[(s b_beta+s^2 v)n] e^[s(1-c)U],
v=M L^2/8,                                         (3.2)
```

on the initial basin. This operator inequality holds for arbitrary logical/syndrome coherences and external references. For positive subnormalized input, `x=Tr V_s rho`, scalar concavity yields

```
Tr V_s Phi_sweep(rho) <= exp[(s b_beta+s^2 v)n] x^(1-c). (3.3)
```

The concentration cost `s^2 v` is a real cost. Choose a small fixed `s>0`, then a sufficiently large fixed `beta J`; it is not permissible to omit this cost or to infer contraction of an exponential moment from mean drift alone.

## 4. Robustness to fixed local coherent retained-bath noise

Retain the actual bath `B` and its actual bath-only CPTP maps. During the finite sweep allow an actual CPTP joint evolution with local HP, identity-annihilating disturbances `N_Z`, supported on boundedly many system and active cooling-ancilla qubits and arbitrary `B`, with

```
sum_Z ||N_Z^*(t)||_cb <= eta n,
```

and the stronger usual bounded-incidence/per-qubit condition when desired. The common bath can be correlated with logical and syndrome degrees of freedom. All norms are complete and retain external references. No reset of `B` is made.

There is a simple useful estimate here. Let `F_t` be the future **nominal** Heisenberg evolution of `V_s tensor I_anc`. The free `H+sum h_R` commutes with each collision and with `V_s`; its part drops out. The remaining future circuit has a fixed finite causal cone. For one disturbance support `Z`, divide the final commuting energy terms into those whose backward cones meet `Z` and the rest. The affected terms have total norm at most a fixed `K_F`. After backward evolution there is a positive `Q_t`, supported away from `Z` and all of `B`, such that

```
Q_t <= F_t <= e^(s K_F) Q_t.
```

Because `N_Z^* Q_t=0` and it is a bimodule map over the untouched algebra,

```
 +/- N_Z^* F_t
 <= (e^(s K_F)-1)||N_Z^*||_cb F_t.                  (4.1)
```

This follows by factoring `Q_t^(1/2)` outside the local map; no bath-dimensional Kraus sum is used. Differentiate `Tr F_t rho_actual(t)` and use (4.1). Gronwall gives the **actual full-sweep** moment bound with an extra factor

```
exp[(e^(s K_F)-1) eta t_round n].                  (4.2)
```

This estimate does not compare the whole actual channel to the ideal one in trace norm. It compares a positive observable multiplicatively, so a fixed local error does not need to be exponentially small.

For finite local reset channels, the needed explicit contract is a thermal replacement map on each working ancilla, perturbed in complete norm by at most `epsilon_R` at that local location. A replacement acts identically on the old retained bath except for returning the working ancilla; old ancilla correlations must be charged to the retained environment, not erased from it. A local implementation can swap a fresh thermal source qubit into the working position and move the old qubit to a spent reservoir register. New sources are the paid thermal resource. For a future positive observable, the same `Q<=F<=e^(s K_F)Q` estimate gives

```
R_actual^* F <= [1+(e^(s K_F)-1)epsilon_R] R_ideal^*F. (4.3)
```

The maps must be local complete reset faults, or obey the corresponding local fault-expansion contract. A globally catastrophic reset flag with probability `epsilon_R` is excluded. Shared retained-bath coefficients are allowed by that contract; an arbitrary joint reset with only small one-ancilla marginals is not. Concurrent physical resets need an actual local reset layer satisfying this contract; sequentializing `O(n)` resets into `O(n)` physical time while maintaining fixed system noise would destroy the promised constant-round resource bound.

With `C_s=e^(s K_F)-1`, a conservative actual moment exponent is

```
f_s = s b_beta+s^2 v+C_s(eta t_round+M epsilon_R),
log x_out <= (1-c)log x_in+f_s n.                 (4.4)
```

Support/incidence constants must include the real reset routing and collision hardware. Equation (4.4) is the physical cooling mechanism, conditional on the stated reset/control noise contract.

## 5. Why positive whole-round repair avoids a hard-wall gap

It is dangerous to compress the whole noisy sweep to a code basin and simply assert exact logical neutrality. `O(n)` local gates can collectively implement a logical operation. It is also dangerous to insert a global hard wall into the classical concentration proof: a global accept/reject predicate can destroy its finite causal cone. The following proof uses neither shortcut.

Choose an interior energy cutoff `u_w` and the canonical module

```
Q_w=P 1_(U<=u_w n),   u_w<u_c/4.
```

Let `A_R=sum_j d_j |1><1|_j` be the energy in all nominal fresh ancillas for one sweep, in units of `J`. For a fixed `v_R>0` and `z>0`, the bad positive thermal branch has mass

```
delta_R <= exp[-{z v_R-M e^(-beta J)(e^(zD)-1)}n]. (5.1)
```

Choose `beta J` so that the bracket is positive. The nominal complete sweep unitary, including every partial collision, commutes with `E=U+A_R`.

Expand the actual joint sweep in the continuous local disturbance terms and discrete reset deviations. With

```
mu=eta t_round+M epsilon_R,
||Gamma_r||_diamond <= (mu n)^r/r!,
```

the tail after `r<=alpha n` is at most

```
delta_N <= (e mu/alpha)^(alpha n)/(1-mu/alpha).     (5.2)
```

Each system/active-ancilla local leg changes `E` by at most a fixed `K_E`; choose

```
u_w+v_R+K_E alpha < u_c,
mu<alpha/(8e).                                   (5.3)
```

On the admitted thermal branch `A_R<=v_R n`, every prefix of every low-order path stays below `u_c n`. Its radius cannot escape: a first bounded local step to radius close to `r_0 n` would still be below `r_dec n`, and confinement would require energy near `h r_0 n`, contradicting `u_c<h r_0/4`. The same canonical no-logical argument as in the governing proof then applies at every local system leg, including ket/bra off-diagonals and all bath/ancilla coefficients. Nominal collision propagators restrict to the identity on the logical factor in this safe joint module. The low-order signed map therefore has the full-module form

```
Gamma_le = id_L tensor C_signed,
||Gamma_actual-Gamma_le||_diamond <= delta,
delta=delta_R+delta_N.                            (5.4)
```

Reset deviations that read old ancillas are included as local faults with old ancillas retained in the environmental algebra; they do not get a free product-state premise. In a fresh-source representation, each faulty reset can add only its bounded local ancilla energy and is included in `K_E r`.

Use the governing proof's positive repair on the **actual** channel:

```
C_P(theta)=Tr_L[P Gamma_actual(I_L/d_L tensor theta)P].
```

The extraction is a complete contraction; (5.4) gives

```
||Gamma_actual-id_L tensor C_P||_diamond <=2delta. (5.5)
```

`C_P` is CP/TNI and retains the same actual environmental algebra plus the charged spent ancillas. Its moment obeys (4.4), since input logical mixing and output `P` compression cannot increase the tested moment.

If `g_s=c s u_w-f_s>0`, every `Q_w`-supported positive input has, after `C_P`, mass at energy `>u_w n` at most `exp(-g_s n)`. Compress **this positive comparison map** to `Q_w` to get `C_w`. The complete gentle bound now yields

```
||Gamma_actual-id_L tensor C_w||_diamond
 <= epsilon_round:=2delta+2exp(-g_s n/2).           (5.6)
```

This is uniform on the entire `Q_w` module, including arbitrary logical/gauge/bath/reference correlations. `C_w` is never normalized. It maps the module to itself and obeys (4.4). Composition for `K` sweeps gives decoded half-diamond logical error at most `K epsilon_round`: contractively telescope CP/TNI maps, and charge the final positive lost mass. Thus `K` can be exponential in `n` at fixed physical temperature, nonzero noise and fixed local precision.

**Status:** a fully specified constructive proof under the stated physical primitives, pending adversarial mathematical checking. The exact simultaneous reset contract, full-module path argument and retained-bath backward-observable bound are the main challenge targets. This is not a theorem for an arbitrary passive finite bath.

## 6. Re-cooling, gates and the existing noisy encoded ports

Let `nu_eq=f_s/c`. The positive round comparison satisfies

```
log x_k <= nu_eq n+(log x_0-nu_eq n)(1-c)^k.       (6.1)
```

For any fixed pre-gate threshold `u_pre`, choose `s` sufficiently small and then `beta`, `eta`, `epsilon_R` so that `nu_eq<=s u_pre/4`; this is possible because `s^2 v/(c s)` vanishes with `s`, thermal heating vanishes with `beta`, and `C_s/s` stays finite. A fixed number of sweeps with `(1-c)^k u_w<=u_pre/4` restores `log x<=s u_pre n/2`. The proof-only pre-gate filter costs `2e^(-s u_pre n/4)`, as in the governing service.

The established selected CCZ gates transfer if their actual finite pulse has the original support-spread/distance margins and if **all** concurrently acting collision Hamiltonians, the system Hamiltonian, calibration errors and retained-bath couplings are included in the gate disturbance budget. A gate can be placed in a finite collision window without a reset event crossing the pulse; discard the used cooling ancillas afterward and start the next complete cooling sweep. Collision interactions continue during the pulse and are charged. A full `O(n)` reset layer of order-one channel distance cannot be hidden in a pulse claimed to have arbitrarily small integrated disturbance. This timing choice is an explicit control resource.

The already proved isolated-staging quantum ports transfer only with their original computational circuit-noise, isolation, encoded sender/receiver, short-link and noiseless-classical premises. The collisional theorem replaces system cooling; it does not prove a new noisy active encoder under the common physical bath or remove the port floor for a bare unknown input. Direct native universal operations remain open unless separately supplied compatible generators are proved.

## 7. Primary-source audit: imports and exact obstruction to black-box transfer

### 7.1 Merkli, 2105.00023v2

Pinned full PDF and HTML in `../sources/primary/merkli_2105.00023v2.*`. Published as Quantum 6, 616 (2022), DOI [10.22331/q-2022-01-03-616](https://doi.org/10.22331/q-2022-01-03-616).

Theorem 1.1 really gives an all-`t>=0` superoperator estimate

```
||V_t-exp[t(L_S+lambda^2 K_Davies)]|| <= C |lambda|^(1/4).
```

The model is a fixed finite `N`-level system, an infinite-volume thermal free boson field, static `H_S+H_R+lambda G tensor phi(g)`, initial `rho_S tensor omega_(R,beta)`, and no interventions. Its form factor has four radial derivatives, the specified infrared powers `p=-1/2,1/2,3/2` or `p>2` and ultraviolet exponent `q>2` [assumptions (1), equations (1.26)–(1.27)]. Assumption (2a), equation (1.28), demands nonvanishing transition matrix elements and reservoir density for every distinct-energy eigenvector pair; (2b) requires simple level-shift eigenvalues.

Proposition 1.2 gives the low-temperature coupling restriction

```
c0 = c0' T^24 [min(1,a,delta/kappa^2,g^1.5)
                /max(1,alpha,kappa(1+kappa/delta))]^(4/3).
```

Here `a` is the smallest nonzero decay rate of the level shifts, `alpha` their largest spectral radius, `delta` their within-block eigenvalue separation, `kappa` the largest spectral-projection norm and `g` the separation between distinct system Bohr frequencies [equations (3.48)–(3.52)]. These symbols differ from our code/noise constants. Equation (2.40) explicitly contains inverse powers of `a`, `delta`, `g` and projection conditioning. Equation (2.30) bounds the purification factor by `Tr exp[beta(||H_S||-H_S)]`.

Applicability verdict: **no size-uniform service import follows from this theorem.** For `n` qubits its `N` is `2^n`; the paper does not give polynomial/constant bounds on the above family parameters or on norm-equivalence factors. Local catalogue couplings do not satisfy the displayed all-pairs FGR premise automatically. The protected logical degeneracy is also contrary to the theorem's simple coupled equilibrium structure. None of these observations disproves a suitably generalized resonance approach. Even with size-independent `C`, using this *global absolute-error estimate* alone to target `e^(-c n)` requires `|lambda|` of order `e^(-4c n)`, slowing dissipative rates `lambda^2`; this is a limitation of that transfer bound, not a physical impossibility result. Repeated controls cannot be justified by restarting its product initial-state premise for free.

### 7.2 Stronger correlated-initial-state resonance result

Merkli, [arXiv:2107.02515v2](https://arxiv.org/html/2107.02515v2), Theorem 2.2 and equations (2.31)–(2.38), extends the all-time approximation to a specified class of initially correlated states obtained by Kraus operations on the uncoupled equilibrium. The full-observable expansion has a correlation term decaying as `(1+t^3)^(-1)`; that term vanishes identically on system-only observables. The remainder is `O(|lambda|^(1/4))`, with constants depending on the initial correlation operation. This prevents the false assertion that resonance theory only allows product initial states. It still provides no uniform arbitrary-admitted-module bound under an arbitrary persistent computational workload. No blanket initial-correlation no-go is asserted.

### 7.3 Ong–Parameswaran–Placke–Hahn, PRA 114, 042445 (2026)

DOI [10.1103/25wc-17zy](https://doi.org/10.1103/25wc-17zy), [arXiv:2605.03011v2](https://arxiv.org/html/2605.03011v2), 22 October 2026. Theorem 1, equation (41), is a **fixed-point trace-error bound**, not a protected logical-channel theorem. Its cycle resets `n_B` ancillas to pure `|0>`; uses time-dependent Gaussian-filtered interactions; randomizes the final time by a Gaussian of scale `T0`; and averages over those random times. Its exact setup is equations (9)–(15).

Writing `t_J(epsilon)=J^2 tau_mix(epsilon)` for the rescaled mixing time, the bound is

```
2epsilon + t_J n_B exp[beta^2/(4sigma^2)-T^2/(2sigma^2+4T0^2)]
 + J^2 t_J poly(n_B,beta/sigma,T/sigma,T/T0)
       exp[5beta^2/(2sigma^2)].
```

Equation (77) displays the hidden size dependence: terms include `J^2 n_B beta T^6/(sigma^3 T0^4) exp[9beta^2/(4sigma^2)]`, `t_J J^2 n_B^2 exp[beta^2/(2sigma^2)]`, and `t_J J^2 n_B^2[1+beta T^6/(sigma^3 T0^4)] exp[5beta^2/(2sigma^2)]`. Appendix A Lemmas 1–2 supply fixed-point/mixing perturbation estimates. Theorem 2 bounds random-channel observable variance with channel-contraction/Jordan prefactor `C`, rather than a reference-uniform computation error.

Applicability verdict: the authors explicitly require `t_J=o(J^(-2))` to make the weak-coupling fixed-point error vanish and leave general validation of this scaling open (discussion after equation (42), Section VII). The expected total evolution time scaling (44) is `~O(T t_J^2/epsilon)`, suppressing other parameters. This is substantial physical-sampler machinery and a mandatory comparator, but an exponentially accurate unique Gibbs state is the wrong target for preserving arbitrary logical information. Our route instead proves basin drift at fixed physical precision.

### 7.4 Wang–Ding: finite coupling beyond Lindblad

[arXiv:2512.03457v4](https://arxiv.org/html/2512.03457v4), 19 September 2026, is stronger than saying all rigorous physical samplers require a vanishing coupling with precision. Theorem S2 (rigorous version of Theorem 1), equation (S21), allows a fixed sufficiently small `Gamma=O(1)` while widening the Gaussian filter. It assumes decay of `gamma` at infinity and integrable derivatives of `gamma` and `gamma e^(beta omega)`; its error has rescaled mixing time times `beta log(sigma)/sigma` plus a Gaussian truncation tail. The microscopic algorithm uses a refreshed thermal ancilla, random bath frequency and random signed local coupling [equations (2)–(3)].

Theorem S10 requires `Gamma^2=O(lambda_gap)`, `sigma=~Omega(beta^2/lambda_gap)` and `T=~Omega(sigma)` to transfer a KMS gap to a mixing bound. Theorem 3's thermal end-to-end result has `Gamma=O(N^(-1/2))` and runtime `~O(poly(N) epsilon^(-2))` for its listed models. The fixed-point result's coupling can be independent of precision; its filter width still scales essentially like `beta t_mix/epsilon`. Hence targeting global error `epsilon=e^(-c n)` through that bound incurs an exponential window. This says nothing negative about obtaining a basin moment bound by a more local argument; that is exactly the constructive route above.

### 7.5 Very recent parallel physical-sampler comparator

Ding–Li–Zhang, [arXiv:2611.03422v1](https://arxiv.org/html/2611.03422v1), submitted 2 November 2026, proves arbitrary-initial-state Gibbs preparation for bounded nearest-neighbour one-dimensional qudit chains at every fixed positive temperature. Theorem 1.1/Corollary 9.2 uses `(4^q-1)n` resettable thermal ancillas, randomized bath frequencies and randomized interaction duration, `alpha^2=c epsilon/n`, `T0=Theta(sqrt(log(n/epsilon)))`, and expected Hamiltonian evolution time `~O(n/epsilon)`. Theorem 9.1 explicitly bounds stationary-state bias by `C n alpha^2+C alpha^2 sqrt(n)/T0` and contracts weighted state differences by `1-kappa alpha^2`.

It is a particularly important current comparator: parallel ancillas and finite physical contacts themselves are not new. Its one-dimensional unique-thermalization aim and accuracy-dependent coupling do not supply a noise threshold for repeated non-Clifford processing in our nongeometric code. It also shows why it is too strong to claim that physical system-bath samplers are generically out of reach or lack end-to-end analysis.

### 7.6 Thermal computation and dissipative fault-tolerance precedents

* Rouze–Franca–Alhambra, [arXiv:2403.12691v3](https://arxiv.org/html/2403.12691v3), Theorem II.4, proves BQP-completeness of approximating local observables at outputs of efficiently simulable low-temperature Gibbs samplers, using inverse temperature polynomial in size. Corollary II.5 gives the corresponding classical hardness for fast-mixing observables. This is an established dissipative computation model, with different temperature and input/noise contracts; it is not this fixed-positive-temperature noisy quantum service. It rules out presenting thermal computation itself as a discovery.
* Dunnweber–Styliaris–Trivedi, [arXiv:2601.20818v3](https://arxiv.org/html/2601.20818v3), 25 September 2026, is a stronger autonomous universal comparator. The main theorem gives a 2D local translation-invariant discrete-time QCA, local correlated/non-Markovian fault strength below a nonzero threshold, suitable encoded initial states, `O(N polylog(ND/delta))` qudits and `O(D polylog(ND/delta))` time. Its current text explicitly leaves a formal continuous-time threshold extension for future work (main-text continuous-time discussion and outlook). Do not promote the continuous Lindbladian outline to the proved discrete-time threshold. Do not deny its actual autonomous universality or correlated-noise scope.
* Pastawski–Clemente–Cirac, [arXiv:1010.2901v2](https://arxiv.org/html/1010.2901v2), PRA 83, 012304 (2011), already develops engineered dissipative quantum memories, including local 4D toric-code protection and dissipative ancillary implementation. Broad autonomous correction and ancillary reservoir engineering predate this programme.
* Rojkov–Zapusek–Reiter, [arXiv:2507.12534v2](https://arxiv.org/html/2507.12534v2), introduces trickle-down dissipative correction operators shared across error subspaces, reducing operator counts and improving biased repetition-code performance. Its equations (4)–(7), numerical code sizes and physical effective-dynamics construction must be distinguished: polynomial count does not make the operators geometrically local, and their trapped-ion realization uses effective elimination with unwanted off-resonant transitions. This is a direct conceptual predecessor to descent-based dissipation.
* Scandi–Alhambra, [arXiv:2505.20064v2](https://arxiv.org/html/2505.20064v2), PRX 16, 011040 (2026), and Slezak et al., [arXiv:2601.16154v1](https://arxiv.org/html/2601.16154v1), were screened as microscopic KMS and physical-thermalization alternatives. The former gives time-linear absolute approximation error; the latter gives polynomial-time thermalization in specified high-temperature/weak/1D regimes. They are not imported to assert arbitrary-bath all-time processing. Their full versions are cached; no priority or general applicability claim is inferred from a title or abstract.

## 8. Costs, strongest incumbent and obstructions

| Item | Actual cost or premise |
|---|---|
| Memory | `n` physical code qubits; accepted code/energy constants retained |
| Cooling hardware | `<=M n` working thermal ancillas, bounded-degree support graph; `chi` layers; real body sizes may be huge constants |
| Temperature | Fixed nonzero `1/beta`, chosen after all code/control constants; no useful numerical threshold claimed |
| Collision control | Gap `Jd`, strength `pi/(2t_col)`, duration `t_col`, exact engineered energy-selective coupling; fixed precision errors included |
| Resources over `K` rounds | `O(nK)` thermal contacts/resets and coupling operations, `O(K)` physical time; reusable `O(n)` working space plus entropy disposal; a literal finite fresh tape has `O(nK)` reservoir qubits |
| Cooling energy/heat | Each contact can exchange at most `JD`; a conservative total heat/thermal-source budget is `O(JD nK)`; actual reset work/control dissipation must be measured before advantage claims |
| Quantum I/O | Existing paid isolated staging and encoded-port contracts only; classical/noise/isolation premises retained |
| Timing | Constant-depth predetermined schedule; local timing/drive errors included in local noise budget; no noiseless measurement or feed-forward correction during HOLD |
| Geometry | Bounded interaction-graph locality, not 2D/3D nearest-neighbour or elementary two-body implementation |

An active FT comparator receives the **same** reset qubits, thermal sources, gates, support graph, routing, control precision, isolation and classical hardware. It can apply coherent syndrome extraction and local recovery on the same code, or use a stronger qLDPC/concatenated architecture. The autonomous 2D QCA is another mandatory comparator. `O(n)` work per cooling sweep is active engineered error control, even if it has no measured syndrome record. Absence of feedback during HOLD is not a total-resource advantage.

Specific failure modes and constructive repairs:

1. **Finite closed bath:** a fixed finite reservoir need not cool indefinitely and has recurrences. Charge the growing thermal tape or a constant-quality reset supply. No autonomous passive finite-bath service is claimed.
2. **Global catastrophic reset/drive faults:** small local marginals do not imply the required expansion. Demand local complete error or an actual all-subset bound; a common bit flipping all `n` hardware operations with fixed probability is outside the theorem.
3. **Only mean drift:** it does not bound boundary tails. The fixed-depth bounded-difference term is indispensable; its very large constant may produce an impractically small threshold.
4. **Hard-wall concentration shortcut:** global clipping changes locality. Use full actual moment bounds and positive whole-round repair, then filter the positive comparison map.
5. **Ignored during-collision noise:** finite-strength collisions are not instantaneous. Their full duration enters `mu`, and their actual causal cone enters `K_F`.
6. **Precision hidden in spectral filtering:** the construction requires the actual finite local energy projectors and matching gaps. Their table complexity is fixed but may be enormous; generic noncommuting Hamiltonians do not have this exact local Bohr decomposition.
7. **Noisy input and recovery:** this theorem preserves an admitted logical payload; it does not create an accurate unknown bare qubit or establish a noisy common-bath encoder. Retain the proven encoded-port gateway scope.
8. **Public or historic significance:** no matched cost advantage or first-of-kind physical fault-tolerance claim is established. The substantive achieved candidate is a physical collision replacement at fixed local accuracy for the existing warm service.

## 9. Reproducibility and challenge list

`../checks/collision_checks.py` verifies the finite-angle Kraus/dual formula, Gibbs stationarity and trace preservation numerically to floating-point accuracy. It also enumerates a six-bit commuting energy with overlapping update read supports and checks the derived mean/mgf bounds. This is a finite diagnostic; it is not the code-family, asymptotic concentration or retained-bath theorem.

Full primary HTML/PDF caches and their hashes are in `../sources/primary/` and `../sources/SOURCE_MANIFEST.json`. Search coverage included named recent sources, primary arXiv/publisher routes and bounded recent Zenodo discovery queries. The Zenodo queries mainly returned irrelevant physics/data records; they do not establish absence of competing preprints or priority.

The strongest immediate challenges are: (i) verify the local relative-observable estimate at reset boundaries including old ancilla correlations; (ii) formalize the exact reset-layer fault-expansion contract and its constant-duration physical realization; (iii) independently check full-module factorization of low-order joint paths while retaining both radius and energy cutoffs; (iv) check that repeated positive repair/filtering keeps all trace deficits and moments; (v) compare the result against coherent FT thresholds and the latest QCA at matched resources. These are explicit mathematical interfaces, not a request for publicity or a declaration of an implementation advantage.
