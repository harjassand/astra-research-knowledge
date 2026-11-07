# Noisy access and repeatable non-Clifford processing in a protected thermal code

Research dossier, 7 November 2026. Governing research record: [protected-quantum-processing-20261107](../work/protected-quantum-processing-20261107/). This is a mathematical research return, not a publication or a hardware claim.

## 1. Strongest result actually obtained

**PROVED, at the physical model and primary-source inputs stated below:** an explicit modification of the recent good quantum locally testable gate codes admits noisy entry, exponentially long storage, and repeatable addressed non-Clifford gate bursts separated by constant cooling dwells. The protection dynamics are a specified, engineered, bounded-body thermal GKSL generator. They remain present during gates. A weak retained perturbation bath and its actual correlations are carried throughout. No exact Gibbs state is required at loading. Section 12 closes WRITE/READ from already protected quantum ports under explicit isolated-staging primitives; bare ports retain their unavoidable endpoint floors.

The construction adds a constant factor of product-state memory ancillas and changes the commuting stabilizer energy. Its decisive step is an exact local stable CSS duality: it transfers a cochain decoder to the second physical error sector without pretending that global soundness implies a local decoder. This yields a commuting energy with many strictly energy-lowering local moves for **both** error types, on the same DATA code that supports the supplied non-Clifford gates.

The state guarantee preserves information entangled with an external reference, even when the admitted logical state is correlated with the gauge and retained bath. Actual immediate decoded writer error adds linearly. There is no replacement of the actual bath, approximate-product writer assumption, or avoidable square-root loss in writer accuracy.

For an explicit infinite size sequence, constants C,c>0 can be fixed independently of size n, storage time T and number g of gate bursts so that

\[
 \epsilon_{\rm final}\leq \epsilon_{\rm ports}
   + C(g+1)e^{-cn}+CnT e^{-cn}.
\]

Different exponents and the exact prefactors are given in Sections 5–7. Here n counts the **entire augmented memory**, and T includes all cooling dwells. Gate durations and the paid I/O durations are additional physical time. The formula is a finite-size, finite-time channel bound, capped by one, and permits exponential T and g below its positive exponents.

**Exact limitations:** the nominal thermal reservoir is an engineered Markovian primitive. Its derivation from a finite-bandwidth microscopic bath, small-body/three-dimensional realization, economical constants and a favorable complete-resource comparison are not proved. The supplied logical gate family is addressed CCZ on specified selected ports, with unused logical coordinates initialized as required by its source. Universality on this architecture is not established. The previous three-body clock memory's noisy-writing problem remains open. No 95+ or civilisation-scale capability has been established.

The complete consolidated constructive proof is [THERMAL_SERVICE_THEOREM.md](../work/protected-quantum-processing-20261107/principal/THERMAL_SERVICE_THEOREM.md), SHA-256 `bb4e12ae7cc82ed68f94d4b162f6c9a85e08671fd88b805a510ee47058666b40`. The [version-bound hostile review](../work/protected-quantum-processing-20261107/challenges/auditor_thermal_service_final_review.md) passes its Sections 1–14 at their stated premises. This dossier supplies the formal synthesis, dependencies, novelty boundary and remaining operations.

## 2. Preserved capital and the change of architecture

Three earlier contracts remain distinct.

1. **N1388 powered native memory:** accepted local DATA confinement and many-hub descent, a physical two-site grouped-controller/reset construction, and an exponential-moment warm basin. Its exact compiler and controller-interface sources have completed whole reviews. Sparse output faults can now be shown to enter its warm basin explicitly; this is a useful transfer, not a new passive memory.
2. **N1694 three-body unary-clock memory:** an exact all-number-sector Hamiltonian representation, thermal majorants and an ideal complete isolated loader. Immediate and short-time noisy handoff do not establish long passive storage from generic noisy writer outputs. Neither the powered N1388 theorem nor this dossier's new thermal generator is its microscopic dynamics.
3. **The previous exact-H consumer:** protection from a specified interacting Gibbs resource and ideal logical access, with a rare-boundary channel estimate. It does not physically prepare that resource or earn generic noisy loading.

The refreshed research repository revision is `d490a9d4429a8152902cebb32fd67c1e4c9285b2`. All 17 refreshed governing science-source hashes match their earlier pinned files. [Source pins](../work/protected-quantum-processing-20261107/sources/REFRESHED_SOURCE_PINS.json) preserve this evidence. Historical candidate headings on exact N1388 files do not revoke their later completed acceptance.

The present strongest construction uses the actual sheaf codes of Li–Li–Han–Liu, with Gay–Granha Jeronimo's local expansion and transpose-complex machinery. It does **not** inherit N1694's clock Hamiltonian or assert their bath contracts coincide. A direct Tanner/CNOT specialization provides a second, simpler structural instantiation but lacks the new code's supplied non-Clifford gate family.

## 3. The finite code/energy construction

### 3.1 Exact imported code data

Use the physical convention of Li–Li–Han–Liu, Definition 2.1, equation (2.7): for a cochain complex, `H_Z=delta^k` and `H_X=(delta^(k-1))^T`, with the prescribed binary/trace-dual coordinates. GJ interchanges the X/Z labels; its parameter conclusions are Hadamard-invariant, but the actual physical cubic gate must retain Li's convention.

For each of Li's three actual degree-two complexes on a six-direction cubical quotient, require its specified fixed local PRS profiles, full-star compatible charts, and uniform product expansion for both the actual primal and coordinate-dual tuples. Its Proposition 3.3 and Section 3.4 verify these conditions and the parallel-walk expansion threshold used by GJ Sections 6–8. The rate of all three blocks comes from Li's cup-product subrank; GJ's separate sufficient Euler-characteristic rate inequality need not hold for every profile.

These inputs give a fixed-field, fixed-degree family with constant rate and linear distance. More importantly for this construction, they give the *actual local complexes*, not merely a code with equally good parameters. See the [exact import audit](../work/protected-quantum-processing-20261107/machinery/thermal_import_audit.md).

### 3.2 Quantitative local descent: a proved refinement

Fix a closed degree-j cochain with block support A. A vertex is active when some correction on its upward star strictly reduces block weight. Let B be the active vertices. Write GJ's constants as

\[
 r_\ell=n_-\kappa_{t-\ell,j-\ell},\quad
 c_{j\ell}={(j-\ell)!\over\prod_{m=\ell}^j r_m},\quad
 D_{j\ell}=\max_{v\in X(\ell)}|X_{\geq v}(j)|.
\]

Their support recursion remains valid at an ell-face containing an inactive vertex: every correction above that face is also allowed above that vertex. Only faces all of whose vertices are active need an additive slack. On one such face, `r_ell D_jell` bounds the missing inequality. Carrying those slacks through the **same** upward recursion of Proposition 6.2.2 gives

\[
 |A|\leq \lambda L_j|A|+Q_j{|A|^2\over Z_j}+C_j|B|,
\qquad
 C_j=\sum_{\ell=0}^j c_{j\ell}r_\ell
             D_{j\ell}D_{j0}\binom j\ell.
\]

