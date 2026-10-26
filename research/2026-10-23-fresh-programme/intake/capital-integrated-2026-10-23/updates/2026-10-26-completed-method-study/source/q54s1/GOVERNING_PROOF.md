# Hidden passive transitions: governing theorem and matched incumbent

All variables below are dimensionless after fixing common force and displacement units. This is a mathematical construction in a stated constitutive-law class, not a fabricated specimen or a claim that arbitrary laws in the class have been manufactured.

## 1. Model, operations and task

Fix `0 < a < b`, `0 < m < L`, and `sigma > 0`. The safe interrogation region is `[0,a]`; the task is force prediction at `b`. Let `F(m,L)` consist of real-analytic functions `f:R→R` with `f(0)=0` and

`m <= f'(x) <= L` for every real `x`.

One observation costs one calibrated scalar force measurement:

`Y_t = f(X_t) + Z_t`, with `Z_t` independent `N(0,sigma^2)`.

`X_t` may depend on the complete retained history, arbitrary computation and independent randomization, but must lie in `[0,a]`. There are exactly `n` readings. This does not describe arbitrary coherent sensors, noiseless derivative oracles, uncounted copies, temporal averaging at zero cost, or an uncharged experiment at `b`.

The physical regularity is substantive. `U(x)=integral_0^x f(s) ds` obeys `U(x)>=m*x^2/2`, and `m<=U''<=L`; it is a nonnegative strongly convex storage energy with force `f`. The port `(velocity,force)` is conservative passive since `dU/dt=f(x)*dx/dt`. Adding unit viscosity gives `xdot=u-f(x)`, whose two solutions driven by the same input contract at rate at least `m`: differentiating the squared state difference and using monotonicity proves this. The obstruction therefore does not rely on negative stiffness, instability, hysteresis, discontinuity, chaos or an unbounded first derivative.

## 2. Explicit two-law construction

Write `A=L-m`, choose `a<c<b`, and let `delta>0`. Define

`sp(z)=log(1+exp(z))`,

`h_delta(x)=A*delta*[sp((x-c)/delta)-sp(-c/delta)]`,

`f_0(x)=m*x`, `f_1(x)=m*x+h_delta(x)`.

Both laws are real analytic on the entire real axis; `sp` has no singularity on that axis. Both vanish at zero. With `s(z)=1/(1+exp(-z))`,

`f_1'(x)=m+A*s((x-c)/delta)`.

Thus both laws belong to `F(m,L)`, uniformly in `c,delta`. Their common **real** analyticity does not assert a uniform complex strip of analyticity; the nearest complex softplus singularities approach the real axis on scale `pi*delta`.

On `[0,a]`, `h_delta` is increasing, nonnegative, and its exact largest safe signature is

`epsilon_delta = h_delta(a) > 0`.

Using `log(1+t)<=t`,

`epsilon_delta <= A*delta*exp(-(c-a)/delta)`.

The target separation is the exact quantity

`D_delta=h_delta(b)`

and satisfies

`D_delta >= A*(b-c)-A*delta*exp(-c/delta)`.

Hence for fixed `c`, target separation tends to `A*(b-c)>0` while every safe force measurement loses its signature exponentially.

## 3. Exact adaptive-optimal ordinary comparator

**Theorem 1 (Blackwell dominance, constructive).** Give the learner both exact laws, including `m,A,c,delta`. For any fixed number `n` of safe noisy force readings, the experiment consisting of `n` independent observations at `a` dominates every possibly randomized adaptive safe-query procedure. This holds for every decision problem on the two hypotheses, not just an information-gain surrogate.

**Proof.** Let `W_t=f_j(a)+sigma*G_t` be independent endpoint readings under hypothesis `j∈{0,1}`. Suppose a competing adaptive procedure requests `x` after the previously simulated history. Put `r=h_delta(x)/epsilon_delta`, which lies in `[0,1]`. With fresh independent `G'_t~N(0,1)`, supply

