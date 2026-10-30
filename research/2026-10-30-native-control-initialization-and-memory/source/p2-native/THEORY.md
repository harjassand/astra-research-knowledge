# P2: useful gates through an uninitialized mediator

Working investigation, 2026-10-30 UTC. **Root derivations and root checks only. No independent review, priority determination, experimental validation, device threshold, or practical advantage is asserted.**

## 1. The useful task and the continuity boundary

The recipient's task is an entangling unitary on two data qubits, including unknown inputs entangled with arbitrary references. The mediator may start dirty and correlated with other retained memory, and its environment continues evolving throughout the operation. The recipient does not need the mediator's microscopic history, a pure mediator, a recovered bath state, a herald, or a return of the apparatus to its initial state.

This is a different useful task from the earlier recovery example. There, an ordinary native syndrome measurement already returned the logical information after one source call. That simpler construction remains the preferred solution to that example. Nothing below supersedes it or identifies logical release with apparatus readiness.

Accepted earlier foundations, including N675 with its dependencies, are not reopened. The old physical-restoration bridge retains its reported scoped independent review; the helper's reported 6,208 rational checks and the separately described root checks do not review the present results. The causal subsystem-recovery law, exact-history/timing results, all actual dirty-register negatives, and restrictions on initialization, concurrency, source classes, and final normalization remain as previously stated. Current local preceding work remains in `../p2_information_rescue_20261030/` and is unchanged.

No missing archive was reconstructed. No helper, worker, chat, model change, external send, upload, export, or alternative transfer was used for this investigation. Ordinary new local proof/code files are the saved work. There is no claim that Capital has received or reviewed them.

## 2. The physical access contract

Let the data be two qubits D, and M contain a spin mediator b and an arbitrary returning environment E. Three signed native Hamiltonian handles are available:

\[
 A=X_1\otimes B_1,\qquad B=X_2\otimes B_2,\qquad C=Y_1\otimes B_3.
\]

During a pulse of handle H the complete Hamiltonian is

\[
 I_D\otimes H_M+sH,\qquad s\in\{+1,-1\}.
\]

The memory drift is always present and is never reversed. The initial joint state of data, memory, and reference is unrestricted. The memory is never reset between segments or cycles. The data axes and the native sign interface are part of the physical specification; they are not synthesized using already reliable entangling gates. Unknown static gains and mediator axes are absorbed into the B_j. A controller that only approximates these sign relations has a real control error, treated below.

The spin-interface sufficient premise is

\[
 B_j=(b_j\cdot\sigma_b)\otimes I_E,\quad b_j\in\mathbb R^3,
 \qquad c=(b_1\times b_2)\cdot b_3\ne0.
\]

For the basic nested bracket, identity offsets in B_1 and B_2 are allowed; the outer B_3 must be traceless. A more general sufficient premise is that \(\{B_3,[B_1,B_2]\}\) is scalar. The spin assumption concerns the controlled interface only. H_M can couple b to E and need not commute with any B_j.

This contract is stronger than possession of an unknown black-box channel and weaker than possession of its full calibrated physical dilation. It is not established by measuring one scalar response. In particular, a scalar tolerance does not certify the interface algebra, its dimension, a drift bound, or its stability.

The pulse construction uses one active handle at a time. The harmonic alternative additionally assumes that the three native controls can be applied additively as one specified joint Hamiltonian. That is an explicit interface change, not permission to declare separately certified noncommuting calls concurrent.

## 3. The algebraic entangling term

Write \(P=Z_1X_2\). Direct multiplication gives

\[
 [A,B]=X_1X_2\otimes[B_1,B_2],
\]

\[
 [C,[A,B]]=-iP\otimes\{B_3,[B_1,B_2]\}=4cP\otimes I_M.
\tag{1}
\]

The sign in the second formula follows from \(Y_1X_1=-iZ_1\). For spin operators, \([B_1,B_2]=2i(b_1\times b_2)\cdot\sigma\), and the anticommutator with B_3 is \(4icI\).

Thus a nested interaction can implement an entangling logical Hamiltonian even though each native handle couples to a dirty mediator. This is a special use of standard Lie/average-Hamiltonian control. The contribution being investigated is its complete native realization with unreversed returning memory, its exact access boundary, and its accuracy/resource consequences; broad novelty of commutator gates is not claimed.

### A useful failed ordering

The first tested ordering generated a combination proportional to

\[
 [C,[A,B]]+[A,[B,C]]=-[B,[C,A]],
\]

which vanishes for these data axes and traceless spin couplings. Noncommutativity alone did not acquire an entangler. The failed ordering is retained in `word_series.json`.

## 4. A 96-segment native realization with drift left on

