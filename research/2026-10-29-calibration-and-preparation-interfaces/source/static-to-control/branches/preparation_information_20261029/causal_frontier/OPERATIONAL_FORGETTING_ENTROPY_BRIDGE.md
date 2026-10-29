# Operational forgetting can replace hidden mixing for a sustained time-arrow claim

29 October 2026. Complementary construction for Astra P1. Ordinary proof below;
independent review has not yet been completed. This is a path-reversal-divergence
theorem. Heat or thermodynamic entropy requires the actual reversal and a
separately justified reservoir/local-detailed-balance interpretation.

## 1. Scientific point and boundary

Microscopic forgetting is stronger than the consequence requires. A hidden
component may remember indefinitely while every allowed future observation
forgets the observable past. Conversely, fitting a short visible history does
not certify this all-future property. The correct sufficient object here is a
uniform bound on the influence of actual observable histories on future
observations, acquired under an honest complete predictive-rank contract.

The theorem below bridges that operational property to a positive sustained
reversal-divergence rate. It neither bounds the microscopic preparation term B
nor assumes that the physically reversed preparation belongs to the reachable
forward predictive space. This last distinction prevents an invalid shortcut:
one cannot apply a forward-core contraction directly to rho-Theta(rho) unless
that vector is known to belong to its domain.

The construction combines standard martingale concentration and variational KL
with Astra's acquired complete-quotient machinery. No historical priority or
practical advantage over equally informed entropy-rate inference is claimed.

## 2. Interface and notation

Let a stationary finite irreducible CTMC L have stationary rho, physical
involution Theta, and an even deterministic memoryless observation. Assume
the intrinsic physical path-reversal divergence rate sigma is finite. Its full
stationary microscopic path KL satisfies

    D(P_hidden[0,T] || R_Theta P_hidden[0,T]) = B + T sigma,
    B = D(rho || rho Theta) < infinity.                         (1)

No numerical upper bound on B is supplied or used. The same proof extends to
other stationary sources only if a suitable physical path-KL bound with an
o(T) boundary term is established; infinite hidden memory alone does not
supply it.

Divide time into blocks of duration h>0. Z_i is a fixed finite observation word
within block i, on a grid symmetric about its midpoint. Its reversal rZ_i
reverses the word. Adjacent words may share endpoint observations. Take a
bounded score f with

    f(rz)=-f(z),       range(f) <= L_f,
    m=E[f(Z_i)],       S_N=sum_(i=1)^N f(Z_i).                 (2)

The full observation word over N blocks reverses S_N to -S_N. It is enough
to include the union of each sampling grid and its reflected grid. No
microscopic parity pulse, physical reverse trajectory or reset is used.

Let F_i=sigma(Z_1,...,Z_i). For every i, every k>=1, and any two positive-
probability histories in F_i sharing the same prefix through i-1, suppose

    TV(Law(Z_(i+k) | history 1),
       Law(Z_(i+k) | history 2)) <= a_k,       0<=a_k<=1.      (3)

Only future marginal blocks are needed for this additive-score theorem. A
uniform bound on the whole future transcript, as supplied by a complete
operational quotient, implies (3). Require

    A = 1 + sum_(k>=1) a_k < infinity.                       (4)

This is not an ordinary two-time correlation-decay premise. It controls all
conditional histories, including rare histories, and every future lag used.

## 3. Theorem and proof

**Theorem.** Under (1)--(4),

    sigma >= 8 m^2 / (h L_f^2 A^2).                         (5)

For |f|<=1, one may use L_f=2, giving sigma>=2m^2/(h A^2).

*Proof.* For a fixed N, set M_i=E[S_N|F_i]. Conditional on a fixed past
through i-1, the variation of M_i between two possible values of Z_i is at
most

    L_f + L_f sum_(k=1)^(N-i) a_k <= L_f A.                 (6)

The past scores are fixed; the present score varies by at most L_f; each
future score mean varies by at most L_f times its block-TV bound. Therefore
the centered Doob increment M_i-M_(i-1) has conditional range of length at
most L_f A. Conditional Hoeffding's lemma and iteration yield

    log E exp[u(S_N-Nm)] <= u^2 N L_f^2 A^2/8.             (7)

