# A finite-bit quantized full-law kinetic receiver

29 October 2026. New implementation and construction, independent whole
review pending. This closes an output-format gate for the direct complex
dual; it does not extend that dual to velocity-dependent collision rates.
No historical novelty or practical all-solver advantage is claimed.

## Exact output contract

Input time t is a nonnegative rational. The initial distribution is the
equal mixture of two centered three-dimensional Gaussian distributions,
with rational covariance matrices

    Sigma1=diag(1,21/20,11/10),
    Sigma2=[[26/25,1/25,0],[1/25,26/25,0],[0,0,21/20]].

They lie between I and (11/10)I. The nonlinear Maxwell collision uses
independent velocities and one of the four signed x/y quarter-turn
rotations, each with probability 1/4, with A=(I+R)/2 and B=(I-R)/2.
Its rate is one. The output is three INTEGERS

    (floor(4V1),floor(4V2),floor(4V3)), V distributed as f_t.

The law is exact conditional on an iid fair-bit input and the stated
outward-ball arithmetic contract. A seeded PRNG execution is a diagnostic
of that program, not a proof that a deterministic seed supplies iid bits.
Neither a discrete law nor this finite output is asserted TV-close to the
unrounded continuous distribution. The mathematical target is its exact
pushforward under the specified quantizer.

## Preserved ideal-real operation

The accepted direct-complex proof and the accepted finite-kernel contraction
give the following ideal-real operation. Use a=1,b=11/10,c=21/20,h=1/20,
C=b^(3/2). Propose v from N(0,bI), draw xi from N(0,I), put
z=xi-i v/b, and draw q from Poisson(h||z||^2/2). The finite-kernel marked
dual supplies a bounded complex H_q(z/||z||,t), of modulus at most one.
Then

    W/C=Re[(-1)^q exp(i(c/b-1)xi dot v) H_q]

is bounded by one, and its conditional expectation is f_t(v)/(C g_b(v)).
The p-coin with probability (1-W/C)/2 therefore has mean p satisfying
2p <=1-ell(v)/C, where ell=exp[-||v||^2(1-1/b)/2]>0.
Huber's established linear Bernoulli factory produces a 2p-coin; accept
the proposal on output zero. This gives f_t exactly, with expected C
proposals. The ordinary expected-query bound is finite when b<2a.

For q>=2 the dual draws an exponential waiting time, selects one of the
four rational rotations, and allocates q marks by Binomial(q,U),
U=||A^T z||^2. Only occupied children are normalized. The finite-kernel
second-moment certificate gives separation probability at least 1/4;
the genealogical tree has at most 2q-1 conceptual blocks and a geometric
number of raw iterations per block. At q=1 the 24-state exact positive
Bernstein program replaces the long-time collision history. It uses four
independent exp(-left/4) coins and one rational categorical column. The
remaining time here is a computable REAL, generally not rational; this
implementation evaluates those coins by certified comparisons, rather
than silently calling the earlier rational-time-only component.

## A persistent ball program, without numerical branch substitutions

quantized.py represents each random real once in a lazy expression DAG.
Each Uniform owns a persistent binary prefix; future refinement adds bits
to it and never resamples the value. All distributional branch decisions
use exact integer comparisons or strict separation of outward Arb bounds.
An unresolved comparison doubles precision. No midpoint, probability
clipping, matrix renormalization or numerical sign is used to decide it.

Normal draws invert the Gaussian CDF by rational bracket bisection, using
Arb erf enclosures. Poisson draws use a persistent uniform compared to the
convergent positive cumulative probabilities. Exponential waits use
-log(U). Finite rotations and categorical choices use fair bits and exact
integers. Huber parameters, its geometric coins and integer powers are
computed in the same ball DAG. Normalized complex marks use transpose
quadratics and Hermitian squared norms, as required by the complex proof.

Generic Arb ** is NOT used for integer powers: in the installed version it
is a logarithmic power and gives NaN on a zero-straddling real interval,
even for a square. Actual finite-kernel projections have exact zero
components, so this prevented convergence. Exponentiation by integer
multiplication repairs that domain issue on every real/complex ball.
FAIL_CLOSED_DEBUG/TRACE/OPERANDS.json and RUNNING_STACK.txt preserve the
failed diagnostic. No output from that interrupted run is claimed.

