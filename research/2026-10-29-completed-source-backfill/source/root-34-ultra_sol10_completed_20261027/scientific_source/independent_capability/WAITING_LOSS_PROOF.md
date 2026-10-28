# Finite spectral-shift acquisition for a recursively retained optical factory

This is a model-side acquisition algorithm. It compiles supplied source,
loss, detector and protocol data into the complete output state and full
source/time costs, without truncating the unbounded retry/waiting times.
It does not acquire a source, memory, experiment, efficient device, general
optimal control policy, or scientific priority. An independent bounded
ordinary-chain/phase-type derivation and check is recorded in
`../factory_independent/PROOF.md`:
literal n4 results agree exactly at lambda=.999,.99999,1, including shifted
PGF values. The phase-type derivation recovers the same spectral shifts.
Exact finite comparisons, the analytic construction and directed larger
acquisitions retain their respective scopes.

The ordinary comparator is the exact finite absorbing Markov chain on the
protocol stack and stored photon counts. That method already has no time
cutoff. The constructed application compresses that chain using the finite
pure-loss spectrum. Joint state/time transforms, memory-generator spectral
shifts and failure resummation are established methods; none is a new
principle here.

## 1. Exact interface, including failure and clock costs

A raw optical slot delivers the number-diagonal state

    rho=p0|0><0|+p1|1><1|+p2|2><2|,
    (p0,p1,p2)=(99/500,4/5,1/500).

Every occupied photon belongs to the same admitted optical internal mode.
No spectral distinguishability, higher source tail, coherent Fock off-diagonal
term or hidden source memory is assumed away by metrology: their absence is
an explicit supplied-model boundary. Source preparation takes one clock,
costs one raw source attempt and produces its photons at the clock end.
Source reset and delivery are included in that clock's interface.

For n=2^k, let F_n be the following fixed policy. F_1 prepares one raw slot.
F_n first prepares F_m, m=n/2; retains that left output; then independently
prepares F_m on the right. Every already stored photon independently survives
each clock with probability lambda. During the entire right preparation,
including all its failed restarts, the left state remains exposed to this
loss. Both completed children then undergo one fusion clock. That clock
includes pair storage loss, a balanced beamsplitter, bucket readout, discard
and restart latency. Ancestor-held photons also lose during every such clock.

Retain output port0 and measure port1 with an on/off detector of efficiency
D=19/20 and no dark clicks. For h photons at the herald port, the acceptance
probability is (1-D)^h. On a click, discard both children and restart THIS
F_n; retained ancestors continue waiting. On no click, return the retained
photon number. Source and fusion failures are all charged. No failure-state
recycling is used. The two supplied memory fixtures are lambda=999/1000 and
99999/100000. Uniform loss during a fusion commutes with its passive
beamsplitter, so pair loss may be placed just before that instantaneous
beamsplitter without changing the discrete-clock model.

The conditioned retained state is number diagonal, by total-phase covariance,
and has support 0,...,2n. Thus this quantum circuit has an exact classical
photon-number transition representation. That fact does not extend to
arbitrary coherent quantum factories.

## 2. Literal finite fusion kernel

For Fock inputs i,j, the balanced beamsplitter probability of k photons
in port0 and i+j-k in port1 is

    P(k|i,j)=k!(i+j-k)!/[i!j! 2^(i+j)]
              *[sum_r binom(i,r)binom(j,k-r)(-1)^(j-k+r)]².       (1)

Let K(l,j;r) be the unnormalized probability of no-click and r photons
returned, when l,j are ready before the fusion clock. Combining uniform
pair loss with the detector, an equivalent exact kernel is

    K(l,j;r)=sum_(k>=r) P(k|l,j) (1-D lambda)^(l+j-k)
                 binom(k,r)lambda^r(1-lambda)^(k-r).             (2)

Its row sum is the success probability, not one. It contains all false
no-clicks due to detector inefficiency and all pair loss during that clock.
The compiler generates (1)–(2) with rational arithmetic for rational inputs.
The independent ordinary-chain construction is asked to build the loss and
beamsplitter steps separately, rather than trust this collapsed kernel.

## 3. Joint state, source-count and completion-time PGFs

Define

    H_n(r;z,u)=E[1_(N_n=r) z^(T_n) u^(C_n)],

where N is output photon number, T the ENTIRE number of clocks and C the
ENTIRE number of raw source attempts, all before the first success of F_n.
This is a joint law, not a product of a state distribution and a waiting
distribution. In particular

    H_1(r;z,u)=p_r z u.

At a node n=2m, suppose the first child returned i photons. If the second
child takes t clocks, the retained first child has l survivors with

    binom(i,l)lambda^(lt)(1-lambda^t)^(i-l).

