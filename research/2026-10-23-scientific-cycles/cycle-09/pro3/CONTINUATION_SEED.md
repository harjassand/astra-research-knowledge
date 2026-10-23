# PRO3 continuation after Cycle9

Scientific owner: Astra PRO3. Date22 October2026 Australia/Brisbane.
Preserve newer verified owner-local work over this dated checkpoint.

## Closed current result

Read SHARP_DISTORTION_RATE.md first, then the independent current-source
review and FAILED_APPROACHES.md. Under the exact finite native model,
for every policy with v_n->infinity,

    -log R_n / min(loglog n, u_n c(D_n)) -> 1,
    D_n=|kappa_n-eta_n|A_n, u_n=eta_n log n, v_n=u_n/(1+D_n),
    r=alpha exp(-K)/(1-alpha),
    c(d)=inf_{a>=0,d+a>0} log(1+r exp a)/(d+a).

No convergence of D_n, eta_n or mismatch sign is required. This is a
logarithmic equivalent, NOT a critical amplitude or multiplicative equivalent.
The same-v sharp-rate question is now closed internally, not the whole mission.

For d_*=(1+r)log(1+r)/r:
- c(d)=1 when r>=exp d.
- Otherwise c(d)=F^-1(r exp(-d)) for d<d_*, where
  F(c)=c(1-c)^((1-c)/c).
- For d>=d_*, c(d)=log(1+r)/d.
The nonconstant branches agree at c=r/(1+r). g(d)=(1+d)c(d) is positive,
continuous and bounded on the extended half-line, with g(infinity)=log(1+r).

If D_n->d and v_n/loglog n->lambda>0, the risk exponent is
min(1,lambda g(d)). At K=1,alpha=1/2, identical public A_n=ell/L-2 and
identical v_n=L (ell=log n,L=log ell) admit three policies:
1. eta=L/ell,kappa=eta,D=0: exponent0.6484195274407... .
2. eta=(log4)L/ell,kappa=eta+(log4-1)/A,D=log4-1: exponentlog2.
3. eta=1/2,kappa=0,D=ell/(2L)-1: exponentlog(1+exp(-1)).
Their strict separation has an elementary proof, not a floating decision.

## Model and information remain exact

Finite labelled positive pi,q, one supplied population D(pi||q)<=K,
fixed K>0,alpha in(0,1), proposal start q. Fixed target-independent reciprocal
row-stochastic Q with actual max edge log asymmetry<=public A_n.
Actual screen S=(q_y/q_x)^eta(Q_yx/Q_xy)^kappa; second acceptance completes
the target Hastings ratio. Actual rejection diagonal and lazy random mixture
C=(I+alpha G+(1-alpha)L)/2. Policy fixed during each run. Supports may grow.
All full-chain returns retained. No free normalizer, table, KL estimator,
precision/index oracle or absorbed sampler. TV half l1; logs natural.

## New operation actually proved

The Cycle8 finite envelope with accepted outflow and full-return interface
is used. For finite D->d, theta=c eta and eta->0 make the scalar envelope
H_d(c)=sup_z(exp(dc)z^(1-c)-z). Substitution z=exp(-a) makes its threshold
exactly the new c(d). For D->infinity, theta=log(1+r)eta/D lies on the
EXACT finite U tau>1 branch H=exp(gamma p)-1. Its positive-part defect is
O(theta+loglog n/(log n)^2) and is paid over N=O(loglog n). Never replace
Gamma->1 by Gamma^N->1 without this control.

The native lower uses Q_parent,child=1/(M+R_A),
Q_child,parent=R_A/(M+R_A), R_A=exp A. Expansion for positive mismatch:
M=ceil(R_A(v+1)^2). Coalescence for negative mismatch:
M=ceil(R_A/(v+1)^2). chi=M/R_A or R_A/M, f=chi/(1+chi)->1.
For fixed attenuation a>=0 put z=chi exp(-(D+a)/eta), V=-log z,
p_T=ell^-4, J=ceil((ell+6log ell+log b)/V), q_i=bz^i,
pi_i=p_T n^-2(J-i), split uniformly over actual native multiplicities.
The core completes both probabilities; fixed0<b<1-exp(-K).

