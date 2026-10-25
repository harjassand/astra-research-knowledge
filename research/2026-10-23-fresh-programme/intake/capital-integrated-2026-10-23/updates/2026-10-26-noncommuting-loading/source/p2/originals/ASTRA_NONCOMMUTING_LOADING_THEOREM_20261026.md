# Spectral-geodesic loading for a noncommuting finite logical code

**26 October 2026 — Astra / foundational physics interim continuation**  
Status: original self-contained theorem candidate, a rigorous complementary protected-code loading no-go, and executed finite-matrix checks, **not** an external mathematical review, historical priority or physical implementation. Reconstructs a governing proof absent from the supplied loading summary. **Preserves the distinction between a full degenerate code and a protected code inside a larger controller.**

## 0. Comparison and decision

The incumbent capacity programme gives an unusual connection from a local bare occupancy restriction to multi-particle continuum spectra. In its homogeneous model it establishes capacity one in all finite sectors, and an exactly quadratic one/two-particle operation whose first nonlinear response occurs at the three-particle level. It does **not** yet establish capacity two for all particle sectors. A strongly different possibility in Astra is the amplifier-entropy/information programme (N557, N967), whose exact information-theoretic consequences may have greater mathematical breadth but do not presently give an identified physical device or operational improvement. I pursued the incumbent's physical preparation bottleneck: is a single physical coupling ramp enough to coherently dress an arbitrarily encoded finite logical subspace with one **noncommuting** bath, with an ultraviolet-independent *state* error? The answer below is yes for the specified completed matrix Hamiltonian, and no general uniform spectral gap is available when an extra bare complementary controller penalty is inserted.

## 1. Model, scope and control contract

Use units `hbar=1`. Let `C` be a complex code Hilbert space of finite dimension `d`, `B>0`, `H_b` a bath Hilbert space, `Q>=B I` a positive **bounded** self-adjoint operator (finite-band, possibly continuous band), and `G:C->H_b` a bounded coupling. Define

`W=Q^(-1)G`, `L=W^*W`, `D=G^*Q^(-1)G=W^*QW`, all as operators on `C`, except `W`. No commutation between `D,L`, or between `Q` and `WW^*`, is assumed.

For a single scalar experimentally specified envelope `eta in [0,1]`, the actual Hamiltonian on `C + H_b` is

```
H_eta = -B I + A_eta,
A_eta = [ eta^2 D      eta G^* ]
        [ eta G        Q       ]
      = R_eta^* Q R_eta,
R_eta(alpha,beta)=eta W alpha+beta.
```

The control requires **both** `eta G` and the calibrated **matrix-valued counterterm** `eta^2 D`. Initial code states are bare and exactly degenerate at energy `-B`; final states are the desired dressed bound code. The full `d`-dimensional bare subspace is the logical code: **there is no additional bare positive penalty `A` whose kernel is a smaller code**. This is a physical control model, not an automatically acquired endpoint-only Jacobi spin-chain interface. No assertion is made for loss, decoherence, control noise, thermal source preparation, maximum N-sector storage, or generic oscillator truncation.

### Theorem 1 (cutoff-uniform matrix-code loading with one scalar envelope)

For every finite `d` and finite-band `(Q,G)` above, there exists a monotone piecewise-`C^2` scalar schedule `eta(s)` for `0<=s<=1`, with `eta(0)=0`, `eta(1)=1`, such that the exact propagator `i d_s U_T(s)=T H_eta(s) U_T(s)` satisfies

```
|| U_T(1) V_0 - exp(i B T) V_1 ||_op
    <= [2(d+1) ell + 5 ell^2]/(B T)
    <= [d(d+1) pi + 5 d^2 pi^2/4]/(B T),
```

where `V_0=(I_C,0)^T`, `V_1=(I,-W)^T(I+L)^(-1/2)` and

```
ell = int_0^1 max_{j:lambda_j>0} sqrt(lambda_j)/(1+eta^2 lambda_j) d eta
     <= sum_j arctan sqrt(lambda_j) <= d pi/2.
```

