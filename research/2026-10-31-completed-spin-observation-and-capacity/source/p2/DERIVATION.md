# A reusable spin measurement from a finite charge interface

## Result and scope

This is a new working construction in a different physical resource setting from the original signed spin handles and from the force/optical apparatus. It preserves those earlier results and their qualifications. It does not derive the new hardware from the old handles.

The construction compiles the complete two-spin singlet/triplet instrument from spin-independent fermion hopping, a local charge sensor, finite classical feedback, and renewed meters. For fixed qualified source and sensor constants, an instrument error at most epsilon costs O(log squared(1/epsilon)) fresh short probes. The common interacting memory may be uninitialized, retained between calls, correlated with the data and an external reference, and arbitrarily fast. Its Hamiltonian is never reversed. The essential restriction is its coupling algebra: it cannot act on spin orientation or on unselected computational spins.

The compilation includes the return of a detected singlet to two separated sites. It therefore supplies a reusable quantum measurement, not merely a correct classical label. A finite adaptive program of L such measurements has error at most the sum of its per-call errors, including all retained bath histories. L counts the routed ideal program, with initialization and resource-building measurements included.

The underlying symmetry protection and computational power are established results, not discoveries here. Freedman, Hastings and Shokrian Zini [1] identify singlet/triplet measurement as a symmetry-protected primitive. Rudolph and Virmani [2] prove universality with independently maximally mixed input spins and only these pair measurements. The contribution developed here is a conditional physical compilation with explicit finite sensing, both double-occupation states, a uniform return bound, and a joint instrument/composition guarantee. It has not established an experimental advantage or a threshold against generic spin noise.

## 1. Physical operations and the qualification that matters

Each computational site has one admitted fermion orbital and a spin-1/2 degree of freedom. A measurement addresses two neighboring sites L and R, initially with one fermion on each. The apparatus can pulse spin-independent hopping on this pair, turn hopping off during charge interrogation and holding, and read the left-site occupation n_L in {0,1,2}. The right-site occupation is 2-n_L. Charge leakage outside this two-particle, one-orbital model is a separate error.

With hbar=1, the on-window Hamiltonian is

\[
H=I\otimes H_M
-\sum_{\sigma=\uparrow,\downarrow}
(c^\dagger_{L\sigma}c_{R\sigma}+c^\dagger_{R\sigma}c_{L\sigma})\otimes G_M
+P_{20}\otimes\Delta_L+P_{02}\otimes\Delta_R.
\]

The bounds are operator inequalities on the entire allowed memory domain:

\[
g_-I\le G_M(t)\le g_+I,\qquad
\|\Delta_L(t)\|,\|\Delta_R(t)\|\le d.
\]

The bounds need to remain true after every allowed history. A set of calibration samples does not establish this condition by itself. An invariant domain, microscopic symmetry, source characterization, and a bound on departures from that domain are physical qualifications.

No bound on the norm of H_M or on its commutators is imposed in the main theorem. All Hamiltonians must nevertheless generate well-defined propagators. The finite-matrix checks use bounded matrices. The analytic argument extends to bounded couplings and a common self-adjoint bath generator with the usual propagator assumptions.

During readout, charge is fixed. A fresh two-level, spinless meter has the coupling

\[
H_{\rm meter}^{(n)}=I_a\otimes H_M^{(n)}+nX_a\otimes F_M,
\qquad f_-I\le F_M\le f_+I.
\]

This is a charge-density coupling. It can be written as n_L Z_a F_M for a localized charge/dipole meter, with preparation and readout in the transverse basis. The X notation is the same interaction in the meter's preparation basis. Its required operations are a short coherent meter preparation, a finite interaction, a binary readout, and renewal. These are detector resources; they do not supply spin rotations to the computer. Constant preparation/readout error is allowed through the probability intervals below.

A pointer source that sometimes produces no probe, detector loss, and dark counts must satisfy the stated click-effect bounds for every input memory state. They are not automatically equivalent to arbitrary state-preparation errors. For the numerical example, survival is at least 0.9 and an additional effect uncertainty is at most 0.01. Failed source/detection events contribute a no-click outcome; other mispreparation is covered only if it obeys these interval bounds and remains charge-QND and spin-independent.

The sensor, active source and all holding operations act trivially on spin orientation. Couplings to unselected computational spins are excluded or separately charged. Exact charge-QND holding is a structural assumption. A fixed residual hopping term during a long readout is not silently included in the detector's classical error probability.

