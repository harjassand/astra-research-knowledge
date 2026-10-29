# Independent review: compact native repair and a shared equilibrium preparation

29 October 2026. Reviewer: producer-workspace/different_consequential_opening.

Reviewed:
physical_frontier/NATIVE_EQUILIBRIUM_TOPOLOGY_OBSTRUCTION.md, Section 7,
plus root's proposed finite-horizon preparation extension communicated in
the present turn. The proof review is ordinary analysis, not a numerical test.

## Findings

The positive compact-force repair is valid. The cubic-bridge argument
supplies exactly the TV continuity of kinetic transition kernels needed to
upgrade weak stationary convergence to full stationary path TV convergence.
It does not require a global mixing coefficient.

The shared equilibrium preparation extension is also valid for the explicit
sinusoidal shear. Conditional correlations do not spoil its bounds. The
temperature-normalized work and the physical total entropy-production
identity must retain their different roles:

    0 <= Sigma_[0,h] = W_[0,h]/theta - D(rho_h||mu_0)
                    <= h sigma_n.

Here sigma_n is the stationary entropy rate of that same shear, used only
as an upper bound; the finite-horizon source itself is not stationary.
No reversed final preparation or native experiment has been acquired.

## 1. Force compactness, invariant states and the Gibbs limit

Let ||F_j||_infinity<=K, Lip(F_j)<=L on a fixed torus, with fixed positive
gamma and theta. Arzela--Ascoli gives a subsequence uniformly converging to
a bounded Lipschitz F with the same constants.

For a two-sided stationary solution the variation-of-constants identity is

    p_0 = integral_{-infinity}^0 e^(gamma s) F_j(q_s)ds
             +sqrt(2gamma theta) integral_{-infinity}^0 e^(gamma s)dW_s.

The first term is bounded by K/gamma. The second has the centered Maxwell
Gaussian law. Independence of these terms is NOT required: their pathwise
sum bound gives uniform moments and tightness. This justifies Step A.

Synchronous SDE coupling under the common Lipschitz constant gives convergence
of finite-time solutions for fixed initial data. Tightness handles the initial
state tails. The limit of stationary measures is stationary for F. Polynomial
moment bounds justify using phi(q)p_i after standard momentum cutoff.

The native conditional momentum LSI and entropy/current relation give

    D(rho_j||(rho_j)_q M_theta)<=sigma_j/(2gamma).

Pinsker therefore forces any weak stationary limit to be nu(q)M_theta(p).
The stationary test phi(q)p_i gives

    theta integral partial_i phi dnu + integral F_i phi dnu=0,

hence distributionally grad nu=(F/theta)nu.

The mollifier argument in the source is sound. For a positive torus
approximate identity, nu_epsilon>0 and

    |grad nu_epsilon|<=(K/theta)nu_epsilon.

Connectedness and compactness, together with normalization, bound both
nu_epsilon and its reciprocal uniformly. The log densities are uniformly
Lipschitz. Their subsequential uniform limit represents the original measure
nu. Since F is continuous, grad nu=(F/theta)nu has continuous right side;
nu is positive C1 and F=theta grad log nu. The limiting force is therefore a
periodic conservative force in the same bounded Lipschitz class.

A nonzero constant circulation on the torus cannot survive this argument:
the globally positive periodic nu makes log nu single-valued.

### Regularity qualification

The proof uses the native entropy/current identity and Gaussian LSI under
their usual stationary finite-entropy/Fisher or weak renormalized kinetic
formulation. It should retain that analytic domain explicitly from
LOCAL_PARITY_THERMALIZATION.md; force compactness alone is not a substitute
for writing down the entropy identity's domain.

This is not a new hidden-mixing assumption. For the usual bounded smooth
kinetic sources these are the standard hypotheses already used by the branch.
The compact limit need not itself be smooth for the weak stationary test.
If the original interface insists on smooth conservative competitors, mollify
the limiting periodic potential; its gradient keeps the K and L bounds and
converges uniformly, so the same Gibbs/path approximation conclusion follows.

## 2. Rigorous kinetic smoothing lemma

Fix t>0. For initial states z=(q,p) and z'=(q',p'), choose compatible nearby
torus lifts and a deterministic cubic eta_q on [0,t] satisfying

    eta_q(0)=q-q',  eta'_q(0)=p-p',
    eta_q(t)=eta'_q(t)=0.

Put eta_p=eta'_q. Let Y be the source from z' and define X=Y+eta,
with torus reduction in position. Then X starts from z, ends at Y_t,
and solves the desired kinetic equation plus momentum drift

    u_s=F(X_q-eta_q)-F(X_q)+gamma eta_p+eta'_p.

The bound

    |u_s|<=L|eta_q|+gamma|eta_p|+|eta'_p|

is deterministic. Cubic scaling gives

    integral_0^t |u_s|^2 ds <= C_t(L,gamma) |z-z'|^2.