`lambda_j` are the eigenvalues of `L`. For `G=0`, the code is stationary and error is exactly zero. **Crucially**, the bound is independent of the number of bath modes, ultraviolet energy range, `||G||`, and the condition number of `L` (for fixed `d,B`). It is an operator-norm/isometry bound and remains true after tensoring an *arbitrary untouched reference* with the identity. It concerns state fidelity, not cutoff-uniform amplitude slew or detuning/coupling work.

### Proof, part A: zero mode, gap and parallel geometry

Let `L=V diag(lambda_j) V^*`, and let `W=U sqrt(L)` be its polar decomposition (`U` is a partial isometry). Put

```
Theta(eta) = arctan(eta sqrt(L)),
C=cos Theta,  S=sin Theta,  M=U tan Theta=eta W.
V_eta = ( C, -U S )^T.
```

Because `C^2+S^2=I` on the support of `L` and `Theta=0` on the kernel,

`V_eta^* V_eta=I`, `R_eta V_eta=0`, and `V_eta^* d_eta V_eta=0` identically. The last identity is matrix-valued and uses only commutativity between scalar functions of `L`, **not** commutativity with `D` or `Q`. Thus all non-Abelian Berry rotations vanish in this fixed gauge. Moreover `R_eta R_eta^*=I+eta^2 WW^* >=I`; the nonzero spectrum of `R_eta^* Q R_eta` equals that of `Q^(1/2) R_eta R_eta^* Q^(1/2) >=B I`. There are exactly `d` zero eigenvalues with a gap at least `B` to every other excitation, for *each cutoff*.

### Proof, part B: explicit reduced inverse even when Q and G do not commute

Write `J=U^*Q^(-1)U`, which need not commute with `L`; `||J||<=1/B`. Set `e_eta=(S,U C)^T`, so for any differentiable schedule `V'_s=-e_eta Theta'_s`. The equation `A_eta chi_eta=e_eta` has the *orthogonal* solution

```
chi_top = S C J C,
chi_bath=Q^(-1) U C - U S^2 J C.
```

To verify it, use `R_eta^* U C=e_eta`, `R_eta R_eta^* = I+U tan^2 Theta U^*` and

`(R_eta R_eta^*)^(-1) = I-U S^2 U^*`.

Then `chi=R_eta^*(R_eta R_eta^*)^(-1) Q^(-1) U C`, which lies orthogonal to the null code. Since the pseudoinverse `R_eta^*(R_eta R_eta^*)^(-1)` has norm at most 1,

`||chi||<=1/B`.

Differentiating the displayed **ordered** matrix products, not moving `J` through `S,C`, gives

`||chi'_s|| <= 5 ||Theta'_s||/B`.

Indeed the code component has three Leibniz contributions bounded by `3||Theta'||/B`; the bath component is bounded by `4||Theta'||/B`; Euclidean block norms give 5. Put `xi_s=-chi_eta Theta'_s`. Then

`A_eta xi_s=V'_s`, `||xi_s||<=||Theta'_s||/B`,

`||xi'_s|| <= [5 ||Theta'_s||^2 + ||Theta''_s||]/B`.

### Proof, part C: a uniform scalar schedule and its total variation

For positive `lambda_j` define `f_j(eta)=sqrt(lambda_j)/(1+lambda_j eta^2)` and `F(eta)=max_j f_j(eta)`. Let `ell=int_0^1 F(eta) d eta` and reparameterize the *single* coupling amplitude by

`s(eta)=ell^(-1) int_0^eta F(u) du`.

Then `Theta'_s` is diagonal in the fixed `L` eigenbasis and has entries `ell r_j(eta)`, with `r_j=f_j/F`, `0<=r_j<=1`. Consequently `||Theta'_s||=ell` throughout.

For each fixed j,

`f_j/f_i = sqrt(lambda_j/lambda_i) (1+lambda_i eta^2)/(1+lambda_j eta^2)`

