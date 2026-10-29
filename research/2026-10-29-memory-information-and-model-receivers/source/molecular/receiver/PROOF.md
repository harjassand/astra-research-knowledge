# Native span transfer and its actual fringe/return contract

The question is whether the demonstrated Ca+/CaOH+ controls can replace an optical S/D memory by the S1/2 Zeeman doublet during infrared science, without silently destroying the histories through motion-dependent logical rotations. Common qubit transfer is sufficient but stronger than every actual consumer needs. This work derives the weaker contract and consumes T's finite-history kernels; it does not propagate another pulse sequence or claim a qualified native gate.

## 1. Source, graph and native resources

The inherited N796 operation/source and T's late-independent hypothesis were read. The primary [Wu et al.2026](https://arxiv.org/html/2511.19687v2) reports the molecular recoil/cat platform. Its selected-mode parameters yield eta729=.088257846, omega/2pi=400225.68 Hz and a modeled packet mean near43.65. They do not specify every added RF/Zeeman control or its joint fidelity. The selected graph is

    a = S1/2,-1/2,    d = D5/2,-5/2,
    b = S1/2,+1/2,    c = D5/2,-3/2.

These are the selected native-allowed levels, not an independently verified complete electronic configuration of the CaOH apparatus. Direct d↔b quadrupole transfer has delta-m=3 and is forbidden. RF d↔c and quadrupole b↔c are allowed. The optical tensor also couples a↔d with amplitude sqrt(5) times b↔c. RF at the D Zeeman spacing drives the entire six-level D chain, not just d,c.