## 2. Why the full triplet survives

The two-spin representation is multiplicity free:

\[
\tfrac12\otimes\tfrac12=0\oplus1.
\]

Write P_s=|s><s| and P_t=I-P_s. An operator commuting with every U tensor U and acting on a spin-trivial apparatus has, on the separated-site subspace, the form

\[
K_y=P_s\otimes A_y+P_t\otimes B_y.
\]

This is a Schur-lemma statement about the instrument, not merely its outcome probabilities. No apparatus record can distinguish two triplet vectors. Arbitrary memory dynamics and record-dependent backaction may occur in A_y or B_y.

This known symmetry principle [1] has a sharp locality condition. Global rotational invariance of a many-spin device is insufficient: exchange with a spectator is rotationally invariant and can change the computation. Three spins also have a multiplicity-two spin-1/2 sector; an invariant pair exchange acts nontrivially on that multiplicity. The code exhibits a restriction equal to diag(-1,1).

A detector can otherwise report the triplet label with probability one while dephasing (|00>+|11>)/sqrt(2). Resolving the individual triplet vectors produces trace-distance disturbance 1/2 in this example. That is the failure the present physical coupling must rule out.

## 3. Deriving the source from fermion hopping

Keep all six two-particle states of the four fermion modes. There are three separated triplets, one separated singlet S, and two double occupations D_L and D_R. Pauli exclusion gives zero hopping on all three triplets. In the singlet charge basis (S,D_L,D_R), the hopping matrix is

\[
-\sqrt2\begin{pmatrix}0&G&G\\G&0&0\\G&0&0\end{pmatrix}.
\]

Thus, at equal charge potentials, only D_+=(D_L+D_R)/sqrt(2) couples to S, with magnitude 2G. D_- is dark. This source operator is derived from spin-independent single-particle tunnelling; a native logical singlet projector has not been assumed.

Spin blockade and charge sensing are established physical mechanisms [3]. The present ideal one-orbital model is stronger than merely observing blockade in a device: higher orbital triplets, spin-orbit coupling, hyperfine fields, spin relaxation, and uncontrolled occupations must be bounded separately.

### A forward-bath spectral window

For H_±=H_M±G, let U_± be the forward propagators and W=U_-^dagger U_+. Then

\[
\dot W=-2i\,U_-^\dagger G U_-\,W.
\]

U_-^dagger appears only in the proof. The apparatus supplies no inverse evolution. For g_-I<=G<=g_+I, the generator has the same spectral bounds regardless of H_M. Consequently the stay amplitude A=(U_++U_-)/2 has the accepted positive-exchange opacity bound. The transfer amplitude B=(U_+-U_-)/2 satisfies B^dagger B=I-A^dagger A.

For the Hubbard source replace G by 2G. For a window tau with 0<2g_-tau<=2g_+tau<pi,

\[
\|A\|\le r_0:=\max\{|\cos(2g_-\tau)|,|\cos(2g_+\tau)|\}.
\]

For variable envelopes use their integrated bounds. Time uncertainty is included by taking the endpoint envelope. A charge-potential perturbation has norm at most d, so Duhamel's inequality changes the full propagator by at most xi=d tau_max. It follows that

\[
\|U_{S,S}\|\le r_0+\xi,
\qquad
s_{\min}(U_{S,D_a})\ge\sqrt{(1-r_0^2)/2}-\xi,
\quad a=L,R.
\]

The second inequality is a return guarantee for each resolved double site and every memory state. It is not just an average transfer probability.

For the explicit source box

\[
g_- =1,\quad g_+=2,\quad \tau_0=\pi/6,
\quad \tau/\tau_0\in[.95,1.05],\quad d\le.02,
\]

one obtains r_0=sin(pi/5), xi=7pi/2000. Hence r_search<0.6 and p_return>0.3. The tighter displayed values are 0.5987808266 and 0.3147948639. The conservative 0.6 and 0.3 bounds are checked with exact rational enclosures in exact_bounds.py.

This favorable example requires both double-charge potentials close to the separated singlet. An ordinary detuning knob does not generically make both double occupations resonant. The example is a declared source qualification, not an assertion that a standard double dot supplies it for free.

### A weaker guarantee without near resonance