Average this EXACT binomial law against the second child's joint PGF by
expanding its final factor. Put

    B_m(j;i,l;z,u)=binom(i,l)
       *sum_(s=0)^(i-l) (-1)^s binom(i-l,s)
                   H_m(j;z lambda^(l+s),u).                    (3)

This is an exact finite spectral expansion of the waiting-loss channel.
It retains the correlation between the right child's output j, its source
cost, and its preparation time. Replacing the random waiting time by its
mean, or replacing this joint PGF by the product of its marginals, is not
this algorithm.

The success PGF for ONE complete attempt at F_n is

    A_n(r;z,u)=z sum_(i,j,l) H_m(i;z,u)
                          B_m(j;i,l;z,u) K(l,j;r).              (4)

The prefactor z charges the fusion clock. The total PGF of that attempt,
before selecting its herald outcome, is

    G_n(z,u)=z [sum_i H_m(i;z,u)]².

Therefore its failed-attempt PGF is F_n=G_n-sum_r A_n(r). Independent complete
restarts give the established renewal identity

    H_n(r;z,u)=A_n(r;z,u)/[1-F_n(z,u)].                        (5)

Equation (5) charges every failed preparation and fusion prefix. It does
not condition their costs away. The compiler carries the three components
H, partial_u H at u=1, and z partial_z H. Multiplication and division use
the product/quotient rule. At z=u=1 their sums give normalization, expected
raw source attempts and expected clocks. Weighted sums r*z partial_z H
give E[N T], so output/time covariance is acquired as well.
The code evaluates this probability vector and its first source/time
derivatives. It does not emit all coefficients of the unbounded joint
completion-time/source-count law; (3)–(5) specify that law implicitly.

Every node succeeds almost surely with finite moments. Indeed, immediately
before fusion there are at most 2n photons. The event that all survive that
clock and bunch into the retained port has probability at least

    s_n >= (lambda/2)^(2n)>0.                                (6)

The herald port is then exactly vacuum. This bound is valid even with a
perfect bucket detector. By induction each child has finite completion-time
moments; a geometrically bounded number of such attempts retains finite
moments. For 0<=z<=1 the denominator in (5) is also at least (6). No pole
is crossed by the acquisition.

## 4. Finite shift bound and actual compression target

For root acquisition at z=1, write every argument as z=lambda^e. At a node
of size n'=2m, (3) shifts e by l+s<=i<=2m=n'. Hence at descendant size m'
of a root n,

    0<=e<=n+n/2+...+2m'=2(n-m')<=2n-2<2n.                  (7)

All needed arguments belong to this finite set. There is no hidden cutoff
on T, retries, photon age or a rare waiting-time branch. Caching (m',e)
gives, for k=log2 n,

    R_n=sum_(m'=n,n/2,...,1) [2(n-m')+1]
       =(2n+1)k-2n+3

scalar-argument PGF nodes. Each node holds a vector of 2m'+1 values. The
total probability entries are

    V_n=[8n²+6n(k-1)+3k+7]/3.

For 0<lambda<1 these are the unpruned implementation's exact counts.
At lambda=1 all shift arguments coincide, and its cache collapses to one
node per level; the lossless control consequently uses fewer entries.

