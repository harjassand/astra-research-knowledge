# Composition-dependent boundary return correction
Status: new personal conditional operator theorem and graph-derived implementation plan. Not reviewed; not a general weak-reversibility result. The purpose is to remove the FALSE requirement of a pointwise scalar occupation gap at every incoming composition.

## Exact operator statement
Let P be the actual full-state section return kernel, killed on entering a fixed residual threshold. The section retains the entire incoming composition. Let r be its unbounded residual, w_theta(r)=exp(theta r), and g(r)>0 a polynomially decaying scale. Split the section into bad B and good G using an explicit composition criterion. All displayed estimates must hold for actual stopping kernels, with their complete physical repair already earned.

Suppose, above a sufficiently large residual threshold:

(A) On B, P w-w <= C g w.
(B) On G, P w-w <=[-c U+C T]w, with T/U<=eta(r)->0.
(C) The killed bad-return operator P_B has norm <=delta<1 in weight g(r)w(r):

    P[1_B g(r_next)w(r_next)] <=delta g(r)w(r) on B.

(D) The same weighted bad-entry quantity on G is <=ell(r)U w, with ell(r)->0.

Then choose D0>C and solve the POSITIVE actual bad-section Poisson problem

    H= sum_(n>=0) P_B^n [D0 g w] on B,    H=0 on G.

Its convergence and bound H<=D0(1-delta)^-1gw are earned by (C), not assumed. On B, PH-H=-D0gw, so P(w+H)-(w+H)<=-(D0-C)gw. On G, PH is bounded by D0(1-delta)^-1 times the left side of (D), and therefore the drift is <=-c'U w after raising the threshold. Thus a composition-dependent section potential closes the boundary even when T/U does NOT vanish on B.

The same theorem applies to polynomial enlargements of w, provided (A)-(D) are proved for those weights; one must not differentiate an already constructed H or assume harmless O(1/r) errors. If per-cycle actual running cost is <=Cw and min(g,U) is bounded below by an inverse polynomial, an appropriate enlarged weight pays the real cycle costs. This is the same actual stopped-cost construction, now with an earned nonconstant section profile.

The theorem itself is elementary positive-kernel algebra. Its scientific content would come from deriving (C)-(D) from reaction graph structure without assumed recurrence, stationary phase laws, or an imposed global barrier.

## A concrete graph-derived route to its difficult hypotheses
For the multi-seed fast source contract in INCOMING_MOMENT_MEMORY_LEMMA_CANDIDATE.md, let a0>=1, v=m-a0>0, and take the bad region A<=K(r)=r^gamma with gamma>0 small. Local source dominance supplies a worst-case reset scale p0(r)=O(r^-v), with a logarithm allowed when a0=1. The clearing-output compensator gives

    P(A_after<=K; clearing)<=C K^m T.

At the section, T<=Cp0 uniformly. Therefore direct bad-to-bad returns have mass O(K^m p0), genuinely small when gamma m<v. This is not an artificial finite cap: the bad region still contains unbounded reservoir composition, and its return operator is controlled by an actual output kernel.

The hard issue is ALL other low-walk/repair branches, not just direct clearing. For these, the incoming-moment lemma gives for every fixed s>0

    E[(1+A_out)^-s; first connector event]<=C_s(1+A_in)^-s.

Its extension from clearing-only to all connector-event outputs follows by adding terminal immigration/activation rewards to the killed supersolution: those events increase A, so their terminal reward is <= the supersolution at the pre-event state. Clearing retains the negative killing correction that controls the high-A region. Do not replace this with a bound conditional on observed A_out.

If a particular connector subevent has probability <=epsilon_N, Cauchy-Schwarz together with the 2s moment bound gives the stronger profile estimate

    E[(1+A_out)^-s; subevent]
       <=C_s epsilon_N^(1/2)(1+A_in)^-s.

Thus rare extra-activation/repair branches can be small not only in total mass but in an incoming-moment weighted norm. This is the candidate tool for summing arbitrarily many such physical stages without forgetting the A reserve.

Before accumulating m low-phase immigrations, phase descent limits the number of ordinary resets. Every immigration race consumes one inverse-A power; transport the remaining inverse powers through resets. Reaching m immigrations or a bad fast immigration should then have probability <=C times the FIRST inverse-m-th moment t, instead of the former cross terms with the global envelope p0. A full processor proof, including rare repeated activations and inactive outputs, remains to be written and checked.

If that transport closes, a good incoming state should have weighted bad-entry estimate

    P[1_B g(r_next)w(r_next)]/w(r)
       <=C p0 K^m T + C p0^2 K^m U,

for g=p0. The first term remembers its OWN first clearing/immigration law; the second corresponds to corrective activation followed by a rare bad output. With a graph-earned good-region ratio T/U<=C/K, the relative leakage is O(p0 K^(m-1)+p0^2 K^m)->0. This earns (D), while (C) comes from K^m p0->0.

## Current exact boundary
The conditional operator theorem above is proved algebraically. The local incoming-moment and source-drift estimates are personally derived. The complete full-processor profile transport and its weighted bad-entry estimate are NOT yet proved. That is the next hard construction; substituting a supplied return estimate here would give away the capability sought. The preceding scalar-gap obstruction explains why this obligation is real and why another uniform averaging theorem would not answer it.