There is also a finite bound for arbitrary bounded charge offsets. Remove the entire charge-diagonal Hamiltonian in the proof. Its charge-dependent rotations differ from the common bath evolution by at most dt. The first hopping-order amplitude from S to a specified D_a is therefore a positive integral, with minimum singular value at least

\[
\sqrt2 g_-\tau-\frac{g_+d}{\sqrt2}\tau^2.
\]

Every even hopping order has zero matrix element between these two charge classes, because hopping connects the center of a star to its leaves. The norm sum of the odd orders from order three onward is bounded by sinh(2g_+tau)-2g_+tau. Thus both directions have transfer amplitude at least

\[
a(\tau)=\left[\sqrt2g_-\tau-\frac{g_+d}{\sqrt2}\tau^2
-\sinh(2g_+\tau)+2g_+\tau\right]_+.
\]

Take p_return=a squared and r_search<=sqrt(1-2a squared). This does not require bath freezing or elimination of a supposedly off-resonant charge state. The cost can be poor: for g_-=1,g_+=2,d=100, an optimized conservative bound gives p_return about 1.25e-5. At large d it scales as g_-^4/(2g_+^2 d^2). This is an existence result, not a favorable device estimate.

## 4. Search, resolve, return

First suppose charge can be measured perfectly. The finite protocol is:

1. Apply N source windows, measuring the site charge after each. At the first observed double occupation, retain whether it is 20 or 02, mark the branch s, and hold it until the search block ends.
2. If every search result was 11, mark the branch t and hold the separated pair.
3. On an s branch, apply up to R release windows. Resolve the site charge after each. On the first 11 result, hold the separated singlet until the common endpoint. If every release result is double occupation, output an explicit abort.

Every branch ends at the same clock time. Internal charge histories remain in M. The computation receives s, t or abort.

Resolving the double site is essential to this proof. At resonance an arbitrary unresolved double-charge state can be D_-, which never returns. When a charge measurement leaves a specified D_L or D_R, each release window has probability at least p_return of separation, uniformly over the retained memory. A two-dimensional unresolved charge input cannot be assigned the one-dimensional return bound. The symmetric source happens initially to populate D_+, but that does not justify the bound after general allowed charge histories.

Let a=r_search^N and b=(1-p_return)^R. The t-labelled Kraus operator has the form

\[
K_t=P_t\otimes V_t+P_s\otimes A_N,
\qquad\|A_N\|\le a,
\]

where V_t is an isometry. Each successful s history is exactly P_s tensor C_h. Stack these C_h into E_s. Uniform success gives

\[
E_s^\dagger E_s\ge (1-a^2)(1-b)I.
\]

Define the comparison isometry E_tilde_s=E_s(E_s^dagger E_s)^(-1/2). This inverse square root defines a mathematical comparator; it is not an operation the apparatus must perform. Its distance from E_s is at most a squared+b. The abort probability is at most b.

In half-diamond distance, the complete flagged instrument is consequently within

\[
\epsilon^{(0)}_{ST}\le a+a^2+\frac32 b
\]

of an instrument with branches P_s tensor E_tilde_s and P_t tensor V_t. The t-branch comparison costs at most a; the s stack at most a squared+b; the abort CP map at most b/2. This bounds coherent singlet/triplet contamination as well as classical errors. Counting only the false-t probability a squared would miss the amplitude error a.

An aborted pair is not available as two computational qubits. Small-error statements include its abort flag instead of discarding unsuccessful events without accounting for their probability.

## 5. A charge detector that tolerates retained memory

For fixed n, the meter's flip effect is B_n^dagger B_n, with B_n=(U_+-U_-)/2 and H_±=H_M^(n)±nF. The same forward spectral argument gives

\[
\operatorname{spec}(B_n^\dagger B_n)
\subseteq\{\sin^2\theta:\theta\in[nf_-\tau,nf_+\tau]\}.
\]

For the second setting below the arc crosses a full phase winding. This does not require extending the old no-wrap assertion without proof. Write the generator of W as a scalar center plus a remainder of norm at most n(f_+-f_-). After factoring the scalar phase, the residual unitary's eigenphases stay within that integrated norm. When this width is below pi, the resulting arc can be followed through the winding. Its sin-squared extrema still give the displayed interval. Neither scalar centering nor factoring a phase is a physical bath inversion.

Set f_-=1,f_+=1.2, timing uncertainty 5%, and use two settings

