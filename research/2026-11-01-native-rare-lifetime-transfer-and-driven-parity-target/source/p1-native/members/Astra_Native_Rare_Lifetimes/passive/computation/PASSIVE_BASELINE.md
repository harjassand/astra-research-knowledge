# Passive unmarked history: the ordinary construction already works

Complementary constructor `producer-workspace/computation_opening`; parent `/root` owns
the stronger misspecification mechanism. The model family is the binary
path Gibbs/heatbath plus positive directed three-cycles developed in the
current task. Prior Astra premises remain bound to revision
51ce47ce39f976517d60e2f87bbe280b651f6056; no prior research chats were used.

## 1. Inputs and honest conclusion

Observe the complete state-valued piecewise-constant trajectory, including
actual transition timestamps, from an arbitrary initial state. Failed
update attempts and channel marks are not observed. The allowed local
move types and the finite neighborhood on which each aggregated move
rate depends are supplied structural conditions. An unknown global-state
dependence cannot be excluded from a finite passive record.

For the previously specified high-temperature path family, ordinary
continuous-time occupation/count likelihood already learns the needed
local parameters in polynomial time, without seeing the rare target,
clamping the source, or resetting it. The existence of this passive
acquisition is therefore not a missing operation worth claiming as new.
The stronger opening is the parent's transfer from a uniformly certified
local rate box to rare hitting/lifetime conclusions when the actual source
does not exactly have the fitted Gibbs law or positive short-cycle form.

## 2. Observable occupation/count likelihood

Index each observable move and its local pre-jump context by k. Write
q_k for its unknown constant rate within that context. Define

    E_k(t)=integral_0^t 1{context k is active at s} ds,
    N_k(t)=number of observed jumps of type k before t.

The intensity of N_k is q_k times the context indicator. The contribution
to the continuous-time path log likelihood is

    N_k(t) log q_k - q_k E_k(t).

This counts the complete holding-time information. Replacing time-weighted
occupancies by the empirical distribution at jump instants is generally
biased, because the embedded jump chain weights states by exit rate.

For every real theta,

    exp{theta N_k(t)-(exp(theta)-1)q_k E_k(t)}

is a nonnegative exponential martingale (a supermartingale suffices).
Choose a deterministic exposure a>0, and freeze coordinate k when its
occupation exposure first reaches a. The stopped exponential bound yields
the ordinary Poisson-Chernoff inequalities, irrespective of the initial
state or temporal dependence:

    P(|N_k/a-q_k|>eta q_k) <= 2 exp(-a q_k eta^2/3),  0<eta<=1.

One passive record can collect all coordinates; each coordinate's count
is frozen at its own exposure threshold. They need not be independent.
A union bound handles all K coordinates. Under an actual lower rate
q_min, choosing a>=3/(q_min eta^2) log(2K/beta) is sufficient.

Rate-confidence validity needs no burn-in or spectral-gap assumption.
Mixing and context mass are needed only for a calendar-time completion
bound. This distinction avoids making a stationarity assumption merely
to validate observed local rate intervals.

If a lower rate is not assumed, invert the Poisson-Chernoff likelihood
deviance at fixed exposure. Retain q>0 satisfying

    N log[N/(a q)]-N+a q <= log(2K/beta),

with the conventional N=0 limit. This gives simultaneous confidence
intervals without using an unknown lower rate as a validity premise.
The fitted reference may be any function of these same data: if every
resulting confidence interval is contained in the proposed reference rate
box, then the deterministic rate-box theorem applies on the single
simultaneous confidence event. Optional fitting does not invalidate it.

## 3. Explicit occupation concentration and burn-in

Let pi be the actual invariant distribution and g an additive symmetric-
part Poincare gap. For a context indicator f with p=pi(f), define
F=f-p. For |theta|<=g/2, a direct Feynman--Kac bound gives

    E_pi exp(theta integral_0^T F(X_s)ds)
       <= exp(2T theta^2 Var_pi(f)/g).