The exceptional-face incidence is bounded by assigning an active vertex; each j-face has only `binom(j,ell)` ell-faces through a fixed vertex. Consequently

\[
 |B|\geq {1-\lambda L_j\over2C_j}|A|
 \quad\hbox{if}\quad
 0<|A|\leq{1-\lambda L_j\over2Q_j}Z_j.
\]

This proves **density** of improving bounded-star moves, not merely existence of one move. All constants are independent of the global tower size. The [full derivation](../work/protected-quantum-processing-20261107/machinery/active_vertex_refinement.md) and [independent check](../work/protected-quantum-processing-20261107/challenges/auditor_thermal_processing.md) retain the exact source recursion.

### 3.3 Exact stable local CSS duality

**Theorem A.** Let `F` be one of the compatible fixed-dimensional cosheaves just specified. Let `K` be its actual kernel cosheaf from GJ equation (7.4), with inverse-transpose local charts as in Theorem 7.2.1. After a constant-factor product-ancilla extension, the degree-k code of F and the degree-(t-k) code of K are related by a type-swapping CSS Clifford whose coordinate matrix and inverse have bounded propagation and bounded row/column incidence. The extension introduces no auxiliary logical qubits.

**Proof.** Use the actual anchored arrays

\[
 A^{r,p}=\bigoplus_{f\leq u,\ \dim f=r,\ \dim u=p}F(u)^*,
 \qquad n_{\rm chain}=p-r,\qquad d=T+\Delta.
\]

The source proves `T^2=Delta^2=0` and `T Delta=Delta T`. Characteristic two gives `d^2=0`.

At fixed upper face u, the horizontal differential Delta is an ordinary finite cube cochain differential. Its critical space consists of constant degree-zero copies. T preserves that subcomplex and induces the physical transpose differential `delta^T`. At fixed anchor f, the vertical differential T is exact below its top degree by Theorem 7.2.1; its top kernel is exactly K(f). Delta preserves those top kernels and induces K's cochain differential.

Put either finite local fiber complex into a paired Gaussian normal form. Let h be its normalized contracting homotopy, i its critical inclusion, and p its critical projection. Thus `h^2=hi=ph=0`. The other differential, denoted delta here, preserves the critical range. Define

\[
 h'=(I+h\delta)^{-1}h,\qquad
 p'=p(I+\delta h)^{-1}.
\]

These inverses are finite polynomials: `h delta` strictly lowers the finite p-filtration in the horizontal reduction and strictly raises it in the vertical reduction. The contraction identities give `dh'+h'd=I-ip'`, `p'i=I`, and `h'^2=p'h'=h'i=0`.

For every old contractible pair `d0 a_i=b_i`, take `a_i'=h'b_i` and `b_i'=d a_i'`. Together with the unchanged critical inclusion these are an actual basis. Relative to the old local basis, its change matrix is `I+Q`, strictly triangular in p. In the vertical case, `b_i` has p one below `a_i`; hence `delta a_i` is also strictly above its original target. Therefore `Q^(t+1)=0`, and the inverse is the finite geometric sum. Each factor has a bounded local cone; finite filtration height bounds both forward and inverse propagation and incidence.

At physical chain degree k a binary coordinate change is a CSS Clifford: X vectors transform by the matrix and Z vectors by its inverse transpose. Adjacent-degree changes only replace check generators. A canceled pair from k to k-1 contributes a fixed `|0>` qubit; a pair from k+1 to k contributes `|+>`. The two cochain conventions differ by a global Hadamard. This produces the claimed type-swapping map with the precise product ancillas inherited from the normal forms. Trace-dual field coordinates make all binary pairings exact. Appending product states preserves absolute distance and adds no logical modes. ∎

A bounded-propagation Clifford need not be called a finite-depth circuit on the memory alone. If actual application is needed, sparse matrices A and A-inverse have the clean-work circuit `|x>|0> -> |x>|Ax> -> |0>|Ax> -> |Ax>|0>`, with fixed-depth edge-colored CNOT additions and O(n) temporary work. Its full-Hilbert action is not A tensor identity on arbitrary work states. The preferred construction never executes that map during a gate; it defines bounded-support pulled-back Paulis algebraically and keeps the original DATA coordinates.

[Full frozen derivation](../work/protected-quantum-processing-20261107/machinery/dual_sector_local_energy_v1.md), [convention addendum](../work/protected-quantum-processing-20261107/machinery/DUAL_ENERGY_V1_CONVENTION_ADDENDUM.md), and [hostile algebra audit](../work/protected-quantum-processing-20261107/challenges/auditor_stable_duality.md) provide the complete normal-form details.

### 3.4 Two commuting energies on the original gate code

In the original Li DATA coordinates, append exactly the normal-form product ancillas. Let `U_F` count nonzero cochain Z-syndrome blocks plus original Z-ancilla defects. Let C be Theorem A's type-swapping Clifford, and set

\[
 U_K=C^\dagger(\hbox{K cochain Z-block energy
                         + target Z-ancilla defects})C,
 \qquad U=U_F+U_K.
\]

`U_F` is a function of the complete original Z stabilizer group; `U_K` is a function of the complete original X group. Hence all terms commute and their common ground space is **exactly** the original DATA code with its fixed product ancillas.

Original F X-star corrections lower `U_F` and commute `U_K`. K X-star corrections pull back to original Z Paulis, lower `U_K` and commute `U_F`. The two instances of Section 3.2 apply in syndrome degrees k+1 and t-k+1, both below t. Add single-site corrections for the corresponding product-ancilla defects. At sufficiently small linear total energy there are at least `kappa U` improving labels, each lowering integer U by at least one, with fixed bounded support and incidence.

Moreover every sufficiently low-energy syndrome can be repaired by at most U such moves. If each has support at most L, a physical Pauli syndrome correction of weight at most `L U` exists. This is a **global low-energy repair bound**, not confinement within an unknown error-history class. It makes an energy-only basin possible. It does not certify the intended logical input: a wrong encoded logical state also has zero energy.

The common ground code retains constant rate and linear distance in the total augmented size. The original Li bounded-incidence cubic DATA circuit, tensored with identity on the added memory ancillas, still preserves it. Overlapping physical cubic gates are edge-colored into fixed depth. Their optional repetition encoding is omitted, since literal single-layer transversality is unnecessary here and would require another energy/descent transfer.

## 4. Complete physical-model assumptions

The following are requirements of the proved model, not conclusions about an available refrigerator or ordinary material.

**Code and local energy.** There is an explicit infinite family of binary stabilizer codes on n total memory qubits, with distance at least `delta n`. The commuting integer energy `U=sum u_v` has O(n) nonnegative terms of bounded norm, bounded body and incidence, and the exact augmented code as ground space. Every term is a finite local function of the declared commuting stabilizer checks; U is therefore syndrome-diagonal and independent of logical labels. For `U<=u_descent n`, at least `kappa U` labels in a catalog of at most `M0 n` Hermitian Pauli updates strictly lower U. Each update changes U by at most a fixed D. Every such low-energy syndrome has a correction of weight at most `C0 U`, with C0 enlarged to at least one. Section 3 proves these properties for the augmented gate codes.