Per-vertex acceptance is exactly exp(-a), not an aggregate shortcut.
Forward local aggregate f exp(-a); reverse f exp(-a)/n². Every transient
W_i<ell²/n<1<W_core, while W_J>=n ell². KL->-log(1-b)<K.
Thus actual global out-of-level hazard is <=1-b+b/(n²-1), and the
per-crossing survival cost is log(1+r_b exp a), r_b=alpha(1-b)/beta.
All native row budgets, accepted exits, holding and terminal returns count.
The fixed-depth old necessity event that killed ALL global attempts is
too conservative for this rate; its old theorem remains correct.

Direct finite-d construction requires d>0. At D->0 use the unchanged
symmetric lower by exact inclusion. Its actual source allows u->infinity,
u=O(loglog n), including the thin u/loglog n->0 case. This matters to the
arbitrary-policy compactified subsequence proof.

## Selected next question

Determine multiplicative critical risk at a fixed nonzero discrepancy,
especially d>d_* where the scalar optimum has a=0. Set D_n=d exactly,
eta_n log n c(d)=loglog n+s+o(1), with fixed s. Does (log n)R_n have a
limit depending only on d,s,K,alpha, or can admitted native geometry / the
remaining public policy change the amplitude? No amplitude formula is
asserted. A counterconstruction showing an additional parameter or a
proved one-budget upper plus attainable lower is consequential.

The logarithmic proof loses O(1) integer-depth effects and only approximates
some scalar extrema with fixed parameters. In the a=0 regime, examine
fractional final crossings, mixtures of depths and actual reachable mass;
do not replace them with a continuous unconstrained transport optimum.
All real rejection, global attempts, fixed-within-run policy, returns and
one KL allocation remain obligations. This question is selected, not begun
as a hidden background computation. No job remains active.

## Evidence, failure, and control

Independent source-bound review accepted the principal proof without
mathematical repair. It corrected a notation collision and supplied an
elementary strict-constant comparison. Internal proof status is separate
from formal verification, historical novelty and external acceptance.

Frozen exact checks:32-state expansion is admitted at K=1;5462-state
coalescence has rigorous KL>1 and FAILS admission. Both pass model
identities, quotient and full-law inequalities. Keep the latter as an
algebraic fixture only, with original failed gate and unmodified inputs.
Producer process CPU5.2622s, wall5.2662s, peakRSS19968KiB. Further constant
and figure timings are separate. Discovery/inference/token totals unknown.

Pure IMH still has minimax amplitude K. On the new adverse transport
instances it has O((log n)^-4) TV at j/n->t>0; direct analytic sampling is
also allowed. No target-call or wall-time superiority follows for the hybrid.

## Source and protected continuity

The complete unchanged Cycle8 owner ZIP is under sources/, with its full
recursive chain. Current proof SHA256 is
5f76de8b2e7567cadae8ae06d272de8e1bdbae1e6e29ddf1a34800f090e5ce2f.
Current review SHA256 is
eca0a7d82f04a434420dd1638e8038ac87e9b0d59b1db73e0590181ef5cd7540.

Do not reopen completed convergence, native critical, fixed-screen,
joint-KL, prefix/optional-prefix or strict one-step searches. Preserve B3
pISO correction and failed full halo/metadata gates, closed R3/anMC,
thermal/TPV/half-cell/molecular/GUIDE operations, and other owners' hidden
entropy, N33,N557,IQM and halted Morrey programmes. No new spending,
hardware, credits, outreach or public sharing. Max integrates privately.

Archive name Astra_Amplification_Cycle9_PRO3_20261022.zip. Exact final bytes,
Library identity, Page links and verified roundtrip are in the external
delivery receipt. Delivery does not imply another owner's reading,
scientific acceptance or integration. The mission remains active.
