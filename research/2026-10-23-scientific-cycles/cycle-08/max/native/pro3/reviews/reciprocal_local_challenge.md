# Focused independent challenge: reciprocal-proposal local energy

Reviewer: `/root/reciprocal_energy_challenge`. Scientific date: 22 October
2026, Australia/Brisbane. This is a bounded check of the principal's proposed
local weighted-energy operation. It is not a duplicate audit of the whole
sampling programme, nor a claim to have proved the full new phase law.

## Scope and verdict

**ACCEPT the local finite lemma as formulated below, without repair.**
The reverse-proposal Jensen representation does replace the use of proposal
symmetry. The actual rejection diagonal must be kept. In the interior case
the exact scalar coefficient is at most the former F(c), and at theta=eta
the complete old weighted-boundary coefficient is retained.

The main Cycle7 source did not yet exist when this check began. This document
binds the complete formulas below, the task received from the principal, and
the exact predecessor sources. A later review must bind any assembled main
source if acceptance of that exact file is claimed. No full-return,
one-information-budget or matching-lower assertion is independently audited
here beyond the stated algebraic interface.

Read source sections:

- Cycle6 `GLOBAL_BOUNDARY_THEOREM.md`, Sections 2-3 (and the surrounding
  finite-certificate definitions): 21,990 bytes, SHA256
  `b381b6a052c309ea66716014820573040b6038ed83de0f19b112754d52233c3c`.
- Selected Cycle5 `CRITICAL_ENDPOINT_THEOREM.md`, Section 3 and the entropy
  preliminaries preceding it: 18,790 bytes, SHA256
  `4a459d8ee78253564a849b3033abc25e548224dc695fbb819cd9860e3a5c9014`.

These are read-only predecessor inputs. Their accepted symmetric theorems
are not reopened.

## 1. Exact local statement

Let q,pi be positive probability vectors on a finite labelled space. Let Q
be row-stochastic with reciprocal off-diagonal support. No symmetry,
stationarity with respect to q, column-sum bound, degree bound or minimum
transition probability is assumed. All quantities stay fixed during a run.
For x!=y with Q_xy>0 write

    r_xy = q_y Q_yx / (q_x Q_xy),
    t_xy = pi_y Q_yx / (pi_x Q_xy),
    a_xy = min(1,r_xy^eta) min(1,t_xy/r_xy^eta),
    L_xy = Q_xy a_xy,
    L_xx = 1 - sum_{y!=x} Q_xy a_xy.

Here 0<eta<1. On absent edges let L_xy=0; no undefined ratio is evaluated.
Let A,E be disjoint sets and S=A union E. Retain the ACTUAL L entries from
rows A into S, kill other outflow, and make rows E absorbing. Denote this
substochastic matrix by L^E. No killed row is renormalized.

Take 0<theta<=eta, theta<1, p=1/(1-theta), D=diag(q^theta) on S and
T=D L^E D^-1. The principal's additional restriction theta<=1/2 is allowed
but is not needed for the local Jensen calculation. For w>=1 set

    E_w(v) = sum_A |v_x|^p + w sum_E |v_x|^p,
    tau = p(1-theta/eta),
    H_w = sup_{0<z<=1} (w z^tau-z).

Because 0<eta<1 and 0<theta<=eta, one has 0<=tau<1. When tau=0 the
supremum is w, approached as z decreases to zero. This convention avoids
an undefined 0^0 and does not assert that a strictly positive finite edge
attains that supremum.

Then for every nonnegative row vector v (indeed, by absolute values, every
real row vector),

    E_w(vT) <= 2^(p-1) [ (1+H_w) sum_A |v_x|^p
                                      + w sum_E |v_x|^p ].       (L)

Empty A or E needs no limiting argument: the relevant missing terms are
zero. The formula is support-uniform.

## 2. Reverse-proposal Jensen weights

At each output y in S choose auxiliary nonnegative coefficients B_xy:

- x in A, x!=y: B_xy=Q_yx;
- x=y in A: B_xx=L_xx;
- x=y in E: B_xx=1;
- every other entry: zero.

Whenever B_xy=0, the corresponding T_xy=0. The only potentially delicate
off-diagonal case is covered exactly by reciprocal support. Diagonal zero
terms are omitted rather than divided by zero.

Since Q is row-stochastic,

    sum_{x in S} B_xy <= 1 + sum_{x!=y} Q_yx <= 2.

This is a bound using the OUTGOING row of Q at y. It is not a false
counting-column bound on Q or T. Weighted Jensen therefore gives

    |sum_x v_x T_xy|^p
      <= 2^(p-1) sum_{x:B_xy>0} |v_x|^p T_xy^p/B_xy^(p-1).

For a retained off-diagonal x in A, the powered coefficient is exactly

    T_xy^p / B_xy^(p-1)
      = Q_xy^p a_xy^p (q_x/q_y)^(theta p) / Q_yx^(p-1)
      = Q_xy a_xy^p r_xy^(-theta p),                (C)

using p-1=theta p. The diagonal coefficient is the original L_xx for x
in A, and one on E. It is not a replaced or inflated rejection probability.

## 3. Scalar defect and real diagonal

Multiplying the output Jensen bound by its energy weight omega_y (one on A,
w on E) and summing over y gives an input coefficient, for x in A,

    L_xx + sum_{y in S,y!=x} omega_y Q_xy a_xy^p r_xy^(-theta p).