**Exact Hamiltonian and reservoir.** Set `H_n=J U`, J>0 fixed. A local integer syndrome table has the exact Walsh expansion

\[
 u(S)=\sum_{A\subset R}\widehat u(A)\prod_{a\in A}S_a,
 \qquad
 \widehat u(A)=2^{-|R|}\sum_\sigma u(\sigma)
                                      \prod_{a\in A}\sigma_a.
\]

Dependent-check strings with zero projectors cause no problem. Thus the Hamiltonian has an exact finite Pauli description; a fixed rescaling clears dyadic denominators if integer coefficients are desired. Local table size and Pauli term count may be enormous fixed constants.

For a catalog Pauli `P_a`, let `Pi_(a,d)` select its change d of U. Because all energy terms commute, this projector depends only on the bounded affected-check neighborhood. The full jump support, including that neighborhood, is charged. Use `A_(a,d)=P_a Pi_(a,d)` with paired rates

\[
 \gamma\leq r_a(-d)\leq\Gamma,\qquad
 r_a(d)=e^{-\beta Jd}r_a(-d),\quad d>0,
\]

and bounded zero-energy rates. A bounded-incidence diagonal Lamb shift is allowed. This defines an **exact engineered GKSL generator** `L_beta` with Gibbs stationarity. No Gibbs initial state is required. It is a Davies-form construction, not a claim that a weak-coupling approximation holds for exponential times.

**Retained environment and weak disturbances.** In addition to that nominal Markov reservoir, retain one bath B throughout writing, gates, storage and extraction. It may have arbitrary internal CPTP evolution and correlations. Joint HP perturbations have at most q memory qubits per term and satisfy

\[
 \sup_i\sum_{Z\ni i}\|\mathcal N_Z^*(t)\|_{\rm cb}\leq\eta,
 \qquad \mathcal N_Z^*(I)=0.
\]

The complete joint interval dynamics must be CPTP; the positive killed compression must exist. Finite bounded GKSL joint models satisfy this directly. Infinite/unbounded baths require their actual domain and normality hypotheses. Bath-only evolution is retained exactly and its norm is not charged as a DATA perturbation. There is no fixed noise-partner graph requirement.

The **nominal Markov thermal reservoir and the retained weak bath are different objects**. The former is a stipulated reservoir primitive, for example with fresh causal output modes and no return of past outputs. The latter may retain memory and correlations. Combining them does not prove a finite microscopic thermal bath realization or permit uncontrolled feedback from the nominal reservoir.

**Gate controls.** A specified finite family of code-preserving physical unitary circuits has bounded depth, body and partial/suffix spread B. During each pulse the same H, cooling channels, retained B and perturbations continue. After the ideal control is removed in its interaction picture, the integrated sum of joint disturbance norms is at most `mu n`. Calibration error must satisfy this actual integrated budget. A fixed fractional calibration error is not removed by making a pulse shorter. If stochastic control flags are used, require independent Bernoulli flags or an actual reference-uniform all-subset fault-expansion bound; one unprotected global bit setting n strong gates is excluded.

**Ports.** The actual immediately decoded writer channel has declared half-diamond error `epsilon_in`. Its actual output must satisfy the support/moment or positive admitted-subchannel conditions below. A physical readout has a separately declared error `epsilon_read`. Quantum I/O machinery can supply paid gateways only under its compatible noise/access contract. Bare unknown ports retain their first/last exposure floors. No ideal decoder is silently counted as a physical readout.

## 5. Warm protection and correlation-safe handoff

### 5.1 Formal theorem

**Theorem B.** Under Section 4, choose `s>0` and an energy cutoff `u_c>0` smaller than the descent threshold and so small that `2 C0 u_c<delta`, with a strict fixed margin. Let `P=1_(U<u_c n)`. Fix deterministic minimum same-syndrome representatives and the corresponding full logical/syndrome frame. There are fixed C and boundary width K such that the following holds.

Put

\[
 a=\gamma\kappa(1-e^{-s}),\quad
 b=M\Gamma e^{-\beta J}(e^{sD}-1)+C_s\eta,\quad
 \nu_{\rm eq}=s b/a,
\]

where M counts the bounded positive-change jump components per cell and `C_s` is a fixed local relative-observable bound. If an arbitrary joint positive subnormalized initial state, including logical–gauge–bath–reference correlations, is P-supported and has

\[
 \operatorname{Tr}e^{sU}\rho_0\leq e^{\nu_0 n+O(1)},\qquad
 \Delta_H=s u_c-\max(\nu_0,\nu_{\rm eq})>0,
\]

then the actual final logical/reference marginal differs from its actual initial marginal in half trace norm by at most

\[
 C nT e^{-\Delta_H n/2+O(1)}.
\]

Uniform reference and input bounds give the corresponding channel statement. The physical constants are chosen before n and T. The same choices work below a sufficiently low fixed temperature and below a sufficiently small fixed perturbation strength. For a positive writer channel with immediate decoded error `epsilon_in`, the end-to-end error adds `epsilon_in` **without a dilation/decoupling loss**. Positive discarded writer branches add their complete mass. A merely coherent energy leakage tail needs its own clipping estimate, typically a square root.

### 5.2 Proof

The exact spectral jump identity gives

\[
 \mathcal L_\beta^* e^{sU}
 =e^{sU}\sum_{a,d}r_a(d)(e^{sd}-1)\Pi_{a,d}
 \leq(-aU+b_{\rm th}n)e^{sU}.
\]

Every active label supplies a fixed negative decrement; all additional negative terms can be discarded. Positive steps are suppressed by `e^(-beta J)` and have a bounded catalog count. For a q-qubit perturbation, factor out unaffected commuting energy. The affected energy is between zero and a fixed constant, so complete norm control yields `+/-N_Z^*e^(sU)<=C_s ||N_Z^*||cb e^(sU)`. Summing gives the displayed b independently of bath dimension.

Compress the **full** physical generator to P. It yields a CP/TNI evolution; its extra loss is positive. Since P commutes U, deleting outgoing gains cannot increase the positive-observable drift. For a nonzero positive subnormalized state, `x=Tr e^(sU)rho`, scalar spectral Jensen gives (the zero state is trivial)

\[
 \operatorname{Tr}Ue^{sU}\rho\geq x\log x/s,
 \quad
 \log x(t)\leq\nu_{\rm eq}n+
                  (\log x(0)-\nu_{\rm eq}n)e^{-at/s}.
\]

Every exiting local leg starts at `U>=u_c n-K`. Thus boundary mass is at most `e^(sK)e^(-Delta_H n+O(1))`. Local full-versus-compressed generator differences vanish on the strict interior. Gentle compression bounds their trace norm by a fixed multiple of their complete norm times the square root of boundary mass. Their complete norms sum to O(n); bath-only terms have no boundary defect. Duhamel comparison with the actual full CPTP propagator yields the claimed bound. The coherent square-root exponent loss is retained.

