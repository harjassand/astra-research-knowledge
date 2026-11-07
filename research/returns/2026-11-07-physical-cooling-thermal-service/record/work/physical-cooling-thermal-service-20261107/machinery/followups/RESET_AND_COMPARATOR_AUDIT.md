# Post-freeze reset and comparator audit

7 November 2026. This note follows, and does not modify, the frozen initial
`../initial/machinery.md`, SHA256
`832e5ad10fe9373e3a7547aa3c0956ffa3ebdd516d207a038cedf451a383ca35`.
I now read the principal's `COHERENT_SWEEP_BRIDGE.md` and auditor's
`COHERENT_BATH_FULL_SWAP_SWEEP.md`, and checked the principal-supplied coherent
threshold references. Thus this is collaborative follow-up, not independent
initial work.

## 1. Adjudication of the strongest compiler

The ground-reference sweep plus signed thermal-input faults is stronger and
simpler than my mixed-thermal-sweep moment proof. Every ground input makes an
active full exchange succeed deterministically. If one successful move changes
at most `R0` initially active predicates, charge each missed initially active
label to the first earlier successful move that spoiled it. A successful visit
charges itself. Therefore

```
kappa U_start <= (R0+1) S,
U_end <= U_start-S <= (1-a)U_start,
a=min(1/2,kappa/(R0+1)).
```

No concentration step or `s^2` moment cost is then needed. At finite temperature,
each independent input qubit has the exact signed preparation expansion

```
Prep_tau = Prep_0+q_d(Ad_X-id)Prep_0,
||q_d(Ad_X-id)||diamond <=2q_d,
q_d=(1+e^(beta Jd))^(-1).
```

Counting this as local order combines thermal/input, reset and continuous joint
errors into the ordinary coefficientwise `exp(z mu n)` bound. The ground circuit
has a finite Stinespring causal cone, so a low-order error may be moved to the
output without inverting a reduced cooling channel. Its system support is at
most `q_eff r`. This proves both the output-energy support recurrence and the
canonical no-logical statement, with all bath/reference coefficients retained.

I checked the principal/auditor positive repair: it is correct at `2 delta`.
If the full-module signed approximation is `T=id_L tensor C_signed`, is output
supported in `Q`, and is within `delta` of the actual CPTP `Gamma`, apply the
complete contraction

```
F(X)=Tr_L[Q X(I_L/d_L tensor dot)Q]
```

to obtain `||C_good-C_signed||diamond<=delta`. The direct triangle on
`Gamma-T+id_L tensor(C_signed-C_good)` gives `2delta`; no separate gentle
compression loss is required. CP/TNI and the positive lost-mass conversion are
essential and are retained by the auditor's proof.

The new two-sector energy in the governing dossier, Section 3.4, has a global
low-energy repair bound: repeated strictly decreasing moves reach zero in at
most `U` steps, so a bounded-support-per-step correction has weight at most
`L U`. This is sufficient for the energy-only basin used by the audited
compiler. It must not be replaced by the weaker low-radius confinement premise
in the older Tanner DATA-only proof. My initial kept the conservative radius
argument; the audited stable two-sector energy makes that extra machinery
unnecessary.

**Verdict:** the audited finite-collision compiler is a proved mathematical
transfer at its supplied DATA, exact-resonance, local complete-noise and fresh
source/no-return premises. I found no gap in its whole-round support/factorization
or `2delta` positivity operation. Its source renewal and hardware/cost limitations
remain real; the operation is powered open-loop error correction.

## 2. Exact Merkli fixed-qubit reset applicability

