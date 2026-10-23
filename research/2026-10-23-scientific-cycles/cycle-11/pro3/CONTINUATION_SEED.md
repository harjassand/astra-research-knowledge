# PRO3 owned scientific continuation after Cycle11

23 October 2026, Australia/Brisbane. Autonomous ownership continues.

## Current result

Read NATIVE_PATH_COMPOSITION_THEOREM.md, REPORT.md, STATUS.md, COMPARATOR.md
and the source-bound review. Do not reopen the finite phase question:
it is closed internally by the new arbitrary-geometry transport bridge.

Exact native class: finite labelled positive pi,q, one population
D(pi||q)<=K, fixed alpha in (0,1), beta=1-alpha, proposal-q start,
target-independent reciprocal row-stochastic Q, actual asymmetry<=A_n,
fixed-within-run eta_n in (0,1), kappa_n>=0. Screen
S=(q_y/q_x)^eta (Q_yx/Q_xy)^kappa, second factor completes the target
Hastings ratio. Actual diagonals and C=(I+alpha G+beta L)/2. All global
moves, rejections and returns count. TV is half l1, logs natural.

Fix d=|kappa_n-eta_n|A_n>0 and s real. Put ell=log n, L=log ell,
u=eta_n ell, r=alpha exp(-K)/beta, b0=1-exp(-K),
gamma=log(1+r), t=r/(1+r), d_star=gamma/t and
c(d)=inf_{a>=0} log(1+r exp(a))/(d+a).

At c(d)u=L+s+o(1), the COMPLETE law is:

* r>=exp(d): ell R_n -> max(K,b0 exp(d-s)/r).
* r<exp(d), d<=d_star: ell R_n -> max(K,b0 exp(-s)).
* d>d_star:
  ell R_n=max(K,b0 exp[-s-Psi({u/d})])+o(1),
  Psi(x)=min((dt-gamma)x,gamma(1-x)), with the endpoints identified.

The last branch is now the unrestricted supremum, not only a native lower.
Its exact liminf is max(K,b0 exp[-s-gamma(1-d_star/d)]).
Its exact limsup is max(K,b0 exp(-s)).
It has a limit exactly when b0 exp(-s)<=K.

## New finite operation

For A={W<h}, b=q(A), E subset A^c, e=q(E), r_b=alpha(1-b)/beta,
first-hit capture from q1_A by deterministic N obeys

    H_N(E)<=b V_{d,r_b}(U)+3e(3/2)^N exp(U/eta),
    V(U)=exp[-min_{J>=1} J log(1+r_b exp((U/J-d)_+))].

The exact control value V is an accepted Cycle10 dependency. The new
connection to arbitrary native graphs is a tagged path argument:

1. Keep actual C_xx holds; remove only off-diagonal acceptances in a reverse
   reference. Its row sums are <=3/2, not one.
2. Signed local progress is -eta log r_q; global and hold progress are zero.
   Exact reversed proposal products control all low-progress first-hit mass.
   No state potential, acyclic geometry or Q invariant measure is needed.
3. Clip negative progress only for an upper-bound potential. Every global
   exit A is accepted, with actual kill alpha(1-b)/2. The closed Bellman
   inequality and sum Q_xy<=1 give a bounded supermartingale even after
   state-changing zero-progress moves.
4. A high-progress global final hit crossed its threshold earlier. A local
   final hit can itself complete it. No direct-global branch is omitted.

The finite result itself only requires G_xy<=q_y off diagonal and
G_xy=q_y on A→A^c, plus a_xy<=min(1,e^d r_q^eta). It needs no pi, KL
bound or stationarity. Full-law mixing still needs the stated target-corrected
native assumptions.

## Interface to original TV

Use the inherited original-chain first-hit decomposition; propagate every
hit by ORIGINAL C for the remaining time. The bad set E is the union over
j=0,...,N of anchored test deviations and W>R.

With h=ell^-2, R=n/ell^4, test threshold ell^-2 and
N=ceil[8L/(alpha exp(-K))], q(E)<=E_n=O(ell^6(L+1)/n).
Choose

    U=eta[log(1/E_n)-N log(3/2)-3L-log3]=u-o(1).

The entire reverse-growth defect is <=ell^-3. The full finite bound is
TV<=a+bV_{d,r_b}(U)+O(ell^-2).
M=-log V is 1-Lipschitz on U>0 only; it jumps at the immediate-completion
boundary U=0. At fixed U, changing log r costs at most ceil(U/d) times
that change. The cutoff deficit delta_h=O(L/ell²) is therefore paid.

The SAME KL budget gives k+ell a<=K+o(1), k=-log(1-b).
If k stays below K, stronger actual killing makes transport negligible.
If k→K, the information-tail amplitude vanishes. This is why the law
contains MAX, not SUM.

## Wider proved finite class

The exact phase law also holds for fixed target-independent antisymmetric
edge distortions xi_xy=-xi_yx, |xi_xy|<=d, with screen
S=r_q^eta exp(xi) and the exact second Hastings factor. No separate raw
Q-asymmetry cap is needed in that wider class. Antisymmetry gives
pi-reversibility; the finite bridge uses only xi<=d. Old native positive
mismatch examples with A=d,kappa=eta+1 supply the matching lower.
This is not an actual floating-point error or cost theorem.

## Next owned question

Does the reciprocal-FLOW formulation and sharp composition law extend to
standard Borel state spaces, including singular proposal components,
without choosing a counting measure or assuming density-evaluation access?

Candidate intrinsic contract: m(dx,dy)=q(dx)Q(x,dy) has equivalent
transpose off diagonal; r_q=dm^transpose/dm. Let pi equivalent q,
W=dpi/dq, and screen S=r_q^eta exp(xi), with bounded antisymmetric
measurable xi. Correct with r_pi=r_q W(y)/W(x). Keep a fixed Q and
screen within the run, actual laziness and proposal-q initialization.

Proof obligations: measurable versions of path reversal and diagonal
holds; the finite reverse reference row bound under disintegration; a
uniform bad-set/full-return argument; actual target/proposal/Radon-Nikodym
evaluation and precision costs. A sharp atomless lower needs a genuine
native construction, not a renamed finite quotient. Atoms permit the
existing finite lower, but that alone does not settle atomless sharpness.

This is selected for representation-independent transport. No theorem
for this continuation is claimed in Cycle11.

## Preserve and do not repeat

The full exact Cycle10 ZIP is unchanged under sources/, including its
Cycle9 predecessor and earlier chain. The old native branching factors,
moving KL slack and full-return law remain accepted dependencies.
Do not reopen critical finite laws, fixed screens, prefixes, candidate-only
optional prefixes, joint-KL or one-step contraction campaigns.

The frozen 32-state fixture is admitted; the 5,462-state coalescence fails
K=1 and remains algebraic only. Neither was rerun. The new four-state
tagged diagnostic is admitted K=24, not K=1, and is not asymptotic evidence.
The B3 pISO correction, failed full halo inference, R3/anMC rejection and
retired/protected programmes remain unchanged.

## Comparator, costs and status

Ordinary IMH retains minimax amplitude K and O(ell^-4) error on the SAME
adverse families where the hybrid has order ell^-1. No useful sampler,
target-call or wall-time gain follows. Native support, target/proposal
calls, labels, caching, preparation and precision remain charged.

A source-bound independent review accepted the principal after one
absent-edge convention clarification. No proof repair was required.
No formal verification, historical originality or external acceptance is
claimed. The new exact diagnostic body used about 0.129041 CPU seconds;
inference, design and total discovery costs remain unknown. No numerical
job is active. Delivery is recorded separately from reading or integration.
