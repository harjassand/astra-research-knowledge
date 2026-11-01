# Finite receiving of the new activity compiler

This records the changes needed to the preserved finite-bit proof, rather than treating a source isometry or its normalization as an input. The underlying standard scalar-source, amplification and controlled-duration arguments are credited to the actual N1511/N1512 sources. The new Gaussian/filter/weighted-CDF conjunction remains author-derived.

## Inputs and certificate errors

Use actual finite classical H,E,c_j and actual precision-capable system block circuits. Form A from Hermitian H and the loss factor E so passivity is exact. Check a rational/finite enclosure of P>=I and A^dagger P+PA<=-gamma P with declared slack. Acquire a certified pmax>=||P|| and upper bounds for a,a_P,a_inv. A computed numerical eigenvalue alone is insufficient. The explicit rank-one family has analytic margins; rounding P requires extra logarithmic rate bits because it is multiplied by A. General supplied certificates retain their actual conditioning/slack costs.

Z is bounded between I and (1+1/K)I. Its square roots, inverse square roots, logarithms and approximate diagonalizing unitary are finite M-dimensional calculations. Tiny pivots/eigenvalue degeneracies are handled by absolute approximation, as in the stage-two Gaussian circuit. There is no exponentially large sector diagonalization or inverse small eigenvalue of Z. A certified approximation error O(delta/K) in a one-particle contraction gives O(delta) error in its second quantization. The same bound, with the constant filter norm, prices S/2 and S^(-1).

The contraction drift C has norm at most O(R+gamma), with a uniform dissipativity certificate. Its exponential has the same explicitly paid scaling/squaring and Julia/Givens/binary-Fock implementation as stage two. The actual Gaussian block cost is O~(M^2 K) plus polynomial small-matrix arithmetic. It is called, not assumed, at every virtual dwell and inverse/amplification slot.

## The imported scalar source has matched parameters

Its physical scalar rates are delta=kappa/2 and nu=2g^2/kappa. Endpoints lie in 0..K. The chosen windows make nu*tau=O(1/(K+1)), so its candidate Poisson cap is logarithmic in the final error/call budget. The finite source uses actual O(K) endpoint posterior/factorial lists, a capped CDF scan, direct conditional exponential quantiles and independent marked candidates. Both row and column use identical seeds. The phase is (-i)^V for every retained virtual grade insertion. Cutoff-crossing and overflow paths select zero without resampling.

The actual grade maps are the two separately acquired coefficient directions; each is a bounded contraction with its own success work. The free dwell's designated block is a contraction preserving number. Replacing the old unitary dwell therefore preserves the precise Dyson/Schur argument. Its failure work cannot be traced out before the complete block. No inverse dissipative semigroup is used.

The original boundary/tie/retention cuts depend polynomially on the event cap, scalar rates, 1/t_min and the physical word derivative. Replace the latter by a bound using KR+h+2g sqrt(K+1); it is still a known polynomial. Consequently resolving these cuts costs logarithmically many extra time bits. No loop over delta*t or an exponentially small endpoint probability is introduced. Small g and zero coefficients have direct branches; positive coefficient magnitudes enter conditioning bits and normalizations as stated.

## The weighted time sources are acquired

The shifted drift Aw has a uniformly bounded exponentially decaying semigroup in the Z metric. Its Lyapunov inverse has norm O(1/kappa), up to finite-dimensional norm conversions. Hence classical finite-matrix inversion to acquire X, followed by reversible scaling/squaring for exp(Aw t), has a polynomial bit bound in matrix size, input lengths, log(1+R), log(1+1/kappa) and requested accuracy. The exact X has trace at most 3M. No growing exp(+kappa t) is multiplied into an underflowed physical kernel.

Every addressed dyadic interval mass is obtained from Jw(b)-Jw(a), Iw(b)-Iw(a), or W(b)-W(a). One coherent prefix evaluation and rotation per clock bit prepares the state; there is no 2^B-entry table. The prefix cutoff argument of stage two selects disjoint first-bad subtrees, so omitted mass controls squared source-state error without a hidden sqrt(B) loss. All other ratios have explicit retained-mass lower bounds. Tiny convolution normalizers are omitted using the product of its known attenuations. Norms of retained physical jump directions are protected by their source mass and the log-Lipschitz bound; they are not evaluated relatively at exponentially small amplitude for free.

Inner time cubature compares averaged contraction words; actual event clocks are compared as amplitudes on a common L2 space. Physical output color is retained. These two errors are not interchanged with timestamp total variation or rare conditional probabilities.

## Global local-error allocation

Let S_calls be the explicit deterministic cap, A0 the padded complete-isometry normalizer and Vcap the virtual word cap. Take a conservative base signal budget

    beta=[epsilon/(10^6 S_calls (A0+1)^2 (Vcap+1))]^4.

Divide smaller powers of beta among the finite number of matrix, source, filter, clock, rotation and grade-map operations. Extra squaring of a precision budget where a square root is taken changes only its logarithm. Source missing-path errors are multiplied by the already bounded scalar Schur norm and filter norms. Thus each acquired no-jump and normalized jump block has its uniform operator error budget on every retained input/reference. Complete-isometry amplification, including adjoints and failure leakage, then has local isometry error below epsilon/(100 S_calls) after constant safety allocation.

Use the physical finite-generator norm bound

    Lgen=1+2h+4a sqrt(K+1)+4KR

with enlarged harmless constants if necessary. Skip residual windows below beta/(100Lgen), charging their channel error; resolve event-time rounding to a correspondingly smaller word. This gives a positive arithmetic duration floor without imposing a minimum physical waiting time. All new derivative/conditioning bounds are polynomial in the displayed quantities, so B is polynomial logarithmic in these values and inverse beta. Large rate magnitudes do not become a number of time slices.

Compare backwards to the EXACT finite-K process with its actual emission counter stopped at the proved cap. Every fallback is unconditional CPTP. The exact count MGF pays its tail; no MGF is assumed for the approximate process. Add the proved vacuum occupation cutoff, CP-preserving coefficient rounding and source/initialization budgets. Contractivity prices all prescribed instruments and retained records. The continuous field is private, so its time-cell embedding is an error-analysis dilation rather than a public clock guarantee.

## Actual cost

Every base word has O(Vcap+1) Gaussian/system slots, and every full first-event call uses O(A0) base/inverse calls. The filters add a fixed number of actual Gaussian/arithmetic blocks. Scalar source and weighted-CDF prefix operations add polynomial work in their finite caps, M,r,B and input/precision lengths. System coupling and H_S queries retain their real gate costs.

For H_S the known maximum duration is tau. Its B-bit controlled circuit has fixed durations tau/2^b whose ACTUAL sum is at most tau, even when every controlled gate is present. Since S_calls*tau=O(T), the ordinary Hamiltonian action contributes O(A0 Vcap hT), plus the repeated precision/query overhead. This is the N1512 scheduling argument at its matched interface, not a claim that a sampled path alone pays for the circuit.

The resulting full query/arithmetic upper bound is polynomial in M,K,pmax,input lengths and logarithmic rate/precision quantities, multiplied by 1+Lambda T+hT+p. It is an elementary-gate bound only when the supplied encodings have the stated polynomial gate costs. It does not price their opaque oracles as free. With bounded mu and pmax, K=O(1+log[(1+aT)/epsilon]); any logarithmic drive/rate dependence in this cutoff remains paid. No favorable metric or practical constant is inferred for an arbitrary bath fit.
