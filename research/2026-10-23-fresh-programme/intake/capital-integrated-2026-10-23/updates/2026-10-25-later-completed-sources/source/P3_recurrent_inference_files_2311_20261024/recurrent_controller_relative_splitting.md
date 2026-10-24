# A source-relative positive splitting certificate for a recurrent controller

New Pro3 companion theorem. Unlike the occupation construction, this result
does not require local generators in different controller phases to commute.
It produces a finite positive operator circuit with an all-input relative
certificate. It does not establish efficient generic contraction of that
circuit. No new executor or numerical results are claimed here.

## 1. Source and common reachability condition

An autonomous finite controller has generator C on m states. Its hidden
switches leave all leaf states unchanged. Given controller c, module i has
a finite silent generator Q_i(c), diagonal recorded killing D_i(c)>=0, and
killed generator A_i(c)=Q_i(c)-D_i(c). Total killing is additive. Conditional
on a controller path, the modules are independent up to the selected event.
A supplied nonnegative mark/reset operator J is applied at a fixed lag t>0;
its event row sums agree with the killing.

For each i, form Qmin_i by taking the minimum across controller phases of
each off-diagonal silent rate and choosing diagonal entries for zero row
sums. Require that its reachability relation equals the reachability
relation of the union of all Q_i(c) off-diagonal graphs. This can be checked
exactly on the local finite graphs. A common irreducible backbone suffices,
but irreducibility is not necessary.

Set

    v_i=max_(c,x) [qout_i(c,x)+d_i(c,x)-qminout_i(x)].

Then A_i(c)>=Qmin_i-v_i I entrywise. Every time-dependent propagator U_i
formed from these phases or their pointwise convex mixtures satisfies

    U_i(0,t)>=exp(-v_i t) exp(t Qmin_i),
    ||U_i(0,t)||_infinity<=1.                            (1)

The first inequality follows from positive variation of constants; the
second follows because each instantaneous generator is substochastic.
All such propagators have the same local support. Obtain a rational

    0<ell_i<=min over reachable (x,y) of
                exp(-v_i t) exp(t Qmin_i)(x,y).          (2)

Reachable graph paths and positive uniformization give a terminating local
obtaining procedure. Unreachable entries stay exactly zero. No minimum over
global configurations is evaluated.

This condition is substantive. If different phases provide different
essential paths, Qmin_i may fail the reachability test. The theorem then
does not apply, even though another source-relative construction may work.
The commuting occupation theorem does not need this common-backbone
condition and can admit a completely frozen phase.

## 2. The positive grid operator

For an integer N>=1 let h=t/N. Define

    S_h=diag_c (tensor_i exp(h A_i(c))),
    T_h=exp(h C) tensor I,
    P_N=(S_h T_h)^N.                                    (3)

The exact survival operator is P_t=exp(tG), where G is the full coupled
controller/local killed generator. Formula (3) is the usual positive
Lie product construction, written without expanding G. Its path
interpretation runs the controller exactly and freezes each local generator
within a cell at the controller state at that cell's left endpoint.

The marked approximation is K_N=P_N J. All terms are nonnegative, and no
event-density row is normalized before the input law is applied.

## 3. Pathwise relative sensitivity to changing the controller path

Define the locally computable constants

    Delta_i=max_(c,d) ||A_i(c)-A_i(d)||_infinity,
    L=sum_i Delta_i/ell_i.                              (4)

Consider two controller schedules that disagree for total duration a.
Interpolate pointwise between their local generators. The derivative of
the corresponding local propagator with respect to interpolation parameter
theta is

    integral_0^t U_theta(0,s) [A_actual(s)-A_other(s)]
                                  U_theta(s,t) ds.

Its infinity norm is at most Delta_i a, using substochasticity of the two
propagators. By (1)-(2), every supported entry along the interpolation is
at least ell_i. Integrating its logarithmic derivative proves

    exp(-Delta_i a/ell_i) U_other(x,y)
      <= U_actual(x,y)
      <= exp(Delta_i a/ell_i) U_other(x,y).              (5)

Multiplying local entries gives the analogous bound exp(+-La) for each
global input/output local-state pair, without forming a global matrix.

Let J_t be the actual number of controller switches on [0,t]. A controller
path and its left-grid-frozen version disagree for duration at most h J_t.
Consequently, if W and W_N are their conditional local transition/survival
weights for a supported global pair,

    exp(-theta J_t) W_N <= W <= exp(theta J_t) W_N,
    theta=Lh.                                          (6)

This includes arbitrarily many controller switches. No switch-count tail
has been discarded.

## 4. Controlling the jump-count tilt after local endpoint selection

Choose a rational zeta>1. Let C_[zeta] have the same diagonal as C and
off-diagonal entries zeta C_cd. Its exponential is a positive jump-count
generating operator:

    (exp(t C_[zeta]))_cd
      =E_c[zeta^(J_t) 1_(C_t=d)].                       (7)

Indeed multiplying each controller path density by zeta^(J_t) multiplies
each off-diagonal jump factor by zeta and leaves all waiting factors
unchanged. Summing those path terms proves (7).

On controller-reachable pairs, define

    M_zeta=max_(c,d reachable)
              (exp(t C_[zeta]))_cd/(exp(t C))_cd,
    B=[log M_zeta+sum_i log(1/ell_i)]/log zeta.          (8)