For retained syndrome states sigma,tau, two fixed canonical corrections and a connecting local Pauli have total weight at most `2 C0 u_c n+q<d_n`. Their zero-syndrome product is a stabilizer. This proves logical neutrality for every compressed system leg, including complete-loss terms, syndrome coherences and bath coefficients. Therefore the entire killed map is `id_L tensor K_GB`, with K CP/TNI.

For an arbitrary correlated initial state, set `R=I-K^*(I)>=0`. Initial LR minus killed final LR equals the positive operator

\[
 \operatorname{Tr}_{GB}
 [(I_{LR}\otimes\sqrt R)\rho(I_{LR}\otimes\sqrt R)].
\]

Its trace is exactly survival loss. Actual-versus-killed error controls that loss too, proving the half-trace bound and direct writer composition. **Never normalize the killed state:** postselection could bias a logical state correlated with the gauge. ∎

## 6. Finite gates: signed expansion, positive comparison, same bath

**Lemma C (full-module positive repair).** Let an actual joint CPTP gate channel Gamma have, on its whole promised logical/gauge/bath input module, an HP approximation

\[
 \Gamma_0=\operatorname{Ad}_{G_L}\otimes\mathcal C_0,
 \qquad \|\Gamma-\Gamma_0\|_\diamond\leq\delta_g,
\]

whose output lies in a chosen warm gauge subspace Q. The approximation need not be positive. Define

\[
 \mathcal C_g(\theta)=\operatorname{Tr}_L
 [Q\Gamma(I_L/d_L\otimes\theta)Q].
\]

Then `C_g` is CP/TNI, acts on the **same actual** gauge/bath algebra, has the required warm support, and

\[
 \|\Gamma-\operatorname{Ad}_{G_L}\otimes\mathcal C_g\|_\diamond
 \leq2\delta_g.
\]

**Proof.** Apply mixed-logical initialization, Q-compression and logical partial trace, all complete contractions, to `Gamma-Gamma0`. Their action on Gamma0 is C0, so `||C_g-C0||diamond<=delta_g`; the direct triangle gives the result. Its missing trace is at most delta_g. Optional TP completion costs a further delta_g, but no completion or bath reset is needed in the service proof. No Choi-dimension factor or gentle square root appears. Factorization on one tested state would be insufficient. ∎

To obtain the hypothesis, perform a joint Duhamel expansion around the ideal bounded-depth control and actual bath-only propagators. Count H, cooling, retained bath couplings and calibration during the pulse. With integrated norm at most `mu n`, its order-r term has complete norm at most `(mu n)^r/r!`. After the ideal suffix, r insertions add at most `B q r` physical error support. A pre-energy cutoff `U<=u_pre n` supplies canonical error weight at most `C0 u_pre n`. Thus the low-order terms land in a common correctable error span with support bounded by

\[
 w_{\rm post}n\leq B C_0u_{\rm pre}n+Bq r.
\]

If energy created per supported qubit is at most `D_E`, enlarged to at least one, choose small fixed `u_post<u_c`,

\[
 u_{\rm pre}={u_{\rm post}\over4D_E B C_0},\qquad
 \alpha={u_{\rm post}\over4D_E Bq},\qquad
 \mu\leq{\alpha\over8e}.
\]

Reserve strict distance margins, for example those in the consolidated theorem's Section 6. For `r<=floor(alpha n)`, output energy is below `u_post n`, and the original error leg differs from its fixed canonical representative by a stabilizer. This proves **the full-module factorization** required by Lemma C, including off-diagonal syndromes and arbitrary bath/reference coefficients. The signed tail is bounded by

\[
 \delta_g\leq\sum_{r>\lfloor\alpha n\rfloor}
                      {(\mu n)^r\over r!}
 \leq 2e^{-\alpha n\log8}.
\]

The physical ideal gate may leave the storage basin midway. Storage is not invoked during that path; all intervening environmental action is counted by the finite-pulse expansion. Fixed sufficiently strong controls can make mu small independently of n. Their strength, calibration and program distribution are charged resources. A stochastic pulse model needs the all-subset assumption of Section 4, not just a marginal fault probability.

## 7. Main processing theorem and proof

**Theorem D (repeatable thermal non-Clifford service).** For the explicit augmented three-block code family of Section 3 and the complete physical model of Section 4, fixed positive constants can be chosen as follows. Use Theorem B's low-energy basin, the gate parameters of Section 6, and choose beta large and eta small so that

\[
 \nu_{\rm eq}\leq s u_{\rm pre}/4.
\]

Set

\[
 \tau_c={s\over a}\log{4u_{\rm post}\over u_{\rm pre}}.
\]

An admitted writer has moment at most `exp(s u_post n+O(1))`. Every actual gate burst is preceded by at least tau_c of cooling/HOLD. For g bursts and total HOLD/dwell time T, the final decoded logical channel satisfies

\[
 \epsilon\leq\epsilon_{\rm in}+\epsilon_{\rm read}
 +\delta_W+2\epsilon_W
 +C nT e^{-s(u_c-u_{\rm post})n/2+O(1)}
 +g\bigl(2e^{-s u_{\rm pre}n/4}+2\delta_g\bigr).
\]

Here delta_W is the complete mass of a discarded positive writer branch, and epsilon_W is an optional full-joint approximation of that writer model, with the conservative factor shown. Omit those terms when the actual writer itself meets the exact support/moment contract. Constants and controls are fixed before n,T,g. Distinct smaller exponents absorb rounding and fixed prefactors.

The logical input may be arbitrarily entangled with an external reference and correlated with the admitted gauge/bath. The comparison retains the actual bath. On the selected linear number of Li logical ports, the gate is the requested addressed product of CCZs, **provided the remaining binary field components and complementary logical coordinates start in computational zero as required by equations (3.226)–(3.227)**. The physical gate preserves the whole code; the generic service theorem also applies to its actual full logical unitary, without claiming that it is the same selected CCZ product on every full logical input.

**Proof.** The moment law after a cooling dwell gives `log x<=s u_pre n/2`. The pre-gate tail above `u_pre n` is at most `exp(-s u_pre n/2)`. A proof-only gauge projection costs at most `2exp(-s u_pre n/4)` in complete trace norm and cannot increase the exponential moment.

Apply the actual pulse, comparing it with Lemma C's CP/TNI exact-logical warm map. The latter has post-energy below `u_post n`, so its moment is at most `exp(s u_post n)` times its trace. Cool again for tau_c. This closes the same inequality with fixed margins.

Carry **only CP/TNI maps**: the admitted writer, killed dwells, energy filters and positive gate surrogates. None is normalized. The scalar law already holds for trace at most one. The entire comparison has the desired logical unitary tensored with a CP/TNI gauge/bath map, valid for correlated inputs. Complete-contraction telescoping gives the displayed full-versus-comparison bound. The positive logical deficit is exactly lost mass, as in Theorem B, converting it into the half-diamond logical estimate. Add actual decoded writer and physical readout errors contractively. ∎

### A concrete useful output: a protected logical magic buffer