Use anti-Hermitian letters \(d=-iI\otimes H_M\), \(a=-iA\), \(b=-iB\), \(c_0=-iC\); c_0 is a generator, while c above is a real scalar.

Make a twelve-segment palindrome by following

\[
 A,C,B,-A,-C,-B
\]

with the reverse of that list. Each segment lasts tau. For each sign triple in

\[
 G=\{(+,+,+),(+,-,-),(-,+,-),(-,-,+)\},
\]

apply the signs to its A/B/C handles. Concatenate those four twelve-segment blocks and then their reverse block order. The resulting 96-segment word W(tau) is itself a palindrome. All 96 drift contributions have the same sign.

An exact noncommutative rational calculation gives

\[
 \log W(\tau)=96\tau d+\tau^3\left(
 16[c_0,[a,b]]+\frac{64}{3}\sum_{x=a,b,c_0}[x,[x,d]]\right)+O(\tau^5).
\tag{2}
\]

All second- and fourth-degree terms vanish. The exact cubic coefficients and the complete physical word are in `word_series.json`; `explore_word.py` reproduces them using Fractions.

Because each data Pauli squares to I,

\[
 [H_j,[H_j,I\otimes H_M]]=I_D\otimes[B_j,[B_j,H_M]].
\]

Consequently the whole cubic term is a clean logical operation plus memory-only evolution:

\[
 \log W(\tau)=-i96\tau I\otimes H_M+
 i64c\tau^3P\otimes I+
 i\frac{64}{3}\tau^3 I\otimes\sum_j[B_j,[B_j,H_M]]+O(\tau^5).
\tag{3}
\]

The environment was neither frozen nor averaged over a presumed initial state.

### Why this tolerates some unknown controls

A static change in a coupling axis or gain changes B_j and c but does not destroy the word's sign identities. An unknown stable pulse shape can also be used in a balanced, time-symmetric base block: the first-order native means must vanish, and the same signed/time-reflected shapes must be reused. The group projection then retains only cubic words with either two identical controls and one drift, or one each of A,B,C. The first class is memory-only; the second gives the central bracket combination. Its scalar coefficient must be nonzero and calibrated or bounded. This is immunity to specified shared structure, not immunity to arbitrary pulse errors.

## 5. A complete-memory bound without the global bath energy norm

A bounded H_M is sufficient but unnecessarily restrictive. Let H_M be self-adjoint, possibly unbounded, and suppose the controlled operators have a norm-C^4 interaction-picture orbit. More precisely, require bounded commutators \(\operatorname{ad}_{H_M}^k(H_j)\) for k=0,...,4, interpreted on a common core and extended so that the corresponding orbit is differentiable in operator norm. These are additional regularity premises, not an automatic extension to all oscillator/Fock couplings.

Normalize any qualified symmetric cycle to physical duration T with bounded fixed shapes u_j(s), s in [0,1]. Set

\[
 h_k=\sum_j \|u_j\|_\infty\,
 \|\operatorname{ad}_{I\otimes H_M}^{k}(H_j)\|.
\]

In the centered interaction picture,

\[
 U(T)=e^{-iH_MT/2}\,\widetilde U(T)\,e^{-iH_MT/2},
\]

where tensor identities on data are implicit. Qualification through degree four means

\[
 \widetilde U(T)=I+T^3K_3+O(T^5),\quad
 K_3=i\kappa P\otimes I+I\otimes M_3,
\]

with M_3 anti-Hermitian. Palindromicity ensures the absence of an even fourth-order term. Define

\[
 C_5=\frac{h_4}{384}+\frac{h_0h_3}{48}+\frac{h_1h_2}{16}
 +\frac{h_0^2h_2}{16}+\frac{h_0h_1^2}{8}
 +\frac{h_0^3h_1}{12}+\frac{h_0^5}{120}.
\tag{4}
\]

Then

\[
 \left\|U(T)-e^{i\kappa T^3P}\otimes
 \left[e^{-iH_MT/2}e^{T^3M_3}e^{-iH_MT/2}\right]\right\|
 \le C_5T^5+\frac12\|K_3\|^2T^6.
\tag{5}
\]

This is a particular same-memory comparison unitary, with no normalization or replacement of the actual physical evolution.

**Proof of the remainder.** Expand the centered interaction propagator into its first four Dyson integrals and a fifth-order integral remainder. The latter is bounded by \((h_0T)^5/5!\), using the norm-one exact unitary at its final integration endpoint. In the n-th integral for n=1,...,4, expand the product of interaction-picture operators through parameter degree 4-n. A parameter derivative of order k has norm at most \(h_k/2^k\), since centered normalized times lie in [-1/2,1/2]. Leibniz and the simplex volume 1/n! bound the omitted coefficient by

