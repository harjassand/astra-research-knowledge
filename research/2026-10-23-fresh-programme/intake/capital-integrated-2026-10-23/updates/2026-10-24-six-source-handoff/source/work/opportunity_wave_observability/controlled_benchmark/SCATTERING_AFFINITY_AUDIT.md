# Scattering-query affinity audit

## Result

For fresh coherent pulses measured before the next pulse, the claimed
classical-transcript affinity bound is valid under a pathwise budget on the
sum of conditional coherent mean photon numbers. It applies to arbitrary
adaptive POVMs and stopping rules. With $\epsilon=cV$, constant-error
distinction therefore needs mean photon budget at least
$\ln(9/8)/(c^2V^2)$ in this restricted architecture.

For arbitrary ancillas, entanglement, and multipass strategies, the hybrid
bound $\mathrm{TV}\le T\epsilon$ is valid when each photon interaction is a
number-preserving unitary query on the complete one-particle mode space, with
$\|S_D-I\|\le\epsilon$, and $T$ is a hard cap on photon-passes on every
branch. It gives $T\ge1/(3\epsilon)$ for two-sided error at most $1/3$.
If $S_D$ is only the accessible sub-block of a lossy scattering channel, the
stated exact constant is not justified by that sub-block norm alone; a
one-photon pure-loss example exceeds $\epsilon$. The full-channel interface
must be specified.

## Fresh coherent pulses: transcript affinity

Write classical Hellinger affinity as
\[
 A(P_0,P_1)=\int\sqrt{dP_0\,dP_1}.
\]
For an input coherent state $|\alpha\rangle$, $n=\|\alpha\|^2$, the two
outputs are $|\alpha\rangle$ and $|S_D\alpha\rangle$. Their overlap obeys
\[
 |\langle\alpha|S_D\alpha\rangle|
 =\exp[-\|(S_D-I)\alpha\|^2/2]
 \ge \exp[-\epsilon^2 n/2].
\]
For any POVM $(E_y)$, its outcome affinity is at least this overlap:
\[
 \sum_y\sqrt{\langle\psi|E_y|\psi\rangle
                   \langle\phi|E_y|\phi\rangle}
 \ge \left|\sum_y\langle\psi|E_y|\phi\rangle\right|
 =|\langle\psi|\phi\rangle|,
\]
with the same integral proof for continuous outcomes. Thus the bound holds
for every per-round POVM, including one selected from the preceding
classical record.

For an adaptive protocol, condition first on the controller's private random
seed (or expose each fresh action coin in the transcript), and include action
choices and stopping decisions. Their conditional kernels are identical
under the two hypotheses given a shared history. If $a_t(h)$ is the
conditional outcome affinity for pulse $t$, then
$a_t(h)\ge e^{-\epsilon^2 n_t(h)/2}$.
The joint transcript affinity can be written as
\[
 A(P_0^{(m)},P_1^{(m)})
 =\mathbb E_R\!\left[\prod_{t=1}^m a_t(H_{t-1})\right],
\]
where $R$ uses the common action kernels and, conditional on history,
normalizes the geometric-mean outcome kernel
$\sqrt{q_0(y|h)q_1(y|h)}/a_t(h)$. If every possible history has
$\sum_t n_t(h_t)\le N$, the integrand is at least
$e^{-\epsilon^2N/2}$, so
\[
 A(P_0^{(m)},P_1^{(m)})\ge e^{-\epsilon^2N/2}.
\]
After a stop, pad with a deterministic zero-energy outcome. For an
unbounded stopping time, every finite-prefix affinity obeys the same bound;
the affinity on the full padded record is its decreasing limit and retains
the bound. Coarsening to the terminal record can only increase affinity.
This requires the stated pathwise budget over all possible histories and
controller random seeds; an average-only budget does not give this
pointwise product argument.

Since $\mathrm{TV}(P_0,P_1)\le\sqrt{1-A(P_0,P_1)^2}$, two-sided error at most
$1/3$ requires TV at least $1/3$ and hence
\[
 N\ge \frac{\ln(9/8)}{\epsilon^2}.
\]
This $N$ is the sum of conditional coherent mean photon numbers on each
classical history. It is not a hard cap on the Poisson-distributed photon
number in each coherent pulse.

## Hard photon-pass cap: hybrid bound and scope

Suppose $S_D$ is unitary on the complete one-particle mode space, including
every output mode counted as part of the query, and the null query is the
identity. On the $m$-photon sector, passive linear scattering acts as the
bosonic restriction of $S_D^{\otimes m}$. Telescoping gives
\[
 \|S_D^{\otimes m}-I^{\otimes m}\|
 \le \sum_{j=1}^m\|S_D-I\|\le m\epsilon.
\]
The same bound holds on the symmetric subspace. For any input entangled with
an arbitrary ancilla, trace distance after one such query is at most this
operator-norm difference: purify the input and use
$D(|\Psi\rangle,|\Phi\rangle)=\sqrt{1-|\langle\Psi|\Phi\rangle|^2}
\le\|(U-I)|\Psi\rangle\|$. Thus a pass containing $m$ photons contributes
at most $m\epsilon$ in TV. Interleave arbitrary hypothesis-independent
controls and measurements and replace the defect query by identity one
photon at a time. The hybrid triangle inequality sums these costs, yielding
\[
 \mathrm{TV}(P_0^{\rm out},P_1^{\rm out})\le T\epsilon
\]
when the total number of photon-passes is at most $T$ on every branch.
Adaptive early stopping is padded by identity/no-photon slots. The cap must
be enforced on every controller outcome branch, including histories used in
the hybrid circuits, not only in expectation or only on histories likely
under one hypothesis. For two-sided error at
most $1/3$, $T\ge1/(3\epsilon)$.

The unitary/completeness condition matters for the exact coefficient. For an
accessible pure-loss channel with single-mode amplitude $s=1-\epsilon$,
$|s-1|=\epsilon$, but a one-photon input produces
\[
 (1-\epsilon)^2|1\rangle\langle1|
 +(2\epsilon-\epsilon^2)|0\rangle\langle0|,
\]
whereas the null output is $|1\rangle\langle1|$. Their TV is
$2\epsilon-\epsilon^2>\epsilon$ for $0<\epsilon<1$. Thus an accessible
nonunitary mode block alone does not establish the exact $T\epsilon$ claim.
If loss ports are included in a unitary dilation, the relevant norm premise
must hold for that full dilation; it cannot be inferred from closeness of
the transmitted block. Alternatively, establish a direct per-photon
half-diamond-norm bound for the full channel and use that bound in the
hybrid. The $T$ statement is a hard photon-interaction result, not a bound
from a mean-photon budget.