Bounded u ensures Novikov. Girsanov relative to the unmodified source from z,
followed by endpoint data processing and Pinsker, yields

    TV(K_t^F(z,.),K_t^F(z',.))
       <= sqrt[C_t/(8gamma theta)] |z-z'|.

The sign and gamma term in the proposed bridge are correct. Periodicity of F
handles torus lifts; Lipschitz continuity applies to their Euclidean difference
because torus geodesic distance is no larger. No elliptic position noise
was inserted.

This establishes TV continuity of the kernel, which is stronger than merely
knowing the semigroup maps bounded measurable functions to continuous ones.
The distinction is essential for the next step.

## 3. Weak measures become TV-close after a fixed smoothing interval

For mu_j weakly converging to mu, with tightness, restrict to a common compact
set up to an arbitrarily small tail probability. Cover it by finitely many
sets on which the kernel varies by at most epsilon in TV, choosing partition
boundaries of mu-measure zero. Replace each kernel on a cell by one fixed
kernel value.

The resulting finite mixture weights converge by weak convergence. Kernel
replacement errors are bounded by epsilon, and the complement by tightness.
Therefore

    TV(mu_j K_t^F,mu K_t^F)->0.

This is exactly the needed inference; mere pointwise convergence of densities
or weak transition convergence would not have been enough.

Uniform force perturbations delta_j=||F_j-F||_infinity have conditional
path KL at most delta_j^2 t/(4gamma theta), independently of initial state.
Thus their transition TV differs by at most delta_j sqrt[t/(8gamma theta)].

Using stationarity on both sides proves TV(rho_j,rho)->0. Applying the
same Girsanov estimate to full conditional paths then gives

    TV(P_Fj^h,P_F^h)
       <=TV(rho_j,rho)+delta_j sqrt[h/(8gamma theta)] ->0.

The contradiction argument for an existential class-dependent modulus omega
is valid. It establishes no computable rate, sample cost, stationary preparation
time or method for acquiring the force Lipschitz bound.

## 4. Shared equilibrium initial preparation: construction

Use the sinusoidal shear F_n(q)=(0,A sin(nq_1)) and start EVERY source from

    mu_0=uniform_position times M_theta(p_1)M_theta(p_2).

The first coordinate remains free stationary kinetic OU. Let Z_2 be a stationary
OU independent of its entire trajectory, with p_2(0)=Z_2(0). Set

    Y_n^0(t)=A integral_0^t e^[-gamma(t-s)] sin(nq_1(s))ds,
    p_2(t)=Z_2(t)+Y_n^0(t).

Choose an independent uniform initial q_2 and integrate p_2. Then positions
remain uniform at each time, and q_2(t) remains independent of the other
current variables after conditioning on its path-dependent shift.

The stationary forcing correlation is

    C_n(u)=(1/2)exp{-[n^2 theta/gamma^2]
                              [gamma u-1+e^(-gamma u)]},

which is nonnegative for every u>=0.

## 5. Transient work and density bounds

Mechanical work under the declared force is

    W_[0,h]=E integral_0^h F_n(q_t) dot p_t dt.

Its instantaneous mean power is exactly

    w_n(t)=A^2 integral_0^t e^(-gamma u) C_n(u)du
          <=A^2 integral_0^infinity e^(-gamma u) C_n(u)du
          =theta sigma_n.

Hence W_[0,h]/theta<=h sigma_n. Nonnegativity of this particular covariance
is load bearing for this monotone truncation argument; the assertion is not
silently generalized to arbitrary stationary forcing covariances.

Let v_n(t)=E[Y_n^0(t)^2]. Then

    v'_n(t)=2w_n(t)-2gamma v_n(t),  v_n(0)=0,

so even the refined bound holds:

    v_n(t)<= (theta sigma_n/gamma)(1-e^(-2gamma t)).

Given the first-coordinate history, p_2(t) is a Gaussian of variance theta
and mean Y_n^0(t). It is a mixture of those Gaussians after conditioning only
on current q_1,p_1. The Gaussian noise Z_2 remains independent of that history.
Convexity of KL and the exact free q_1,p_1 marginal therefore give

    D(rho_t||mu_0)<=v_n(t)/(2theta)
            <=[sigma_n/(2gamma)](1-e^(-2gamma t)).

This checks the asserted density bound despite the force/history correlations.
One must condition before taking the mixture; it would be wrong to assert
that Y_n^0 is independent of current q_1,p_1.

## 6. Physical total entropy production

The reference energy is kinetic energy; the applied shear is an external
nonconservative mechanical force. With the stated single-temperature Maxwell
bath, the mean first law is

    Delta E = W - Q_bath.

System Shannon entropy satisfies

    D(rho_h||mu_0)-D(rho_0||mu_0)
         =Delta E/theta-Delta S_system.

Since rho_0=mu_0,

    Sigma_[0,h]:=Delta S_system+Q_bath/theta
               =W/theta-D(rho_h||mu_0).

Equivalently, the nonstationary entropy balance gives

    Sigma_[0,h]
      =gamma theta integral_0^h integral rho_t
         |grad_p log(rho_t/M_theta)|^2 dq dp dt >=0.

Therefore

    0<=Sigma_[0,h]<=W/theta<=h sigma_n.

This is physical total entropy production under the declared mechanical/bath
model. It is not an arbitrary same-stationary-law reversal KL, and no
reversed final preparation has been performed. Interpreting an actual
actuator's cost would additionally require its implementation: switching on
a spatially intricate nonconservative force is not proved cost-free by this
system-plus-bath balance.

## 7. Consequences retained under shared preparation

The source's position marginal is uniform throughout. Thus the full-path
Girsanov KL to the free equilibrium, with the SAME initial mu_0, is exactly

    D(P_n^{mu_0}[0,h]||P_0^{mu_0}[0,h])
          =h A^2/(8gamma theta).

Against another native equilibrium initialized in its Gibbs law, initial
KL contributes D(mu_0||nu_V), and orthogonality of F_n to gradients gives
the same exact native optimum through free equilibrium.

The root's score integral F_n dot(dp+gamma pdt) keeps source mean A^2h/2
and stationary native-equilibrium mean zero. Its uniform second-moment
argument remains valid (and source moment bounds improve).

Thus vanishing TOTAL physical entropy over a fixed horizon, shared canonical
initial preparation, and fixed bath do not repair native full-path equilibrium
closeness without force regularity or an appropriate observation topology.
The obstruction is not a hidden stationary preparation cost.

The fixed preparation is a mathematical native equilibrium operation with
no n-dependent distribution. This does not constitute an acquired laboratory
preparation, nor remove the increasing spatial resolution of the force.