\[
 T^5\frac1{n!}\sum_{k_1+\cdots+k_n=5-n}
 \prod_{j=1}^n\frac{h_{k_j}}{2^{k_j}k_j!}.
\]

Adding n=5 with all k_j=0 gives (4). The exact lower-degree identities leave I+T^3K_3. The unitary exponential Taylor remainder is at most \(\|K_3\|^2T^6/2\). Multiplication by the two exact half-drift unitaries changes no norm. This proves (5).

The bound depends on local dynamical regularity of the interface, not the norm of an extensive bath Hamiltonian or the dimension of its history. It does not assert that those local bounds are small or known in a given device.

### Reuse and causal composition

For N repetitions, the same physical memory undergoes the same cycle each time. Telescoping gives at most N times (5), compared with

\[
 e^{iN\kappa T^3P}\otimes V_M(T)^N.
\]

Choosing N and the duration to make \(N|\kappa|T^3=|\theta|\) gives a completed entangling gate with error O(T^2), total physical duration O(T^-2), and O(T^-3) cycles. The constant includes c and the local commutator bounds. Arbitrary initial reference/memory correlations are covered by the operator norm.

Each comparison is a per-operation product unitary and can be composed with later, specified operations on the same memory. This is a causal per-call reference; it is not an inference from normalization of a completed-program amplitude. Coherent control of different native programs would require its own physical construction: a memory unitary depending on a coherent program selector cannot simply be ignored.

## 6. The smoother attempt: failure, repair, and comparison

The first six-tone guess paired frequencies {1,2}, {3,4}, {5,6}, with amplitudes chosen to have zero mean and zero second moment. Exact Fourier integration disproved the guess. For example, the DAB coefficient is \(217/15000\) times \((2\pi i)^{-2}\); there are also repeated-control resonances. Disjoint Fourier support did not cancel mixed drift terms.

For real cosine controls \(u_a(s)=\sum_n a_n\cos(2\pi ns)\), the linear second-moment condition is

\[
 \sum_n a_n/n^2=0.
\]

For disjoint supports, the mixed one-drift term vanishes when

\[
 \sum_{n,m}\frac{a_n b_m}{m^2-n^2}=0.
\tag{6}
\]

The repaired nine-tone design uses A frequencies {1,3}, B frequencies {7,11,17}, and C frequencies {8,12,16,20}. A has amplitudes (1/10,-9/10). The B amplitudes are the normalized rational null vector of its moment condition and (6) against A. The C amplitudes are the normalized null vector of its moment condition and (6) against A and B. The supports avoid all repeated-control resonances while retaining ABC resonances. All amplitude l1 norms equal one.

`harmonic_series.py` computes every Dyson coefficient through degree four by exact rational Fourier integration and takes a noncommutative logarithm. It checks that only D, the three memory-only cubic double commutators, and multilinear ABC terms remain. Exact amplitudes and coefficients are in `harmonic_series.json`, together with the failed six-tone result.

For the numerical fixture below, the useful coefficient per physical period cubed is approximately -0.0000617180168621. Full joint Schrödinger integration followed by powers of the actual period unitary retains the same memory throughout. Refining the integration tolerance changes the longest repeated result by a computed telescoping discrepancy below 2.3e-10; this is a convergence check, not an interval-arithmetic proof.

The smoother waveform did not win the useful comparison. At total duration about 3182, its chosen product-gauge operator error is about 0.002375, versus about 0.000580 for the pulse word at duration about 3185. The waveform also needs simultaneous additive controls and accurately maintained relative harmonic weights. Its success is an alternative construction, not an acquired advantage. A scalar calibration of the useful angle is considered separately below rather than mistaking a phase offset for irrecoverable damage.

## 7. Raising accuracy without reversing the bath

The slow holding-time dependence motivates a second construction. The idea is to cancel the next data-dependent error while permitting whatever memory-only evolution the physical sequence produces.

### Native sign group and its restricted invariant algebra

Changing the signs of A,B,C by g in G is an allowed modification of the native control word. It can also be represented mathematically by data Pauli conjugations, but no ideal Pauli pulse is inserted physically. Every data word generated by A,B,C and the memory drift has second-qubit factor I or X_2. Under G, an invariant word has either all-even A/B/C parities or all-odd parities. Its data factor is respectively I or proportional to P. Thus, within this actual generated algebra, a G-invariant coefficient has the form

\[
 I_D\otimes M+P\otimes Q.
\tag{7}
\]

Flipping just C preserves the I part and reverses the P part. The central useful term \(i\lambda P\otimes I\) commutes with every operator of form (7), and with arbitrary memory-only terms.

### The order-raising lemma

Suppose a palindromic native word has memory-only logarithm coefficients below odd degree m>3, apart from the useful cubic \(i\lambda\tau^3P\), and its first possibly bad data term is degree m. Its leading memory drift is the same for every native sign variant.