Proof: decompose a unit L2(pi) vector h=c+v, with pi(v)=0. The real
part of its tilted generator quadratic is at most

    -(g-|theta|)||v||^2 +2|theta||c|sqrt(Var f)||v||
       <= theta^2 Var(f)/(g-|theta|).

This bounds the semigroup norm and hence the stationary Feynman--Kac
expectation. Because Var(f)<=p, taking theta=+/- g eta/4 yields

    P_pi(|E_k(T)/T-p|>eta p) <= 2 exp(-g T p eta^2/8).

In particular the lower-tail failure at eta=1/2 is at most
exp(-g T p/32). This is ordinary spectral-gap concentration, not a new
claim; Lezaud2001 gives more developed versions for nonreversible
processes with the same symmetric-part gap.

If pi_min>=kappa and the initial state is arbitrary, then

    ||Law(X_t)-pi||_TV <= (1/2) kappa^(-1/2) exp(-g t).

Thus burning in for

    t_burn >= [0.5 log(1/kappa)+log(1/(2 beta_burn))]/g

puts the whole subsequent path law within beta_burn in total variation
of its stationary-start version. For K contexts of stationary mass at
least p_min, all exposure thresholds a are reached by an additional time

    T >= max{2a/p_min, 32/(g p_min) log(K/beta_occ)}

except with probability at most beta_burn+beta_occ. Observing and processing
the actual path costs its number of jumps; a global exit-rate cap Lambda
bounds the expected number by Lambda(t_burn+T). Rates, masks and contexts
can be updated locally; there is no hidden enumeration of 2^n states.

For the exact original path family, every one-site conditional outcome
has probability at least rho=2/5. Every specified pattern on r sites
therefore has probability at least rho^r, even if those sites are not
adjacent. A lower bound for the full-state mass is

    kappa=2^(-n) (0.9/1.1)^(2n-1).

The supplied true symmetric-part gap g>=1/2 and fixed neighborhood radius
therefore give a polynomial completion-time bound. The reset/clamp
observation cost is replaced by the explicit local-context coverage cost.

## 4. Two ordinary exact-family reconstructions

### 4.1 Known-tree stationary marginal reconstruction

Under the exact Gibbs model on a known tree,

    pi(x)=product_edges p_ij(x_i,x_j)
              /product_vertices p_i(x_i)^(deg(i)-1).

Estimate each one- and two-site marginal by its actual time occupancy.
The empirical pair and node tables are consistent because they come from
the same time-weighted record. On the event of positive table cells, their
tree product is a normalized distribution. If every cell has relative
error at most eta and t=-log(1-eta), then

    |log(pihat(x)/pi(x))| <= (2n-3)t, for n>=2.

This normalized-law bound is better than separately adding all canonical
parameter errors. Positivity can be handled by reporting insufficient data
when a cell is zero, or by a common small uniform pseudocount mixture that
preserves consistency and whose added error is charged.

Canonical factors can be recovered by

    b_ij=p_ij(00)p_ij(11)/[p_ij(01)p_ij(10)],
    a_i=[p_i(1)/p_i(0)]^(1-deg(i))
              product_(j neighbor i) p_ij(1,0)/p_ij(0,0).

Their log errors are at most 4t for b and (4deg(i)-2)t for a when
deg(i)>=1. On a path this is at most6t. The mean transfer may still use
the tighter normalized law bound if the fit is kept consistent; later
factor clipping/quantization must have its own error added.

For a forward directed cycle i, the unique simultaneous two-bit transition
is11->00. Its observed count has compensator

    alpha_i integral 1{pair i is11}/v_i(11;boundary) dt.

Use the learned local factors in this exposure. A deterministic uniform
local-factor log error r implies that the learned exposure differs from
the true exposure by at most exp(+/-r). Count-martingale concentration
then gives the corresponding alpha error. For an inverse cycle, use its
unique00->11 transition and corresponding local exposure instead.
Reusing the same trajectory
does not break this deterministic sandwich or the confidence union.

### 4.2 Clean transitions, with the orientation condition made explicit