\[
\tau_s=\frac{\pi}{2(1+1.2)},\qquad \tau_l=2\tau_s.
\]

After the stated 0.9 survival and 0.01 effect uncertainty, the following wider, rationally certified intervals suffice:

| Left charge | Short-setting click probability | Long-setting click probability |
|---|---:|---:|
| 0 | [0,0.01] | [0,0.01] |
| 1 | [0.34,0.63] | [0.84,1] |
| 2 | [0.84,1] | [0,0.21] |

Every conditional probability after any previous probe record lies in the appropriate interval. No iid assumption is made. Use m_l long probes and m_s short probes. Classify as charge 1 when the long frequency exceeds 0.535. Otherwise classify as charge 2 when the short frequency exceeds 0.3, and charge 0 otherwise.

For Bernoulli observations with conditional probability at most a, the exponential-supermartingale argument bounds an upper tail by exp[-m D(z||a)]. A lower bound b gives the corresponding lower-tail bound exp[-m D(z||b)]. Conditional memory evolution changes none of this argument. The relative entropy is

\[
D(z\|p)=z\log(z/p)+(1-z)\log[(1-z)/(1-p)].
\]

Exact logarithmic enclosures give exponents at least C_l=1/4 and C_s=7/10 at the stated thresholds and worst interval endpoints. The charge error probability is at most

\[
\eta\le e^{-m_l/4}+e^{-7m_s/10}.
\]

The initially considered single-time, three-rate detector had a substantially smaller worst separation exponent, about 0.03284. The two-time design uses ordinary hypothesis testing to avoid that unnecessary cost. This is not a claim of a new classical estimation method.

### Turning the probability bound into an instrument bound

Because the probe is charge-QND, its total isometry decomposes as sum_n P_n tensor W_n. In sector n, stack the records correctly classified as n into W_nn. The uniform classification bound says W_nn^dagger W_nn >= (1-eta)I. Normalize this correct-record stack by its polar factor to define a perfect charge-instrument comparator.

The squared norm distance of the full isometries in that sector is at most 2(1-sqrt(1-eta))<=2eta. Different physical charge sectors are orthogonal, so their norm errors take a maximum, not a sum. After any permitted tracing of meter degrees of freedom, the half-diamond error is therefore at most

\[
\delta_{ch}\le\sqrt{2\eta}.
\]

This lifting step is why classical classification alone is insufficient. All internal meter records may stay in the retained memory. The high-level algorithm uses the coarse labels, not arbitrary postselection on fine apparatus records.

## 6. Finite accuracy and actual cost

Replacing the N+R perfect charge measurements in the search/return construction gives

\[
\epsilon_{ST}\le r^N+r^{2N}+\frac32(1-p)^R
+(N+R)\delta_{ch}.
\]

One explicit allocation for 0<epsilon<=1 is

\[
N=\left\lceil\frac{\log(6/\epsilon)}{-\log r}\right\rceil,
\quad R=\left\lceil\frac{\log(6/\epsilon)}{-\log(1-p)}\right\rceil,
\quad\delta_{ch}=\frac{\epsilon}{2(N+R)},
\]

\[
m_l\ge8\log(2/\delta_{ch}),\qquad
m_s\ge\frac{20}{7}\log(2/\delta_{ch}).
\]

This allocation proves total error <=epsilon. exact_bounds.py chooses the integer schedules with rational logarithmic enclosures and verifies the analytic allocation; it does not infer a box guarantee from matrix samples. The resulting table is generated by run_checks.py and stored in results.json.

| Certified target half-diamond error | Search windows N | Release windows R | Long + short probes per charge readout | Total fresh probe slots |
|---|---:|---:|---:|---:|
| 1e-2 | 13 | 18 | 76 + 27 | 3,193 |
| 1e-4 | 22 | 31 | 117 + 42 | 8,427 |
| 1e-6 | 31 | 44 | 157 + 56 | 15,975 |
| 1e-8 | 40 | 57 | 196 + 70 | 25,802 |

The certificate applies to the declared mathematical box, not to an experimental device. The corresponding tighter evaluations of the analytic error expressions, and the sampled matrices, use ordinary floating point.

The resource count is (N+R)(m_l+m_s) fresh meter preparations and binary readouts, at most N+R source/release windows, classical records and feedback, and storage for the entire fixed duration. A time upper bound is