`Y_t=m*x+r*(W_t-m*a)+sigma*sqrt(1-r^2)*G'_t`.

Under either hypothesis this has exactly mean `m*x+j*h_delta(x)` and variance `sigma^2`, independently of earlier fresh measurement noises conditional on that history. The random transformation uses the known pair and the adaptive procedure but does not depend on `j`. Applying it successively simulates the entire competing transcript from the endpoint experiment. Any decision based on the simulated transcript is therefore available to the endpoint observer. QED.

The ordinary incumbent is consequently **exactly optimal**, not a weak polynomial fit or a chosen bad baseline. It keeps the sample mean and uses the midpoint likelihood test. Its equal-prior Bayes error (also its minimax error, by symmetry) is

`p_star(n)=Phi(-sqrt(n)*epsilon_delta/(2*sigma))`.

To achieve error at most `p<1/2`, the exact required count is

`n >= 4*sigma^2*[Phi^{-1}(1-p)]^2 / epsilon_delta^2`, rounded upward.

Combining with the signature bound gives

`n >= 4*sigma^2*[Phi^{-1}(1-p)]^2 * exp(2*(c-a)/delta)/(A^2*delta^2)`.

Any estimator claiming target error strictly less than `D_delta/2` under both laws yields a hypothesis test by choosing the closer target force. Its worst-case failure probability is therefore at least `p_star(n)`. The exact optimal comparator already receives more source-family knowledge than an unrestricted discovery system; ignorance cannot evade the lower bound.

**Finite-difference bridge.** Spend an even `n` on `n/2` independent pairs at `a` and `a-w`, `0<w<=a`, then retain only their differences. Dividing by `w` does not improve signal-to-noise. The optimal test on these differences has

`p_difference=Phi(-sqrt(n)*[h_delta(a)-h_delta(a-w)]/(4*sigma))`.

Its discrimination signal is at most half that of the endpoint incumbent for the same count. Keeping both raw records can only recover an ordinary safe-query procedure already dominated by Theorem 1. A separately calibrated derivative detector is a different operation and is not assumed here.

## 4. Sharp discontinuity despite bounded stiffness

Define the safe-to-target modulus

`omega(epsilon)=sup{|f(b)-g(b)| : f,g∈F(m,L), sup_[0,a]|f-g|<=epsilon}`.

**Theorem 2.** `omega(0)=0`, but

`lim_(epsilon↓0) omega(epsilon)=(L-m)*(b-a)`.

**Proof.** At zero error, the real-analytic identity theorem gives `f=g` on `R`. For positive error, integrate the derivative difference from `a` to `b` to get

`|f(b)-g(b)| <= epsilon+(L-m)*(b-a)`.

For the lower bound set `d=b-a` and `c_delta=a+sqrt(delta*d)`, with `0<delta<d`. Use the pair in Section 2. Its safe signature is at most `A*delta*exp(-sqrt(d/delta))`, which tends to zero, while its target separation tends to `A*d`. For every fixed positive `epsilon`, sufficiently small `delta` meets the safe-data constraint and gives target separation arbitrarily close to `A*d`. Taking suprema and then the limit proves the claim. QED.

For an oracle returning the **entire safe curve** with adversarial uniform error at most `epsilon`, let `R(epsilon)` be the minimax absolute prediction error at `b`. Midpoint data between the two constructed laws gives `liminf R(epsilon)>=A*(b-a)/2`. Conversely `Y(a)+(m+L)*(b-a)/2` has error at most `epsilon+A*(b-a)/2`, so

`lim_(epsilon↓0) R(epsilon)=(L-m)*(b-a)/2`, whereas `R(0)=0`.

This is a sharp limiting result. It does not claim the exact positive-epsilon modulus or risk has been determined.

For Gaussian observations, choose `delta` after any fixed `n` and target accuracy radius below `(L-m)*(b-a)/2`. Theorem 1 gives worst-case failure arbitrarily close to `1/2`. Thus there is no uniformly consistent extrapolation procedure over `F(m,L)` at any increasing finite sample budgets. For each fixed pair, however, endpoint measurements identify the pair as `n→infinity`; pointwise learnability is not denied.