Let P_N be the observed word law and P_N^R its reversed law. Since reversal
takes S_N to -S_N,

    log E_(P_N^R) exp(u S_N)
       = -u N m + log E_(P_N) exp[-u(S_N-Nm)]
       <= -u N m + u^2 N L_f^2 A^2/8.                      (8)

The KL variational inequality gives, for every real u,

    D(P_N||P_N^R) >= 2uNm-u^2 N L_f^2 A^2/8.

Optimizing u=8m/(L_f^2 A^2) gives

    D(P_N||P_N^R) >= 8N m^2/(L_f^2 A^2).                  (9)

Observation is a reversal-compatible coarse graining, so (1) and data
processing bound the left side by B+Nh sigma. Divide by Nh and send N to
infinity. The fixed unknown finite B disappears. This proves (5).

No reverse-mixing assumption is needed: (8) uses the algebraic reversal of
the same stationary word law, not a separately acquired backwards process.
No hidden realization is identified in the proof.

## 4. How an acquired quotient can supply the all-history bound

This paragraph is an explicit classical specialization of the acquired
complete-quotient mechanism preserved in
sources/OPERATIONAL_QUOTIENT_RESET_CERTIFICATE_excerpt_1_120.md. That source
reports candidate status with independent review pending. The following
finite-dimensional calculation is reconstructed here and does not promote
its other quantum/infinite-dimensional claims.

Assume the full controlled future/prefix table of the declared stationary
source has an independently warranted rank upper bound r. A legal r-by-r
core H is actually acquired and certified invertible. The raw physical
prefixes tau_j have masses m_j in [0,1]; the empty prefix is tau_1 with
m_1=1. Coordinates x represent a predictive class as sum_j tau_j x_j. The
full rank promise plus core nonsingularity makes this representation exact
for EVERY future test and EVERY reached conditional state. Its trace row is
m, not an arbitrary row of ones.

For a normalized reached conditional state mu, its r test probabilities
lie in [0,1]^r and x=H^-1 p. Thus a certified bound

    ||x||_1 <= K,       K >= sum_(ij) |(H^-1)_ij|           (10)

holds uniformly, including conditioning on rare histories. This is why
rare-history amplification does not disappear; it is charged in core
conditioning K and its acquisition precision.

Let R be PASSIVE waiting for exactly h, with observations discarded and
no externally driven change of the native generator. The true quotient
matrix C satisfies mC=m. It is acquired from the raw shifted table
H_R,ij=probability(prefix j, wait h, future i), so C=H^-1 H_R. Define E to
select coordinates 2,...,r and

    W_m y=(-sum_(j>=2)m_j y_j, y_2,...,y_r),
    D=E C W_m.

Then mW_m=0, EW_m=I, ||W_m||_(1->1)<=2, and on trace-zero tuples

    C^k W_m = W_m D^k.                                    (11)

