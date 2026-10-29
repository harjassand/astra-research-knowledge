# Independent review: acquired preparation and common-equilibrium access

29 October 2026. Review of new root constructions; no predecessor re-audit,
physical operation or acquired stationary reset is claimed.

## Versions and decision

* OPERATIONAL_PREPARATION_AFTER_ACQUISITION.md:
  4ae954de97fddb911ba2151e5153a028afe9a6665b5c27b99bd2a4a70c25553d.
* COMMON_EQUILIBRIUM_OPERATION_ACCESS.md:
  822cbf7c581bc18c16d21765b3a55760ecf5b19678329f51275396b66ecea69f.

Exact reviewed copies are preserved under port_frontier/reviewed_versions/.

**Decision:** Both constructions are valid at their stated interfaces. The
uniform-state exact reset theorem, the old-record joint guarantee, the finite
residual/density-qualified bound, and the common-equilibrium acquisition
corollary survive the detailed checks below. No missing factor was found in
their principal displayed bounds.

The finite-data claim remains conditional on exact closure for the uniform-state
theorem, or on the explicit density/error qualifications for the approximate
theorem. A fitted near-zero residual is not promoted to a pointwise reset.

## 1. Uniform pointwise evaluation and event closure

Let F(x)=(f_1(x),...,f_r(x)), 0<=f_i<=1 and G>=gI. For v=Fc,

    |v(x)| <= ||F(x)||_2 ||c||_2
            <=sqrt(r/g)||v||_(L2(pi)) = C ||v||_2.

This is a statement for the declared feature representatives at every state.
On a countable full-support space, equality in L2 identifies every value, so
native conditional effects and their representatives agree pointwise. On a
continuous space, a purely L2 construction establishes only pi-essential
equality; singular initial states require the additional pointwise premise
already stated in the root note. It is correct not to silently cover Dirac
preparations at pi-null points.

For every cylinder event of an admitted service program, exact operation and
label closure put its conditional effect f_A(x)=P_x(A) in V. The extension to
arbitrary events is justified as follows. Finite linear combinations of cylinder
indicators approximate bounded path functions in the relevant measure space;
conditional expectation is an L2 contraction. Since V is finite-dimensional,
it is L2 closed. A monotone-class argument therefore places every event effect
in V modulo pi. Countable full support gives equality at every x. The same
argument applies after fixing external randomization and a history-selected
service policy, then averaging. Thus the use of ALL service events is justified,
not merely a consequence for a selected finite test set.

Every event effect has 0<=f_A<=1, so

    ||f_A-pi(f_A)||_2^2 <=1/4.

This uniform variance bound is what permits the horizon-independent reset
guarantee once the entire service algebra is exactly closed.

## 2. Exact contraction gives the stated reset

Because W preserves pi and1, its invariant finite V decomposes as
span{1} plus V_0, and W preserves V_0. Hence

    ||W^m(f-pi f)||_2<=kappa^m ||f-pi f||_2.

Apply the evaluation bound and the preceding event variance estimate:

    sup_x |W^m f_A(x)-pi f_A| <= (C/2)kappa^m.

The SAME bound holds for every event A and every admitted program, so taking
their supremum gives TV, clipped at1, exactly as in equations (3)--(4).
No hidden-state total-variation contraction is used. A frozen hidden spectator
therefore does not invalidate the result when it lies outside the service
effect space.

The norm in (1) is an operator/singular-value norm in the acquired Gram metric.
For a nonreversible product word it should not be replaced by the largest
eigenvalue modulus without an additional norm bound. The note uses the norm
correctly. For an actual reversible baseline wait, the restricted centered
spectral gap supplies the exponential norm bound as stated.

The iteration count is correct for 0<kappa<1, with ceiling and truncation at
zero. kappa=0 requires at most one execution of the word. A finite numerical
certificate for kappa<1 and g>0 can be acquired conditionally on the exact
service/word closure; it does not certify that exact closure from noisy data.

## 3. Old records, policies, and discarded reset instruments

Let R be an arbitrary retained old classical record. Conditional on R=r, the
initial hidden distribution may be arbitrary and correlated with r. For any
joint event A(r,service record), fix r and its prescribed service policy; its
effect f_(A,r) lies in V and takes values in[0,1]. Uniformity in x gives

    |int mu_r(dx) W^m f_(A,r)(x)-pi f_(A,r)|<=epsilon_reset.

Integrating over the SAME distribution of R proves the joint-TV statement.
The reference uses the same r-selected policy, so it does not claim that
outputs become independent of deliberate uses of R. It removes extra
dependence through the source's hidden starting state.

The operational qualification about reset records is essential and correctly
stated. An averaged clock kernel can contract by averaging over a variable
whose retained realized value selects a noncontracting conditional operation.
New reset observations, elapsed-time records, randomization keys or correlated
apparatus variables cannot be retained outside the theorem and then supplied
to the service controller. Either they are absent/discarded from the permitted
service interface, or their joint instrument must be included in the acquired
representation and in the contraction statement. A deterministic-duration
word avoids an extra random-clock conditioning issue but does not automatically
remove state measurements or apparatus memory.