is nondecreasing when `lambda_i>lambda_j` and nonincreasing when `lambda_i<lambda_j`. Hence `r_j=min_i(f_j/f_i)` is the minimum of one nondecreasing envelope and one nonincreasing envelope, making it unimodal (at most one change from increase to decrease); its total variation is at most 2. The piecewise-smooth envelope `F` has only finitely many mode switches, so these derivatives exist almost everywhere and are integrable. Thus

`int_0^1 ||Theta''_s|| ds <= ell sum_j TV(r_j) <=2d ell`.

The inequality `ell<=sum_j arctan(sqrt(lambda_j))<=d pi/2` follows from `max_j f_j<=sum_j f_j`. **No ultraviolet spectral constants enter these estimates.**

### Proof, part D: exact Duhamel integration

In the interaction picture eliminating `-B`, `V_eta(s)` is a zero-eigenvalue isometry. Differentiating `U_T(1,s) V_s` gives the exact identity

`U_T(1)V_0-V_1 = -int_0^1 U_T(1,s) V'_s ds`.

Insert `V'_s=A_eta(s) xi_s`, integrate by parts using `partial_s U_T(1,s)=iT U_T(1,s) A_eta(s)`, and use unitarity. The operator-norm error is at most

`[2 sup_s ||xi_s|| + int_0^1 ||xi'_s|| ds]/T`.

Parts B/C give the claimed `[2(d+1)ell+5ell^2]/(BT)` bound. Spectator references do not alter operator norms. The result is uniform in ultraviolet bandwidth but uses `d` fixed. QED.

## 2. Second attack: an exact finite-time geometric implementation and a speed limit

A second, stronger *but more demanding control* follows by allowing the **bath spectral shape** to vary, instead of scaling `G` by one scalar. Let `Theta_f=arctan sqrt(L)`, `M_s=U tan(s Theta_f)` and

`H_s^shape+B = [ M_s^* Q M_s, M_s^* Q; Q M_s, Q ]`.

This has the *same* initial and final Hamiltonians as in Section 1, but intermediate couplings are `Q M_s`, a mode-dependent shaping generally impossible with only the scalar `eta G` knob. Its parallel bound code is the exact Grassmann geodesic

`V_s=(cos(s Theta_f),-U sin(s Theta_f))^T`.

Define the constant Hermitian shortcut generator

```
K = i [ 0             Theta_f U^* ]
      [ -U Theta_f       0       ];
```

its operator norm is `||K||=||Theta_f||<=pi/2`. If the full nonlocal Hamiltonian `H_s^shape+K/T` can be implemented, the exact solution for any `T>0` on the code is `exp(i BT s)V_s`: **zero loading error**, without an adiabatic limit, for every reference-entangled input. This is the standard counterdiabatic/transitionless-driving mathematical idea (Berry 2009) made explicit for this spectral code and endpoint. It does **not** establish a physical advantage, because `K` requires the entire bath polar isometry `U` and the shaping requires `Q U`; their spatial complexity, sensitivity and individual control amplitudes can diverge despite `||K||<=pi/2`.

Conversely, if the only available control were a Hamiltonian with operator norm at most `h` (after removing a scalar energy origin), any exact unitary code mapping requires `T>=||Theta_f||/h`: the worst-case principal angle of the initial and final subspaces is `||Theta_f||`, and a state cannot traverse a larger Fubini-Study angle than its norm-limited action. The direct K-only rotation saturates that state-space bound. This is a **Hilbert-space speed limit conditional on arbitrary nonlocal bath control**, not a claim about endpoint-local speed limits.

## 3. Important failure: a bare penalty on non-code controller states destroys uniform-gap inference

Suppose the physical bare impurity has more states than the code and a fixed positive matrix `A` selects only `C=ker A`. Then the Hamiltonian is `R_eta^* Q R_eta+diag(A,0)`, not the factorized Section 1 model. Its zero-mode vector on `ker A` exists but **the uniform excitation-gap argument is no longer valid**. An exact explicit two-controller-state example suffices:

`Q=B I_2`, `W=sqrt(lambda) I_2`, `A=a |2><2|` with `B,a>0`. One logical state remains at eigenvalue 0 for `H+B`, but the complementary dressed state has a positive eigenvalue

