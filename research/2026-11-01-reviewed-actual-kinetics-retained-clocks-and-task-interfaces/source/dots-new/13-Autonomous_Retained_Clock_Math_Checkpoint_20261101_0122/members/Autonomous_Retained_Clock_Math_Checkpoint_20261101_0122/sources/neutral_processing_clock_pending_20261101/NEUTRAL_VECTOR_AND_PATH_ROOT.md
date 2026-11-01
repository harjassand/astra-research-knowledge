# Root extension: a slow vector survives received neutral processing

Status: NEW conditional proof, independent review pending. Ordinary storage inequalities and the separately written vector-to-path theorem are components. No physical process, feedback, or executable model acquisition is supplied by this abstract statement.

Use the exact reference form, unit e, a,q,sigma and ACTUAL energy evolution from PASSIVE_PORT_CLOCK_ROOT_V2. Start u(0)=e, write u=c e+x. The previously proved finite-horizon bounds give

 C_T <=sqrt(a/2)/(a-sigma), Y_T<=sigma C_T.

The hidden storage inequality, after dropping its nonnegative dissipative integral, gives

 ||x(T)||^2 <=2 C_T Y_T <=sigma*a/(a-sigma)^2.

Let d=aq-1=sigma/(a-sigma). Therefore

 ||x(T)||^2 <=d(1+d),
 |c(T)-exp(-aT)| <=d/2,
 ||u(T)-exp(-aT)e||^2 <=d+(5/4)d^2.

The last step uses Hilbert orthogonality, not a triangle bound. If a<=k and kq<=1+epsilon, then d<=epsilon and k/a-1<=epsilon. Consequently

 ||u(T)-exp(-kT)e||
 <= sqrt(epsilon+(5/4)epsilon^2)+epsilon/EulerNumber.

Uniformity holds on every finite horizon with the same reference certificate. No spectral mixture representation, global gap, or processing strength bound is required, but the complete energy-solution premises remain required.

## Observable chronology is a separate receipt

For path prediction one needs P_{s,t}e, not merely P_{s,t}^*e. Receive the backward evolution v(r)=P_{t-r,t}e for r in[0,t-s]. It satisfies v'(r)=L_{t-r}v(r), v(0)=e, in the actual common weak solution class. If this evolution earns the SAME scalar and hidden-storage inequalities (e.g. the received common-domain symmetric reference plus neutral skew or dissipative processing annihilating e on both sides), the vector bound applies to P_{s,t}e too. One cannot infer this just by swapping the symbols in a nonautonomous equation. The concrete compact transverse drift class should be checked in both orientations.

## Global slow observable and finite paths

For a conservative Markov model restrict the reference form to the invariant mean-zero Hilbert space. Require injectivity there and finite inverse FORM of mean-zero psi. Set e=psi/||psi||. Actual processing must preserve the reference probability pi and mean-zero space and annihilate psi on both sides. These premises exclude generic observed-state feedback.

When the backward energy evolution is received,

 ||P_{s,t}psi-exp(-k(t-s))psi||_2
 <=||psi||_2 [sqrt(epsilon+(5/4)epsilon^2)+epsilon/EulerNumber].

For an actual +/-1 partition label Z at L2 distance eta from psi, add (1+exp(-k(t-s)))eta. Insert this d_i into ROOT_VECTOR_TO_PATH_THEOREM.md. A common invariant pi and initial density bounded by R are preserved at all predetermined sampling times, so that theorem's entropy-chain proof extends to these time-inhomogeneous actual propagators without change:

 KL(actual finite label path || fixed-rate two-state sampled chain)
 <=R sum_i d_i^2/(1-exp(-2k Delta_i)).

This would receive a retained-state sampled process despite arbitrary predetermined internal neutral processing. It is not a continuous renewal theorem, arbitrary adaptive observation/control theorem, relative extreme-tail guarantee, or automatically a finite processed mean. Each additional proof join and the actual global slow trial/current construction must be independently accepted before any concrete numerical claim.
