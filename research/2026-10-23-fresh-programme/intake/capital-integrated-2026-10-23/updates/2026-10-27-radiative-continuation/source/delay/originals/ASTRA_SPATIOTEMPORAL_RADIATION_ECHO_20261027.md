# ASTRA foundational physics: a finite-time spatiotemporal radiation echo without a common dark state

27 October 2026. New derivation and executed checks. This is a theorem for a specific, time-dependent, number-conserving, rotating-wave continuum Hamiltonian, **not** a Maxwell-complete hardware demonstration or a claim of historical novelty. Energy unit `B=1` throughout.

## 1. Decision and comparison

The previous radiative-rank theorem establishes that, for a stationary coupling `W(omega)=v(omega)R` with `v` nonzero on an open energy interval, exact final continuum vacuum from an initially empty continuum forces `Rq(t)=0` throughout any finite-duration operation. Full-column-rank `R` therefore rules out a perfect finite-time two-edge transfer without a bypass. Its successful alternatives were a complex direct counterdiabatic edge or an exactly common radiative dark direction for two intermediate emitters; the latter is spoiled by independent or spatially distinguishable radiation.

Rather than introduce another ideal permanent dark mode, I attacked the structural assumption `W(omega)=v(omega)R`: separated emitters in a dispersive-propagation waveguide have **frequency-dependent phase columns**. The resulting null condition lives in an algebra of temporal translation operators, not one fixed vector space. This is the stronger explanatory mechanism investigated here.

Giant-atom decoherence-free interactions, time-delayed waveguide QED and quantum state-transfer inverse engineering are established antecedents. In particular see Kockum, Johansson and Nori (2018), arXiv:1711.08863; Carollo, Cilluffo and Ciccarello (2020), PR Research 2 043184, arXiv:2006.13940; and Liu, Cai and Tan, PRA 113 033727 (2026). No literature-priority assertion is made for the particular algebraic construction below.

## 2. General exact terminal-radiation equation

Take the one-excitation Hilbert space `C^s \oplus C^n \oplus L^2((0,Omega),domega;C^2)`, with `s` storage modes and `n` emitter modes. The two photon directions are `sigma=+1,-1`, free bath energy is multiplication by `omega >=0`, and each emitter is at propagation-time coordinate `x_j`. Define the time-independent bounded coupling

    (W q)_sigma(omega) = v(omega) sum_{j=1}^n exp(i sigma omega x_j) q_j,

with `v` nonzero a.e. on some open spectral interval and `integral |v|^2/omega < infinity`. The number-conserving Hamiltonian is

    H(t) = [ H_int(t)   W^* ]
           [ W          omega ].

The bath is initially vacuum. The *exact* radiative amplitude is

    xi_sigma(omega,T) = -i v(omega) exp(-i omega T)
                     sum_j exp(i sigma omega x_j) F_j(omega),

    F_j(z) = integral_0^T exp(i z t) q_j(t) dt.

Every `F_j` is entire in complex `z` for integrable finite-duration `q_j`. Final radiation is *exactly vacuum*, not merely absent in one output direction, iff both sums vanish on an open interval, hence identically as analytic functions of `z`.

### Two distinct emitters cannot make a nontrivial terminal echo

For `x_1 != x_2`, the two-row/two-column determinant is

    det W_phase(z) = 2i sin[z(x_1-x_2)]

up to a nonzero sign. It is nonzero on a dense subset of any real open interval. Consequently `F_1=F_2=0`, and Fourier uniqueness gives `q_1=q_2=0` almost everywhere. If storage modes communicate *only* via these emitters and have no direct storage-storage hopping, they cannot transfer a one-photon excitation exactly while restoring the continuum to vacuum in finite time.

This is an obstruction for **two distinct point-like coupling positions and both propagation directions**. It does not exclude multiport giant atoms, a chiral one-direction source, direct bypass edges, time-varying radiation coupling, or finite discrete baths.

### Three equally spaced emitters admit time-dependent cancellation

Set `x=(-tau,0,+tau)` with `tau>0`. Subtracting the two radiation equations implies `F_1(z)=F_3(z)`. The remaining equation gives

    F_2(z) = -2 cos(z tau) F_1(z).

In the time domain (zero extension outside `[0,T]`), this is *exactly*

    q_1(t)=q_3(t)=f(t),
    q_2(t)=-f(t-tau)-f(t+tau).                       (A)