If a valid interval calculation certifies ||D||_(1->1)<=c<1, two normalized
reached conditional states x,x' satisfy

    ||C^k(x-x')||_1 <= 4K c^k.                            (12)

Any complete future transcript is an actual stochastic map applied to
sum_j tau_j x_j. Its output total variation is at most half the coordinate
1-norm, since each tau_j is positive with mass at most one. Consequently

    TV(future from x after k waits,
       future from x' after k waits) <= min(1,2K c^k).     (13)

After block i, block i+k starts after k-1 passive waits. Hence (3) follows
with

    a_k=min(1,2K c^(k-1)),
    A=1+sum_(j>=0)min(1,2K c^j)<infinity.                 (14)

The easy conservative bound A<=1+2K/(1-c) is sufficient. A tighter A is
computed by summing the finite saturated prefix and its geometric tail.
When c=0, a_1<=1 and a_k=0 for k>=2, so A<=2. Adjacent blocks need not be
independent because they can share an endpoint.

For r=1 the quotient is already independent of its reached preparation;
handle it directly instead of applying an empty-matrix formula.

The rank/core condition is essential. A matrix fitted from a finite visible
record can omit a nearly invisible slow orientation. It does not supply
(10)--(13) without the honest complete-rank/invariance premise. The companion
adaptive-lift obstruction shows why a finite experiment library cannot
create that premise universally.

## 5. Finite uncertainty and actual acquisition

Given simultaneous intervals |C-Chat|<=F and |m-mhat|<=d, with m_1=1, use

    Dhat_lj=Chat_lj-Chat_l1 mhat_j,
    B_lj=F_lj+F_l1+|Chat_l1| d_j,
    c_cert=max_(j>=2) sum_(l>=2)(|Dhat_lj|+B_lj).           (15)

Because |m_j|<=1, (15) bounds the true induced norm. Accept only if
c_cert<1. The matrix inverse and K must have their own valid enclosure;
the H uncertainty is not silently discarded. This can be ordinary exact
rational interval computation once the actual confidence intervals exist.

The core acquisition needs the paid repeated-start law, stationarity,
the actual raw joint prefix/wait/future experiments, timing calibration,
instrument action, count/precision budget and full-rank promise. A single
trajectory does not automatically yield those raw tables. The present
bridge does not resolve cold-start acquisition with none of that structure.

After an independently acquired certificate and a fixed score choice, a
single stationary record of N blocks suffices to estimate m. Equation (7)
gives, with failure probability at most alpha,

    |mhat-m| <= L_f A sqrt(log(2/alpha)/(2N)).              (16)

Insert the nonnegative lower confidence bound on |m| into (5), and add the
core-certificate failure probability by a union bound. Data-selected scores,
waiting times or cores need held-out validation or a simultaneous coverage
argument. A pilot-selected driven reset cannot be substituted for passive
waiting: it would change both the process and the physical cost being
certified. A separately justified initial operational burn-in may replace
stationary preparation with its explicit bias debit; it is not supplied here.

## 6. What has changed, and what remains conventional

Full hidden Dobrushin contraction can fail even when (13) holds uniformly.
For example, append to any observed finite mixing source an independent
stationary hidden component ignored by every declared readout/action. Its
mixing can be arbitrarily slow, or it can retain a conserved variable. The
observable quotient and K,c do not change. The conclusion is insensitive to
that irrelevant memory, while a uniform hidden contraction requirement is
not. For the finite irreducible version, use an arbitrarily slow irreducible
hidden component; (1) remains valid and B finite for each fixed model.

The strongest equally informed route is ordinary relative-entropy-rate
inference with a supplied uniform process-mixing condition. It can use the
same concentration and variational argument and may yield sharper bounds.
The addition here is the exact bridge from an acquired complete FORWARD
operational quotient to a physical sustained-reversal consequence, without
requiring a microscopic reset, hidden mixing, a bound on B, or reachability
of the reversed microscopic preparation. It is an information-interface
result, not a new concentration inequality or a device advantage.

The genuine new resource remains an honest all-future predictive closure
plus its measured passive forgetting. Finite correlation fits and finite
rank estimates without an architectural rank upper bound are insufficient.

## 7. Primary comparison

Kontorovich and Ramanan, Annals of Probability 36 (2008), 2126--2158,
DOI 10.1214/07-AOP384, https://arxiv.org/pdf/math/0609835, develops the
martingale/mixing route to concentration for dependent and hidden-Markov
sequences. The additive-score proof (6)--(7) is a simple standard
specialization, not a novelty claim.

Pollock et al., Physical Review Letters 120, 040405 (2018),
https://arxiv.org/pdf/1801.09811, formalizes Markovianity in terms of all
allowed interventions and causal breaks. Taranto et al., Physical Review A
99, 042108 (2019), https://arxiv.org/abs/1810.10809, makes instrument-dependent
memory explicit. Operational versus microscopic memory is therefore an
established distinction. The entropy bridge above is the proposed assembly
at the present Astra interface, with priority unestablished.