\[
T\le (N+R)\tau_{hop,max}
+(N+R)(m_l\tau_{l,max}+m_s\tau_{s,max})
+T_{renew/read/switch/hold}.
\]

The two coupling scales need not be equal. The example duration field uses the meter's specified units; it is not a duration in seconds. Probe loss is paid repeatedly in source/readout rates. No probe must survive the whole accuracy-amplification sequence, so the direct long-photon survival penalty of the previous Zeno construction is absent from this qualified model. Existing optical heralding/filtering approaches can also avoid that penalty; it was never a lower bound on all optical architectures.

The improvement operation is actually supplied: more short, renewed charge probes and more bounded transfer/return windows. It uses no fine gain estimate, calibrated logical rotation, bath reset, long coherent phase-estimation oracle, or unsupplied entanglement-purification circuit. The counts remain substantial, and qualification acquisition has not been assigned an invented shot cost.

## 7. Reuse with arbitrary correlated histories

For each call the comparison instrument has branches P_q tensor V_q, where V_q is an isometry on all retained memory and records. In a sequence, each complete history is a product of the requested spin projectors tensor a product of memory isometries. Tracing memory reproduces the ideal spin measurement program even when its initial state was correlated with the spins and a reference.

The source and detector inequalities must hold on every allowed conditional memory state. They permit a hybrid channel comparison without independence between calls. For L adaptive calls, with fine detector histories kept internal,

\[
\tfrac12\|\mathcal P_{actual}-\mathcal P_{ideal}\|_\diamond
\le\sum_{j=1}^{L}\epsilon_j+\epsilon_{source/routing/holding}.
\]

If the guarantee is stated only on the valid charge input sector, use the usual hybrid with ideal prefixes, which remain in that sector. The actual channels must still have physically defined CPTP extensions on leaked inputs; no accuracy is claimed there. Such leakage is already part of the prior channel error.

Choosing epsilon_j proportional to epsilon/L costs O(L log squared(L/epsilon)) short probes for fixed qualification constants, relative to L ideal singlet/triplet calls. This statement is not an overhead bound relative to a conventional gate count unless the cost of the ideal measurement-only compilation, routing, source building and caps is also included.

Universality then follows by supplying the published ideal measurement-only consumer [2], not by asserting that one parity bit is a computer. Its construction is polynomial but is not a practical low-constant gate compiler. The local transport consumer below establishes a useful operation with only the operations actually compiled here.

## 8. A supplied singlet resource and exact forced teleportation

### Mixed-spin source

Take a sacrificial spin B, arbitrary and correlated with old memory, and a fresh C in I/2 independent of that joint input. The exact source identity is

\[
P_s(\rho_{BM}\otimes I_C/2)P_s
=|s\rangle\langle s|_{BC}\otimes\operatorname{Tr}_B\rho_{BM}/4.
\]

On t, discard/replace C and try again; B may remain dirty. Every ideal trial succeeds with probability 1/4, so the mean is four measurements and the k-trial failure tail is (3/4)^k. The fresh independent mixed source, replacement, disposal, and storage of B are physical operations. A maximally mixed marginal alone is insufficient: a correlated Bell triplet has maximally mixed single-spin marginals and zero singlet probability.

### A charge-qualified source alternative

A single admitted orbital with two fermions has a one-dimensional spin sector. Conditioning an arbitrary orbital-plus-memory state on double occupation produces a closed-shell singlet and a memory state. Applying the already constructed site-resolved release protocol makes a separated singlet with the same uniform return bound. This can replace the mixed-spin factory when the hardware supplies a charge-qualified filled orbital; no spin-axis preparation is required.

The loading operation is still real. A reservoir, charge/energy transfer, success rate, and independence from stored-spin operations must be provided. Charge heralding verifies the spin factorization but does not manufacture a nonzero loading rate from an arbitrary reservoir. A claimed rate lower bound must be uniform over retained source histories, and a finite source cap and holding time must be included. This alternative is a source specification, not a free improvement inserted into the numerical mixed-source example.

### Transport with no corrective spin rotation

Let A contain an unknown spin, possibly entangled with a reference, and let BC be a singlet. Measure AB with the compiled s/t instrument. If s occurs, the input has been teleported to C. If t occurs, measure BC with the same s/t instrument and retry AB, regardless of the BC outcome.