Prepare the selected logical ports in plus states and the required complements in zero. One addressed parallel CCZ burst produces a tensor product of Theta(n) logical CCZ magic states. Theorem D protects their collective state during long storage and Theorem E returns it at encoded ports. This is a useful non-Clifford resource buffer within the same model. The physical CCZ controls and polynomial gateways remain paid resources; no new constant-overhead magic factory, distillation advantage or universal native gate set is claimed.

### Noisy writer admission without Gibbs domination

For a final-release positive fault instrument on at most `c_W n` locations, require the operator inclusion intensities `sum_(F superset A)W_F^*(I)<=p_W^|A| I`. A location has bounded output spread b_W and changes energy by at most `D_E b_W` per fault. Then

\[
 \mathbb E z^{|F|}\leq[1+p_W(z-1)]^{c_W n},\qquad
 \nu_W(s)=c_W\log[1+p_W(e^{sD_Eb_W}-1)].
\]

Keep `|F|<=zeta_W n` with zeta_W below the common energy/distance margins. Chernoff gives exponentially small discarded mass for sufficiently small fixed p_W; the admitted unnormalized moment is `exp(nu_W n)`. Every retained branch belongs to one common correctable error span, with arbitrary bath coefficients. This earns the contract from a real supported release, rather than applying it to an arbitrary unprotected polynomial-depth encoder. Its bath need not be Gibbs or thermal.

### Corollary at the earlier accepted structural code input

The same thermal completion applies directly to the accepted Tanner DATA local-distance energy, retaining **both** the radius and energy cutoffs used in N1388. Two identical CSS blocks have a direct transversal CNOT service. No original controller/forest operation is needed in that changed DATA-only Hamiltonian. This is a useful fallback and a simpler proof of a different thermal model; it is not a native CNOT theorem for the old controller or a noisy-writing theorem for N1694.

## 8. Resource accounting and comparison target

| Resource | Earned bound or explicit limitation |
|---|---|
| Memory | O(n) qubits, including all added product-state memory ancillas; constant rate along the explicit size sequence |
| Hamiltonian | O(n) exact finite-table Pauli terms, bounded body/incidence with potentially enormous fixed constants |
| Cooling | O(n) tagged resolved local jump channels; engineered spectral response, maintained temperature and Markov/no-return assumption are primitives |
| Gate burst | O(n) physical control locations, fixed depth and duration; fixed peak strength large enough for the integrated local disturbance budget |
| Cooling dwell | Fixed `tau_c=(s/a)log(4u_post/u_pre)`, possibly very large |
| Classical/program access | Actual local gate selectors, protected distribution, code tables and acquisition costs are charged; no globally faulty command bit for free |
| I/O | Restricted isolated-staging encoded-port closure in Section 12, with polynomial paid resources; CFG circuit-noise/classical/isolation primitives retained; no ideal receiver counted as bare hardware |
| Geometry | Bounded interaction-graph range/degree; no bounded-density Euclidean embedding or literal three-body realization |
| Microscopic environment | No exponentially accurate finite-bandwidth/finite-bath implementation of the nominal Markov generator is supplied |
| Advantage | No proved improvement in complete space, work, precision, threshold, refrigeration or feasibility over equally equipped active/autonomous FT |

During a nominal, unforced, fixed-H HOLD, net system-energy exchange is `Tr H rho(T)-Tr H rho(0)=O(n)`, independent of duration. O(nT) jump opportunities are **not** O(nT) net heat. Additional driving/noise can supply a compensating energy current; HP generator norms alone do not determine a thermodynamic work/heat split. Work during control, refrigeration efficiency, reservoir preparation, bandwidth and correlations remain to be quantified. The model does not establish a thermodynamic saving.

The independent finite parameter check deliberately uses illustrative structural constants rather than actual Li/Tanner data. Its severe sufficient control/noise ratios demonstrate why existence of fixed constants is not evidence of an economical device. No numerical physical threshold is reported.

A fair active comparator receives the same gates, resets, cooling, routing, source quality, classical hardware, timing and isolation. It can retain data in an ordinary FT representation or use a stronger qLDPC architecture. The existing 2D autonomous universal QCA is also a mandatory comparator, at its actual discrete-time noise and initialization contract. Removing a correction schedule during HOLD is not, by itself, a total-cost advantage.

## 9. Strongest obstructions and repaired inferences

### 9.1 Bare unknown inputs impose a sharp floor

**PROVED obstruction, established quantum-I/O phenomenon.** Suppose k bare unknown qubits first undergo independent dephasing `Z_p=(1-p)id+p Ad_Z`, `0<p<=1/2`, before any redundancy. For every downstream CPTP procedure R,

\[
 {1\over2}\|R\circ Z_p^{\otimes k}-\operatorname{id}\|_\diamond
 \geq 1-(1-p)^k.
\]

Feed half a maximally entangled state. The entanglement fidelities of R after the different Pauli inputs are Bell-basis diagonal entries of its normalized positive Choi state and sum to one. The largest dephasing branch probability is `(1-p)^k`, so final entanglement fidelity is at most that value. The Bell-projector test proves the lower bound; identity recovery attains it. No memory size or subsequent processing removes information lost before redundancy.

One bare input therefore retains an O(p) floor. For k proportional to n, a global error floor can approach one. Protected source/receiver ports or an honest endpoint-noise target are essential. Known-state preparation does not solve this arbitrary-unknown-input problem.

### 9.2 Exact reduced writer accuracy does not generally control a correlated bath

Let `Omega_+` and `Omega_-` be equal/unequal classical correlations of gauge qubit A and bath qubit B, with both marginals maximally mixed. Both writers `rho_L -> rho_L tensor Omega_+/-` have the same exact reduced system channel and bath marginal. Under the same Hamiltonian `H=g X_L (I+Z_A Z_B)/2`, time `pi/(2g)` gives logical X for one resource and identity for the other.

This defeats composition based only on reduced writer accuracy in a correlation-sensitive model. It is not a counterexample to the original protected memory. Theorem B repairs the interface by proving uniform `id_L tensor CP/TNI` behavior on the entire admitted module. That is why a reduced writer estimate suffices **there**, without refreshing the bath.

### 9.3 Equilibrium bottlenecks do not admit every decodable state

A reversible five-state path `a0-a1-b1-b2-c` has stationary weights `pi(a0)=pi(c)=(1-3epsilon)/2` and the three middle weights epsilon. Use neighbor Metropolis probabilities `(1/3)min(1,pi_j/pi_i)`. The bottleneck ratio for `A={a0,a1}`, `B={b1,b2}` is `4epsilon/(1-epsilon)`. Yet a1 reaches c in three steps with probability exactly `1/27`. A writer with mass p on a1 has immediate A-support but fast failure mass at least p/27.

This disproves the generic all-state inference from a stationary bottleneck estimate. It is not a bounded-strength lattice counterexample: the energy difference needed to make epsilon small grows. No failure of N1694 follows.

### 9.4 Gibbs domination can be both unaffordable and sufficient, in different regimes