`gamma(lambda,eta) = [B(1+eta^2 lambda)+a - sqrt((B(1+eta^2 lambda)+a)^2-4aB)]/2`

which behaves as `a/(1+eta^2 lambda)` for fixed `eta>0` and `lambda->infinity`. A variational test with the normalized dressed complementary state gives the rigorous bound

`gamma(lambda,eta) <= a/(1+eta^2 lambda)`.

The bare penalty therefore loses its distinguishability in a strongly dressed continuum. To hold this gap at a fixed nonzero value in this example requires growing `a=Omega(lambda)` or a different dressed/nonlocal penalty. This **does not prove slow loading** (selection rules may suppress transitions), but it decisively invalidates importing the Section 1 *uniform-gap proof* into the previously reported `ker A` controller construction merely because its Berry connection vanishes. Also `P_C f(L)P_C` is not generally `f(P_C L P_C)` when `[P_C,L]!=0`: code normalization must use the restricted Gram `I_C+eta^2 P_C L P_C`, not the full-code matrix functional.

A hypothetical dressed penalty `V_s A V_s^*` on the **full** factorized kernel retains the complement gap `a` and preserves code geometric transport, but adds bath-support and code–bath controls, and at the final endpoint is generically **not** the original bare penalty. Such a comparison cannot be called an implementation of the bare-only shared controller.

## 4. Work accounting and hierarchy interface

The calibrated counterterm has positive work along quasistatic loading: for an initial code vector `xi`, writing `C_eta=(I+eta^2 L)^(-1/2)`,

```
W_det(xi)= 2 int_0^1 eta <xi,C_eta D C_eta xi> d eta >=0,
W_coupling(xi)= -W_det(xi),    W_net=0.
```

This follows from separate Hellmann–Feynman derivatives for `eta^2 D` and `eta G`; it holds without `[D,L]=0`. In the L eigenbasis, the positive-work matrix has entries

`(W_det)_{ij}=2 D_{ij} int_0^1 eta/ sqrt((1+eta^2 lambda_i)(1+eta^2 lambda_j)) d eta`.

The scalar case is `W_det=(D/L) log(1+L)`. Depending on the microscopic cutoff realization, the two canceling gross contributions grow without bound. Therefore a cutoff-uniform coherent fidelity bound is NOT a bound on calibratable control work, maximum source/detuning amplitude, or high-frequency spectral-mode resolution.

For an oscillator impurity capped at occupation `k-1` and *genuinely quadratic* lower sectors, second quantization transfers the one-body operator error to total particle number `N<=k-1` with at most an `N` factor in the isometry norm. This is exact for a bosonic oscillator ladder with the specified quadratic matrix controls. It is **not** a generic reduction for a single shared quantum controller or the native Jacobi endpoint-only interface. The existing first-forbidden `k`-particle spectral certificates and unresolved all-`N` capacity-two question are retained without modification.

## 5. Executed numerical checks and independence

`astra_matrix_loader_audit.py` constructs full Hermitian one-particle finite-band Hamiltonians with random complex noncommuting bath/controller couplings. Its actual `||[L,J]||=7.82024` (noncommuting). At sampled ramp positions:

* Norms `||V^*V-I||` are at the `1e-15` scale.
* Null-vector and reduced-resolvent residuals are at or below `1.2e-13` for the tested matrices.
* Every nonzero spectral gap stays above `B=1.5`.
* Direct `DOP853` complex Schrödinger integrations give code-isometry errors of about `0.5015, 0.1752, 0.06895, 0.03341` at `T=2,6,15,30`, respectively; the conservative `1/T` theorem bounds hold.
* The bare-penalty example shows gaps shrinking roughly as `a/(1+lambda)` across `lambda=10,...,1e5`.

One coding error was found and corrected in this same audit: SciPy initial conditions must be **complex dtype** when integrating the Schrödinger equation. Real dtype silently discarded imaginary derivatives and gave false adiabatic failures. The committed/rerun executable and JSON use complex dtype and preserve the corrected results. The numerical evidence is not a substitute for Parts A–D of the proof.