The maximum is over the small controller, and finite local/bridge lower
certificates make it obtainable. M_zeta>=1 and B>=0. Both matrix
exponentials in (8) are finite positive source calculations; the tilted
one is not a stochastic transition matrix.

Fix a controller bridge from c to d and the supported local input/output
pair. Reweight this bridge by W_N and normalize. Since

    product_i ell_i<=W_N<=1,

the tilted conditional moment obeys

    E_(bridge,W_N)[zeta^(J_t)]
        <=M_zeta/product_i ell_i.                       (9)

For 0<=theta<=log zeta, concavity of x^(theta/log zeta) gives

    E[exp(theta J_t)]<=exp(theta B).

Also Jensen's inequality and
E[J_t]<=log(E[zeta^(J_t)])/log zeta give

    E[exp(-theta J_t)]>=exp(-theta B).

These two bounds hold under the selected bridge in (9). Thus even local
endpoint evidence cannot force an unbounded unaccounted jump-count moment:
the source support lower bounds pay for its maximum possible reweighting.

## 5. All-input relative operator theorem and explicit depth

Integrating (6) under the selected bridge and using (9) proves

    exp(-theta B) P_N <= P_t <= exp(theta B) P_N,        (10)

entrywise whenever theta=Lt/N<=log zeta. Controller or leaf structural
zeros are shared. Positive multiplication by J gives the same sandwich
for K_N and the true first-event density K_t=P_tJ.

For any supplied nonnegative initial joint law with nonzero marked output
mass, the conditional output-TV error is therefore at most

    tanh(Lt B/(2N)).                                    (11)

For a target 0<epsilon<1, one sufficient integer depth is

    N>=max(1, Lt/log zeta, Lt B/[2 atanh(epsilon)]),     (12)

rounding upward. If L=0, local generators do not change across the controller
and the split is exact. Rational zeta=2 is a simple default; optimizing it
against the small-controller moment bound is permitted but not required.

For bounded local data, fixed local dimension and fixed horizon, L is at
most linear in the number of modules and B has at most a linear local
contribution. The conservative depth is then O(n^2/epsilon), in addition
to controller and source conditioning constants. This is a depth bound,
not an efficient-contraction theorem.

The proof uses a controller jump-count exponential moment, rather than an
absolute Poisson tail converted through a selected record probability.
Jump-count bridge calculations themselves are established machinery.

## 6. Evaluation errors and repeated application

All factors in (3) can be obtained with local/finite-controller positive
entrywise enclosures. Suppose a retained one-cell operator L_h satisfies

    L_h<=S_h T_h<=c_h L_h.

Positivity implies L_h^N<=P_N<=c_h^N L_h^N. Combining with (10) gives
an overall spread at most

    exp(2LtB/N) c_h^N.

Local numerical precision must account for this N-fold factor; numerical
error is not free because the same cell is reused. A relative input
certificate multiplies this spread. Every later approximate kernel
application incurs its own spread, while common exact later positive
operations preserve the already obtained one.

The physical controller endpoint and all required local variables must be
retained. An input may already contain arbitrary controller/leaf or
historical-count correlations. The certificate is valid for that input;
its compact execution is a separate representation issue. This theorem
does not identify an unknown biological entrance distribution.

## 7. Storage versus contraction: the precise limitation

The repeated-cell circuit stores O(m sum_i |E_i|^2+m^2) scalar entries plus
the repetition count and certificates. Its full expansion over controller
grid histories can nevertheless contain m^(N+1) product-operator terms.
There is no claim that generic filtering, product queries or subsequent
compression can be performed in time polynomial in this circuit description.

For example a direct exact evaluation on a positive product-mixture input
can enumerate the controller grid histories while maintaining local rows.
That avoids enumerating global leaf configurations but has exponential
dependence on N. Tensor contraction can choose another order and exploit
additional structure, but arbitrary repeated-controller interactions can
produce large ranks. Any truncation or compression needs a new certificate.

Compact arithmetic circuits for structured propagators are already
available from established polynomial/squaring or time-ordered methods.
Small circuit storage alone is not a distinction over those incumbents.
The use of this theorem is a transparent source-local relative certificate
for the positive grid construction. The recurrent commuting-occupation
theorem supplies a stronger explicit positive-product width and controlled
contractions for its admitted class.

## 8. Primary comparison and status

Hobolth and Stone, *Simulation from endpoint-conditioned, continuous-time
Markov chains on a finite state space* (2009), explicitly treats bridge
uniformization and endpoint-conditioned jump-count weights:
https://arxiv.org/pdf/0910.1683

Celikkaya and Shelton, *Deterministic Anytime Inference for Stochastic
Continuous-Time Markov Processes* (2014), provides the full time-ordered
operator expansion and structured local Kronecker evaluation:
https://proceedings.mlr.press/v32/celikkaya14.pdf

Shao, Gao and Xue, *Aggressively truncated Taylor series method for accurate
computation of exponentials of essentially nonnegative matrices*, already
obtains componentwise relative finite-matrix exponential error bounds and
positive interval algorithms:
https://webapps.cs.umu.se/uminf/reports/2012/004/part1.pdf

Positive operator comparison and projective filtering error propagation are
likewise established, as detailed in `conditioning_stable_entrance.md`.
This new derivation makes no historical priority, architecture-necessity or
comparative runtime claim. Existing programmes receive the same compact
source, controller calculation, tensor representations and retention rights.
The theorem and obtaining procedure are proved here; no new implementation,
run or expanded numerical comparison is claimed.