No nonzero constant emitter vector is dark for all `omega`: if a frequency-independent vector satisfies both radiation equations, it must have `q_1=q_3` and `q_2=-2cos(omega tau) q_1` on an open interval, forcing all three entries to zero. Equation (A) is therefore a **spatiotemporal radiative kernel**, not a conventional common dark subspace.

There is a sharp duration obstruction. The required `q_2` vanishes outside `[0,T]`. Looking at times `(-tau,0)` forces `f=0` on `(0,tau)`; looking at `(T,T+tau)` forces `f=0` on `(T-tau,T)`. Thus `supp f subset [tau,T-tau]`, and a nonzero square-integrable history requires **T>2 tau**. Conversely, any such `f` inserted in (A) cancels both radiation directions at `T`.

For three non-equally spaced positions one can use the frequency-dependent cross product of the two radiation rows, yielding component Fourier factors proportional to `sin[z(x_3-x_2)]`, `-sin[z(x_3-x_1)]`, `sin[z(x_2-x_1)]`. Their inverse transforms are finite differences of delayed pulses. Equal spacing permits the shorter cosine factorization (A).

## 3. A fully positive, *on-band*, real-symmetric, no-bypass Hamiltonian

The source identity alone does not establish a physical quantum trajectory. Here is an exact closed-Hamiltonian realization that fills that gap **at the stated unrestricted internal-control interface**.

Use

    Omega=12, T=12, tau=1/2, mu=2pi, eta=.01, alpha=.16,
    v(omega)=eta sqrt(omega) (1-omega/12)^2, 0<omega<12.

Crucially, the internal carrier `mu=2pi` lies **inside** the radiation continuum, rather than above its UV cutoff. The radiation continuum is gapless and retains both directions.

Define the nonnegative bump on `[tau,T-tau]`, extended by zero elsewhere,

    s=(t-tau)/(T-2tau),      f(t)=[4s(1-s)]^3,
    I=int_0^T f(t)^2 dt=(T-2tau) 4^6 Beta(7,7)
      =3.750915750915751... .

Set the three real emitter envelopes

    h(t)=alpha [f(t), f(t-tau)+f(t+tau), f(t)]^T,
    q(t)=i exp(-i mu t) h(t).

Since `mu tau=pi`, the emitter sources obey (A) *exactly*, so their completed radiation amplitudes vanish at `t=T` for every energy in the entire continuous band.

For each `t`, form the exact radiation wavefunction by the Duhamel convolution

    xi(t)=-i int_0^t exp[-i omega(t-s)] W q(s) ds.

Let

    rho(t) = sqrt(1-||h(t)||^2-||xi(t)||^2),
    theta(t)=(pi/2) I_s(7,7),
    r(t)=rho(t) [cos(theta(t)), sin(theta(t))]^T,

where `I_s` is the regularized incomplete Beta function, clipped to `0,1` outside the bump support. It obeys `theta'=(pi/2) f(t)^2/I`. Our analytic estimates below give `rho(t)>0.9189` for all `t`. The complete normalized target state is

    Psi(t) = [ exp(-i mu t) r(t),  q(t),  xi(t) ]^T.

At the endpoints it is the storage transfer

    Psi(0)=|a,vac>,       Psi(T)=exp(-i mu T)|b,vac>.

The radiation sector is **nonzero at intermediate times**. This is an exact final-time reabsorption/echo, not an instantaneous dark-state process.

### Exact real, two-local internal controls, with no storage bypass

Define the known time-dependent vector `g(t)=exp(i mu t) W^* xi(t)` and real vectors

    y(t)=-h'(t)-Re g(t),      z(t)=-Im g(t).

Radiation norm conservation gives the compatibility identity

    r^T r' = h^T y.                                     (B)

