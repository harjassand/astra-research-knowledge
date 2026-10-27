# Shared Gaussian records: an acquired reuse compiler

27 October 2026. This extends the scalar, independent-copy absorption identity
in frozen source S1, Section 6. It preserves that source and the preceding
construction. It is a finite, positive compiler theorem, not a proof of the
general polylogarithmic Gaussian-mean target or a historical novelty claim.

The purpose is precise: a completed approximate Gaussian output can be reused
as a noisy affine center while retaining old outputs. No derivative, mean,
conditional distribution, fitted coefficient, or current-law operation is
queried. Correlated fresh Gaussian seeds pay explicitly for the reuse.

## 1. Inputs that are actually required

Every vector has physical dimension d. A Gaussian seed slot is a d-vector.
For i=1,...,k suppose an already acquired finite program Q_i(c;xi_i), with
q_i seed slots, has the following metadata proved from its source code:

* a deterministic every-execution original-value-query cap N_i and arithmetic
  cap A_i;
* a deterministic nonzero scale r_i and deterministic vector v_i in R^{q_i};
* the exact pathwise gauge identity, for all inputs and seeds,

      Q_i(c+r_i h; xi_i+v_i tensor h)=Q_i(c;xi_i);             (1)

* under independent standard Gaussian seed slots, a standalone law within
  epsilon_i in TV of N(m_i(c), S_i^2 I_d), uniformly over c.

The function m_i is an analysis target, not an oracle. Usually
m_i(c)=E g(c+r_i G), but the theorem does not use this formula. Program Q_i
can contain earlier acquired corrections; its entire actual law is used.
All its original-value calls, coefficient acquisition and finite arithmetic
are included in N_i,A_i. Identity (1) must also preserve every queried
physical point when source-level reuse is claimed.

There is an existing record R=(R_1,...,R_m), with a proved joint contract

 TV(Law(R), N(m,C tensor I_d)) <= epsilon_in,                  (2)

where m is a deterministic vector of unknown analysis means and C is a
known positive-definite m by m scalar covariance matrix. This is a JOINT law
contract. Individually approximately Gaussian marginals are insufficient.
The record is available; its latent standardized Gaussian error is not.

Fix a known k by m coefficient matrix A and known offsets b_i, and define
the intended exact centers c_i=b_i+sum_j A_ij m_j. Coefficients, scales,
gauges, offsets and covariance transforms must not depend on the unknown
Gaussian record error or on observed record values. Conditioning on an
independent, already fixed outer anchor is permitted if all contracts are
uniform and hold conditionally on that anchor.

## 2. Precision is the resource spent by a read

Let H be the block-column matrix with column i equal to v_i/r_i in child
block i and zero in all other child blocks. Thus

      H^T H = diag(||v_i||^2/r_i^2).

Let J be a chosen positive-definite m by m slack matrix and suppose

      P_new = C^{-1} - A^T H^T H A - J  > 0.                 (3)

Set C_new=P_new^{-1}, choose deterministic factors L L^T=C and
T T^T=C_new, and form the (m+sum q_i) by m matrix

                  D = [ -T^{-1} L ; H A L ].                 (4)

Then D^T D = I-L^T J L < I. In particular I-DD^T is positive definite.
Choose its ordinary scalar Cholesky factor P:

                      P P^T=I-DD^T.                         (5)

All matrices in (3)-(5) are known scalar metadata. Cholesky uses only
finitely many real arithmetic operations and positive square roots. No
matrix of derivatives or source-dependent fitted matrix is acquired.

The inequality with J=0 is enough for a positive semidefinite square root
and the law identity below. Strict slack is retained here so P^{-1} exists,
conditioning is controlled, and the resulting program's own gauge can be
computed. The slack is not silently free: it subtracts further precision.

## 3. The actual algorithm

Draw M=m+sum q_i fresh independent standard Gaussian d-vector slots G.
Compute xi=P G, divide xi into an old-record block xi_0 of m slots and
child blocks xi_i, and output

       R_new,old = R + T xi_0,
       R_new,i   = Q_i(b_i+sum_j A_ij R_j; xi_i).             (6)

These are finite positive randomized programs. The child calls may use
correlated or nonstandard seeds internally in (6); their pathwise gauge,
not an assumption about their marginal input seeds, justifies this use.
Neither m, c_i, nor the old standardized error is evaluated.

### Exact full-joint-law identity for an ideal input

