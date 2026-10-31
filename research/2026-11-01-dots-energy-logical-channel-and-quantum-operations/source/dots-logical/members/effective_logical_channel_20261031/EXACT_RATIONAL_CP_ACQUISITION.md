# Executable rational acquisition of the localized effective qubit channel

Scope: known uniform zero-field open chain, finite positive rational Boltzmann ratio q with |(q-1)/(q+1)|<=1/40, H0=X, one localized coupling A_l=Z, time1, no controls in this executable fixture. The mathematical logical-channel theorem covers more, but this program does not claim to implement that full generality. The output is an exact CP/TP effective-channel representation with a finite-rate logical error certificate, not an executed quantum circuit or a physical experiment.

## 1. Actual input acquisition

Input is the succinct KNOWN PROGRAM (n,l,q), a rational physical rate lambda and rational target epsilon. It is not a length-n unknown table or samples from an unknown source. The uniform model globally certifies the row contraction kappa=19/20: with t=(q-1)/(q+1), interior absolute row sum is2|t|/(1+t^2)<=1/20 and boundary sum is|t|. A negative weak bond is allowed. Invalid size/site, nonpositive parameters, excessive bond strength and failed finite-rate admission are rejected.

The received theorem gives model error U/sqrt(lambda)+W/lambda with U=9440/361 and W=310400/6859. Code uses the integer floor of sqrt(lambda) as a LOWER bound in its denominator, so its numerical admission is conservative and exact-rational. If this bound exceeds epsilon/2, return ABORT. The bound is2 for lambda<1. No floating square-root comparison is used.

Allocate epsilon/4 to local coefficient truncation, epsilon/8 to effective-channel approximation, and reserve epsilon/8 for OPTIONAL actual quantum gate synthesis. A radius R is increased until8(1/20)^(R+1)/(19/20)<=epsilon/4, or until the whole physical chain is included, in which case the coefficient error is exactly zero. Acquire only the at most2R+1 nearby uniform factors. Solve the tridiagonal system (-M)v=C[:,l] in exact fractions and take D=v_l. The Thomas elimination pivots do not vanish: strict row diagonal dominance implies inductively that each eliminated pivot exceeds the magnitude of its remaining upper entry. Direct fraction arithmetic is implemented. This obtains the positive local effective covariance without a source-state table or preparation.

The coefficient solve and its bit complexity are polynomial in local radius and input bit length. The dependence on n for this uniform program is only its integer description/boundary comparisons; this is not a claim that arbitrary billion-entry source data can be inspected at constant cost. Radius is logarithmic in the requested coefficient accuracy. General local factors need their actual access and a separately paid global certificate.

## 2. Exact rational approximant with a complete-norm certificate

For this qubit the effective Schrödinger generator is

    L(rho)=-i[X,rho]+2D(Z rho Z-rho).

Its diamond norm is at most C=2+4D. Let eps_num=epsilon/8 and delta=eps_num/9. Choose a power of two N=2^s>=4C. Thus ||L/N||diamond<=1/4. Let

    E0=sum_(k=0)^K (L/N)^k/k!.

Choose K by the exact integer inequality

    e0=2/4^(K+1)<=delta/(4N).

The exponential Taylor remainder is at most e0 in diamond norm: the tail is bounded by exp(1/4)*(1/4)^(K+1)/(K+1)!<=2/4^(K+1). Every Taylor coefficient is rational complex in the supplied qubit basis. E0 preserves trace and Hermiticity EXACTLY, because L does and its constant term is the identity. Compute Ehat=(E0)^N by s exact rational squarings; no floating exponential is used.

Since the exact channel E=exp(L) has diamond norm one, telescoping products or the recursion e_(j+1)<=2e_j+e_j^2 gives

    ||Ehat-E||diamond <=(1+e0)^N-1
                         <=2N e0<=delta/2.

Here N e0<=delta/4<1/2. Ehat remains exactly trace- and Hermiticity-preserving, but it is NOT presumed CP.

For these weak, time1 localized fixtures D<=1/kappa, so C is bounded by an absolute constant and N<=32. K grows logarithmically with1/epsilon. Rational numerator/denominator lengths grow polynomially with input/coefficient bits and K (including K!); the finite squaring count does not hide an inverse-accuracy simulation loop. All of these actual fractions are serialized, not replaced by floating estimates.

## 3. Exact CP repair, with no unearned Choi gap or postselection

Use the UNNORMALIZED Choi convention

    J(E)_(2i+a,2j+b)=E_(a+2b,i+2j),

where E uses column vectorization. Trace preservation is Tr_output J=I_2. The exact rational Jhat is Hermitian and has this marginal exactly. Since ||Jhat-J(E)||op<=||Jhat-J(E)||1<=2||Ehat-E||diamond<=delta, Jhat>=-delta I_4.

Set

    Jcp=(Jhat+2delta I_4)/(1+4delta).

It is strictly positive, with eigenvalues at least delta/(1+4delta), and its output marginal is exactly I_2. Hence it defines a genuine CPTP map. Its distance from E is bounded without diagonalizing J:

    ||Ecp-E||diamond
       <= ||Ehat-E||diamond+8delta
       <=8.5delta<9delta=eps_num.