For `||h||>0`, put

    C = r' h^T/||h||^2 + r y^T/||r||^2
        - (r^T r') r h^T/(||r||^2 ||h||^2),

    Q = (z h^T+h z^T)/||h||^2
        - (h^T z) h h^T/||h||^4.

These **real** matrices satisfy

    C h=r',     C^T r=y,       Q h=z.

Set

    H_int(t) = mu I_5 + [ 0_(2x2)  C(t) ]
                          [ C(t)^T    Q(t) ].

The zero upper-left off-diagonal block means **no direct storage-storage hopping**. Every allowed off-diagonal term is an ordinary, real two-mode hopping, although the storage-emitter and emitter-emitter connection graph is fairly dense and time dependent. The source envelopes vanish cubically at endpoints; the matrices extend continuously by zero there. Direct substitution in `i dPsi/dt=H(t)Psi` verifies the complete trajectory, including all continuum amplitudes. The functions `C,Q` are predetermined open-loop controls, computed from the known bath; they are not postselected measurements.

### Uniform spectral positivity, with no time-grid assumption

The zero-energy square completion of the radiation continuum requires

    H_int(t) - W^* omega^(-1) W >= 0.

Here the `W^*omega^(-1)W` term occupies only the three-emitter block. The following bounds hold **uniformly in continuous time**:

    ||W|| <= 0.053666,
    ||h|| <= 0.391919,              ||h'|| <= 0.427548,
    ||xi|| <= 0.043566,            rho >= 0.918967,
    ||xi(t)||/||h(t)|| <= 0.321994,
    ||r'(t)||/||h(t)|| <= 2.318541,
    ||C(t)|| <= 5.104873,          ||Q(t)|| <= 0.051841,
    ||W^* omega^(-1)W|| <= 0.001440.

Sketch of the derivation, to make the certification independently auditable:

1. `||W|| <= sqrt(6)||v||_2`, and `||W^*omega^-1 W|| <=6 int |v|^2/omega = 6 eta^2 Omega/5`.
2. For the compact bump, `||h||<=sqrt(6)alpha` and `||h'|| <= (12/(T-2tau))sqrt(6)alpha`.
3. Plancherel on each truncated source trajectory gives `||xi|| <= sqrt(4pi) ||v||_infinity (4alpha sqrt I)`. No finite radiation discretization is used.
4. The three nonnegative components of `h` are monotone increasing until `T/2` and decreasing thereafter. For the shifted pair this follows from monotonicity of `s(1-4s^2/L^2)^2` on `0<=s<=2tau`, since `2tau<L/(2sqrt5)`, `L=T-2tau=11`. Because `xi(0)=xi(T)=0`, integrating forward or backward gives `||xi(t)||<=||W||(T/2)||h(t)||`.
5. Conservation gives `|rho'|/||h|| <= (||h'||+||W||||xi||)/rho_min`; also `theta'/||h|| <= pi/(2I sqrt(2)alpha)` because the two outer emitter amplitudes each equal `alpha f`. Insert these in the formulas for `C,Q`.

Therefore, as quadratic forms on the emitter+storage sector,

    H_int-W^*omega^-1 W >=
    (2pi-5.104873-0.051841-0.001440) I > 1.1250 I.       (C)

For an arithmetic-only conservative checkpoint, the weaker rounded bounds `mu>6.28, ||C||<5.12, ||Q||<0.053, Schur<0.002` already give a positive margin **above 1.105**. This is an **internal Schur positivity margin**; the complete continuum Hamiltonian has spectral infimum zero because arbitrarily soft photons remain.

The proof also holds on every fixed bosonic number sector for the **quadratic** second-quantized Hamiltonian in the sense of nonnegative energy. It does not claim finite dressed excitation capacity, a conditional Boolean gate, or an actual engineered electromagnetic interface.

## 4. Independent executed checks

The script `astra_temporal_dark_inband_certified_20261027.py` independently solves the radiation convolution using ODE integration and propagates the *actual full* time-dependent Schrödinger state under the reconstructed real-symmetric Hamiltonian, at 40 positive-frequency quadrature nodes per propagation direction. It is independent of the analytic cancellation and positivity proofs.

Observed results (these are **numerical diagnostics**, not the theorem certificates):

| Diagnostic | Value |
|---|---:|
| Smallest sampled Schur eigenvalue | `5.2803955334` |
| Largest storage-emitter hopping norm | `1.0022894768` |
| Largest transient continuum amplitude norm | `0.0028440636` |
| Final continuum norm | `8.96e-14` |
| Entire-state transfer error | `2.85e-11` |
| Maximum equation residual | `2.01e-15` |
| Maximum imaginary part of internal Hamiltonian | `0` |
| Direct storage-storage hopping | `0` |

The separate `astra_temporal_dark_inband_uniform_certificate_20261027.py` evaluates the rigorous continuous-time inequalities and writes them as structured JSON. The first, high-carrier, no-bypass construction and its own uniform margin (`>40`) are also preserved in `astra_temporal_dark_no_bypass_20261027.py`, but the **on-band** realization above is the stronger physics result.

## 5. New robustness bound and observed failure modes

If the emitter coordinates change by `delta x=(delta x_1,delta x_2,delta x_3)` but the designed internal controls remain fixed, then

    ||delta W|| <= sqrt( 2 int_0^Omega omega^2 |v(omega)|^2 domega ) ||delta x||_2.

For `v=eta sqrt(omega)(1-omega/Omega)^2`, the integral is `eta^2 Omega^4/280`. Duhamel for the complete unitary evolution therefore gives the *entire state-vector* change

    ||U_delta(T)-U_0(T)|| <= T eta Omega^2/sqrt(140) ||delta x||_2
                            = 1.460427 ||delta x||_2.          (D)

This is a conservative rigorous bound, not a manufacturing tolerance.

Independent full-state propagation (`astra_temporal_dark_inband_perturbation_20261027.py`) with 40 modes per direction, retaining all radiation, found:

| Perturbation (fixed design controls) | Final full-state error |
|---|---:|
| Symmetric outer-emitter shifts by `+-0.01` | `0.00013883` |
| Centre-emitter shift by `0.01` | `0.00076969` |
| 1% increase in all radiation-coupling amplitudes | `3.32e-6` |
| Centre-emitter onsite offset `0.001` | `0.00102214` |
| Centre-emitter onsite offset `0.01` | `0.01022059` |

The last perturbation breaches a one-percent **state-vector** target, despite the Hamiltonian remaining positive: coherent onsite calibration, rather than geometric radiation leakage, is the stronger limitation in this particular parameter regime. The tested errors are inclusive, with no survival conditioning. They are not universal performance or fabrication predictions.

## 6. What changed, what failed, and the governing boundary

**Proved for the declared interfaces:**

- An analytic no-go for any nonzero finite-duration source with two distinct point emitters in two propagation directions.
- A necessary-and-sufficient time-shift relation for exactly zero terminal continuum radiation with three equally spaced emitters, including the sharp source-duration threshold `T>2tau`.
- An explicit positive, gapless continuous Hamiltonian that realizes the temporal echo in finite time, with *real* internal two-local hopping, no direct storage-storage edge, and a certified positive Schur margin while the emitter's carrier is **inside** the radiation band.
- A full-state, non-postselected Duhamel bound on emitter-position errors.

**Not acquired:** a sparse nearest-neighbour graph or a particular Maxwell-compatible laboratory implementation of `v(omega)` and the prescribed coupling trajectories; preparation of the initial storage state and timed controls; control work/slew calibration, independent radiation outside the declared two channels; extension to interacting multi-photon storage and an actual conditional photon gate; external priority. A positive instantaneous Hamiltonian does not make its time-dependent controls free of work.

**Why the alternative matters:** the previous complex bypass is simpler and remains *exactly dark at all intermediate times*; it is the stronger choice when direct controllable complex hopping is available. The present mechanism instead uses finite propagation delays and ordinary real internal couplings. It supports an exact terminal radiation echo despite the absence of a common frequency-independent dark state, at the cost of additional emitters, time-dependent dense couplings and a delay-calibration interface.

The next high-value attack is to replace the precomputed dense internal controls by a **fixed finite-range coupling graph with a small independent control alphabet**, or to prove a resource lower bound excluding that reduction. This is the missing interface between the algebraic cancellation theorem and a genuinely implementable new capability.

## 7. Files and reproduction

Run with NumPy/SciPy using the following ordinary standalone scripts (each writes JSON):

- `astra_temporal_dark_inband_certified_20261027.py`: in-band real-symmetric, no-bypass full Hamiltonian and independent Schrödinger propagation.
- `astra_temporal_dark_inband_uniform_certificate_20261027.py`: continuous-time, continuous-frequency positivity proof estimates.
- `astra_temporal_dark_inband_perturbation_20261027.py`: complete photon-output perturbation experiments.
- `astra_temporal_dark_control_20261027.py`: first complex-control constructive test.
- `astra_temporal_dark_no_bypass_20261027.py`: independent no-direct-storage-edge complex-control construction with a uniform certificate.
- `astra_temporal_dark_real_controls_20261027.py`: earlier out-of-band real-control benchmark.

This work is preserved as separate proof, scripts, and exact executed result files. No GitHub mutation or research-priority assertion has been made.