For analysis replace R by m+L Z, Z standard Gaussian and independent of G.
By (1), the child output in (6) is exactly

        Q_i(c_i; (P G)_i-(H A L Z)_i).

The retained old record is exactly

        m+T[(P G)_0+T^{-1}L Z].

Together the effective seeds are eta=P G-D Z. They are centered jointly
Gaussian with covariance P P^T+D D^T=I. Thus every effective seed slot is
independent standard Gaussian. Consequently the retained record is exactly
N(m,C_new tensor I_d), and is independent of every standalone child output;
all standalone child outputs are mutually independent. This proves the
entire law, not merely a covariance or moment identity. Nonlinearity and
non-Gaussianity of the child programs cause no approximation in this step.

### Approximate inputs and approximate children

Apply the same Markov kernel (6) to the actual and ideal input records.
Total variation contracts under a Markov kernel. Then use the product-law
bound for the independent standalone children. The result is

 TV(Law(R_new),
    N((m,m_1(c_1),...,m_k(c_k)),
      blockdiag(C_new,S_1^2,...,S_k^2) tensor I_d))
       <= epsilon_in + sum_i epsilon_i.                     (7)

This is an actual-output reuse contract. It requires no derivative, Stein
kernel, covariance oracle, conditional Gaussian law of a child, or proof
that the realized output map is conservative. The old record's complete
error is charged once, irrespective of how many children read it in this
layer. Repeated layers add their standalone error budgets.

For a W2 input contract and fixed-seed child center Lipschitz constants L_i,
the same coupling gives the alternative bound

 E_new <= sqrt(1+||diag(L_i) A||op^2) E_in
                    +(sum_i e_i^2)^{1/2},                  (8)

where e_i are uniform standalone W2 errors and the metric on the record
space is its ordinary product Euclidean norm. No independence of the
implemented errors is asserted or needed.

## 4. Repeated layers compile a DAG without copying its old subtrees

At each layer keep the current known covariance C, spend the precision
A^T diag(||v_i||^2/r_i^2) A plus the chosen slack J, append the new diagonal
child noise block, and continue. Every previously computed mean record is
retained with enlarged, explicitly tracked covariance. Its underlying source
program is not rerun merely because several later nodes read it.

The resulting joint TV error is at most the initial error plus the sum of
all new child error budgets. Any final deterministic affine output has its
corresponding Gaussian target and no larger TV error. If the final affine
weights are w, its known noise variance is w^T C w. A final independent
Gaussian reserve can raise this to a prescribed variance only when
w^T C w does not exceed that variance. This is a paid output-noise condition.

The closure holds for predeclared affine mean circuits. A coefficient chosen
from the observed noisy record generally depends on Z; then eta need not be
Gaussian and (7) cannot be invoked. A data-dependent algorithm needs a new
argument rather than treating the metadata as fixed after observing it.

## 5. The resulting program can retain a computable gauge

Suppose the incoming record program has a known external-center gauge w
at external scale r. Suppose b_i(x+Delta)-b_i(x)=kappa_i Delta, with fixed
scalar kappa_i, while A and all covariance metadata are fixed. Shift the
incoming program's seeds by its existing gauge, so its output R remains
identical. In the fresh slots shift G by

      P^{-1} [0 ; H kappa] Delta.                            (9)

Each child then has precisely the shift required by (1), and all retained
records and all physical value-query locations remain unchanged. Therefore
the assembled program has explicitly computable external gauge vector

      w_new = [ w ; r P^{-1}[0 ; H kappa] ],                 (10)

in units Delta/r. If lambda_min(P P^T)>=eta>0,

 ||w_new||^2 <= ||w||^2 + r^2 ||H kappa||^2/eta.             (11)

Thus gauge closure is constructive and its growth is charged. If a child
does not already possess (1), this compiler does not invent that property.
In particular the preceding variational Newton correction is not shown
here to have a finite gauge-compatible acquisition program.

## 5A. A complete affine DAG has one explicit precision matrix

Suppose logical node i has intended mean

       m_i=m_i(b_i+sum_{j<i} a_ij m_j),

where the notation on the right denotes the target function of child i.
Let A=(a_ij) be strictly lower triangular, D=diag(S_i^2), and
Gamma=diag(||v_i||^2/r_i^2). In the zero-slack version, append each new
node's independent noise precision and subtract each read's precision.
The final exact covariance is

              C^{-1}=D^{-1}-A^T Gamma A.                    (13)

