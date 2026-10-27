# Joint Gaussian absorption and a finite DAG compiler

27 October 2026. Frozen sources and first-round results are unchanged.
This is a positive, acquired joint-law operation with an essential precision
condition. It does not establish the general polylogarithmic N687 target.

## Acquired interface

A mean routine is a finite program Q(c;xi) with s Gaussian vector seed slots
and a *known* scalar-slot vector v and radius r satisfying, for every seed,

    Q(c+r Delta;xi+v tensor Delta)=Q(c;xi).             (1)

The identity preserves actual source-query points. It is not a conditional
mean oracle. For example, n^{-1}sum_j g(c+r xi_j)+s xi_{n+1} has
v=(-1,...,-1,0), ||v||^2=n. Its n calls and Gaussian approximation error are
separate charges. The frozen R16 compiler supplies another explicit example.

An acquired record Y in (R^d)^k is within TV delta of N(m,C tensor I_d),
with unknown m and known positive C. Child i has center
c_i=b_i+sum_j a_ij m_j, gauge v_i, and radius r_i. Put K=H A, where block
i of H is v_i/r_i. Thus K^T K=A^T Gamma A,
Gamma=diag(||v_i||^2/r_i^2). No intended center c_i is evaluated.

## Theorem 1: retained-record absorption

If P_new=C^{-1}-K^T K>0, put C_new=P_new^{-1}. There is an implementation
evaluating each child once whose exact comparison joint law is

    N(m,C_new tensor I_d) tensor product_i Law(Q_i(c_i;G_i)),       (2)

with all G_i independent standard seeds, independent also of the retained
record. Approximate-input joint TV costs at most delta. If each standalone
child has uniform Gaussian TV error epsilon_i, those errors add once.

Implementation: take Cholesky C=LL^T, C_new=TT^T and

    B=[-T^{-1}L; K L],       B^T B=I.
    G ~ standard Gaussian with k+sum_i s_i slots,
    Xi=G-B(B^T G).
    Y_new=Y+T Xi_0,
    child_i=Q_i(b_i+sum_j a_ij Y_j;Xi_i).              (3)

All matrices and all arguments in (3) are available. No unobserved input
noise or unknown mean is needed. The projection is applied by two matrix
products, without forming an unknown covariance square root.

Proof: for exact input Y=m+L Z, define Eta=Xi-B Z. Equation (1) makes each
child equal Q_i(c_i;Eta_i), and Y_new=m+T Eta_0. Since Z and G are independent,
Eta is jointly Gaussian with covariance I-BB^T+BB^T=I. This proves (2) for
all measurable events. Apply the same Markov kernel to an input coupling
for the TV claim; tensorization bounds the independent child errors.

Within this specified linear Gaussian absorption interface, retaining
covariance C_tilde requires

    C_tilde^{-1} <= C^{-1}-K^T K.                     (4)

This is the Schur-complement condition for positive fresh seed covariance.
Equality is optimal in Loewner order within this interface; it is not an
information-theoretic optimum among all source-aware algorithms.

## Theorem 2: global DAG precision criterion

For a fixed acyclic circuit c_i=b_i+sum_{j<i}a_ij m_j, m_i=mean_i(c_i),
provide actual child routines Q_i with deterministic query caps q_i,
uniform standalone errors epsilon_i for N(mean_i(c),tau_i^2 I_d), and the
gauges above. Let A be strictly lower triangular, D=diag(tau_i^2), and
Gamma=diag(||v_i||^2/r_i^2). If

    P=D^{-1}-A^T Gamma A>0,                           (5)

then every Q_i need be evaluated only once. The final record has joint TV
error at most sum_i epsilon_i from N(m,P^{-1} tensor I_d). If

    w^T P^{-1} w <= sigma^2,                          (6)

return w^T Y plus an independent Gaussian with the remaining variance. Its
law approximates N(w^T m,sigma^2 I_d) with the same TV bound.

Proof: apply Theorem 1 before each append. Each read subtracts
Gamma_ii a_i a_i^T from old precision; appending the independent comparison
child adds tau_i^{-2} to a new diagonal slot. This gives (5) inductively.
Full positivity implies positivity at every intermediate stage, since each
intermediate precision is a principal block of P plus the PSD contributions
of future reads. TV contracts under the executed kernels and adds once.
Gaussian addition and linear postprocessing prove (6).

Resources: sum_i q_i source calls on every execution, not an independently
expanded tree. With N nodes and s_i seed slots, conservative extra arithmetic
is O(N^4+sum_i i^2 s_i+d sum_i(i+s_i)i), in addition to child arithmetic.
Storage can be O(d(N+max s_i)+N^2+N max s_i), plus child working storage.
All loops and matrix sizes are fixed before source observations. With a
strict precision margin, Cholesky and divisions require finite real
arithmetic. A finite-bit implementation needs a separate rounding budget.

The coefficients may be conditioned on external history independent of the
record noise. Choosing A from the observed record and then using a fixed
Gaussian comparison would invalidate this proof. This is a fixed affine
circuit reuse contract, not arbitrary conditioning on observed samples.

## Exact limitations and next application

For one parent variance tau^2 and one read a, feasibility is
a^2 tau^2 ||v_child||^2/r_child^2<1. After M identical reads, the retained
variance is tau^2/(1-M a^2 tau^2 ||v_child||^2/r_child^2). Thus precision is
spent additively and eventually exhausted. Extra output noise does not by
itself reduce a physical-query-preserving gauge.

In a DAG, output-only sinks have zero columns in A: their large final noise
does not enter A^T Gamma A. Internal nodes can use smaller noise. This is
essential when applying the theorem to R16, whose output/internal child
labels are different. The full source-dependent routine errors, gauge
sizes, derivative-stencil coefficients, recursion depth, and output noise
test remain to be proved together; writing (5) is not that proof.

The singular projection in (3) provides joint-law reuse. A compatible
external-center gauge and independent reserve require additional work.
The companion round2_reuse analysis now CONSTRUCTS both using known
query-preserving output responses. It retains a fixed reserve fraction
within DAG layers and repairs gauge/response nonorthogonality with one
unused seed slot, at a factor sqrt(2) in gauge norm and at most two in
guaranteed reserve precision per recursive promotion. These are paid costs.
AFFINE_ORACLE_NORMAL_FORM.md gives a second code-derived construction,
allowing a separately tracked known affine center response.

## Verification

The companion round2_reuse/check_block_absorption.py checks matrix identities
with exact rational arithmetic and executes projected-seed absorption on
nonlinear conservative vector black boxes. Every physical query is compared
pathwise with its effective-seed replay. The root normal-form script separately
verifies reserve extraction and compatible responses. Empirical moments are
not TV evidence. Theorem 1 first proves the complete product of standalone
child laws, before any Gaussian approximation is applied.