### Other physical approaches and historical context

Shi et al., *Phys. Rev. X* 6, 021027 (2016), analyzes established bosonic impurity bound-state physics. Yoshida et al., *Phys. Rev. A* 98, 062705 (2018), and Shi et al., *Phys. Rev. Lett.* 121, 243401 (2018), establish substantial multibody physics that must remain comparators rather than be relabeled a new force. Berry, *J. Phys. A* 42, 365303 (2009), establishes transitionless quantum driving. This note offers explicit spectral factorization, a common-amplitude noncommuting-code uniform bound, a geometric shortcut at its actual control cost, and a specific controller penalty gap-collapse diagnostic. External priority is **unknown**.

## 6. Remaining hard physical construction

1. **Native-interface acquisition.** Build a physically declared Jacobi-chain endpoint model realizing `eta G`, `eta^2 D` (or an approximation) with quantified truncation, counterterm, slew, bandwidth and noise. The present proof requires independently controlled matrix counterterms and is not an endpoint-only implementation.
2. **Restricted-code shared controller.** Section 7 rules out *uniform* loading with only a common scalar envelope; Section 8 constructs a repaired two-stage loader with off-code source selectivity and exact cross-counterterms. The outstanding physics is to acquire that stronger source/control interface from a native endpoint-only system, or prove an approximate version with realistic calibration errors.
3. **All-sector capacity two.** The exact `N=3` hard-triple theorem and finite-cutoff Stieltjes transfer do not prove `E_N>=-2B` for `N>=4`. Earlier finite-bath convexity tests remain numerical evidence only. Neither the matrix loader nor the geometric shortcut changes that unresolved many-body spectral fact.


## 7. A stronger result: exact *time* no-go for selective noncommuting-controller loading

Section 3 showed that the full-code gap proof can fail. That observation alone did not rule out fast selective loading, because a closing gap can remain dynamically dark. The following explicit finite-dimensional family gives a much stronger operational obstruction: **no single scalar-amplitude protocol of bounded duration can load the designated one-dimensional code, even though its dressed bound eigenstate exists at every amplitude, has zero geometric self-connection, and is below the bath continuum.** This closes one serious loophole in the old noncommuting-controller loading summary.

### Theorem 2 (an almost-conserved competing dark direction)

Fix positive `B=1`, `Q=2`, `a>0`. Use two bare impurity/controller states `c,d` and one positive-energy bath mode `b` of energy `Q-B=1`. Let the bare controller penalty be `A=a|d><d|` and define, for any `lambda>0`,

```
W=(sqrt(lambda),lambda) : C^2 -> C,
R_eta = (eta sqrt(lambda), eta lambda, 1),
H_eta+I = 2 R_eta^* R_eta + a|d><d|.
```

This is exactly the properly retuned matrix model of Section 1 **plus a proper-subcode bare penalty**, so `G=2W`, `D=2W^*W` and `[A,W^*W]` is nonzero for every `lambda,a>0`. The desired code at `eta=0` is `|c>=(1,0,0)`. For every eta, the state

`v_eta=(1,0,-eta sqrt(lambda))/sqrt(1+eta^2 lambda)`

is an **exact** eigenvector with energy `-1`: `R_eta v_eta=0` and `<d|v_eta>=0`. Its final target is `v_1=(1,0,-sqrt(lambda))/sqrt(1+lambda)`, approximately a pure bath excitation when lambda is large.

Now define a *competing, eta-independent* nearly conserved state

`phi_lambda=(sqrt(lambda),-1,0)/sqrt(1+lambda)`.

It obeys `R_eta phi_lambda=0` for **every real eta** (even if the scalar envelope overshoots), so

`(H_eta+I)phi_lambda= -a|d>/sqrt(1+lambda)`

is independent of eta. This identity, rather than a spectral gap estimate, is the mechanism.

For **any** measurable/piecewise-integrable time-dependent scalar envelope eta(t) with the prescribed quadratic detuning eta(t)^2 D, let U_T be its exact finite-dimensional Schrödinger propagator after removing the scalar `-I` phase. Duhamel's formula applied to the fixed `phi_lambda` gives