Switching still must implement the actual kernel word without an unmodeled
kick. The theorem executes a real word with actual durations and costs; it
does not substitute a contracting matrix for a physical operation. The initial
stationary acquisition remains separately supplied. The result is a reuse
operation, not a bootstrap of its own original calibration conditions.

## 4. Approximate projection preparation

Write H=L2(pi). Q_0 is self-adjoint nonpositive, P is orthogonal with1 in V,
A_0=P Q_0P|V, and d_0=||(I-P)Q_0P||. The standard Duhamel identity gives

    ||exp(tQ_0)P-P exp(tA_0)||<=t d_0,

since both semigroups are contractions. Taking adjoints yields the root's
needed version ||P exp(tQ_0)-exp(tA_0)P||<=t d_0. There is no omitted
adjoint-weight factor because this is the reversible BASELINE norm.

For a density g_0 with pi(g_0)=1 and ||g_0||_2<=K,

    ||g_0-1||_2<=sqrt(K^2-1),
    ||g_t||_2<=K,       g_t=exp(tQ_0)g_0.

Because both full and compressed evolutions preserve1 and the centered
compression has gap lambda,

    ||P(g_t-1)||_2
       <=[exp(-lambda t)+t d_0]sqrt(K^2-1).

Thus equation (6) is correct. The compression gap is an acquired finite
operator property after numerical and inverse-compression uncertainty; it is
not being substituted for a full microscopic mixing rate.

## 5. Approximate complete-service comparison

Let E_dyn(T)=k^2 T D exp((k-1)JT). The physical service started from g_t differs
from its signed true-compression prediction by at most K E_dyn(T) in L1.
The physical service started from pi differs from its signed prediction by at
most E_dyn(T). Their projected initial functionals differ by dual norm at most

    delta_t=[exp(-lambda t)+t d_0]sqrt(K^2-1).

The path-word sum for the difference of those initial functionals is bounded
by k delta_t exp((k-1)JT). Triangle inequality gives exactly

    (K+1)E_dyn(T)+k delta_t exp((k-1)JT).

The endpoints are both genuine physical service laws, so half this L1 bound
is a valid TV ceiling. No positivity of the intermediate signed predictor is
needed for the triangle inequality. Conditional old-record guarantees require
the corresponding density bound for the actual conditional initial laws, or
an explicitly integrated joint bound, as the root note states.

The minimizer of exp(-lambda t)+t d_0 is correctly given by
t=lambda^-1 log(lambda/d_0) when 0<d_0<lambda, with value
(d_0/lambda)[1+log(lambda/d_0)]. If d_0>=lambda the minimum of this particular
upper bound occurs at t=0. This does not assert that longer physical waiting
is harmful; it correctly says this certificate no longer improves.

## 6. Common-equilibrium chronological moments

For each actual kernel T_j self-adjoint in the SAME L2(pi), every word O in
T_j and visible projectors has adjoint equal to the reverse word. Therefore

    <O_i1,T O_l1>_pi = <1,reverse(O_i) T O_l1>_pi.

The right side is a single actual chronological event probability. It is in
[0,1] regardless of feature depth, because every factor is a genuine Markov
kernel or a visible indicator multiplication. This removes the multiplicative
importance weights in the differing-equilibrium construction; it does not
remove physical word length or preparation costs.

G, K_j and D_j are symmetric. Their upper triangles require at most
(1+2s)r(r+1)/2 moment settings, as claimed. Hoeffding actually permits the
smaller sufficient bound N>=(2eta^2)^-1 log(2M_entries/delta); the root's
N>=2eta^-2 log(2M_entries/delta) is conservative and valid. No within-trial
independence of feature readings is needed; the assumption is independent
baseline-prepared trials for each setting.

Two successive physical calls produce T_j^2 and hence the conditional-feature
Gram <T_j f_i,T_j f_l>. Squaring one stochastic future outcome gives a different
object and is correctly excluded. Zero Schur residual directly certifies
T_j-invariance without a generator inverse, rate cap or positive spectrum.
The resulting execution interface consists of those calls and endpoint
observations; it does not silently recover trajectories or discarded clocks.

The self-adjoint detailed-balance qualification is also correct. A kinetic
system reversible only under an odd parity involution is not automatically
covered by reversal of the chronological operation word. Its required parity
access would be an additional operation, as the corollary explicitly states.

## 7. An optional stronger construction found during review

The full hidden condition pi W=pi can be weakened. Exact V closure only needs
the acquired constant action and the centered reduced map. A separate note,
PREDICTIVE_PREPARATION_WITHOUT_HIDDEN_STATIONARITY.md, develops this fully:

    ell=pi|V, P0 f=f-ell(f)1,
    A=P0 W|V0, b=ell W|V0,
    ||A||<=kappa<1, ||b||<=delta.

The actual word then prepares a unique operational functional
ell_*=ell+b(I-A)^-1P0, regardless of hidden starting state. It need not prepare
a microscopic stationary distribution. Its full future-record reset error is
at most (1/2)[sqrt(r/g)+delta/(1-kappa)]kappa^m. Relative to the original
baseline service, an additional acquired stationary-bias floor is retained.

This is a NEW construction, not part of the reviewed root version or an
automatic extension to approximate closure. It is presented separately for
root's scientific choice and new load-bearing review.
