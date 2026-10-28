# What the certificate actually costs

The acquired operation has two separate inputs: an exactly declared thermal
amplitude and a verified small multiplicative residual. Its finite-ring
readout is implemented. The tested small-collar residual is not small. The
following costs describe how the certificate can be acquired or rejected;
they do not count an unperformed wider-collar computation as completed.

For n sites, block size b>=2ell+2, and m=n/b seams, the source-local
expansional has dimension5^(2ell). One outside-edge commutator acts on
2ell+1 physical sites. SU(2) invariance reduces its complete operator norm
to M=0, with dimensions19 and381 for ell1 andell2. All integer-spin irreps
are still represented. Actual ell1/ell2 local matrices, inverse products,
norm proposals and the alternative QBP factor/temperature derivative were
computed; only the symbolic ell1 failure and the separately described
interval arithmetic are claimed as certificates.

A residual integral need not be treated as a free numerical oracle. For the
raw C(s)=exp(-s L/2)exp(s K/2), put kappa=20ell-15. The known local bond
spectral interval [-6,4] gives

    ||C(s)|| ||C(s)^-1|| <= exp(kappa s).

For D(s)=C(s) h_out C(s)^-1, differentiating gives
D'=[-L/2+C K C^-1/2,D]. Since ||h_out||<=6,
||L||<=6(2ell-1), and ||K||<=6(2ell-2), it follows that

    ||D'(s)|| <= M_ell(beta),
    M_ell(beta)=36[(2ell-1)exp(kappa beta)
                    +(2ell-2)exp(2kappa beta)].

Thus mu(s)=||h_out-D(s)|| is Lipschitz with this fully explicit constant.
At rational midpoints, finite local exponentials can be enclosed by matrix
Taylor series over the source field Q(sqrt6), with a paid remainder
exp(x)x^(K+1)/(K+1)!. The analytic inverse is a second finite exponential
product; no supplied large-system inverse is required. An entrywise interval
matrix gives a rigorous norm upper by sqrt(||R||_1||R||_infinity), or a
verified rational norm-factorization can sharpen it. These are finite
arithmetic operations; their accuracy is an acquisition cost.

With bins of width h and upper values mu_j, midpoint integration gives

    integral_0^beta mu(s)ds <= h sum_j mu_j + beta h M_ell(beta)/4.

For a target global residual nu*, reserving half its budget for quadrature
requires h<=2nu*/(m beta M_ell(beta)), hence at least
m beta^2 M_ell(beta)/(2nu*) bins with this simple Lipschitz rule. Each local
matrix evaluation has ordinary dense cost of order K D^3 arithmetic
operations and D^2 storage before using sparsity/symmetry, where
D=dim(M0 on2ell+1 sites). A higher-order validated quadrature may improve
this deliberately conservative cost; no such speedup is assumed here.

At the first rung nu* is below9.31e-8. Even the conservative ell1 midpoint
rule would require roughly6e11 bins on ring512. The exact lower bound in
PROOF section6 rejects that amplitude immediately instead of pretending
to execute this expensive calibration. The numerical local norm samples
alone are not substituted for an integral certificate.

The readout has a separate, unavoidable cost. For the actual b4/ell1 source
the open block is625-dimensional, the one-copy transfer is25-dimensional,
and the squared-density transfer is625-dimensional. Positive repeated
squaring computes their full cyclic traces in O(log m) dense products,
without discarding any eigenmodes. The implemented positive kernels make
each multiplication/addition count explicit and the clipped-entry tails
are charged. Local exponentials are degree80 positive Taylor polynomials,
scaled to norm argument at most2, followed by squaring. This is a small
computation on the available host, as measured in the replay record.

For general ell the squared-density transfer dimension is5^(4ell). Dense
storage is8*5^(8ell) bytes, and a naive dense product costs O(5^(12ell)).
At ell2, storage alone is1,220,703,125,000 bytes. That computation was not
attempted on the shared16GiB host. A future structured method must acquire
its own full closed-trace error/tail bound. The present scalar error
compiler does not supply that contraction.

The bounded QBP collar avoids the raw expansional's very large norm, but its
temperature derivative contributes an inside residual as well as the outside
commutator. The actual coupled ODE was executed. The resulting ell2 residual
is still substantial and numerical; neither bounded factor norm nor a local
Gibbs identity certifies the required global residual.

The same already-computed block transfers give genuine coarse target bounds
by ordinary ALT/Golden--Thompson inequalities, with restored absolute scales.
These require no successful residual. Their true log-purity widths at beta3/4
are about112.88 for ring256 and225.75 for ring512. They therefore do not pay
the requested first-rung accuracy of roughly7.44e-7.

The strongest ordinary BS-CMI/MED/thermal-MPO algorithms can exploit different
state/environment structure and are not excluded by these costs or failures.
Their quantitative marginals, effective interactions, temperature constants
and finite-loop corrections must be acquired at the same precision. No
complete practical advantage over those methods is established here.