1. Concatenate its four G variants and their reverse order, eight subwords in all. The lower logical term is unchanged by G. Through degree m, cross-commutators of lower terms are memory-only because the only lower logical term is central. Therefore the first bad coefficient is projected into (7). The result S is still a palindrome.
2. Let S_+ be this projected word and S_- its native C-sign reversal. Set \(r=2^{1/m}>0\) and execute

\[
 R(\tau)=S_+(\tau)\,S_-(r\tau)\,S_+(\tau).
\tag{8}
\]

Chronological direction is immaterial in this displayed palindrome. The physical memory drift runs forward in all three calls.
3. The degree-m P coefficient is multiplied by \(2-r^m=0\). The useful cubic coefficient is multiplied by \(2-r^3>0\). All new lower cross-commutators are memory-only. Palindromicity eliminates the next even degree. The first remaining bad data term is therefore degree m+2.

This proves an order increase of two, without an inverse of H_M, a fresh bath, a clean mediator, or a pre-existing clean logical gate. Exact native sign/timing relations are premises of the construction and remain real control obligations.

For the base word m=5. The first raised word has 2304 segments, duration

\[
 768(2+2^{1/5})\tau,
\]

and useful cubic coefficient

\[
 \lambda_1=512c(2-2^{3/5}).
\]

It has a same-memory product reference through degree six and per-cycle data error O(tau^7). Repetition for a fixed useful angle gives O(tau^4) error. The finite root numerical checks observe seventh-order single-cycle scaling in the small-tau regime.

`check_order_raising.py` verifies the critical composition identity exactly in Q[r]/(r^5-2). It uses arbitrary noncommuting memory letters D,M,N and a first data error E, with the useful L central. Through degree six the only data-dependent term is (2-r^3)L. That exact check reviews the stated abstract quotient identity, not every physical premise. The group-projection step is supplied by the analytic argument above; full 16-dimensional physical simulations are separate root checks.

The construction can be iterated. If q counts the number of order raises, the first bad per-cycle degree is 5+2q, the completed-gate error is O(tau^(2+2q)), and the physical duration remains O(tau^-2) for fixed q. Thus the sufficient accuracy dependence becomes O(epsilon^(-1/(q+1))). The segment count increases by 24 at every raise, and the constants, bandwidth, and required local commutator regularity also grow. This is not a statement that arbitrarily high order is efficient or fault tolerant. General concatenated dynamically corrected gates and high-order commutator formulas are prior constructions; the present claim is the explicit native quotient construction under the stated interface.

For local regularity at higher order, the Dyson argument in Section 5 has the general remainder constant

\[
 C_m=\sum_{n=1}^{m}\frac1{n!}
 \sum_{k_1+\cdots+k_n=m-n}\prod_{j=1}^{n}
 \frac{h_{k_j}}{2^{k_j}k_j!}.
\]

It bounds the omitted degree-m term in the centered propagator by C_m T^m. At the first raise, m=7 and norm-C^6 interface orbits suffice. The centered logarithm through degree five is a memory-only polynomial plus the useful cubic; its bounded memory polynomial defines a unitary reference. Exponential remainders start at the next unmatched degree. No bound on the global bath energy is inserted by the recursion.

### 7.1 Why ordinary angle calibration was tested first

In the original fixture, ordinary angle calibration removes most of the basic word's apparent error. At tau about .02, optimizing a common logical angle reduces the chosen product-operator error from 0.000580 to 0.0000290. More concretely, retuning the actual native duration from .0199974182 to .0200023006 using an exactly estimated data X_1 signal gives the desired pi/4 gate with joint product error about 0.0000265. At tau about .012, actual signal retuning gives error about 0.00000209 at duration about 8846. This defeats a numerical advantage claim for the longer word in this fixture.

The signal retuning is an ideal-estimated-signal comparison for a specified calibration memory state, not a completed finite-shot physical calibration. Its resulting *joint unitary* is nevertheless compared uniformly with the desired logical operation on arbitrary inputs. The code distinguishes full-matrix angle fitting, actual duration retuning, and physical calibration acquisition. Both constructions must pay their actual acquisition costs.

### 7.2 A retained-sector error that one common calibration cannot remove

Keep the same three controlled interfaces and replace the memory drift by

\[
 H_M=.23Z_b+.14Z_bZ_E+.11X_b.
\tag{8a}
\]

Z_E is conserved. The two environment sectors therefore have different mediator dynamics, while c=.925 is identical in both. They may be populated incoherently or be part of an arbitrary coherent retained memory.

Exact rational free-word expansion and four-qubit Pauli arithmetic give the following component of the fifth-degree logarithm of the **basic 96-segment word**:

\[
 K_5\supset i q_E P\otimes I_b\otimes Z_E,
 \qquad q_E=\frac{7187362}{46875}\ne0.
\tag{8b}
\]

The check also verifies that this component comes entirely from terms containing two drifts and three controlled couplings. The exact certificate is `sector_certificate.json`, reproduced by `exact_sector_check.py`. The coefficient is about 153.3303893 in the tau convention of (2).

This is not a memory-only phase and is not a common logical angle. A scalar angle changes P tensor I_M; a memory commutator has zero bus trace separately in each conserved sector. Thus neither scalar recalibration nor a memory commutator can remove (8b).

There is also a lower bound on the actual useful logical task. Let N tau^3=theta/(64c), and take the mediator maximally mixed in each of the two fixed environment sectors. Denote the two resulting logical channels by E_+ and E_-. Use the product reference through cubic order. Its memory part commutes with Z_E, and its logical part commutes with P. To first order in the fifth-degree perturbation, tracing the mediator leaves a difference of logical Hamiltonians whose P coefficient is

\[
 2a\tau^2,\qquad a=\frac{q_E\theta}{64c}.
\]

**Justification of the expansion.** The principal logarithm is valid for sufficiently small tau. Replacing N log W by its degree-five truncation costs O(N tau^7)=O(tau^4). The second Duhamel term in the remaining fifth-degree perturbation is also O((N tau^5)^2)=O(tau^4). In the first term, the bus trace is invariant under the reference memory unitaries, and the P component is invariant under the reference logical rotation. The retained Z_E component therefore cannot be time-averaged away.

For a normalized maximally entangled data/reference input, an infinitesimal Hamiltonian difference H produces Choi trace norm 2 times the standard deviation of H in the maximally mixed state. The P coefficient above alone implies

\[
 \|J_{\rm norm}(E_+)-J_{\rm norm}(E_-)\|_1
 \ge4|a|\tau^2-O(\tau^4).
\]

For any one common target channel, the triangle inequality then gives a worst-sector logical trace-distance error of at least

\[
 |a|\tau^2-O(\tau^4).
\tag{8c}
\]

At theta=pi/4, a is approximately **2.034212942**. A common unitary calibration leaves the distance between the two channels unchanged. This lower bound concerns actual logical outputs, even after the memory is discarded. It is not an artifact of requiring the full memory history or a particular product gauge. It is an obstruction for this unmodified pulse family and a common calibration, **not** an impossibility for other native control programs, sector identification with additional operations, reset, or encoded error correction.

The numerical normalized-Choi witness divided by tau^2 is about 2.04738 at tau .01, 2.03891 at .006, and 2.03538 at .003, approaching the analytic coefficient. The raised word cancels the entire degree-five data term, including (8b), without learning the sector. Thus the order-raising construction removes a demonstrated memory-dependent logical error, rather than just correcting an unnecessary surrogate task.

The finite raised-word results are not monotone in duration: in this sector fixture the joint fitted-angle error is about .000252 at duration 32,372 and .000294 at duration 82,818, before falling to about .00000172 at duration 230,026. The asymptotic theorem does not license a monotone finite-resource advantage. At the smallest reported errors, floating-point unitarity drift is explicitly recorded; these are numerical checks, not rigorous interval bounds.

### 7.3 Continuing the attack on the timing requirement

The ratio r=2^(1/5) in the three-call construction is an actual control requirement. If it has an error delta_r, the fifth-degree cancellation leaves a completed-gate contribution O(delta_r tau^2). Maintaining the ideal O(tau^4) scaling requires delta_r=O(tau^2), in addition to calibrating the changed useful cubic angle. The proof does not make that timing accuracy free.

A second exact composition eliminates the independent irrational ratio:

\[
 R_{\rm clock}(\tau)=S_+(\tau)^{16}\,
 S_-(2\tau)\,S_+(\tau)^{16}.
\tag{8d}
\]

All intervals are one or two ticks of a common clock. The fifth-degree data coefficient is multiplied by 32-2^5=0; the useful cubic is multiplied by 32-2^3=24. The palindrome and the memory-only cross-commutator argument are unchanged. Hence this construction also has per-cycle error O(tau^7) and completed-gate error O(tau^4), with forward memory drift throughout.

The exact abstract certificate now checks both compositions. A clock cycle contains **25,344 constant-control segments, 26,112 common clock ticks**, and has logical coefficient 12288c tau^3. A two-tick constant-Hamiltonian segment can be executed as two identical one-tick evolutions, so it does not demand an independently tuned pulse ratio. The same stable shared-control premise and the actual effects of jitter remain obligations; a common clock has not become an ideal physical resource by being named.

