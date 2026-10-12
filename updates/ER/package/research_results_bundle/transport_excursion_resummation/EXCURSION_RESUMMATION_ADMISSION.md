# Admission test: local coherence excursions before balance projection

## Decision

**Do not admit the proposed positive-renewal shortcut as an affordable interacting-current algorithm.** Conjugate pairing makes a coherence excursion real, not positive. At the fully comparable point t = U = d = 1, the exact four-site chain already has a strictly negative off-diagonal excursion entry. Replacing such excursions by positive full-configuration measurement resets changes the onsite-dephasing generator: no positive reset rate can be extracted with a completely positive Markovian remainder. Partial local measurements are exact and positive, but retain the many-body coherent propagation that the proposed shortcut was supposed to remove.

This is a bounded rejection of that specific mechanism. It is not a no-go for every quantum renewal representation, tensor compression, stochastic resummation, or transport algorithm. No generic exponential classical-complexity lower bound is claimed. No economical bounded-variance construction survived this test.

## 1. Exact object being tested

Use H = -(t/2) sum(XX+YY) + U sum ZZ and L = -i[H,.] + gamma sum_i(Z_i . Z_i - .), with d = 4 gamma. For computational configurations x,y,

D(|x><y|) = -(d/2) Hamming(x,y) |x><y|.

Work within a fixed particle-number sector. Let P retain configuration-diagonal operators and Q=I-P. These are **not** the previous global balance projection. Since PLP=0, a diagonal initial state obeys the exact population equation

p'(s) = integral_0^s K(s-u) p(u) du,
K(s) = PLQ exp(s QLQ) QLP.

The Q propagator forbids an intermediate configuration-diagonal return. Its Dyson expansion groups paired forward/backward hopping paths into precisely the proposed irreducible excursions. It is an exact definition, not an evaluation algorithm.

For a single hopping edge with energy mismatch Delta, the second-hopping-order contribution is

K_yx^(2)(s) = 2 t^2 exp(-d s) cos(Delta s).

A nearest-neighbor exchange in the XXZ chain can have Delta = +/-4U. This formula is the exact second-order coefficient when the diagonal Hamiltonian and noise are resummed. It is not the full many-body kernel with neighboring hops frozen by fiat.

### Full interacting, comparable-parameter counterexample

Take the periodic four-site chain in its two-particle sector. Keep all six configurations and every allowed hop. At t=U=d=1, its P and Q dimensions are 6 and 30. The exact kernel obeys

-1.112 < K_(1001,1010)(1/2) < -1.111.

Thus even the complete Q-excursion resummation on this small interacting chain cannot be interpreted as a nonnegative transition kernel. This sign is certified by a rational 50th-order exponential series with an explicit matrix-norm remainder, rather than inferred from floating-point plotting. The numerical central value is -1.11187271739029.

The four-site example only falsifies positive entries of this exact excursion operation. A memory kernel is not itself a waiting-time density, so this alone does not disprove all positive renewal constructions.

## 2. Why the simplest positive-renewal repair changes the noise

An isolated two-configuration system does admit positive Poisson full measurements, with coherent flights between them. More generally, if the actual generator were

L = -i[H,.] + r(P-I),

complete-basis measurements at rate r would produce positive endpoint kernels r exp(-r s) |<y|exp(-iHs)|x>|^2. The no-event term also contains quantum flight, so this is not a classical state that simply waits at x. Evaluating those transition probabilities still costs interacting quantum propagation.

The onsite noise in the many-body chain is not r(P-I), and one cannot extract even an arbitrarily small such component with a completely positive Markovian remainder.

### Exact four-configuration obstruction

Choose the four configurations

x1=1010, x2=0110, x3=1001, x4=0101,

which describe two independent particle-hole exchanges and all have the same charge. Their dephasing-rate matrix is

q/d = [[0,1,1,2], [1,0,2,1], [1,2,0,1], [2,1,1,0]].

For c=(1,-1,-1,1), sum c=0 and c^T q c=0. A dephasing generator with rates q' can be completely positive only if q' is conditionally negative semidefinite: c^T q' c <= 0 for every zero-sum c. This follows directly by differentiating positivity of the Schur matrix exp(-s q') at s=0 on the subspace perpendicular to the all-ones vector.

Subtracting a reset term r(P-I) leaves q'_xy=q_xy-r for x!=y and q'_xx=0. But then

c^T q' c = r ||c||^2 = 4r > 0.

Therefore no r>0 works. This also rules out a general Lindblad remainder: since the remaining noise fixes every configuration projector, any such remainder must be dephasing on this sector. Keeping the Hamiltonian in the remainder cannot repair the conditional complete-positivity failure; a Hamiltonian derivation does not contribute to that dissipative quadratic form.

This is the smallest same-charge independent-exchange square. One-particle sectors have only Hamming-distance-two off-diagonals and do not expose the issue; testing only them would give a false impression of a general reset construction.

### Quantitative finite-time version, with precise scope

On m disjoint particle-hole pairs, choose one particle per pair. The 2^m configurations all have the same total charge. For a **pure-noise segment** of duration tau, its Schur multiplier matrix is

C_tau = [[1,a],[a,1]] tensor-powered m times,
a = exp(-d tau).

If that channel contains a positive full diagonal-reset component of weight p, then C_tau-p I must be positive semidefinite. Consequently

p <= lambda_min(C_tau) = (1-exp(-d tau))^m.

At a fixed microscopic tau=O(1/d), this weight is exponentially small in m. To allow a fixed weight p0 in (0,1), necessarily

tau >= -(1/d) log(1-p0^(1/m))
     = (log m - log(-log p0) + o(1))/d.