If (13) is positive definite, every intermediate precision matrix is
positive: it is a principal submatrix of the final precision plus the
positive semidefinite costs of reads that have not occurred yet. The
singular fresh-seed map at a stage with no slack is especially simple.
In (4) D_stage has orthonormal columns, so

       xi=(I-D_stage D_stage^T) G,
       eta=xi-D_stage Z

has exactly identity covariance and is Gaussian. This implements the
full-joint-law compiler without an unacquired square root. The singular
version alone does not prove an external gauge for the complete program;
Section 5's positive slack gives that stronger metadata contract.

The final full-joint-law TV error is at most sum_i epsilon_i, and every
logical child is run once. No ancestor is rerun merely to provide a center.
Positive slack subtracts an additional explicitly accumulated known
precision matrix from (13).

For W2, a componentwise error recurrence is sharper than (8). At the instant
node i is created, couple its actual input cloud to the ideal Gaussian cloud.
Retaining an old record leaves its actual-minus-ideal error unchanged. The
new child center error is at most sum_j |a_ij| e_j in L2. After the exact
absorption identity, independently couple each ideal standalone child law
to its target Gaussian. Hence valid coordinate error bounds satisfy

       e_i <= e_i,standalone + L_i sum_{j<i}|a_ij|e_j.        (14)

In vector notation, with B=diag(L_i)|A|,

       e <= (I-B)^{-1} e_standalone,
       W2(final affine output, ideal affine output)
                  <= |w|^T (I-B)^{-1} e_standalone.           (15)

The inverse is the finite sum I+B+...+B^{n-1}; no spectral assumption or
solver oracle is needed. Formula (15) retains attenuation of errors at
internal nodes by downstream Lipschitz coefficients. It can therefore use
larger internal error budgets than the uniform full-cloud TV contract.

### Read nodes and output-only sinks have different noise costs

An output-only sink has zero column in A. Therefore it contributes no
term to A^T Gamma A, its row and column in the precision matrix (13) have
no off-diagonal entries, and its final Gaussian noise remains exactly its
standalone S_i^2. Internal nodes that will be read require smaller noise;
output-only sinks can have the large noise allowed by the final output
budget. Giving every node the same small noise is an unnecessary loss.

For n nodes, suppose ||v_i||<=V, r_i>=r_min, each row of |A| has sum at
most A0, and all internal child noises are at most tau. Then

 ||Gamma^{1/2} A D^{1/2}||op
       <= (V/r_min) sqrt(n) A0 tau.                         (16)

Here columns of sinks vanish, and ||A||op<=sqrt(n)A0 follows from the
row-sum bound and the corresponding n A0 column-sum bound. Choosing
tau<=r_min/(2 V sqrt(n) A0) makes (13) positive with a 3/4 margin in the
D^{-1} metric. More precise matrix norms can improve this sufficient bound.

For the S1 metadata, inserting r_min=r delta^t, V=delta^{-t},
A0=B(r/S)delta^{-4t-10w}, and an actual total-node bound
n<=B delta^{-10w}, gives an allowed internal noise of order
S delta^{6t+15w}/B^{3/2}. Thus the internal smallness label loses at most
6t+15w, up to the explicit coefficient constants; sinks retain their
improving radius factor delta^t. This is a conditional application of S1's
metadata, not a new audit of its entire fixed-exponent proof. It shows that
the DAG method does not automatically destroy S1's crucial distinction
between output and internal transitions. Uniform high-order constants,
the actual node count, gauge growth, and a polylogarithmic total recursion
still have to be proved before claiming the general target.

## 5B. Constructed reserve closure removes the singular-gauge caveat

There is a stronger complete closure for programs with a supplied independent
final Gaussian reserve, as in S1. The reserve must be part of the actual
program, not a property inferred from approximately Gaussian output laws.

For a program with seed array z, a query-preserving output response is a
known scalar matrix W such that, for every output displacement u,

      R(z+W u)=R(z)+u,

and every physical source query is unchanged. If W has full column rank,
Gaussian orthogonal decomposition constructs the exact independent reserve

      R(z)=R(z-W(W^T W)^{-1}W^T z)
                         +(W^T W)^{-1}W^T z.                (17)

The second term is N(0,(W^TW)^{-1} tensor I_d), independent of the first
term and of every physical query. This is an exact source-code identity.

Assume the old cloud has an acquired response W_old satisfying

                 W_old^T W_old <= rho^{-1} C^{-1},