Independent review then found an additional literal-program gate: recursive
DAG evaluation could hit Python's fixed recursion limit on a finite,
positive-probability trajectory. Arithmetic evaluation now uses an explicit
postorder stack and dependency nodes. ITERATIVE_DEPTH_CONTROL.json evaluates
a chain of depth10000 at the unchanged recursion limit1000. Normal-CDF leaf
comparisons have constant call depth. POST_POWER_EXECUTION.json preserves
the pre-stack successful run. The same fixed-seed full consumer replay
produced IDENTICAL bins, acquired bits, comparisons and other operation
counts after the stack repair; execution time changed as reported below.

## Almost-sure termination, and the cost claim not yet earned

Every finite ideal trajectory only requires finitely many random draws.
The Poisson rate is finite almost surely. The marked genealogy and Huber
factory have finite expected ideal-real operation counts under this input
and contrast, hence terminate almost surely. Each comparison against a
fresh uniform has equality probability zero, including probabilities zero
or one. Normal inversion only compares its original uniform to countably
many fixed rational-point Gaussian CDF values. Factory threshold equalities
or its epsilon clamp occur on countably many radial level sets of a
continuous Gaussian proposal and also have probability zero.

For any such finite trajectory, all required divisions, logarithms and
occupied-child normalizations have nonzero denominators/positive arguments.
Their outward enclosures converge as requested precision increases. The
integer-power repair covers exact zero components without dividing by
them. Finally f_t is a Gaussian covariance mixture with covariance at least
I, so it assigns zero mass to the quantizer boundaries. Refinement settles
all three floors almost surely. Adaptive allocation of unused iid bits is
the ordinary lazy-product source construction.

These statements prove almost-sure termination of the discrete receiver.
They DO NOT alone prove finite expected total bit/arithmetic work. That
stronger operational gate remains UNKNOWN pending a paid conditioning and
precision analysis. In particular an observed precision maximum is not a
uniform theoretical precision bound. A debugging precision limit, when
enabled, raises an explicit failure and never returns a replacement sample;
the production execution uses no such limit.

## Actual execution and ordinary alternatives

EXECUTION.json records one fixed-seed run of 200 outputs at each t=0,3,10^6.
They completed in 1.640,1.345,1.379 seconds after imports, using 403482,
325551,338081 acquired bits respectively and maximum Arb context 192 bits.
The t=3 and 10^6 cases actually traversed q>=2 collision branches (32 and
52 rotations). These finite paths exercise the repaired implementation;
they do not establish the ideal iid law, expected-cost theorem, or accuracy
by Monte Carlo.

consume.py also implements ordinary Wild recursion using the SAME rational
initial covariance catalog, kernel, iid-bit interface and integer-bin
output. Its 200 outputs took .115 seconds at t=0 and 2.621 at t=3, the
latter using 3907 initial leaves. There is no Wild execution at t=10^6;
its exp(t) expected leaf count is a property of that ordinary genealogy,
not a lower bound for every alternative solver.

An equally informed approximate-output alternative receives the explicit
equilibrium bound in EQUILIBRIUM_CONTROL.md. It can use a single Gaussian
at large t for a PAID TV tolerance, rather than an exact transient tree.
That different accuracy contract can be much cheaper. No general practical
advantage follows from the displayed exact-output timing comparison.

Scientific source inputs: root_complex_collision/PROOF.md,
root_rotation_kernel/PROOF.md, t_collision_operation/SECOND_MOMENT_KERNEL.md,
and the exact independently checked finite singleton program with SHA256
a4c77e5ddd4ef37582263692b41d7cc36ec21c7ca9ea67aa8cada8cd3d8bbdcb.
Arb/acb outward arithmetic: python-flint 0.9.0, official documentation at
https://python-flint.readthedocs.io/en/stable/arb.html and acb.html.
Ordinary exact random variates and lazy real comparisons are prior tools;
see Karney arXiv:1303.6257v2 and the already acquired Huber factory source.