This bound applies to extracting reset components from the pure onsite-dephasing channel, including the noise segments in a splitting construction. It is not a lower bound for every Hamiltonian-augmented channel or an assertion that all reset waiting times are exponential in system size. Larger intervals must still pay for the intervening interacting coherent propagation.

## 3. Two distinctions that prevent false positives

### Classical waiting law versus memory kernel

For a resonant dimer, the population memory rate is k(s)=2t^2 exp(-d s), which is nonnegative. Yet the unique state-changing, classical alternating-renewal waiting transform is

f_hat(z) = k_hat(z)/(z+k_hat(z))
         = 2t^2/(z^2+d z+2t^2).

At t=d=1,

f(s) = (4/sqrt(7)) exp(-s/2) sin(sqrt(7) s/2),

which changes sign. This rejects a configuration-only semi-Markov interpretation whose state stays fixed between changes. It does not reject the positive measured quantum-flight construction above. Thus neither sign of the memory rate nor complete positivity of the original Lindblad evolution establishes the desired cheap classical renewal law.

The standard relation f=k*g and the distinction between classical waiting and quantum flights are explicitly discussed in Megier, Smirne and Vacchini, *Evolution equations for quantum semi-Markov dynamics*, Section III, equations (18)-(22): https://arxiv.org/abs/2007.11276. General positive quantum renewal constructions are developed in Vacchini, *Quantum renewal processes*: https://arxiv.org/abs/1906.00693. These primary papers provide the definitions; the chain-specific counterexamples above are checked directly here.

### Positive local measurements retain coherent information

There is an exact positive unraveling

D = 2 gamma sum_i(P_i-I),
P_i(rho) = (rho + Z_i rho Z_i)/2.

At each event only site i is measured. The conditional state on unmeasured sites remains coherent and may remain entangled. Already four sites with two particles retain a three-dimensional conditional sector after measuring one site; the general conditional sector is not specified by one classical spin configuration. Subsequent hopping can recreate coherence on previously measured sites, so 'every site has been measured sometime' is not a global reset at a common instant.

Using this unraveling is ordinary monitored-state simulation unless a separate evaluated compression theorem is supplied. Positivity of trajectory probabilities alone does not bound the cost of calculating their Born probabilities, propagating the conditional state, or estimating the response observable.

## 4. Sampling, horizons and errors are still charged

### A concrete signed-time sampling bill

Consider even the exactly evaluated single-edge paired contribution f(s)=exp(-d s) cos(Delta s), Delta>0. Its signed and absolute masses are

I = d/(d^2+Delta^2),
Z = [d + Delta csch(pi d/(2 Delta))]/(d^2+Delta^2).

Their ratio is R=Z/I=1+(Delta/d)csch(pi d/(2 Delta)). At Delta=4U and U=d, R=10.9287517265.

For independently sampling m such excursion times before analytically resumming their cancellations, even the optimal importance distribution has relative second moment R^(2m). This follows from Cauchy-Schwarz: integral f_total^2/p >= (integral |f_total|)^2, and both integrals factor for the m-fold example. Relative root-mean-square error epsilon requires at least (R^(2m)-1)/epsilon^2 independent samples in this particular estimator family.

This is **not** a lower bound on arbitrary estimators or regroupings, nor a claim that every many-body current path consists of these independent factors. Indeed the scalar integral I can be evaluated analytically at constant cost. Its purpose is to show exactly why pairing conjugates and leaving excursion times to Monte Carlo does not by itself prove bounded variance. A successful many-body resummation would have to remove the correlated signed contractions with equal explicitness.

### Excursion lifetime is controlled; total response time is a separate bill

In a fixed-charge sector every Q matrix unit differs on at least two sites, so the dissipative part of QLQ is at most -d. The Hamiltonian part is skew-adjoint in Hilbert-Schmidt norm. Hence

||exp(s QLQ)||_(2->2) <= exp(-d s).

Writing a=||PLQ|| and b=||QLP||, the tail of the integrated excursion operation is bounded by

||integral_T^infinity K(s) ds|| <= (a b/d) exp(-d T).

An operator-error budget eta therefore permits T >= d^(-1) log(a b/(d eta)) whenever the logarithm is positive. Endpoint norms, their volume dependence, and the precision of evaluating the truncated Q propagator must be included; the bound is not a dimension-free cheap oracle. A local spatial truncation would additionally need a valid propagation bound and its error accounting for this projected operation.

Most importantly this only bounds an **individual coherence excursion**. Repeated diagonal intervals are not dephased, and long-wavelength density modes are slow. It does not justify truncating the infinite-time current-response integral at O(1/d). Current response also begins and ends with off-diagonal current insertions, so the population kernel alone is not the estimator: endpoint source/observable factors and their cancellations must be carried. A complete algorithm still needs a finite-volume or thermodynamic error theorem, the total horizon or resolvent error, number of excursions needed, evaluated coherent-block cost, variance and sample count, and propagation of every approximation error to the final response.

## 5. Reproduction and stopping condition

Run

python check_excursion_reset.py

It checks the conditional-negative-definiteness witness, finite-time reset eigenvector, dimer waiting transform, and a rational negative-kernel certificate for the full four-site interacting chain. Small floating-point outputs are diagnostics; the reported sign interval has an exact rational remainder certificate.

Parameters are supplied model inputs; no measurement or parameter-learning costs are hidden in the test. No physical experiments were performed.

Stop this branch here. Reopen only for a concrete evaluated operation that compresses the retained coherent state or resums the correlated signed excursions, together with a full accuracy/variance/horizon bill at comparable t,U,d. Merely relabeling local measurements as renewal events or displaying the formal Q resolvent does not meet that gate.