for a fixed rho in (0,1]. Assume each child has a response W_i from its
untouched final reserve, satisfying

      W_i^T W_i <= rho^{-1} S_i^{-2},
      (v_i/r_i)^T W_i=0.                                    (18)

The last condition says that the child's center gauge does not touch that
reserve. A literal fresh reserve sqrt(rho) S_i G_res supplies (18), with
all metadata explicitly known.

Use the zero-slack projector layer. Write P0=C^{-1}, P1=C_new^{-1}, and
Q=A^T H^T H A, so P1=P0-Q. For a desired displacement u of the retained
old outputs, define

      r=C P1 u,
      q=[ T^{-1}(u-r) ; H A r ].                             (19)

One checks D^T q=0. Shift old raw seeds by W_old r and new raw Gaussian
seeds G by q. Since (I-DD^T)q=q, the retained output changes by
r+T q_0=u. Every new child center shifts by A r and its seeds shift by
H A r, so the child's gauge leaves its output and all queries unchanged.
Thus (19) is an acquired response for retained outputs. Desired displacements
of the new child outputs use their W_i in the corresponding fresh blocks;
these vectors are orthogonal to D, to q, and to each other by (18).

The exact energy identity is

      ||q||^2=u^T(P1-P1 C P1)u.

The old-seed response energy is at most rho^{-1} u^T P1 C P1 u. Since
0<P1<=C^{-1}, one has P1 C P1<=P1. Therefore the assembled response satisfies

 W_new^T W_new <= rho^{-1}
                     blockdiag(C_new^{-1},S_1^{-2},...,S_k^{-2}). (20)

All matrices defining W_new are known and computed in (19). Hence (17)
constructs an exact query-free Gaussian reserve of at least rho times the
complete target covariance at every DAG layer. The fraction rho is retained;
it is not multiplied once per layer. This proves the helpful property from
the finite Gaussian seed representation rather than assuming it from TV.

### External-center gauge with the projector

Suppose the incoming cloud also has a known external-center gauge V_old,
in units of a physical displacement Delta (no scale normalization here),
and the new deterministic offsets have derivative kappa_i Delta. Let

      Gamma=H^T H,
      a=A^T Gamma kappa,
      r=-C a Delta,
      q=[ -T^{-1}r ; H kappa Delta+H A r ].                  (21)

Again D^T q=0. Shift old raw seeds by V_old Delta+W_old r and new raw
seeds by q. The incoming gauge first preserves all its queries and outputs;
its output response then adds r. Formula (21) cancels every new center
shift while preserving all final retained and new outputs. This constructs
the new gauge, without inverting the singular projector.

For a scalar external gauge vector, put s=kappa^T Gamma kappa and
t=a^T C a<=s. The fresh energy is exactly s-t, and the old output-response
energy is at most t/rho. The triangle inequality therefore gives

        ||V_new|| <= ||V_old|| + sqrt(s/rho).                (22)

For H layers, the total increment is at most
sqrt((H/rho) sum_i ||v_i||^2 kappa_i^2/r_i^2). The desired original scale
can be restored by multiplying V by that scale. This is a charged gauge
bound with a fixed reserve fraction; no positive precision slack is needed.

The orthogonality in (18) is required for each standalone child when it is
plugged into the circuit. The finished parent can obtain the same metadata
for a later recursive role by retaining its designated independent final
reserve, as S1 already does. The internally constructed response (20) is
enough for record retention inside the DAG, and need not be orthogonal to
the parent's external-center gauge.

This reserve construction alone does not turn a post-reserve W2 bound into
a pre-reserve W2 bound. For a final TV smoothing argument one still needs
the stated pre-reserve coupling contract, or a separately paid fresh final
reserve, or the full-TV contract (7). Deconvolution of an approximate law
is not being assumed.

## 5C. Orthogonal metadata can be constructed without changing the output

External-gauge orthogonality to the constructed response W_new is not
automatic. It must not be assumed when a whole compiled record or a selected
internal record is promoted to a child program. A simple affine-query
example is Q(x;z1,z2)=g(x+z1)+z1+z2: V=(-1,1) is its output-preserving
center gauge and W=(0,1) is its output response, but V^T W=1.

There is nevertheless an exact, zero-query repair for a scalar external
center coefficient (one common d-vector center). Add one unused standard
Gaussian d-vector slot to the seed list. The actual program ignores it.
For any t>0 and any nonzero gauge vector V, define

       V_aug = [ V ; t ||V|| ],
       W_aug = [ W ; -V^T W/(t ||V||) ].                    (23)