For a product thermal bit distribution with excitation a, independent bit flips p raise it to `b=a+p(1-2a)`. Global domination can require `(b/a)^n`, exponential in volume. This defeats an unqualified shortcut to the old sublinear-barrier memory theorem; it does not prove that memory fails.

For a genuinely **linear** barrier, that same volume-scale cost can be affordable. Under Gibbs-preserving dynamics, any normalized state supported on `U<=u_pre n` obeys `rho<=exp(beta J u_pre n)exp(-beta H)`. A boundary at `U>=u_c n` is therefore bounded by `exp[(log2-beta J(u_c-u_pre))n]` on n qubits. At sufficiently low fixed temperature this already gives warm storage, assuming the logical/boundary hypotheses. Thus storage alone does not justify claiming a new protection principle. The descent/moment machinery earns re-cooling, perturbation tolerance and sustained gate workloads.

### 9.5 Further rejected shortcuts

- Global qLTC soundness alone does not give bounded-support physical descent in the transpose sector. The exact stable-duality energy construction resolves that gap by changing the Hamiltonian and adding specified ancillas.
- One improving move does not imply linear active density; Section 3.2 supplies the missing quantitative argument.
- A signed truncated fault expansion is not a prepared positive state. Lemma C supplies an actual positive comparison.
- Normalized surviving states can bias logical/gauge correlations. The proof keeps every comparison CP/TNI and subnormalized.
- The ideal partial gate path need not be protected. The finite-pulse proof counts all intervening dynamics and checks correctability at its endpoint.
- A short-time handoff cannot be iterated as long storage without a proved restoring operation or drift.
- Replacing the memory's Hamiltonian approximately does not preserve exponential lifetime at fixed hardware accuracy: ordinary simulation errors can grow as time times approximation error.
- Transporting a gate through code duality gives a conjugate of the same logical subgroup; it does not automatically add a useful independent Hadamard or a universal gate set.

## 10. Existing machinery, primary comparators and novelty audit

