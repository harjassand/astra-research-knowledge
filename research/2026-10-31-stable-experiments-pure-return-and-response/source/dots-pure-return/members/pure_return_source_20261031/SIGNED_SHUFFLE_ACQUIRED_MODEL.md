# A completely specified centered source with factorially many labels
31 October 2026. Model/interface construction. The full rapid-source compiler remains a separate pending receiving theorem.

## 1. Avoiding an unearned mean-subtraction operation
For an arbitrary succinct family B_pi indexed by n-card permutations, computing the uniform operator mean need not be easy. The condition PKP=0 cannot be obtained by silently subtracting that unknown mean.

Instead specify a DIFFERENT physical source from the outset: its classical state is (sigma,pi), with sigma in{+1,-1}. At a rate-lambda event, pi undergoes TOP-TO-RANDOM shuffling and sigma is independently redrawn fair. Its stationary law is uniform on2 n! labels. Between events the system Hamiltonian is

    H_sys + sqrt(lambda) sigma B_pi,

where each B_pi is bounded Hermitian, ||B_pi||<=b, and the family has an actual controlled circuit. The sign is a real part of this model, not a claim that arbitrary unsigned noise is equivalent to it.

One explicit example with H_sys=0 is B_pi=b U_pi^dagger Z_1 U_pi, where U_pi applies a supplied finite list of noncommuting system gates in permutation order. The controlled B_pi circuit executes that actual list and its inverse, paying O(n) selected gates plus permutation/selection arithmetic. It does not tabulate n! matrices. This example is a task definition, not a complexity-separation or practical-advantage claim.

## 2. Acquired source channel and pure stationary state
Let Φ_perm be the shuffle channel in ACQUIRED_SHUFFLE_MULTISTEP_RETURN.md. Its Kraus operators are K_c=T_c/sqrt(n), with the acquired insertion isometry described there. Define

    Φ=Reset_(|+>) on sign tensor Φ_perm,
    ψ=|+> tensor (uniform pure permutation state).

A Kraus family is K_(z,c)=|+><z| tensor K_c, z=0,1. Its fixed-state coefficients are c_(z,c)=1/sqrt(2n). The source Stinespring operation is acquired by transferring the old sign into a private record, preparing a fresh |+>, and executing the acquired permutation insertion isometry. It has2n Kraus labels, not2n! labels. Uniform ψ and the environment coefficient state are prepared by known finite arithmetic/range circuits.

The source-diagonal coupling

    K=Z_sign tensor sum_pi |pi><pi| tensor B_pi

is Hermitian with norm at most b. Its pure stationary compression is exactly PKP=0 because <+|Z|+>=0. No likelihood, partition function, uniform permutation operator average or coherent unknown-distribution preparation is used.

## 3. Exact classical-process receiving
On source diagonal observables, Φ† is the TOP-TO-RANDOM transition with independent fair sign reset. The system-valued diagonal algebra is also preserved by the commutator with K and system-only instruments. Therefore the quantum source initially ψ reproduces the entire accessible system process of the specified classical signed source. This holds under arbitrary references and instruments at prescribed times, with their outcomes retained. The source and its artificial dark-jump records remain inaccessible.

In particular, this is not merely agreement on one initial system state or one-time covariance. Conversely it does not identify physical source measurements with the private quantum jump records.

## 4. One explicit return horizon supplies both needed certificates
For any m>=1, Φ^m=Reset_(|+>) tensor Φ_perm^m. The all-card-labels-seen event is invariant under card relabeling, and its constant root is uniform conditional on that event. Thus the previous exact normalized decomposition gives

    (Φ†)^m Q <= delta_m Q, delta_m<=n exp(-m/n).

Take m=max(1,ceil(n log(16n))). Then delta_m<=1/16. This is the acquired operator return certificate of the abstract opening.

Its overlap contraction A=(<c| tensor I)W is Π_plus tensor P_perm, where P_perm is the acquired random-to-top pullback matrix. It reduces P and has ||A^m Q||<=1/4 by projection of the m-step dilation. Hence the same polynomial n log n certificate supplies both the Lyapunov activity bound and the scaled fast-kernel operation; it is not inferred from eigenvalues alone.

Every quantity here is obtained from the actual known stochastic program and a coupon-collector/symmetry proof. This is not learning an unknown physical source from samples. If its transition law or couplings must instead be fitted, that acquisition and model error are additional burdens.

## 5. Intended and excluded consequences
The source uses factorially many classical labels but only polynomial-size known registers and circuits. If the pending whole pure-return receiving theorem closes, its source dependence can be polynomial in n and the certified return horizon, rather than explicit2n! or inverse stationary mass. The usual H_sys, coupling, control, precision and output-estimation costs still apply.

Generic quantum simulation already avoids a full Hilbert-space matrix; the additional target is avoiding a loop proportional to the rapid source rate while retaining finite-rate corrections and memory. Direct shuffling, high-order elimination, compressed process methods and general fast-forwarding remain necessary comparators. No novelty, practical crossover, statistical acquisition advantage or civilisation-level capability has been established for this example.