Both original pathwise identities continue to hold: the new slot affects
neither an output nor a query. Moreover

       V_aug^T W_aug=0,
       ||V_aug||^2=(1+t^2)||V||^2,
       W_aug^T W_aug
          =W^T W + W^T V V^T W/(t^2 ||V||^2)
          <=(1+t^{-2}) W^T W.                               (24)

Thus t=1 makes the gauge norm at most sqrt(2) times larger and preserves
at least one half of the previously constructed reserve covariance. If
V=0, no augmentation is needed. Formula (17), applied to W_aug, constructs
the orthogonal Gaussian reserve explicitly. This is not an extra output
noise draw or a changed distribution: the new raw seed is unused by the
actual sampler, and only the analytical seed-space decomposition changes.

All metadata in (23) are computed by known scalar linear algebra. The cost
is one Gaussian d-vector slot, O(number_of_seed_slots times number_of_outputs)
scalar arithmetic to compute the cross Gram matrix, and zero source calls.
It applies to arbitrary acquired programs with the two pathwise interfaces,
not only affine value-query programs.

Consequently the following representation class is constructively closed:
finite actual value-query programs, a complete Gaussian-law error contract,
a computed center gauge, and a computed query-free output response. A
promotion can restore the orthogonality required by (18) through (23).
After H promotions with t=1 the guaranteed reserve fraction is at least
rho_initial/2^H, and the direct augmentation contribution to gauge growth
is at most 2^{H/2}. The complete gauge recurrence also contains (22), whose
1/sqrt(rho) costs must be charged. These isolated factors do not by
themselves prove a polylogarithmic total bound. When a parent already has
an untouched final reserve, as S1 does, using that reserve avoids this loss.

For output-only sinks the inherited child reserve directions are untouched
by later reads, and the external gauge remains orthogonal to those specific
directions. A final affine combination can therefore use their weighted
independent reserves, together with any explicitly paid final reserve.
Promoting a retained internal record requires the general check or repair.

## 6. Every-execution computation and queries

One layer calls each child once, for exactly the sum of its prescribed caps
(or at most that sum if the children themselves have fixed caps), and makes
no new source query to retain old records. It uses M new Gaussian d-vector
slots. Safe scalar preprocessing cost is O(M^3+m^3), storage O(M^2+m^2),
and vector arithmetic cost O(d M^2+d k m), plus the full child costs.
Gauge construction uses triangular solves with the same known P. This is
polynomial in record and seed count and d; it is not an uncharged PDE solve
or covariance acquisition. Lower-rank implementations may be cheaper.

Every query cap survives changed seed distributions because it is a cap on
EVERY child execution. Strict known slack controls matrix conditioning. If
finite bits are used, approximation of these matrices and all child programs
needs a separate perturbation budget, and the final comparison must be to
a commonly rounded Gaussian target. This note proves the exact-real form.

## 7. Exact limitation: sharing consumes precision

With one old record of variance s^2 and k children whose normalized gauge
and center-read coefficients have a common product h=a||v||/r, retention
at new variance t^2 requires

                    1/t^2 + k h^2 < 1/s^2.                 (12)

It follows that k h^2 s^2<1 is necessary for this Gaussian absorption lift.
Keeping the old variance unchanged (t=s) cannot absorb even one nonzero
read. More generally the matrix condition (3) exactly identifies the
precision spent by each shared layer. This is a failure of the particular
lift when its capacity is exhausted, not a lower bound for the target.

Independent copied-center trees in S1 avoid shared-read correlations by
paying additional calls. This compiler is an alternative that pays a known
joint precision budget. It can reduce a repeated subtree to one stored
record when (3) stays positive and the final noise budget closes. Neither
tradeoff uniformly dominates the other.

## 8. Exact remaining obligation for the general Gaussian-mean target

To close the target using this instrument one must supply actual child
programs with small standalone Gaussian-law error, computed gauges, and
complete original-value costs, and a circuit for which (3), (11), and the
final target-noise budget close with polylogarithmically many total original
queries and polynomial arithmetic. This note supplies the previously
unproved sharing/reuse operation under those explicit metadata contracts.
It does not supply the general acquired superlinear correction or show that
the old fixed-exponent circuit satisfies a polylogarithmic precision budget.