| Primary source and exact location | Imported or competing result; applicability and boundary |
|---|---|
| M. Crainic, [math/0403266v1](https://arxiv.org/html/math/0403266v1), Main Perturbation Lemma 2.4 and special-retract statement 3.2 | Perturbed contraction identities are established homological algebra. Local Gaussian contraction gives a special retract; finite filtration gives a polynomial inverse. Paired-basis locality and CSS energy synthesis are checked additionally. |
| W. Gay and F. Granha Jeronimo, [2609.20780v1](https://arxiv.org/html/2609.20780v1), Lemmas 6.1.3/6.2.1, Proposition 6.2.2, Theorem 6.3.1, Lemma 6.4.1; equations 7.1–7.6 and Theorem 7.2.1 | Exact local filling, support recursion, anchored arrays and actual-coordinate transpose exactness. Section 3 supplies density and stable-energy derivations, rather than inferring a local decoder from global repair. |
| Y. Li, Z. Li, Z. Han and Z.-W. Liu, [2609.26691v3](https://arxiv.org/html/2609.26691v3), Definition 2.1, Proposition 3.3, equations 3.20/3.31–3.33, Section 3.4 and equations 3.223–3.227 | Actual complexes, simultaneous primal/dual charts and bounded-incidence cubic circuits. The selected CCZ ports retain their zero-initialization restrictions. |
| Y. Hong, J. Guo and A. Lucas, [2403.10599v3](https://arxiv.org/html/2403.10599v3); [Nature Communications16,316(2025)](https://doi.org/10.1038/s41467-024-55570-7), Theorem B.8 and Appendices E.2–E.3 | Passive qLDPC Gibbs sampling and finite-depth measurement-free correction precede this work. Its formal HGP mixing result uses a special weighted start. Generic Metropolis correction is not a discovery here. |
| H. Bombin, R. W. Chhajlany, M. Horodecki and M. A. Martin-Delgado, [0907.5228v2](https://arxiv.org/html/0907.5228v2); [NJP15,055023(2013)](https://doi.org/10.1088/1367-2630/15/5/055023), Sections VI.5 and VIII.3 | Sudden-noise tolerance, thermal storage and fast transversal gates already coexist in higher-dimensional color-code proposals. Thermal protected computation itself is established prior architecture. |
| Balasubramanian–Davydova–Lin, [2605.10943v1](https://arxiv.org/html/2605.10943v1), Theorems 2.6/3.16/5.13 and Corollary 5.14 | 3D passive-memory comparator with thermal encoding and separate initialization. The present nongeometric model does not supersede its geometric claims. |
| Dünnweber–Styliaris–Trivedi, [2601.20818v3](https://arxiv.org/html/2601.20818v3), formal Theorem 1 | Existing 2D autonomous universal computation with polylogarithmic overhead. Its continuous-time discussion is an outline. |
| Zhao–Yuan–Han–Liu, [2609.39965v3](https://arxiv.org/html/2609.39965v3), Theorem 1(1) versus 1(2) | Soundness yields local-stochastic residuals; confinement alone gives decoder-defined logical success without that residual guarantee. Neither is unknown-state quantum I/O. |
| Christandl–Fawzi–Goswami, [2408.05260v3](https://arxiv.org/html/2408.05260v3), Lemmas 40–42; Theorem 43; Theorem 53 with Definitions 47–48/52 | Exact noisy quantum-I/O machinery. Literal Theorem 53 has an operational communication metric. The direct one-sided lemma proof supplies the stronger retained-auxiliary processing statement under its actual stochastic staging premises. |
| Rakovszky–Placke–Breuckmann–Khemani, [2412.09598v2](https://arxiv.org/html/2412.09598v2), Theorem 1 | Approximate stationarity of projected equilibrium under the stated Kraus/bottleneck hypotheses. It does not admit every decodable initial state. |
| Yu–Wei, [2510.14160v2](https://arxiv.org/html/2510.14160v2), Theorem 1 and Propositions III.1–III.2 | Localization under an energy/variation budget. A persistent bath does not automatically meet that budget. |
| Cubitt–Montanaro–Piddock, [1701.05182v4](https://arxiv.org/html/1701.05182v4), Proposition 29 and Section 8.5/Theorem 32 | Simulation error `2epsilon t+4eta` with local-encoding/leakage premises. Fixed approximation accuracy cannot supply exponential lifetime for free. |

Eldar's [1911.04461v3](https://arxiv.org/html/1911.04461v3) predates the combination of qLTC thermal error control and shallow decoding for circuit-complexity bounds. Its static nearly-constant-temperature result is not imported as a noisy processing theorem. The [late-primary audit](../work/protected-quantum-processing-20261107/principal/HPL_IMPORT_AND_CONNECTIONS.md) records the exact HPL applicability and screened connections.

**Derived here:** additive-slack active density; the exact stable local normal form with correct ancillas/types; two-sector energy on the actual recent gate code; correlation-safe handoff; positive finite-pulse comparison; and sustained service composition. Many ingredients are standard. Their names, scalar estimates and coding parameters are not relabeled as discoveries. First historical priority for the combined result remains **UNKNOWN**.

Recent Zenodo title/metadata queries and exact record checks are preserved in the machinery manifests. They were bounded discovery searches with noisy first pages. Unread titles are not cleared proofs, and failure to find an equivalent theorem is not an absence/priority theorem. Soryun IV is a meaningful non-Markovian common-recovery comparator under a different fixed-domain spatial-regularity envelope; independent local bath faults do not automatically meet it.

## 11. Decisive remaining problems and constructive attacks

1. **Microscopic environment for the same service.** Replace the exact nominal GKSL primitive by a specified finite-bandwidth joint Hamiltonian/environment. Prove the admitted joint basin and error bound for exponential lifetime, including writing and repeated controls. A finite-time weak-coupling approximation is insufficient. Uniformity over all weak retained-bath states relies on the present nominal cooler; it cannot simply be transplanted to a purely passive finite bath.
2. **Original three-body clock model.** Prove nonstationary control of target defects and every clock-number sector after fixed-rate noisy writing. Promising attacks are a local clock/syndrome Lyapunov correction or a spacetime witness estimate using the exact dressing and clock gaps. Global Gibbs order pays volume and is inadequate for the old sublinear protection exponent. Clock faults are not absent checks.
3. **Small primitive costs.** The new energy/cooling channels have potentially huge fixed support and table counts. An exact low-body/controller realization must preserve the nonstationary proof. The accepted native compiler is a plausible alternate route, but actual controller/frame/access and gate-service specialization must be checked before claiming small-body hardware.
4. **Direct universal operations.** The selected CCZ service is earned. Compatible Clifford/Hadamard, ancillary state, measurement and extraction services still need proofs. Transporting a gate through duality does not add a new logical generator. Paid active gateways are inherited machinery and do not demonstrate a native thermal universal processor or a cost gain.
5. **Matched resource advantage.** Choose a workload, finite codes and rates. Charge acquisition, ports, locality, precision, bandwidth, refrigeration, reset and readout. Compare against active qLDPC and autonomous QCA with the same primitives. The current constants and polynomial staging may remove any advantage. A rigorous analytical advantage would suffice; a laboratory demonstration is not a blanket prerequisite.
6. **Larger magic-resource opening.** [Wei–Han–Li–Liu2609.40220v1](https://arxiv.org/html/2609.40220v1) connects protected low-energy spaces to intrinsic nonstabilizer circuit complexity. A more consequential capability would be an efficient fault-tolerant extractor of useful non-Clifford resources from a protected non-Abelian thermal phase at positive rate and controlled full-cycle cost. NLTM alone supplies neither that extractor nor its noisy basin or advantage. Existing gauging/magic-fountain protocols are a mandatory baseline; the unresolved step is their noisy thermal acquisition/extraction and full-cycle cost contract. This connection was screened, not solved or awarded a capability score.

The nearest precise opening is a useful physically specified realization of the derived warm processing service, or a comparable nonstationary theorem for the original clock model. This round completes a mathematical bridge; it does not establish a more feasible or lower-cost quantum computer.

## 12. Closed WRITE/READ at paid encoded ports

**Theorem E (restricted hybrid port closure).** Add the following explicit primitives to Theorem D: isolated active staging obeying CFG's independent circuit-stochastic model at `cp<1`; its computational scheme, including the cited scheme's noiseless classical-processing assumption; matched parallel short SWAP links for all n memory qubits; and already computationally encoded sender/receiver ports. Outside the short links, staging has no coupling to the memory's retained bath B. The bath remains on the original memory hardware throughout.

Then WRITE and READ close with exponentially small internal error and polynomial paid staging/port resources. This is a proved mathematical hybrid capability under additional primitives, **not** a common-bath preparation threshold or an accurate bare-qubit endpoint theorem.

**Exact imports and proof.** CFG Lemma 40 approximates an encoded circuit on its full computational logical/gauge module in diamond norm. Lemma 42's output interface is an exact positive good/bad mixture on that module. Consequently one-sided WRITE, without a bare input interface, has circuit error

\[
 \epsilon_{W,\mathrm{FT}}\leq2S_E(cp)^\ell.
\]

Tensor the physical output interfaces. Their positive sparse support flags remain valid on correlated output gauges and external references, and yield the release support/moment bounds of Section 7. Execute the short parallel SWAP into memory. During it count H, cooling, B coupling and link faults in the same finite-pulse expansion. The old memory state, however correlated, moves to auxiliary staging degrees; it is not substituted for a fresh bath. The retained low-order terms act identically on the new logical payload and land in a warm memory span. Lemma C gives the positive same-environment comparison.

For READ, add a charged final cooling dwell and proof-only low-energy filter. Capture the encoded block into isolated staging by the same short-SWAP argument. Feed it through n physical-to-computational-code interfaces and the encoded realization of a promised decoder. Lemmas 41 and 40 give

\[
 \epsilon_{R,\mathrm{FT}}\leq2(n+S_D)(cp)^\ell.
\]

The input-interface bad flags are sparse, but the memory's residual error need not be local stochastic. Choose strict cutoffs so their **combined** error span, including capture faults, has weight below the distance margin. The actual promised decoder corrects that whole span, including arbitrary bath/reference coefficients. B and the old memory hardware are external references to the isolated staging operation; their correlations do not disappear and need not be reset.

To stay inside the proved circuit core of Lemma 40, the decoder is fully coherent: extract syndrome into work, unroll O(n) passes through O(n) local hubs, reversibly record decreasing-move labels, apply controlled Paulis and syndrome updates, then Clifford-unencode and discard work. At most O(n) energy decreases are needed. Coherent histories absorb syndrome-dependent phases, so the entire promised operation is identity on logical information even for correlated inputs. A conservative waiting-inclusive size is `S_D=O(n^4)` and `S_E=O(n^3)`. The underlying computational scheme's own classical assumptions are still retained; replacing outer feedback does not remove them automatically.

If `delta_LS` is the exponentially small interface-support tail, `delta_link` the signed link-pulse tail and `delta_f` the final energy-filter cost, a conservative port bound is

\[
 E_{\rm ports}\leq2(S_E+S_D+n)(cp)^\ell
                 +4\delta_{LS}+4\delta_{link}+2\delta_f.
\]

The last filter retains its genuine square-root leakage loss. Choose final cutoffs `u_f<u_dec<=u_post(service)` first, and take `nu_eq<=s min(u_f,u_pre(service))/4` by the subsequent beta/eta choice. Reserve a combined support fraction wbar with `D_E wbar<u_dec` and strict distance margins, then choose capture support, interface-fault fraction and link duration below wbar. A longer dwell alone cannot lower the moment below `nu_eq`. All thresholds are simultaneously attainable by the earlier parameter order. Choose

\[
 \ell\geq{c_F n+\log(2(S_E+S_D+n))+O(1)\over|\log(cp)|}.
\]

Then `ell=O(n)`, so CFG's polynomial block/gadget size gives polynomial peak space, locations and duration. Charge every waiting location, all resets, routing, code access, parallel links and control strengths. Input/output accuracy is defined at encoded ports; an ideal final decoder defines that metric, not an uncharged physical bare release. ∎

Literal CFG Theorem 53 concludes a weaker operational communication metric and a fixed-channel formulation. The proof above uses its underlying one-sided lemmas directly and compares with the actual intended operation sequence, so it never appends a potentially enormous inverse computation merely to turn processing into an identity channel.

[Complete frozen port proof](../work/protected-quantum-processing-20261107/challenges/quantum_ports_closure.md), [coherent decoder addendum](../work/protected-quantum-processing-20261107/challenges/quantum_ports_coherent_decoder_addendum.md), [version-bound port review](../work/protected-quantum-processing-20261107/challenges/auditor_quantum_ports_review.md), and [exact import audit](../work/protected-quantum-processing-20261107/machinery/CFG_PORTS_IMPORT_AUDIT.md) contain all interface inequalities, intensity bounds, source hashes and limitations. Active preparation while coupled to the same unrestricted B remains outside this theorem. Polynomial staging and exact Markov cooling preclude an unearned complete-cost advantage.

## 13. Theorem and status ledger

| ID | Statement | Status and dependency |
|---|---|---|
| A | Exact bounded-propagation stable CSS duality of the actual anchored complex | **PROVED** under the stated local exactness/compatibility hypotheses; homological perturbation is established machinery |
| A-density | Linear density of improving cochain-star moves | **PROVED** by additive-slack refinement of the imported support recursion |
| A-energy | Two commuting, independently descending sector energies on original gate DATA plus specified product ancillas | **PROVED** from A, A-density and exact CSS types; ground code and distance retained |
| B | Nonstationary warm thermal storage, including retained-bath/logical/reference correlations | **PROVED IN THE SPECIFIED GKSL MODEL**; actual positivity, locality, rates and moment gap are essential |
| C | Signed full-module gate approximation admits a CP/TNI same-environment surrogate at error 2delta | **PROVED** by complete contractions; no pulse square-root loss |
| D | Repeated finite non-Clifford bursts with cooling always present and fixed restoring dwells | **PROVED IN THAT MODEL**, with the exact selected-port initialization and control contract |
| E | Noisy WRITE/READ at encoded ports with polynomial isolated active staging | **PROVED RESTRICTED TRANSFER** from verified CFG lemmas plus common-span and same-bath SWAP proofs; source classical/noise/isolation assumptions retained |
| N1388-admission | Supported physical release faults enter its accepted powered warm basin | **PROVED TRANSFER** at the original native contract; no passive-model identification |
| Bare-port floor | Error at least `1-(1-p)^k` before redundancy under the permitted dephasing channel | **PROVED, ESTABLISHED PHENOMENON**; disallows a vanishing fixed-noise global bare-port target |
| Generic all-state bottleneck inference | Decodability or A-support alone yields projected-equilibrium lifetime | **DISPROVED AS A GENERAL INFERENCE**; not a lattice-memory failure theorem |
| Raw transpose local descent | Global qLTC soundness automatically yields the needed physical local decoder | **NOT ESTABLISHED / NOT USED**; replaced constructively by the changed energy |
| Old N1694 noisy long HOLD | Generic realistic writer outputs covered by its old microscopic theorem | **OPEN** |
| Native universal thermal operations | Complete compatible universal set on this new architecture | **OPEN**; selected CCZ and separately supplied compatible gates are the earned scope |
| Microscopic/small-body/3D realization | This same service with finite-bandwidth baths and economical physical couplers | **OPEN** |
| Full-resource advantage | Better feasibility or total cost than matched active/autonomous FT | **NOT ACHIEVED** |
| Historical firstness | First exact result of this scope in all literature/Zenodo | **UNKNOWN** |
| North-star capability | Transformative protected quantum processing or demonstrated nearby 95+ route | **NOT ACHIEVED; no probability or future score awarded** |

The machine-readable companion is [PROTECTED_QUANTUM_PROCESSING_THEOREM_LEDGER.json](PROTECTED_QUANTUM_PROCESSING_THEOREM_LEDGER.json). PROVED refers to a mathematical statement at its complete hypotheses. It does not certify the hypotheses in a laboratory or grant first priority.

## 14. Independent work, challenges and reproducibility

Exactly three GPT-6.1 Sol researchers at maximum reasoning worked independently alongside the principal before exchanging initial reports. All four initial reports were frozen and preserved:

- [Principal initial](../work/protected-quantum-processing-20261107/initial/principal.md): `863ad29f6951c2596189db9ad929793a6e5523e453203451346d0cdd7b31f0c3`.
- [Machinery initial](../work/protected-quantum-processing-20261107/initial/machinery.md): `6baa2223900dfd66a82e312709b09f3418483c0411a48ebbf638a5988de9f0bf`.
- [Constructor initial](../work/protected-quantum-processing-20261107/initial/constructor.md): `21d053255b8337a37f057f0c367d8a06043e9bfa1964c9929a31e69e4053be60`.
- [Auditor initial](../work/protected-quantum-processing-20261107/initial/auditor.md): `0d2debc4f800d5a3d0dc3376fd358b233f965d61ac5f581f5091759ed46b3d7d`.

Initial agreement on powered warm admission did not end the investigation. The principal's thermal route was challenged against HGL, color-code thermal computation, the autonomous QCA and the raw dual-sector obstruction. The latter was repaired through the explicit stable normal form. Subsequent challenges removed an avoidable pulse square root, retained all TNI trace losses, clarified canonical projectors and Li's selected logical input, and closed the restricted encoded-port construction. Failed shortcuts and earlier versions remain in the record.

The [principal adjudication](../work/protected-quantum-processing-20261107/principal/ADJUDICATION.md), [full theorem](../work/protected-quantum-processing-20261107/principal/THERMAL_SERVICE_THEOREM.md), [stable-duality review](../work/protected-quantum-processing-20261107/challenges/auditor_stable_duality.md), [correlated-handoff review](../work/protected-quantum-processing-20261107/challenges/auditor_correlated_handoff.md), [version-bound service review](../work/protected-quantum-processing-20261107/challenges/auditor_thermal_service_final_review.md), [port closure](../work/protected-quantum-processing-20261107/challenges/quantum_ports_closure.md), [coherent decoder addendum](../work/protected-quantum-processing-20261107/challenges/quantum_ports_coherent_decoder_addendum.md), and [final port review](../work/protected-quantum-processing-20261107/challenges/auditor_quantum_ports_review.md) provide the detailed dependencies and corrections.

The principal reran the finite supporting checks: 100 exact GF(2) filtered-normal-form cases; coherent Steane/reference admission and positive-surrogate examples; dependent-check Walsh expansion; finite Davies drift/Gibbs stationarity; scalar simultaneous-margin checks; Bell input floors; and the reversible bottleneck counterexample. All passed. These checks supplement the proofs. They do not establish asymptotic locality, lifetime, an actual-code threshold, physical feasibility, novelty or external validation.

[Research-record index](../work/protected-quantum-processing-20261107/INDEX.md) and [validation report](PROTECTED_QUANTUM_PROCESSING_VALIDATION.json) identify final hashes, exact source versions, review scope and check artifacts. No earlier published manuscript, release record, website or shared producer checkout was modified for this research round.