The terms8delta arise from the diamond norm2 of the map with Choi I_4 and the normalization correction4delta times a channel of norm one. The positive floor is a consequence of the deliberately added padding and the error certificate, not an assumed lower eigenvalue of the true channel.

Compute the four-by-four Hermitian LDL decomposition in exact rational arithmetic, Jcp=L diag(d_j) L dagger, with d_j>0 and L unit lower triangular. The code verifies both this identity and the TP marginal exactly. Define FOUR Kraus operators by

    K_j[a,i]=sqrt(d_j)*L[2i+a,j].

These are exact algebraic numbers and sum_j K_j dagger K_j=I_2. This is an ACTUAL CP channel representation, not a normalized postselection or merely a dense exponential asserted to be a channel.

## 4. Constructive finite gate interface, not an executed backend

Stack the four K_j into an8-by-2 isometry V mapping a qubit and two zero environment qubits to sum_j |j> K_j|input>. Exact TP establishes V dagger V=I. A deterministic small-dimensional unitary completion, followed by ordinary QR/two-level unitary synthesis, yields an8-by-8 circuit. Its dimension is fixed; no source configuration basis is enumerated.

To make precision explicit, allocate the reserved eps_gate=epsilon/8 to this optional compilation. Approximate the isometry/unitary completion in operator norm at most eps_gate/8, then approximate all elementary two-level rotations and their fixed three-qubit decomposition to total operator norm at most eps_gate/8. The resulting Stinespring error is at most eps_gate/4, so the output channel diamond error is at most eps_gate/2 (allowing remaining slack for numeric completion). Standard stable QR may pivot on a maximal entry; tiny pairs can be skipped only with a charged norm error, so no unpriced tiny pivot inversion is assumed. Exact algebraic entries can be evaluated to the needed absolute accuracy; their square-root tolerances are squared when necessary. With constant dimension the required arithmetic and angle bits are polynomial in certificate bit length and log(1/eps_gate). A conservative fixed number of two-level rotations, plus the ordinary paid one-/two-qubit decomposition and synthesis of each angle, suffices.

The Python prototype does NOT generate those quantum gates. It supplies and exactly verifies their finite isometry input. Runtime/gate claims must therefore distinguish classical CP acquisition from this constructive but unexecuted gate-synthesis step. The compiler does not count arbitrary external system controls for free; there are none in this executable fixture.

## 5. Final guarantee and verifier meanings

The exact CP artifact's logical-channel error is at most

    model_bound + coefficient_bound + eps_num.

After the optional paid gate synthesis it is at most that plus eps_gate, bounded by epsilon because the assigned budgets sum to epsilon. The mathematical receiver supplies arbitrary initial CQ correlations and, for the specific native geometric source/diagonal coupling, arbitrary initial quantum source correlations by invariant-algebra reduction. The final bath is discarded. This is not a retained-bath simulator, a jump/heat record, or a source-control certificate.

`verify_channel` checks only the exact4-by-4 Hermitian/TP/positive-LDL representation. It has strict shape, integer(not boolean), positive denominator and canonical-fraction checks; malformed objects returnFalse. It cannot certify source parameters or approximation accuracy. `verify_record` separately recomputes the known-program acquisition from the declared inputs and compares the COMPLETE deterministic record using recursive EXACT type-and-value comparison (so bool/float aliases cannot pass as integers), then checks CP. It rejects changed radii, coefficients and error assertions. Neither verifier certifies that a physical black box actually follows the declared known program. Exact large JSON integers must be parsed as arbitrary-precision integers, not IEEE doubles.

## 6. Reproducible checks and ordinary payoff

Run `python effective_logical_channel_20261031/test_effective_qubit.py`. The current83 assertions include exact CP/TP, positive LDL and reconstruction, coefficient locality against exact full solves, malformed/tampered records, failed finite-rate admission, and n=10^12/n=10^9 succinct-program cases. Floating Choi comparisons against SciPy expm are diagnostics only; the actual error certificate is the preceding rational norm proof.

A separate run

    python effective_logical_channel_20261031/acquire_effective_qubit.py \
      --n 1000000000 --site 500000000 --lambda 1000000000000 \
      --epsilon 1/10000 \
      --output effective_logical_channel_20261031/effective_billion_spin_certificate.json

produced a PASS with radius4 (nine local sites),389807bytes of exact rational/algebraic certificate, and approximately0.65seconds on this execution environment before the final verifier-only parser refinements. Timings are observations, not universal runtime guarantees. The analogous n16,lambda10^8,epsilon0.01 artifact uses radius2 (five sites),158572bytes, approximately0.24seconds. Current rerunnable checks record their own timings. No billion-site physical experiment, unknown-data acquisition or quantum hardware execution occurred.

This ordinary reduced method wins the specified logical task at its admitted rate/accuracy, rather than improving the old full-output simulator's gate ledger. It acquires the effective covariance and a certified CP channel directly. Its omissions are deliberate and priced by the model bound; at smaller rates or below that error floor, this certificate aborts. No novelty or superiority over equally informed ordinary model-reduction/dense-channel methods is claimed: those methods are precisely the constructive winner used here.