An all-forward family of three-cycles creates only single-bit0->1 jumps and the
two-bit11->00 jump. Therefore every observed single-bit1->0 jump is
pure heatbath, without needing a channel mark. Its rate at neighbors l,r is

    q_down=1/(1+a_i b_(i-1)^l b_i^r).

Local count/exposure estimates at neighbor00 recover a_i=1/q_down-1.
At neighbor01 they recover a_i b_i. The same finite set of contexts
therefore identifies the Gibbs factors directly from nonstationary data.
For the unique pair11->00 jump with both outside boundary bits zero,

    q_double=alpha_i/(a_i a_(i+1)b_i).

This identifies alpha_i using another observable local rate. Positivity
and the bounded factor ranges make all transformations uniformly stable.
No equilibrium averages, reversibility assumption about the whole driven
chain, or hidden update attempts are needed for this all-forward subclass.
The actual parent's alternating-orientation model does not satisfy this
all-down-jumps shortcut. The following orientation-dependent construction
does apply to that model and is independently checked by the physics
collaborator in native_clean_check.py (8417 exact rate checks,32 models).

Use ordered pair bits(i,i+1), and forward cycle(0,0)->(1,0)->(1,1)->(0,0).
Condition the left neighbor of site i to be0 (or omit at the left endpoint).
This blocks a single-bit contribution from the pair on its left, for both
orientations. If the right neighbor is1, both up and down jumps at i are
pure heatbath. If the right neighbor is0, the down jump is pure for a
forward pair on the right, and the up jump is pure for an inverse pair.
At the last site both directions are pure under the left-neighbor0 condition.
These statements follow by listing the three arrows of each cycle; no
unobserved channel marks are used.

For known heatbath attempt rate1, the pure neighbor00 rate determines a_i:
for a forward right pair a_i=(1-q_down)/q_down; for an inverse right pair
a_i=q_up/(1-q_up). The two pure neighbor01 rates have ratio a_i b_i,
determining b_i. If the attempt rate lambda_i is also unknown, their sum
determines lambda_i and the same formulas use lambda_i in place of1.
The unique double jump with outside bits0 identifies alpha_i as above for
forward orientation; the inverse double jump starts at00 where v_i=1 and
has rate alpha_i directly. This is still ordinary identifiable CTMC rate
learning and does not itself constitute a new scientific barrier.

### 4.3 Concrete failed naive comparator

Take two bits, a_1=a_2=b_1=1 and alpha_1=1. The stationary law is uniform.
Heatbath flips have rate1/2. The directed cycle adds rate1 to
00->01, 01->11, and11->00. Thus the observed single-bit rate ratio

    q(00,01)/q(01,00)=3

is not the Gibbs odds1. Applying a reversible rate-ratio formula to the
driven chain gives the wrong parameter. Its embedded jump-chain masses
are (2/7,2/7,1/7,2/7), not the uniform time-stationary masses.

The strongest ordinary occupation/count construction above fixes both
problems. This failure does not establish a novel passive learning barrier.

## 5. Primary comparator actually read

Gaitonde, Moitra and Mossel, COLT2026, "Learning Ising Models from
Evolutions"; the author's full49-page paper is arXiv2507.15173v1,
"Better Models and Algorithms for Learning Ising Models from Dynamics":
https://arxiv.org/html/2507.15173v1 .

Theorems1.1--1.2 cover full unmarked continuous-time trajectories from
arbitrary initial configurations. The parameter theorem applies to
reversible single-site chains; the original driven two-bit family is
outside that theorem's scope. Section6, Algorithm3 and Theorem6.5
explicitly use local occupation and short-window flip counts to estimate
transition rates, then use reversibility to recover Ising parameters.
It gives known-graph parameter runtime on the order of
n*2^d*log(n/beta)*poly(1/parameter_accuracy), with the displayed
accuracy exponent4 and additional bounded-width/nondegeneracy constants.

The paper's inability to apply verbatim to the driven source is not a
general failure of existing inference: the supplied high-temperature
mixing and known local move architecture make ordinary CTMC likelihood
sufficient as proved above. The proposed passive capability should credit
this machinery, then identify the actual extra rare-output transfer.