This is a forced-measurement protocol with known antecedents [4]. The exact rational certificate verifies every success history through eight AB attempts: each is proportional to |s>_AB tensor I_(A to C). There is no Pauli correction.

The first AB attempt succeeds with probability 1/4. Following a failed AB attempt, the BC result has probabilities 3/4 and 1/4; the subsequent AB success probabilities are respectively 1/4 and 3/4. Therefore

\[
\Pr(\text{still unfinished after }k\text{ AB attempts})
=\frac34(\frac58)^{k-1}.
\]

The mean number of AB measurements is three and the mean number of BC measurements is two: five in total, plus the mean four source measurements when using the independent-mixed-spin factory.

The resource is reusable within this three-spin cell. A successful A-to-C transfer leaves AB in a singlet. Reversing the roles of the ends then transfers C back to A with the same protocol and leaves BC in a singlet again. No fresh spin source is required for subsequent back-and-forth transfers. Each direction uses five ideal measurements on average; meter renewal and data holding continue to be paid. Both directions are certified with exact fractions. For any capped sequence of such transfers, the same joint-channel composition bound applies to the accumulated measurement calls with the actual retained M. This is a directly supplied repeated-use capability, independent of the more elaborate universality construction.

The three-site sequence uses only neighboring pairs AB and BC. Repetition along spare tracks can provide transport. A larger processor needs actual buffers, source sites, edge selection and storage; arbitrary distant pair access is not included at zero cost. L in the composition theorem counts the routed sequence and any finite caps.

With source cap k_s and teleport cap k_t, at most L_max=k_s+2k_t-1 ideal s/t calls are needed. The ideal failure probability is at most (3/4)^k_s+(3/4)(5/8)^(k_t-1). Physical errors add at most Delta=L_max epsilon_ST to the complete flagged instrument. On successful output, a conservative conditional error bound is 2Delta/(p_ideal-Delta), when the denominator is positive. This is a conditional statement with its success probability included.

For a concrete conservative instance, k_s=50 and k_t=31 give at most 111 measurements and ideal capped failure at most 1.131e-6. Assigning each measurement error 1e-6/(4*111) requires 29,432 fresh probe slots per call in the certified schedule. The worst-case total is 3,266,952 probe slots. Using the conservative allocation Delta<=2.5e-7 gives conditional successful-output error below 5.001e-7, in addition to the separately reported failure probability. This is a complete bounded protocol with a large cost, not a claim that the mean of nine ideal measurements implies a cheap physical transfer.

## 9. What this does not correct

An additional Hamiltonian term E_bad(t), containing spin-dependent disturbance, unwanted spectator coupling, or residual hopping during charge readout, contributes at most the integral of its norm to a Duhamel comparison. Dissipative/model errors require their own channel bounds. Increasing the number of probes generally increases exposure to those terms. It is therefore invalid to extend the arbitrary-accuracy theorem to fixed generic symmetry-breaking noise.

For example, a field acting inside the triplet can rotate or dephase a triplet state while every reported spin label stays correct. The error is not repaired by a longer charge record. A finite-temperature medium with uncontrolled spin exchange is also outside the spin-trivial coupling algebra even if the full device has a global rotational symmetry.

The fixed-strength bath-motion floor of the original signed-handle approach is absent only for the explicitly protected algebra: fast motion of a common spin-blind M has already been included exactly. This does not bound a real device's spin-active noise. No fault-tolerance threshold, retained-memory purification theorem, or experimental storage advantage has been proved here.

The short source box also assumes a favorable charge spectrum; the nonresonant bound shows how sharply the cost worsens without it. The detector assumes fixed charge while it is interrogated. A quieter switch, source qualification, and storage cannot be acquired merely by naming them.

## 10. Comparison on equal resources

An ordinary controller with this same Hubbard source, sensor, renewal, coarse spectral bounds, and protected storage can run this construction. There is no separation theorem between it and conventional control. A controller given a more accurately learned model may choose a shorter pulse or readout; its acquisition cost and stability assumptions should be counted when used in a comparison.

The direct high-accuracy optical Zeno construction from the earlier work remains subject to its fixed-loss bound. It is not the strongest general optical comparator. Duan, Wang and Kimble [5] already obtain cavity-scattering gates robust to coupling variation with dominant losses signalled. Barrett and Kok [6] use double heralding; Leung and Ralph [7] use filtering/distillation to recover conditional fusion fidelity in their model. Liu, Wu and Du [8] explicitly propose an error-heralded parity detector for electron-spin purification. These alternatives must receive their actual mode, resonance, spin-control and source qualifications, and the new scheme must receive its charge and symmetry qualifications. No component-count or wall-clock advantage follows from the present calculations.