The implementation carries 3V_n entries including its two derivatives.
This excludes fusion kernels: their separate storage is
sum_(m'=n,n/2,...,2) (m'+1)²(2m'+1)=O(n³), and the literal beamsplitter
probability cache is also O(n³). Those costs are reported, not hidden behind
the much smaller PGF-node count. Straight contraction is a polynomial number
of arithmetic operations; the provided loops have a conservative O(n^6)
bound, not a claimed optimal exponent.

For comparison, the literal depth-first ordinary Markov chain has the
following count when every source weight is positive and 0<lambda,D<1:

    M_1=1,
    M_n=(n+1)²+(n+2)M_(n/2).

There are (n+1)² ready-fusion input pairs. While preparing the left child
there is one parent frame; while preparing the right child there are n+1
possible stored-left counts. Consequently M_2=13, M_4=103, M_8=1111,
M_16=20287 and M_32=690847 transient states. Its transition matrix and rewards
are already an exact ordinary solution with no time cutoff. The comparison
is about this explicit representation's size, not a lower bound against
factored, sparse or spectral ordinary phase-type solvers. Such a solver may
recover the same compression.

## 5. Precision and measured bit costs

Exact rational arithmetic need not have polynomial bit size just because
the scalar circuit is polynomial. The attained Fraction acquisitions have
maximum cached numerator/denominator sizes 1836/1833 bits at n4 and
32107/32101 bits at n8 (lambda999/1000). No larger exact-rational bit-size
claim is made from those two observations.

The larger implementation instead evaluates the rational circuit with
directed dyadic intervals. At fixed precision b, each endpoint is an integer
divided by 2^b. Addition/subtraction are exact; multiplication and division
use integer floor/ceiling at each operation. Every division checks that the
entire denominator interval excludes zero. Thus a returned interval is an
enclosure under ordinary integer-arithmetic correctness; it is not an
agreement-of-floats certificate. The separate files retain all endpoints,
interval widths, operation counts and maximum integer bit lengths.

Polynomial precision is sufficient for approximate evaluation of this
specific circuit class. One conservative argument is as follows. Let
q=lambda/2. Equation (6) bounds every reciprocal by q^(-2n). Recursive
source expectations obey C_n<=2C_(n/2)q^(-2n), hence
C_n<=n q^(-4n). Along every trajectory the number J of fusions is at most
the number C of source preparations minus one: a source creates one active
output, and each fusion removes at least one active output. Thus
T=C+J<=2C, and source and clock expectations are bounded by 2n q^(-4n).
Binomial absolute
coefficient sums in (3) are at most 3^(2n+1) times polynomial factors. Thus
all exact intermediate values and all division condition numbers are
bounded by exp(poly(n, input-bit-size)). The circuit has polynomially many
gates, and the add/multiply/divide derivatives on a sufficiently small
neighborhood have the same form of bound. Propagating absolute rounding
errors through this finite circuit therefore requires only
poly(n,input-bit-size)+O(log(1/epsilon)) bits for prescribed absolute output
error epsilon. This is an existence bound, not an optimized precision bound
or a statement that exact rational numerators stay small. The actual dyadic
acquisition supplies a posteriori widths at the attained finite precision.
Those widths cover arithmetic rounding under the exact supplied parameters;
they do not include physical parameter uncertainty or calibration error.

## 6. Scientific and physical limits

The decisive prior is [Kuzmin et al., npjQI5,115 (2019), SM E.2,
Eqs.19–25](https://arxiv.org/html/1905.00335v2): it defines a joint
density-matrix/completion-time distribution, propagates waiting-memory
decoherence through a Laplace-domain Liouvillian resolvent and resums all
failed mergings geometrically. The spectral shift behind (3), and the
renewal denominator (5), inherit this transform machinery. The detailed
[Kuzmin and Vasilyev, PRA103,032618 (2021), Sec.III.2,
Eqs.6–15](https://arxiv.org/html/2009.10415v1) explicitly derives the shifted
Laplace argument in Eq.7. Its documented linear-size nested recursion
replaces each newly generated segment's completion law by a Poisson process
of the same mean rate; the following approximation-validity paragraph
discusses that step. This factory implementation retains the exact nested
joint laws rather than making that replacement. That distinction is about
the stated implementations, not a limitation of the prior general method.

[Goodenough, Coopmans and Towsley, Quantum9,1744 (2025),
Secs.3–5](https://arxiv.org/html/2404.07146v5) additionally obtains exact
fidelity moments and distributions through generating functions for
swap-ASAP repeater chains, including a global cutoff policy. Exact
non-Monte-Carlo acquisition is therefore not a general advance here.
[Vinay and Kok, PRA99,042313 (2019)](https://doi.org/10.1103/PhysRevA.99.042313)
and [Shchukin, Schmidt and van Loock](https://arxiv.org/abs/1710.06214)
are further ordinary statistical/Markov comparators.

The acquired scope is the explicit application (1)–(5), bound (7), directed
evaluation and literal ordinary-chain comparison for this number-dependent,
state/time/source-correlated photon factory. An equally informed symbolic
or factored phase-type implementation may recover exactly this compression.
No separation from that strongest comparator, historical priority or new
photon-generation mechanism is established.

All source weights, same-mode support, storage survival, detector response,
deterministic clock lengths, reset, mode matching and instantaneous passive
step inside its clock must be measured or engineered before physical reuse.
Model inputs have not been acquired here. Different scheduling, cutoffs,
state recycling, multimode correlations, non-Markov storage or arbitrary
mode-dependent decay are not automatically covered. Common lambda and
finite Fock support are what make the integer shift set close. Replacing
them by a general collection of rates can enlarge the spectral set.

Large mean photon number or exact finite Fock cutoff does not certify a useful
approximate non-Gaussian computational resource. The constructed ideal
factory actually loses total Wigner-negative volume in the attained
examples, despite acquiring additional negative rings. No optimality,
material advantage, quantum-computing advantage, novelty clearance or
civilisation-changing capability is inferred.