Use the ACTUAL identity L_xx=1-sum_{y!=x} Q_xy a_xy. The displayed
coefficient is at most

    1 + sum_{y in S,y!=x} Q_xy
             [w a_xy^p r_xy^(-theta p)-a_xy].       (D)

Outflow into the killed complement contributes a nonpositive term and may
be dropped. No return is removed from the eventual sampler; this is only
the auxiliary first-hit operator.

For r>=1 and 0<=a<=1,

    w a^p r^(-theta p)-a <= (w-1)a <= w-1 <= H_w.

For 0<r<1, the permitted interval is 0<=a<=r^eta. The function
f(a)=w a^p r^(-theta p)-a is convex, so its maximum on that interval
is at a=0 or a=r^eta. At the latter endpoint, with z=r^eta,

    f(r^eta)=w r^(p(eta-theta))-r^eta=w z^tau-z<=H_w.

Also H_w>=w-1>=0 by evaluating z=1. Hence every bracket in (D) is at
most H_w, and sum_{y!=x}Q_xy<=1 proves the A coefficient bound 1+H_w.
An input x in E has only its absorbing diagonal, giving exactly w. This
completes (L).

The second acceptance factor was bounded by one where helpful, but not
discarded from the actual diagonal. This distinction is essential. The
relaxation proves an upper; it does not create an admitted adverse chain.

## 4. Exact interior and endpoint interfaces

For w=1 let

    c_eff = 1-tau = theta(1-eta)/(eta(1-theta)).

If theta<eta then 0<c_eff<1, and elementary maximization gives

    H_1 = F(c_eff),
    F(c)=c(1-c)^((1-c)/c).

If theta=c eta with 0<c<1, then

    c_eff=c(1-eta)/(1-c eta) <= c.

Since F(c)=sup_{0<z<=1}(z^(1-c)-z) is increasing in c,

    H_1 <= F(c).

Consequently the former interior LOCAL p-energy bound, with 1+F(c),
survives unchanged throughout 0<eta<1 and theta=c eta. This is an
inequality, not an illicit assertion that c_eff equals c at finite eta.

At theta=eta (hence eta<1), tau=0 and H_w=w for every w>=1. The
local bound is exactly

    E_w(vT) <= 2^(p-1)[(1+w)sum_A |v_x|^p+w sum_E |v_x|^p],

the whole weighted endpoint coefficient needed by Cycle6. It is obtained
directly from this finite calculation, not by substituting c=1 in an
unproved strict-c estimate.

Optional closed scalar form, not needed by the principal's old constants:
for 0<tau<1,

    H_w = w(1-tau)(w tau)^(tau/(1-tau))   if w tau<=1,
          w-1                            if w tau>=1.

The formulas agree at equality. At tau=0, H_w=w separately. This
general-w refinement is a valid scalar bound, not a new phase-law claim.

## 5. Mixture interface checked algebraically

The existing independence proposal component does not involve Q. Its own
q-density Jensen calculation gives the weighted coefficient b+w e on A
and w on E, with the same prefactor 2^(p-1), provided A={pi/q<h}
and E is a subset of its complement. Combining that accepted operation
with (L) by convexity of the actual lazy mixture gives

    E_w(v D P^E D^-1) <= Gamma_{theta,w}(e) E_w(v),
    Gamma_{theta,w}(e)
      = 1/2 + 2^(p-1)/2
          [1 + (beta H_w-alpha(1-b))_+ + alpha w e].

The transformed initial energy of q1_A is exactly b. Thus the same
weighted Holder step gives first-hit mass at most

    (b/w)^(1-theta) e^theta Gamma_{theta,w}(e)^(N(1-theta)).

This is a finite absorption interface only. The principal must still
retain the original chain after hits, bound the accumulated Gamma power,
use one KL information budget, and identify a matching admitted lower.
No asymptotic theorem follows merely from this displayed norm estimate.

## 6. Challenges that were resolved and remaining scope

1. Arbitrary Q can have arbitrarily large counting columns. Direct reuse of
   the old counting-column proof is invalid. The explicit auxiliary B above
   repairs the representation rather than assuming a missing Q property.
2. Pointwise T_xy<=Q_xy^(1-eta)Q_yx^eta at theta=eta is insufficient by
   itself. The proof uses powered coefficients and subtracts actual accepted
   outflow through L_xx.
3. Negative weighted defects for r>=1 were not assumed: for w>1 they can
   be positive, but they are bounded by w-1 and hence H_w.
4. The weighted endpoint supremum w may not be attained by a finite positive
   edge. Attainment is unnecessary for the upper, and no lower is inferred.
5. No target normalization, target-table access, empirical KL inference,
   adapted within-run kernel or free reverse-proposal oracle is introduced.

Internal acceptance of this local calculation does not certify historical
originality, formal verification, external mathematical acceptance, a useful
implementation or a sampling speedup. Ordinary IMH remains the comparator.

## Observed resources

First observed tool clock: 2026-10-22 02:23:37 UTC (12:23:37 Brisbane).
No numerical experiment, old scientific suite, network query, paid resource,
target sampler run or unrelated owner work was used. Two source excerpts were
read; hashes of both whole predecessor files were computed. Model inference,
token count, total discovery cost and monetary cost are unknown. A separate
receipt records this source's exact final byte identity and completion clock.