Primary source: Merkli, *Dynamics of Open Quantum Systems II, Markovian
Approximation*, [arXiv:2105.00023v2](https://arxiv.org/html/2105.00023v2),
Theorem 1.1, Proposition 1.3, equations (1.26)–(1.28), (1.33)–(1.42),
(3.48)–(3.52), (3.63)–(3.70). The cached full PDF is SHA256
`8c00223487b6b8276f0502153ad028c8895c190a28151943d9b745d6aeef5017`.

Consider one qubit with `H_A=(Delta/2) Z`, `Delta>0`, `G=X`, and an independent
infinite-volume free boson reservoir with dispersion `omega(k)=|k|` in a thermal
state at a fixed positive temperature `T=1/beta`. Take the isotropic real form
factor

```
g(k)=g_rad(|k|),
g_rad(r)=r^3/(1+r^6) [2+e^(-r)].
```

All displayed hypotheses hold:

1. In equation (1.26) choose `p=q=3`, and `h(r)=2+e^(-r)`. Thus `p>2`, `q>2`.
   Every one of `h,h',...,h''''` is bounded on `(0,infinity)`, and its limit at
   zero is respectively `3,-1,1,-1,1`, all nonzero. The radial form factor is
   smooth for `r>0`. Its squared radial `L^2(R^3)` density behaves as `r^8` at
   zero and `r^(-4)` at infinity, both integrable. The usual field relative-bound
   integral `||g/sqrt(omega)||_2` is also finite (powers `r^7` and `r^(-5)`).
2. In the energy eigenbasis, `G_12=1` and `G_11=G_22=0`. The only distinct-energy
   transition gap is `Delta`. The FGR quantity in (1.28) is
   `4 pi g_rad(Delta)^2>0`.
3. With the paper's spectral density
   `S(omega)=(pi/2)omega^2 int_(S^2)|g(omega,Sigma)|^2 dSigma`,
   one has `S(omega)=2 pi^2 omega^2 g_rad(omega)^2`, so `S(Delta)>0`.
4. The level-shift blocks at Bohr frequencies `+/-Delta` are one-dimensional.
   The zero-frequency block has eigenvalues `0` and
   `2i S(Delta)coth(beta Delta/2)`, which are distinct. Hence the simplicity
   assumption holds. Its spectral projections are orthogonal, so the paper's
   projection condition number `kappa` is one. The Bohr-frequency separation is
   `g_Bohr=Delta`; the smallest nonzero decay rate and level-shift gap are fixed
   positive constants. The Lamb-shift principal-value integrals are finite
   under the verified form-factor assumptions.
5. The initial new boson reservoir is thermal and independent of the qubit plus
   all old references. The Hamiltonian is static during the reset dwell. These
   are operational assumptions, not consequences of an accurate ancilla marginal.

Theorem 1.1 therefore supplies, for `|lambda|<c0`, an all-time reduced-channel
estimate of order `C |lambda|^(1/4)`. Proposition 1.3 allows the sufficient
low-temperature bound `c0=c0' T^(76/3)` for this `p>-1/2` qubit case. These are
fixed-dimensional constants; there is no `2^n` many-body factor here. The paper
does not supply a turnkey numerical value of its absolute constants, so this
is an existence-level fixed-accuracy reset construction, not a numerical
hardware specification.

### Complete reset estimate and its precise operational scope

Let `V_t` be the actual reduced qubit channel, let `D_t` be the Davies channel,
and let `R_tau(X)=tau Tr X`. The state-uniform trace estimate extends to all
Hermitian trace-class operators by positive/negative decomposition, and then
to arbitrary operators by real/imaginary decomposition. The standard
fixed-input-dimension inequality `||T||diamond<=2||T||_(1->1)` gives the
conservative bound

```
||V_t-D_t||diamond <=4 C |lambda|^(1/4).           (2.1)
```

Use the generator (1.33), rather than copying a relaxation formula blindly.
Writing

```
r_beta = c_hat_beta(Delta)+c_hat_beta(-Delta)>0,
```

the population displacement from `tau` decays as `exp(-lambda^2 r_beta t)`;
off-diagonals decay as `exp(-lambda^2 r_beta t/2)` up to a unitary phase. A
direct qubit block estimate, uniform over every external reference, gives

```
||D_t-R_tau||diamond <=6 exp(-lambda^2 r_beta t/2). (2.2)
```

The constant six is deliberately conservative: the diagonal displacement
contributes at most four and the two off-diagonal blocks at most two, before
using the slower decay exponent. Thus

```
||V_t-R_tau||diamond
 <=4 C |lambda|^(1/4)+6 exp(-lambda^2 r_beta t/2).  (2.3)
```

For a fixed reset tolerance `epsilon_R>0`, it suffices to choose

```
0<|lambda|<min(c0,(epsilon_R/(8C))^4),
t_reset >= 2/(lambda^2 r_beta) log(12/epsilon_R).
```

Both are constants independent of memory size and runtime, albeit potentially
very poor ones. A finite set of target gaps `Delta in {J,...,JD}` can be handled
by taking the worst constants across that finite set.

There is a visible typographical issue in the primary source: equation (1.37)
prints a minus sign before the Gibbs population term. That would tend to a
negative population and contradicts its immediately preceding fixed-point
equation (1.36). The reset argument above instead derives the positive relaxation
from (1.33). This local typo does not invalidate the all-time approximation
theorem. No questionable printed rate convention is needed in (2.2).

The new outgoing boson bath may be correlated with the qubit and old references.
The complete reset estimate is valid for subsequent operations **only when that
outgoing reservoir is never accessed again**. Its trace is then the genuine
reduced channel in (2.3). One may not silently keep the outgoing reservoir in
the accessible common bath and use (2.3) as a joint reset estimate. The theorem
also cannot be restarted on the same disturbed reservoir for every cycle.
During reset the qubit must be disconnected from DATA except for charged local
disturbances, and the fresh reservoir must be independent of the old accessible
environment. Switching and waiting errors must be charged or supplied through
an explicit reset primitive. The boson field interaction has unbounded full
operator norm; it is not automatically one of the bounded joint `N_Z` noise terms
of the DATA theorem.

A fresh noninteracting finite Gibbs tape is cleaner for a completely finite
requested horizon. The principal/auditor true-Gibbs two-spin source-pair
construction can be used without any Markov approximation. Its `O(nK)` reserve,
private stationary waiting and permanent no-return after use remain charged.
The fixed-qubit Merkli construction is an optional source/reset implementation
with fresh reservoirs; it is not an economical recycled refrigerator theorem.

## 3. Exact coherent-threshold comparators

### Han–Zhao–Xu–Wang–Liu, 2609.20537v1

Primary source: [*Coherent error threshold for quantum LDPC codes*](https://arxiv.org/html/2609.20537v1),
17 September 2026; cached HTML SHA256
`dbacd5c15ba738560efe1a22a4722d29e1285f9fccb4e5c54093200ed87a2c98`.

The local coherent model is a depth-`D` circuit, `D` fixed, with disjoint gates
per layer on at most `r` qubits, generated by bounded operators of strength
`eta`. Supports need not be geometrically connected. It is followed by perfect
measurement of all stabilizer checks and a CPTP recovery. Theorem 1/rigorous
Theorem 14 gives optimal-recovery code-capacity suppression; Theorem 2/rigorous
Theorem 18 gives minimum-weight recovery. Informal bounds are respectively
`C sqrt(n)e^(-c d_n)` and `C_MW n e^(-c_MW d_n)` for `d_n=Omega(log n)` below
fixed thresholds.

The channel extension in Theorem 15 uses a depth-`D` tensor-product-per-layer
CPTP noise circuit with local strength `half||Phi_alpha-id||diamond<=p`.
With the paper's counting constant `chi`, it gives

```
q(p)=2 chi sqrt(2p),
epsilon_opt <=2 sqrt[D/(chi(1-q))] sqrt(n) q^(d_n/(2r)).
```

Theorem 19 supplies the corresponding minimum-weight channel threshold:
`rho_MW(p)=2^D chi_MW (2p)^(1/(2r))` and
`epsilon_MW<=2n rho_MW^d/[chi_MW(1-rho_MW)]`.

**Actual distinction:** these are strong general qLDPC coherent/channel
**code-capacity** theorems with ideal syndrome measurement and recovery.
The paper explicitly leaves noisy circuit-level extraction and persistent
non-Markovian noise as further problems. It does not implement the finite
temperature lowering sweep or establish its repeated warm-gauge invariant
module. Conversely the current compiler does not supersede the paper's much
broader `d=Omega(log n)` result. For our linear-distance code, the elementary
total-order tail already gives a coherent threshold with sufficiently small
constant total local strength; cluster resummation is not needed for that fact.
Claiming a new general coherent threshold here would be wrong.

### Terhal–Burkard, quant-ph/0402104v2

Primary source: [*Fault-Tolerant Quantum Computation For Local Non-Markovian Noise*](https://arxiv.org/html/quant-ph/0402104),
PRA 71, 012336 (2005), Theorem 1. The noise amplitude is gate time times half
the spectral width of the bounded local system-bath interaction. The displayed
threshold is `Delta_SB t0 <1/[e A_C(A_C-1)]` for their code/gadget assumptions,
with `N polylog(N/sqrt(epsilon))` noisy locations. Crucially their theorem
retains the stated “noninteracting qubits have noninteracting baths” assumption.
It is incorrect to attribute unrestricted common-bath scope to this particular
theorem without its later extensions. The paper explicitly supplies fresh
ancillas prepared offline. The fine-grained coherent fault-path argument is a
direct predecessor to the present norm expansion.

### Aharonov–Kitaev–Preskill, quant-ph/0510231v1

Primary source: [*Fault-tolerant quantum computation with long-range correlated noise*](https://arxiv.org/html/quant-ph/0510231),
PRL 96, 050504 (2006), equations (1)–(5), (22)–(25). The bath Hamiltonian is
arbitrary, while a two-body perturbation `H_SB=sum_(ij)H_ij` can act on each pair
of system qubits and the common bath. A sufficient local strength premise is

```
eta=t0 max_i sum_j ||H_ij|| <eta0.
```

The paper converts this to a standard non-Markovian fault amplitude
`epsilon=e^(1+1/(2e))sqrt(2eta)` and imports the accuracy-threshold machinery.
Algebraic spatial decay faster than `r^(-D)` makes this local sum finite in
dimension `D`. Its higher-body discussion yields the corresponding root-strength
scaling. Thus arbitrarily long quantum computation under a bounded common
coherent bath is established FT capital. The present logical-preservation
tail is not a new principle of non-Markovian fault tolerance.

## 4. Exact novelty and full-cost conclusion

The defensible new composite statement is: **the supplied low-energy local
descent code admits a finite-duration, finite-gap thermal-collision recovery
block whose whole-round error map closes a repeatable warm logical module at
fixed local precision, including the supplied bounded joint coherent bath
noise and selected code-preserving gates.** This replaces an exact DATA GKSL
cooler by explicit resettable-ancilla dynamics. Established thermal operations,
fault-path methods and subsystem positive repair are credited as ingredients.

There is no first-priority claim. Autonomous quantum memories and universal
QCA computation, physical collisional Gibbs samplers, coherent qLDPC code-capacity
thresholds and common-bath accuracy thresholds are all existing comparators.
The thermal-sampler results solve a different task: they approach a unique Gibbs
state and would erase unknown logical information if applied as such. Their
failure to transfer as a black box does not make them weaker in their own scope.

A matched active architecture can execute **the identical collision circuit**
with identical reset stream, q-body interactions, timing and local noise. Hence
this compiler by itself cannot establish a strict advantage over the class of
active machines that includes that implementation. Removing measured syndrome
feedback during HOLD is an operational feature, not a full-cycle cost advantage.
The strongest incumbent also receives the same high-connectivity local gates,
source quality and protected I/O, and can choose a different qLDPC architecture.

Earned model theorem and unearned capability claims should be split exactly:

* **Proved at supplied primitives:** finite-collision warm recovery block;
  coherent same-environment CP/TNI composition; finite-temperature token faults
  within a fixed threshold; repeated selected useful gates with stated margins.
* **Restricted inherited transfer:** noisy encoded ports with isolated staging
  and its existing classical/noise assumptions.
* **Open:** practical constants; elementary small-body/Euclidean implementation;
  efficient contaminated-source factory; repeated strong bath reuse; generic
  common-bath noisy encoding; native universal set; complete cost advantage;
  experiment; historical priority.