`|| U_T phi_lambda-phi_lambda || <= a T/sqrt(1+lambda)`.

Moreover

```
|| |c>-phi_lambda || = sqrt(2-2 sqrt(lambda/(lambda+1))),
|<v_1|phi_lambda>| = sqrt(lambda)/(lambda+1).
```

By a triangle inequality, **uniformly over all such scalar controls**,

```
|<v_1|U_T|c>>|
 <= sqrt(lambda)/(lambda+1)
    + sqrt(2-2 sqrt(lambda/(lambda+1)))
    + a T/sqrt(lambda+1).
```

For fixed `T,a`, the success probability therefore vanishes as `O((1+aT)^2/lambda)`. To obtain success probability at least `p>0`, the runtime necessarily obeys

```
T >= sqrt(lambda+1)/a * [sqrt(p)
       -sqrt(lambda)/(lambda+1)
       -sqrt(2-2 sqrt(lambda/(lambda+1)))]_+.
```

In particular `T >= (sqrt(p)/a) sqrt(lambda)-O(1)` at fixed p. The proof holds for arbitrary smooth/nonmonotone/discontinuous scalar schedules; it is **not** a limitation of a chosen adiabatic ramp. All Hamiltonians have an exact code eigenstate; there is no dissipative conditioning or dropped failure branch. The obstruction is the second nearly invariant bare direction created by an extremely strongly coupled *off-code* state. The data include a fully positive-energy bath oscillator, not a fictitious zero-frequency mode.

### Executed high-precision audit

`astra_restricted_controller_no_go.py` checks the exact vector identities with `mpmath` at 65-digit precision over eta=0, .02, .4, 1 and `lambda=10,...,1e6`. Maximum matrix residuals are below `3e-58`. For `a=1`, `T=10`, `lambda=1e6`, the rigorous **upper bound** on loading success probability is `0.000143999847...`; to reach success probability 0.9 requires `T>=946.68377...` in binding-energy time units. These are **rigorous-bounding numerical evaluations**, not simulated failure rates. The commutator is nonzero: `||[A,L]||_F^2=2a^2 lambda^3`.

### Physical interpretation and repair contract

The calibrated common-amplitude drive leaves `phi_lambda` nearly invariant; strengthening or reshaping the **scalar time envelope alone** cannot defeat the trap. The full-code theorem is not contradicted because removing the penalty `A` changes the logical input-output contract and all bare states are then code states. A bypass may use independently shaped `G_c(t),G_d(t)`, a direct bath-mode coupling or a controller mixing drive, but such an additional physical knob must be counted. The geodesic shortcut in Section 2 provides a conditional exact route if nonlocal `U` and `Q U` controls are available; it is not realizable from the same single scalar envelope. The obstruction persists with `B` fixed and a positive bath gap: it does not depend on infrared continuum singularities or a cutoff limit.

## 8. Constructive repair: load the protected code before completing the off-code source

Theorem 2 identifies a genuine control obstruction, but also its cause. This section gives an exact constructive workaround which does **not** assume a uniform gap for the completed shared controller.

### Theorem 3 (selective-source completion; exact restoration with no extra code error)

Decompose the finite bare impurity space as `C ⊕ D`, with protected logical code `C=ker A`, `A|_D>=a I_D` for `a>0`, and set `dim(C)=c` fixed. Let the bath satisfy `Q>=B I` and write the **final** source as `W=(W_C,W_D)`. The final physical Hamiltonian is

`H_final+B = R_full^* Q R_full + diag(A,0_bath)`, `R_full=(W_C,W_D,I_bath)`.

Control assumption: in addition to turning up the logical source `W_C`, the operation can **independently gate the off-code source** `W_D` and can apply the *complete*, dynamically compensated matrix counterterm `D(t)=W(t)^* Q W(t)` including its cross-blocks. This need not be available for an endpoint-only chain or an unspecified controller.