The spin-qubit precedent arXiv:0902.2826 uses **Raman** manipulation. A proper direct-RF precedent is [Kurz et al.2014](https://doi.org/10.1038/ncomms6527), with RF plus quadrupole shelving in another40Ca+ apparatus. Root independently read its governing primary passages. Its2.8 us RF preparation is pi/2, so T infers a5.6 us pi swap at that drive; neither time is a measured hot-cat control in the CaOH apparatus. Added coil/field uniformity, coherent RF/729 phase references, actual B, transition selectivity, pulse noise and readout are resources, not supplied by the RF trap drive.

Pure optical q=-2 is not automatically a single travelling-wave polarization. For a wave with k along x and linear epsilon along y, relative to quantization z, the E2 gradient has q=+2 and−2 with equal magnitudes; q=0 cancels. Exact single-q=-2 rank-two gradients generally require more field structure. Ordinary Zeeman frequency resolution can suppress the mirror S,-1/2→D,+3/2 and S,+1/2→D,+5/2 edges, but requires the actual field/geometry and detuning/error bounds. No pure-gradient actuator or infinitely resolved transitions are granted here.

## 2. Full resonant D-chain dark space: a positive structural result

Let D_j have m=-5/2+j. In the resonant RF/carrier RWA, the D-chain edge ratios relative to d↔c are

    beta = (1, sqrt(8/5), 3/sqrt(5), sqrt(8/5), 1).

Let P>0 be the d-c RF Rabi amplitude and O_n=g_n O the b-c optical amplitude, g_n=exp(-eta²/2)L_n(eta²). Ignore only the explicitly off-resonant spectator edges for this statement. In bipartition A=(D0,D2,D4,b), B=(D1,D3,D5), the coupling matrix, up to1/2, is

    C = [[P, beta1 P, 0, O_n],
         [0, beta2 P, beta3 P, 0],
         [0, 0, beta4 P, 0]].

C has rank3. Its kernel has D4=D2=0 and P D0+O_n b=0. Therefore the full seven-level resonant graph has exactly one dark vector

    |D_n> = cos(theta_n)|d> - exp(i phi) sin(theta_n)|b>,
    tan(theta_n)=P/(|g_n|O),

with the sign of g_n included in the endpoint phase. The ideal untouched |a> adds a second dark direction. Thus the extra resonant D levels do **not** structurally prevent the desired two-dimensional isometry.

For constant relative optical/RF phase and g_n of one sign, the dark energy and Berry phase vanish. The counterintuitive path P:0→nonzero, O:nonzero→0 maps d→-exp(i phi)b independently of the magnitude of g_n, leaving a. Hence the ideal carrier-RWA endpoint is a common code isometry, with common free motional evolution separated. On the source finite range n=0,...,119, g0=.99611 and g119=.26463 are positive. That is not an all-Fock or all-mode promise: carrier factors eventually have zeros/sign changes, and spectators contribute products of their own g_nu. Occupation/tail admission must be qualified.

If phi varies, the Berry phase is -integral sin²(theta_n) dphi and can depend on n. A single chirp/phase correction is not automatically common to the whole hot packet. If g_n changes sign, an n-dependent pi endpoint phase likewise remains. At P=0 the resonant dark kernel is larger; the rank argument alone supplies no uniform finite-time adiabatic theorem. T's executed full-chain finite-time errors and local schedule are its independent pulse computations, not a structural no-go or a laboratory result. This work does not rerun them.

## 3. Off-resonant and sideband phases: what the ideal proof omits

With approximate LS factors gS=2,gD=6/5, write Delta=(gS-gD)muB B/hbar. In a consistent rotating frame, a is detuned by−Delta while b and the RF-resonant D chain have zero diagonal. The same drives couple a to d with sqrt(5)O_n/2 and to b through the off-resonant ground RF. The latter RF amplitude relative to d-c is gS/(gD sqrt(5)) in the same angular convention. These terms are linked to the actual fields; they are not independently tunable noise parameters.

Even at the carrier level, virtual a mixing produces n-dependent dispersive phases. If v_n=(sqrt(5)O_n|d>+lambda P|b>)/2 and |Delta| is sufficiently large compared with the electronic drive scales, the leading dark shift is |<v_n|D_n>|²/Delta, while the spectator shift starts at−||v_n||²/Delta. That is a conditional perturbative expression, not a native bound without B and the omitted edges. Adding a and its two driven edges generically removes the exact zero-eigenvalue dark-space protection. It does not prove that the finite transfer/return fails its actual observable.

Importantly, the carrier-only spectator shift is not the full sideband answer. The optical a-d contribution contains denominators Delta+(m-n)omega and all amplitudes of exp[i eta(a+a†)]. If |Delta| dominates the admitted motional offsets, the leading term uses sum_m|D_mn|²=1 and is **independent of n**. Keeping only g_n²/Delta would falsely create a leading native tagging term. Near an unwanted sideband resonance that expansion fails instead. Actual detunings, all populated modes and sufficient tails must therefore be acquired before asserting either cancellation or tagging. The full optical sidebands in T's model do not include every additional Zeeman edge or a measured B.

Physical phase-reversed pulses do not automatically implement the inverse of the full dynamics: the trap Hamiltonian, Zeeman detunings and dispersive shifts are not reversed merely by adding pi to a drive phase. T correctly uses a physical return command in its numerical consumer rather than granting V†. A ground-Zeeman scalar IR Hamiltonian is a useful second-order, linearly polarized limit; ellipticity, finite-B corrections, residual D population, gradients and control noise remain native debts.

## 4. Weakest return contract for the actual science

First suppose, only to expose the hinge, that forward transfer is diagonal in Fock number with logical W_n and return is its exact inverse. For a code-independent parked science S with motional blocks S_mn, the echo has blocks

    (U_echo)_mn = W_m† W_n tensor S_mn.

Thus n-dependent W_n cancels if the particular science commutes with n. It need not cancel for recoil, which changes n. Identical code-space population transfer is insufficient to settle the fringe; conversely failing an arbitrary-qubit isometry is not by itself a rejection. A common logical rotation cancels around code-independent science. A code-independent bath rotation is harmless to which-code coherence but can still rotate the recoil geometry unless compensated or included in the target.

The inherited all-q=0 reference already includes a known electric kick. If the kick is inside parking, it probes noncommuting motion and can expose some W_m†W_n errors; it must not be dismissed as plain q=0 science. Its tested timing, momentum and modes remain the scope. With physical return R rather than V†, the connection is R_m V_n and has to be evaluated with the actual detector/uncat.

In the three-electronic-state model, both a and b fluoresce. If Q_code is a code Pauli with zero on b and P_b is unused-ground population, physical bright-minus-dark is Q_code+P_b after an analyzer that leaves b untouched. In particular

    pDark = [1 - <Q_code> - p_b]/2.

This is why a bare optical Bloch expectation cannot silently serve as the fluorescence probability. The consumed kernels instead include the actual optical analysis pulses and physical bright signs(+1,+1,-1), without postselection.

## 5. Finite molecular words give a sufficient, weaker receiver

Assume the initial atom/motion/reference state is independent of the molecule/common environment. Purify the former for notation, not as a physical extra ancilla. During the short science interval assume frozen selected motion and a common dilation/finite-word description

    U(x) = sum_{h=-H}^H exp(i h kx) tensor M_h,
    U(x)†U(x)=I for every x.

For four source-admitted two-band pulses with one achromatic momentum increment, H=4 suffices. Rotational/internal dimension can be arbitrary. Unpaid spontaneous-emission momenta, extra bands, moving traps during science, pre-existing molecule-motion correlations or branch-dependent environment labels can destroy this finite description. An open-channel version is allowed only if its common Kraus/dilation words satisfy the same pointwise TP identity and finite support; arbitrary jumps are not erased.

Let |out_h> be the full native instrument output for word D(i h eta), including forward parking, physical return, uncat and analysis. For physical observable O define

    K_jh = <out_j|O|out_h>,
    C_hj = Tr(M_h rho M_j†).

Then C>=0 and Tr C=1, and the measured mean is Tr(CK). Crucially pointwise unitarity gives the extra identities

    sum_{h-j=l} C_hj = delta_l0.

The coefficient matrix is independent of the instrument only under the initial product/common-dilation assumptions. No all-C attainability is needed: optimizing over a larger PSD/autocorrelation set gives a valid sufficient upper bound, not an attained native molecular worst case.

For the extra initial-G and charge-preserving-free-interval promises of the source two-band construction, all-q-plus has words{0} and{1} in distinct final bands. With only q2 reversed, the blocks are G:{-2,0,2}, E:{-1,1,3}. Cross-band C entries vanish. These are additional admissions, not consequences of a generic degree4 word expansion.

Any Hermitian Toeplitz T_jh=t_{h-j} obeys Tr(CT)=t0. Therefore:

* A zero-diagonal Toeplitz subtraction is null for a pointwise mean error.
* A full Toeplitz subtraction is null for a normalized **nonzero optical phase coefficient**, when the instrument and its nuisance phase are fixed across that phase cycle. Its constant bias is then independent of the optical phases.

This quotient is ordinary finite-dimensional Gram/semidefinite reasoning; T and this worker independently reached the diagonal-sum refinement. It is not a new generic tomography or sampling principle.

For a specified admitted science family, the exact observational condition is Tr[C(phi) deltaK]=0 at its relevant settings/linear combinations. The computable PSD/autocorrelation relaxation and Toeplitz certificates are sufficient conditions; they are not claimed necessary for every native four-pulse family or optimal over its actual reachable coefficient set.

## 6. Uniform D-phase certificate without phase gridding

T's supplied model resolves ground and D pieces, giving error kernel

    F(z)=A+z B+z^-1 B†,       |z|=1,
    A=Kgg+Kdd-Ktarget, B=Kgd.

The nuisance is a uniform D phase, fixed across optical phase settings. It is not an arbitrary motional/Zeeman-resolved Stark operator. Choose T(z)=T0+z T1+z^-1 T1†, with Toeplitz coefficient matrices. For raw means their diagonals are zero; for a nonzero harmonic they may be unrestricted. For each sign and admitted block, a PSD matrix X certifies

    r I - sign[F(z)-T(z)] = [I,zI]† X [I,zI],
    X00+X11 = rI - sign(A-T0),
    X01 = -sign(B-T1).

This explicit algebra is a sufficient certificate. Matrix Fejer–Riesz factorization is established machinery (e.g. [primary author source, Theorem1.1](https://zalara.github.io/Papers/MatrixFejerRieszArxivOriginal.pdf)); no new general factorization theorem or optimum is claimed. Our proof needs only the displayed PSD-Gram implication.

kernel_bound.py treats the numerical optimizer as a proposal. Toeplitz coefficients and Hermitian X are rounded to rationals. An exact Fraction LDL of the realification checks X+delta I>0. If e0 bounds the constant residual and e1 the first-coefficient residual by entrywise complex l1 sums, then

    r_safe = r + max_blocks(2 delta + e0 + 2 e1)

is valid uniformly on the unit circle. The2delta comes from [I,zI]†[I,zI]=2I. The final residual reference is the **exact canonical Hermitian part of the original supplied binary64 A**, captured before float symmetrization. B is its original supplied binary64 matrix. The initial run that instead certified rounded symmetrization is retained separately, not silently relabeled. This certifies arithmetic on those finite kernels, not their physical/ODE/truncation accuracy.

For mean-bright=2pBright-1, raw probability error is at most r_safe/2. For a normalized5x5x5 nonzero DFT coefficient of real per-setting errors, the character phases are uniformly distributed over five roots. Subtracting the phase-independent bias gives the sharper bound

    |delta coefficient_probability| <= [(1+sqrt(5))/5] r_safe/2.

Indeed max_theta (1/5)sum_j|cos(theta+2pi j/5)|=(1+sqrt(5))/5. This is a finite normalized phase-cycle statement, not an unnormalized sum or an automatic continuous-harmonic identification. Exact rational radii and a rational outward upper for this algebraic factor are saved; printed binary64 decimals are approximate displays.

## 7. Actual consumed result, and useful-target check

The pinned T kernel bytes have SHA a962a6121b7b1985fe5e33cbd38cf7d0d846d66b16cd7edb6592e7c93b2b560d. KERNEL_BINDING.json snapshots the generating code and dependencies. No native propagation is rerun here. The input model has one mode N=100, full optical sidebands, added ideal selective ground-RF swaps, physical same-command return and full optical analysis. Other Zeeman edges, measured field/noise, spectators and native RF acquisition remain unpaid.

For T's smooth-BB1 shelving/return input the resulting physical probability bounds are:

| Admitted class | Axis | Raw mean probability error | Nonzero normalized5³ probability coefficient error |
|---|---|---:|---:|
| General degree4 | Z | .00168851 | .00108624 |
| General degree4 | Y | .00122523 | .00079084 |
| Extra initial-G/charge blocks, q2 minus | Z | .00055344 | .00035062 |
| Extra initial-G/charge blocks, q2 minus | Y | .00047123 | .00030391 |

Table decimals are loosened upward; exact fractions govern. They quantify only the admitted supplied model kernels. The stronger coherent gate criterion is not needed for these bounds. The initially bad bare-pulse kernels are retained as the same-input ordinary control, as are T's simpler raw/operator and Frobenius-Toeplitz bounds. This SDP certificate is more expensive; no generic speed advantage is inferred.

The final16-case solver/certificate consumer took5.356 s after imports; the initial rounded-reference run took5.419 s and remains preserved. Some solver proposals were optimal_inaccurate; exact PSD/residual checks, not those status labels, establish the upper bounds. The pinned producer's kernel generation cost .865 s is additional and credited to T, not an independently implemented pulse simulation.

X is not promoted as a useful spectroscopy channel merely because an error is tiny. word_examples.py explicitly composes four admitted resonant two-band rotations and the normalized optical phase cycle, then contracts with the **actual Ktarget** for Z/Y. In an assumed p=.03-per-pulse model (not inferred CaOH excitation), q2-minus gives nonzero target probability coefficients about1.769e-4(Z) and4.228e-4(Y). Their direct floating model-specific all-z triangle errors are about3.03e-7 and2.02e-7 for the smooth-BB1 kernels. Larger p=.5 controls are also saved. This .052 s algebraic test is neither a molecular fit nor an advantage/affordability result. The universal bounds above alone need not admit the weak signal at a useful relative precision.

The supplementary exact_word_coefficient.py removes phase-quadrature roundoff from this non-null check. It extracts the selected four-pulse Laurent coefficient by integer phase exponents. Every selected path pair contributes (sin(theta/2)cos(theta/2))^4=p²(1-p)², so p=3/100 gives rational coefficients. Contracting them with the exact canonical Hermitian supplied Ktarget gives nonzero rational real parts; the same-input all-z complex-l1 error bounds are below3.20e-7(Z) and2.19e-7(Y). It took .0278 s after imports and reran no ion dynamics. This certifies the declared finite-matrix example, not physical p or source-model accuracy.

## 8. What the native calibration does and does not acquire

Classical known kicks supply K_hh. They are real, valuable loaded tests, especially at source-calibrated timings and strengths; matching them does not generally determine coherent K_jh. A small explicit PSD trace-one coefficient example in WORD_EXAMPLES.json has off-diagonal terms with cancelling lag sums. A zero-diagonal non-Toeplitz kernel changes its contraction while leaving all kick diagonals unchanged. This is a linear information statement, not a claim that the abstract perturbed kernel is a fabricated native instrument or that every unmodeled instrument is possible.

Conditional polarization-identity acquisition could recover a d-word kernel from d diagonal preparations plus four normalized superpositions per pair: d+4*C(d,2)=153 configurations for d=9, per physical analyzer. Preparation norms/success probabilities and trial/reset costs must be counted. The current CaOH setup is **not** granted those coherent superpositions, an extra controlled-displacement ancilla, or full process tomography for free. Ordinary calibrated instrument modeling/tomography is the equally informed alternative. The present finite kernels are actually acquired from the source-informed computation, not from a few experimental kick points.

## 9. Decision

The ideal selected resonant control graph admits the desired common carrier-RWA span transfer without a hot Hadamard; no dark-space dimension obstruction was found. Full native errors and return phases remain essential, but they should be judged on the actual consumer. The finite-word/Toeplitz/uniform-phase receiver supplies such a sufficient model-side test, includes physical fluorescence, and preserves source/calibration costs. It is a composition of established controls and Gram/SOS tools, not a claimed new STIRAP principle.

Native all-mode transfer/readout, physical phase/selectivity/noise, IR-loaded finite-word closure, molecular coefficient/signal, loss/reset and complete throughput remain NOT_ACQUIRED. Neither the passing finite model nor its certificates establish those physical facts. The constructive result is the scoped graph and consumer receiver, not an arbitrary-qubit requirement or a claimed useful spectrometer.