More generally, at odd bad degree m, use S_+^(2^(m-1)), then S_-(2 tau), then S_+^(2^(m-1)). It cancels that degree with useful cubic coefficient 2^m-8>0. The rapidly increasing word length and constants prevent any claim that this is automatically efficient.

`check_integer_clock.py` executes the physical gate on the retained-sector fixture, including both short and doubled segments, and records completed-gate errors and the logical Choi witness. The useful result is a reduced *kind* of timing requirement, not an unconditional performance win. Long cycles can have poor finite-duration behavior; all such data are retained.

The smallest integer-clock numerical row, tau about .0016, has accumulated unitarity drift about 1.2e-8 and reported product error about 2.1e-8. That row is explicitly marked **precision-limited** and is not evidence for a gate accurate to that level. Its sector-channel witness is likewise unresolved at that precision. The exact composition identity and the asymptotic analytic theorem do not depend on that row.

## 8. A genuine obstruction for the useful task

The failure c=0 has a stronger meaning in a restricted, precisely stated access class.

Take the admissible zero-drift memory case with a single mediator spin. Suppose all controlled mediator vectors lie in a common plane. Rotate its mathematical coordinate basis so that this plane is the real X-Z plane. Allow arbitrary local unitary controls on the two data qubits as well as the controlled couplings. Do not add mediator measurement/reset, initialized work systems with new couplings, or another symmetry-breaking Hamiltonian.

Let

\[
 \Theta=(Y_1Y_2\otimes I_b)K,
\]

where K conjugates the whole chosen computational basis. Every allowed Hermitian Hamiltonian is odd under Theta. Antiunitarity then makes every available unitary commute with Theta. This is an exact control symmetry, with no small-error expansion.

For a maximally mixed mediator, the resulting data channel E is covariant under the two-qubit spin flip

\[
 F(\rho)=Y_1Y_2\rho^*Y_1Y_2.
\]

The target \(U_\theta=e^{i\theta P}\) is transformed by that spin flip to U_-theta. Define \(\delta=\sup_\rho\|E(\rho)-U_\theta\rho U_\theta^\dagger\|_1\). Covariance and the triangle inequality imply

\[
 2\delta\ge\sup_\rho\|U_\theta\rho U_\theta^\dagger-
 U_{-\theta}\rho U_{-\theta}^\dagger\|_1=2|\sin(2\theta)|
\]

for |theta|≤pi/4. Hence

\[
 \delta\ge |\sin(2\theta)|.
\tag{9}
\]

At theta=pi/4 the worst-case trace-distance error (using the conventional factor 1/2) is at least 1/2. This is an obstruction to the actual logical channel even if the mediator is discarded at the end; it does not arise from requiring microscopic memory restoration. It holds even with stronger local data unitary controls than the positive construction uses.

For a nonzero known drift that breaks the symmetry, additional mediator access, a suitable prepared resource, measurements, or new workspace interactions, this proof need not apply. Since the robust unknown-drift class includes zero drift, no uniform guarantee over that class can evade this zero-drift instance without changing the stated native access.

### A near-plane speed bound

If only B_3 has a component of norm h perpendicular to the common B_1/B_2 plane and its amplitude is at most one, compare a duration t protocol with its coplanar Hamiltonian. Duhamel bounds the joint unitary difference by ht and the reduced channel trace-norm difference by 2ht. A protocol with logical error delta must therefore satisfy

\[
 t\ge\frac{|\sin(2\theta)|-\delta}{2h}
\tag{10}
\]

when the numerator is positive. Here \(h=|c|/|b_1\times b_2|\) for independent B_1,B_2. This establishes a chirality-limited speed scale in that access class. It does **not** prove that the epsilon dependence or large constants of the pulse construction are necessary.

## 9. Scalar acquisition with retained memory

If c is not supplied, the constructed operation offers a data-only calibration channel; it does not acquire the rest of the dilation. For the actual known calibration input |+>_1|0>_2 and a measurement of Y_1X_2,

\[
 \langle Y_1X_2\rangle_{e^{i\phi P}|+0\rangle}=-\sin(2\phi).
\]

Choose a probe duration/count using a supplied upper bound on |c| so that |phi|≤pi/8. The response is invertible and its derivative with respect to c is bounded away from zero. A real data preparation procedure, measurement, classical controller, entropy outlet for repeated data preparation, and their independently bounded biases are needed. No ideal reset of the dirty mediator is used or silently substituted.

The uniform complete-memory bound also permits correlated calibration trials. Conditional on every previous record, the same logical signal differs by at most b from its ideal value, where b includes the operator-error contribution (at most twice that error for this observable), preparation trace-norm error, and measurement bias. For m outcomes in {-1,+1}, the conditional-range Hoeffding martingale bound gives