**Stage I.** Set `W_D(t)=0` and ramp `W_C(t)=eta(t) W_C` with the single-envelope arc-length schedule of Theorem 1 on `C`. The complementary bare sector is then decoupled. For loading duration `T_1`, the full isometry error on the initially bare code satisfies

`epsilon_1 <= [2(c+1) ell_C+5 ell_C^2]/(B T_1)`, `ell_C<=c pi/2`.

The ideal final encoded code is the fixed isometry

```
V_C = ( C_C,
        0_D,
       -W_C C_C )^T,
C_C=(I_C+W_C^* W_C)^(-1/2).
```

**Stage II.** Freeze `W_C` and ramp `W_D(t)=tau(t)W_D` from zero to its full value, while retuning **all** of `D(t)=W(t)^*QW(t)` and off-diagonal source `G(t)=QW(t)`. Let

`R_tau=(W_C,tau W_D,I_bath)`.

For every `tau`, `R_tau V_C=0`, `A V_C=0`, and even `R'_tau V_C=0`. Therefore

`H_tau V_C=-B V_C` and `(partial_tau H_tau)V_C=0` **exactly**.

No matter how fast or nonmonotonically `tau(t)` changes, the ideal already-loaded code acquires only the known phase `exp(i B T_2)`. After both stages, using unitarity on all imperfect/leakage branches,

`|| U_(2) U_(1) V_0 - exp(i B(T_1+T_2)) V_C || <= epsilon_1`.

This is a complete operator-norm statement and is unchanged by arbitrary untouched reference systems. **Its constant is independent of the strength of `W_D`, the ultraviolet bandwidth and the size of the complementary spectral gap**, though it depends on code dimension `c`, `B`, and physically realizable counterterms. In particular the previous no-go family `W_C=sqrt(lambda)`, `W_D=lambda` becomes uniformly loadable in *state error* with this one additional independently gated source channel plus full matrix compensation. The no-go did not disprove coherent loading in principle; it disproved doing it with *only one shared envelope* and a fixed bare penalty.

### Executed check and physical control precision

`astra_selective_source_completion.py` tests twenty complex noncommuting finite-bath controllers (`c=2`, `dim(D)=2`, five positive bath modes, strongly mixed matrices). In completed examples the commutator `||[A,W^*W]||` is as large as `7013.2`, and the complementary excitation gap falls to `0.0007297` despite the bare bath gap `B=1.25`. Nevertheless `||H_tau V_C+B V_C||` is at most `8.1e-14`, `||partial_tau H_tau V_C||` at most `5.7e-14`, and the isometry error below `1.7e-15` over all checked source settings. The exact identities above, not the numerical sample, prove the theorem.

**Important cost:** Stage II's full matrix counterterm is indispensable. In the explicit no-go family, its cross component is `D_dc(tau)=Q tau lambda^(3/2)`. Omitting or miscalibrating that component by relative fraction `epsilon` leaves a code-state residual

`||delta H V_C|| >= |epsilon| Q |tau| lambda^(3/2)/sqrt(1+lambda) ~ |epsilon| Q |tau| lambda`

if this is the only error. Hence keeping a fixed absolute **instantaneous** eigenvector residual can require relative calibration accuracy of order `1/lambda` at large lambda. A simple inclusive Duhamel guarantee accumulates `T_2 sup ||delta H||`; no small actual gate error is inferred just from exact ideal dynamics. Source slew, matrix counterterm amplitude, off-code switching, finite energy resolution, and noise all remain real costs. For arbitrary controller matrices, a physical source-selective channel implementing this model has not yet been supplied.

**Core explanatory consequence:** The existence of a dressed logical eigenstate, a spectral gap and coherent *reachability* are three distinct properties. A nearly conserved competing dark direction can obstruct reachability under a restricted control algebra even when the target is a perfectly valid bound eigenstate. Conversely, independently completing an off-code coupling while holding the code exactly in the kernel supplies a rigorously nonadiabatic, error-preserving loading mechanism. The mechanism should be understood as a controllability and source-geometry statement, not a newly identified fundamental force.
