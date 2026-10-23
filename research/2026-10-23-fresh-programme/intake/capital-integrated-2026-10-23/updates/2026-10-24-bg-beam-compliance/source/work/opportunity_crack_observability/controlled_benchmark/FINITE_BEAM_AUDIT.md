# Finite-beam attenuation interface: independent bound

## Verdict

For unloaded transmission with absorption-only readout, a fixed finite
transverse beam-density bound gives a uniform per-photon joint-TV bound
$M\mu V_b$, even if the incident transverse coordinate is revealed. It
implies an adaptive stopped-photon lower bound $\Omega(V_b^{-1})$ for
constant-error distinction, without a survival-interior assumption. If the
detector reports only aggregate survival/count outcomes and survival
probabilities stay uniformly inside $(0,1)$, per-photon KL is $O(V_b^2)$
and the stronger $\Omega(V_b^{-2})$ bound follows. That quadratic claim does
not extend automatically to coordinate-resolved data. This contract
excludes phase readout, ideal point rays, mechanical loading, and unbounded
or unknown calibration effects.

## Uniform single-photon bound

Fix a beam direction and parameterize parallel rays by transverse location
$u$. Let $\ell(u)$ be the length of the ray inside the slit volume $C_b$,
and let $\tau_0(u)$ be its intact optical depth. Replacing the slit material
by a transparent void changes this depth to $\tau_1(u)=\tau_0(u)-\mu\ell(u)$,
with both depths nonnegative. The incident coordinate has normalized
density $k$. If it is not observed, the one-photon survival probability is
\[
 p_0=\int k(u)e^{-\tau_0(u)}du,\qquad
 p_1=\int k(u)e^{-\tau_0(u)+\mu\ell(u)}du.
\]
For either aggregate survival probabilities or the joint observation of
coordinate and survival, use $|e^{-a}-e^{-b}|\le|a-b|$ for nonnegative
$a,b$. It gives
\[
 |p_1-p_0|
 \le \mu\int k(u)\ell(u)du
 \le \mu M\int\ell(u)du
 =\mu M V_b.
\]
The joint law of $(u,Y)$, where $Y$ is the survival bit, has TV exactly
$\int k(u)|e^{-\tau_1(u)}-e^{-\tau_0(u)}|du$, so it obeys the same bound.
Fubini gives $\int\ell(u)du=V_b$ for every direction. Thus the bound is
uniform in direction, slit orientation, and beam choice. It also holds
conditionally at every history when an adaptive policy chooses a fresh
$(direction,k)$, provided the same fixed $M$ applies to every allowed
action. A fixed slit length and bounded $\mu$ ensure finite depth changes;
the Lipschitz inequality itself needs no extra exponential factor.

For an adaptive stopping rule, couple the experiments recursively. While
their histories agree, use the same random draw for the next action (the
policy has the same conditional action kernel under both hypotheses), then
maximally couple the next $(u,Y)$ observations. Conditional mismatch
probability is at most $\delta=\mu M V_b$. The chance that the first mismatch
occurs on photon $t$ is therefore at most $\delta P_0(N\ge t)$: agreement
through $t-1$ is a subset of the null event that the policy has not yet
stopped. Summing over $t$ gives
\[
 \|P_0^{\rm terminal}-P_1^{\rm terminal}\|_{\rm TV}
 \le P(\text{some mismatch before null stopping})
 \le \delta\sum_{t\ge1}P_0(N\ge t)
 =\mu M V_b\,\mathbb E_0N.
\]
If no mismatch occurs, both policies stop with the same terminal record. A
test with error at most $1/3$ under both hypotheses has terminal TV at least
$1/3$, hence $\mathbb E_0N\ge(3\mu M V_b)^{-1}$. This is a sequential
coupling bound and needs neither an interior-probability assumption nor
independence of successive adaptive actions. It presumes a valid test returns
an output under both hypotheses; infinite $\mathbb E_0N$ is already a trivial
lower-bound case.

## KL and adaptive sample lower bound

Assume uniformly over both hypotheses and every allowed action/history the
survival probabilities satisfy $p_j\in[\xi,1-\xi]$ for some fixed
$0<\xi<1/2$. For Bernoulli photon survival,
\[
 D(\operatorname{Ber}(p_0)\Vert\operatorname{Ber}(p_1))
 \le \frac{(p_0-p_1)^2}{p_1(1-p_1)}
 \le \frac{\mu^2M^2}{\xi(1-\xi)}V_b^2
 =:cV_b^2.
\]
For $N$ photons with adaptive actions, the action-selection kernels are the
same functions of the past under both hypotheses, so they contribute no
conditional KL. The chain rule bounds transcript KL by $NcV_b^2$.
Constant-error testing forces transcript total variation bounded below by a
positive constant; Pinsker therefore gives $N=\Omega(V_b^{-2})$.

The stopped-count version follows from the same chain rule. Let $\tau$ be
the number of photons, and require an output test with unconditional error
at most $1/3$ under both hypotheses. Truncate the transcript after
$n=\lceil 6\mathbb E_0\tau\rceil$ photons, with a sentinel if it has not
stopped. Under hypothesis 0, Markov gives
$P_0(\tau>n)\le\mathbb E_0\tau/n\le1/6$; the event “stopped by $n$ and
outputs 0” consequently has probability at least $1/2$ under 0 and at most
$1/3$ under 1. Its probability gap is at least $1/6$, so the truncated
transcript has TV at least $1/6$ and KL at least $1/18$ by Pinsker. The
stopped chain rule gives
\[
 D(P_0^{\tau\wedge n}\Vert P_1^{\tau\wedge n})
 \le cV_b^2\,\mathbb E_0(\tau\wedge n)
 \le cV_b^2\,\mathbb E_0\tau,
\]
whence $\mathbb E_0\tau\ge(18cV_b^2)^{-1}$. Rounding $n$ or small
expected counts only changes constants. If the expectation is infinite,
the lower bound is immediate. Correctness conditional only on eventual
termination, with no termination-probability guarantee, is insufficient
for this argument.

The interior condition is material. The probability-difference bound alone
does not imply quadratic KL: Bernoulli parameters $1-V_b$ and $1-2V_b$
have difference $V_b$ but KL of order $V_b$, because the failure outcome
itself is rare. Moreover, the coordinate-resolved experiment can carry
order-$V_b$ KL even when aggregate survival is interior: a region of
transverse area proportional to $V_b$ can have an order-one conditional
survival contrast while the beam density remains bounded. Thus the robust
adaptive lower bound for the richer coordinate-resolved observation is the
$\Omega(V_b^{-1})$ coupling bound above; the quadratic-KL result is only for
the explicitly coarsened, uniformly interior Bernoulli observation. A
uniform lower bound on both survival and absorption probabilities prevents
the aggregate boundary regime.

## Interface limits

The beam cap is essential: an ideal point ray has no finite $M$ and can be
aimed through a vanishing-volume slit, so this uniform bound need not hold.
The bound is on expected photon count, not elapsed time: translating it into
wall-clock cost requires a source-rate and acquisition protocol. The result
uses only photon survival/count data from an unloaded body. A phase-sensitive
detector has a different likelihood and may respond to integrated
refractive-index contrast; it is outside this proof. Mechanical loading can
change crack aperture/volume during observation and likewise changes the
forward model. The proof allows arbitrary common background depth so long
as the defect changes it by exactly $\mu\ell(u)$; hypothesis-dependent
calibration shifts, scatter, or profile errors are separate signals and must
be included in a different observation model.