## 5. Even a fixed finite jet has a vanishing safe signature

This is an additional mathematical observation, not an assertion that a derivative detector has been built. Suppose derivative channels through a fixed order `r_max` have fixed positive noise floors and finite observation counts. For `r>=1`, put `q=exp(-(c-a)/delta)` and take `q<=1/2`. Differentiating the absolutely convergent series `t/(1+t)=sum_(k>=1) (-1)^(k+1)t^k` with `t=exp((x-c)/delta)` gives

`sup_[0,a] |h_delta^(r)(x)| <= A*delta^(1-r)*C_r*q`,

where `C_r=sum_(k>=1) k^(r-1)*2^(-(k-1))` is finite for every fixed `r`. The force channel has the earlier bound `A*delta*q`. Consequently every fixed finite collection of these noisy derivative channels has vanishing total Gaussian KL as `delta→0`, at any fixed finite budgets. An independent stiffness sensor can improve a particular case by powers of `delta`; it does not establish a uniform bridge over unboundedly narrow transitions. This statement does not cover increasing derivative order with uncharged precision/resources or other physical observables.

## 6. Passive network rearrangement cannot supply arbitrary amplification for free

Consider an explicitly bounded equilibrium operation. Let `z∈R^d` be free coordinates, `s(z)=B*z+d0` the vector of `M` unknown-component strains, and

`E_j(z)=E_known(z)+sum_e U_j(s_e(z))-load^T*z`.

Assume both equilibria `z_j` are interior, `E_1` is `beta`-strongly convex, and `s_e(z_0)∈[0,a]`. Then

`||z_1-z_0|| <= ||B||_2*sqrt(M)*epsilon_delta/beta`.

**Proof.** `grad E_0(z_0)=grad E_1(z_1)=0` and

`grad E_1(z_0)-grad E_0(z_0)=B^T*h_delta(s(z_0))`.

Strong monotonicity and Cauchy–Schwarz give `beta*||z_1-z_0|| <= ||grad E_1(z_0)||`, followed by the displayed bound. QED.

A linear displacement sensor of norm at most `K` with independent isotropic Gaussian coordinate noise `sigma^2 I` therefore has one-vector-record KL at most

`K^2*||B||_2^2*M*epsilon_delta^2/(2*beta^2*sigma^2)`.

For adaptive choices satisfying these common bounds at every history under both laws, the chain rule adds these KL bounds. A `d`-coordinate vector record contains `d` scalar sensor channels; it is not charged as a single scalar force reading in Theorem 1. Finite material count, coupling, sensing gain and inverse stability margin cannot expose an arbitrarily narrow hidden transition uniformly. This is an explicit resource inequality, not a theorem that every passive network is worse than a scalar detector. Large gain or near-critical small `beta` can change the information per measurement and must be charged and supported. The executable checks use anchored chain/parallel networks and verify the sensitivity bound numerically.

## 7. What the theorem does and does not establish

The completed object is the explicit pair, exact adaptive comparison, sharp modulus and bounded-network obstruction. The source-supported general phenomenon of analytic-continuation instability predates this work. These elementary arguments do not establish novelty of the exact passive/adaptive specialization; priority remains unresolved. The proof defeats the attempted universal acquisition bridge under the stated operation class, including an optimum incumbent. It neither refutes the cited analytic system-identification theorem with fixed known features/excitation constants nor SafeOpt with its specified regularity class. It is not a physical device, a measured material, a claim about all possible detectors, or a new useful operation for civilisation-scale science.

The precise missing operation is either (i) supported direct interrogation in the target transition regime, (ii) a separately demonstrated compatible sensor that couples to it below the safe strain with quantified noise and full resource cost, or (iii) a justified quantitative prior such as a common complex analytic domain/norm or a transition-width lower bound. Merely assuming such an operation or bound would erase the acquisition problem being investigated.