\[
 \Pr(|\bar y-y_{ideal}|>b+s)\le2e^{-ms^2/2}.
\]

An independently initialized bath and IID samples are unnecessary under this uniform conditional bias contract. The contract and real preparation/readout are not obtained merely by fitting the observed sinusoid. On the chosen branch, the mean-value theorem turns this into a c interval; a lower bound away from zero is necessary for uniformly finite relative-accuracy cost.

An error delta_c in c produces a useful-angle error of approximately |theta delta_c/c|. Calibration duration, the number of complete physical probe gates, data preparation/readout errors, holding, and entropy export belong in any claimed advantage. No such favorable device-level accounting has yet been demonstrated.

## 10. Native errors, holding, and actual negatives

An uncompensated Hamiltonian error delta_H(t) contributes at most its integrated operator norm to the joint unitary error. For an unknown data holding term of strength zeta, this is zeta times the entire physical duration. A shared static gain error already absorbed in B_j is different from a plus/minus sign imbalance or a time-varying error that violates the symmetry.

For a fixed order q, a typical sufficient budget is

\[
 a_q\tau^{2+2q}+b_q\tau^{-2}+\text{calibration/preparation/readout terms}.
\]

The first term is the derived coherent remainder; the second can include uncorrected holding and residual native bias. Optimizing this upper bound gives a design tradeoff, not an impossibility theorem. The actual coplanarity obstruction (9) has a different proof and scope.

In the finite fixture, a 0.1% imbalance between negative and positive pulse gains worsened the basic gate's product-operator error from approximately 0.081 at tau about .05 to 0.484 at tau about .02. A data-only holding term .001 X_1 produced errors about .457 and 1.857 at those two scales. Smaller pulses did not make these real defects disappear.

The initially proposed identity-offset negative was wrong: an identity component in inner B_1 cancels from [B_1,B_2] and is benign for (1). Its successful runs are retained. Moving the offset to outer B_3 creates a genuinely noncentral cubic term and a persistent error in the tested fixture. A scalar gain calibration cannot establish that this term is absent.

The harmonic shape perturbation and data-holding perturbation are separately retained in `harmonic_checks.json`. A particular small shape perturbation need not increase every fitted error; it is not labeled an impossibility. It invalidates the exact qualified cancellation and must be assessed as its actual complete physical process.

No reset, rejection flag, error detector, source isolation, reliable logical memory, or noisy-control threshold has been acquired. Error correction still requires its genuine syndrome acquisition, controls, holding, readout, entropy disposal, and marked fault supports. If these gates are later embedded in the earlier fault-tolerance machinery, its initialized circuit-wide hypotheses must still be established.

## 11. Strong ordinary alternatives and prior work

The entire mechanism belongs in comparison with ordinary Hamiltonian engineering. No advantage over an optimally calibrated controller with the same physical access has been established.

* **Native syndrome recovery:** already solves the preceding logical-repair example; full coherent bath retrieval is an unnecessarily stronger task there.
* **Known-generator cancellation / optimal control:** full Hamiltonian knowledge and suitable signed controls can support shorter compiled trajectories. Learning that physical generator, including its returning environment, is an extra resource if it is not already available. Knowledge of only c is not equivalent.
* **A seven-pulse ordinary entangler in a stronger special case:** if H_M=0 and the three mediator axes are known orthogonal Pauli axes with calibrated strengths, let A=X_1 X_b, B=X_2 Y_b, C=Y_1 Z_b. Conjugating B by exp(-i pi A/4) produces D=X_1X_2Z_b. Conjugating C by exp(-i pi D/4) produces P. Thus a desired exp(-i theta P) is made from seven native pulses using the two conjugations. The mediator can still be arbitrary. This construction wins that calibrated, drift-free case; no reset is needed. Its immunity to an unreversed arbitrary H_M is not supplied by those seven pulses.
* **Direct reset / refresh:** where actual mediator access and reset exist, they deserve a full comparison, including reset duration, errors and entropy export. They are not automatically available through the present three handles.
* **Delayed recovery / echo:** a known jointly invertible excursion can be delayed or undone when its inverse and output access exist. The present construction never claims an unknown bath inverse. The earlier passive-inverse and cancellation failures remain failures under their original premises.
* **Dynamically corrected gates:** bounded-control and arbitrarily high-order error-suppression constructions are established prior machinery. Their physical control assumptions must be matched; they should be used directly when they already supply the requested operation. The native order-raising lemma here does not claim to invent that general framework.

Primary sources consulted:

1. Lloyd, Landahl and Slotine, *Universal quantum interfaces*, Phys. Rev. A 69, 012305 (2004), https://doi.org/10.1103/PhysRevA.69.012305 . Broad indirect-control precedent.
2. Albertini and D'Alessandro, *The Lie algebra structure and controllability of spin systems*, Linear Algebra and its Applications 350 (2002), https://doi.org/10.1016/S0024-3795(02)00290-2 . Lie controllability and structural obstructions are established subjects.
3. *Exact Algebraic Conditions for Indirect Controllability of Quantum Systems*, SIAM J. Control Optim. 53 (2015), https://doi.org/10.1137/130949816 . Auxiliary-state dependence and indirect-control conditions.
4. Khodjasteh and Viola, *Dynamical quantum error correction of unitary operations with bounded controls*, Phys. Rev. A 80, 032314 (2009), https://doi.org/10.1103/PhysRevA.80.032314 . Bounded-control native alternatives.
5. Khodjasteh, Lidar and Viola, *Arbitrarily accurate dynamical control in open quantum systems*, Phys. Rev. Lett. 104, 090501 (2010), https://doi.org/10.1103/PhysRevLett.104.090501 . Arbitrary-order concatenated dynamically corrected gates.
6. *Efficient product formulas for commutators and applications to quantum simulation*, Phys. Rev. Research 4, 013191 (2022), https://doi.org/10.1103/PhysRevResearch.4.013191 . High-order commutator formulas are prior.
7. Oreshkov, *Holonomic Quantum Computation in Subsystems*, Phys. Rev. Lett. 103, 090502 (2009), https://doi.org/10.1103/PhysRevLett.103.090502 . Initialization-free subsystem holonomies are prior; the exploratory polar/STIRAP route was not counted as a new capability.
8. Verstraete, Wolf and Cirac, *Quantum computation and quantum-state engineering driven by dissipation*, https://arxiv.org/html/0803.1447v2 . Reciprocal clock/dissipative computation was an early working alternative, not a novelty claim.

These searches do not establish priority for any lemma here. Denied full-page retrievals were not retried through alternate routes. Earlier transfer restrictions remain in force.

## 12. Finite fixture and review ledger

The complete-memory fixture is two data qubits, a mediator spin, and an environmental spin, with

\[
 b_1=(.9,.2,-.1),\quad b_2=(-.2,.8,.3),\quad b_3=(.1,-.3,1.1),
\]

\[
 H_M=.17X_b+.13Z_bX_E+.11Y_E,
 \qquad c=.925.
\]

Both the drift/control commutators and the control/control commutators are nonzero. The actual 16-dimensional joint unitary is powered without resetting any subsystem. Operator norm comparisons cover arbitrary dirty memory states and correlations in this finite model.

The word's cubic factorization is checked directly against the matrix identity. The harmonic result has an exact rational Fourier-series certificate plus independent-in-method numerical integration, all performed by the same root. The order raise has an exact abstract algebraic-number certificate plus full physical simulations. These are finite mathematical/computational checks, not independent analytic review.

A product gauge obtained from the polar factor of a partial data trace is a chosen comparison unitary. It is Frobenius-optimal for that fixed logical target, but is not certified optimal in operator norm. It is not a physically implemented memory reset. The named explicit-reference errors and chosen-gauge errors must not be conflated. No plotted or tabulated upper bound is an impossibility claim.

The higher-order construction improves the mathematical accuracy exponent, with substantial pulse and holding costs. The smoother construction did not improve the tested useful task. The strongest ordinary logical-angle calibration comparison is recorded in the accompanying numerical work; its result must be carried alongside any numerical advantage claim.

## 13. Uncompleted exploratory trails

Early analysis considered reciprocal computation clocks, polar-factor transfer through a static distorted coupling, and time-dependent dark-space geometry. Existing Feynman/dissipative computation, quantum polar algorithms, degenerate STIRAP, and initialization-free subsystem holonomies were strong ordinary alternatives. Those paths did not acquire a new operational advantage here. In particular, an attempted fast echo of bright-state dynamics does not automatically preserve adiabatic dark transport. No proof or device capability is claimed for that suggestion.

A further harmonic-design observation was retained but not promoted to a completed gate: two-frequency cosine pairs with zero second moment have a vanishing mutual mixed-drift coefficient when their inverse-square frequency sums agree. A rational search found three disjoint resonant pairs (875,3000), (910,2184), (1785,952), with 875+910=1785. The high frequencies and long common period make an efficiency benefit doubtful; the full physical gate was not executed. This candidate is not part of the qualified nine-tone result.

The promising retained principle of the current construction is narrower and concrete: the useful data operation can depend on an invariant of a native interaction algebra while the full apparatus state remains unknown and evolves forward. The work supplies a native pulse mechanism, a local-dynamics error law, an accuracy-raising construction, and an actual useful-task obstruction under matched access. Its hardware and optimal-control advantages remain unresolved.