The new conditional statement is narrower and useful: the finite fermionic/charge construction supplies a complete repeatable measurement and an accuracy-improvement operation under noncommuting, retained, spin-blind memory dynamics. A later comparison can test whether its required protected interfaces are easier to supply than the alternatives' optical matching and spin controls.

One optical opening was examined before selecting the spin interface. For a scalar reciprocal two-port mixer U with first column (a,c), a reversed passage U-transpose and a rail swap X give the exact identity

\[
\langle0|U^{\mathsf T}X\,\operatorname{diag}(F_0,F_1)U|0\rangle
=ac(F_0+F_1).
\]

A signed swap instead gives ac(F_1-F_0). This can cancel a quiet reference against an active optical amplitude without learning the scalar mixing angle. However, its use for a protected parity filter still needs matching operator-valued amplitudes for the two complementary spin transitions, a suitable quiet reference, and actual success-probability and source bounds. An operator-valued, memory-entangled controller cannot be substituted for scalar a,c in this identity. Reciprocity of a classical optical mixer does not supply an inverse bath evolution. The matched scalar filtering mechanism also overlaps established optical error-heralding methods; it was not promoted to a new physical advantage.

## 11. Executable evidence

Run `python p2_spin_interface/run_checks.py` from the working directory. The script constructs the four-mode fermion Hamiltonian, checks triplet blocking and the dark double-charge state, samples piecewise noncommuting source and sensor baths, enumerates all search/release histories in small instances, checks instrument completeness, and writes results.json. Bath norm scales include 1000 in source/meter units. These sampled matrices are ordinary floating-point checks, not a proof of the operator boxes.

exact_teleportation.py checks 255 success histories using fractions and proves the two-state recurrence exactly. exact_bounds.py certifies the declared coarse source and detector bounds and integer allocations using rational arithmetic, Machin's formula for pi, Taylor remainders and the atanh series for logarithms. It does not certify any physical device's admission to the model.

Earlier accepted foundations, including the prior instrument and composition results, are left unchanged. This new derivation and implementation remain working research.

## Primary sources

1. M. H. Freedman, M. B. Hastings, M. Shokrian Zini, *Symmetry Protected Quantum Computation*, Quantum **5**, 554 (2021). [Article](https://quantum-journal.org/papers/q-2021-09-28-554/) · [Author manuscript](https://arxiv.org/abs/2105.04649).
2. T. Rudolph and S. S. Virmani, *The two-qubit singlet/triplet measurement is universal for quantum computing given only maximally-mixed initial states*, Nature Communications **14**, 7800 (2023). [Article](https://www.nature.com/articles/s41467-023-43481-y).
3. A. C. Johnson et al., *Singlet-triplet spin blockade and charge sensing in a few-electron double quantum dot*, Physical Review B **72**, 165308 (2005). [Abstract](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.72.165308).
4. P. Bonderson, M. Freedman and C. Nayak, *Measurement-Only Topological Quantum Computation via Anyonic Interferometry*, Annals of Physics **324**, 787–826 (2009). [Author manuscript](https://arxiv.org/abs/0808.1933).
5. L.-M. Duan, B. Wang and H. J. Kimble, *Robust quantum gates on neutral atoms with cavity-assisted photon-scattering* (2005). [Author manuscript](https://arxiv.org/abs/quant-ph/0505054).
6. S. D. Barrett and P. Kok, *Efficient high-fidelity quantum computation using matter qubits and linear optics* (2005). [Author manuscript](https://arxiv.org/abs/quant-ph/0408040).
7. P. M. Leung and T. C. Ralph, *Improving the fidelity of optical Zeno gates via distillation* (2006). [Author manuscript](https://arxiv.org/abs/quant-ph/0609224).
8. Y.-T. Liu, Y.-M. Wu and F.-F. Du, *Self-error-rejecting multipartite entanglement purification for electron systems assisted by quantum-dot spins in optical microcavities*, Chinese Physics B **31**, 050303 (2022). [Article](https://doi.org/10.1088/1674-1056/ac4489). The accessible abstract supports the comparison; no unverified operator-uniform guarantee is attributed to it.
