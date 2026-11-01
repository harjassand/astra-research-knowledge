# Actual unweighted source-time storage before a macro exit

Status: root exact-generator component, pending independent review. It is a stopped-domain budget, not cone admission or clearance.

Use the exact twelve-channel rate2 model. Start from a fixed initial state (or apply the statement conditionally on the initial sigma-field with a declared deterministic initial-storage ceiling). Fix a positive integer Emax, a physical horizon d, and a stopping domain satisfying

 E<=Emax, B>=cN>=1, A<=B, C+D+4E<=B/2,

with fixed c,N>0. All domain exits are retained as actual outcomes and must be charged separately by a consumer. Define the globally evaluated storage

 W=A+2(Emax+1-E).

Before an exit it is positive; every actual one-step target of the E ceiling also has W>=0, since E jumps by at most1 and counts are nonnegative. Other exit targets cannot exceed that one-step E ceiling.

Direct actual-generator identities are

 G(A-2E)=1+4A-5A²+A(C+D-B+4E)-CD,
 q_W=1+A+11A(A-1)+A(C+D)+10AE+3CD+AB.

The twelve W marks, in reaction order birth, death, 2A->AC, reverse, 2A->AD, reverse, 2A->AE, reverse, AE->CD, reverse, CD->AB, reverse, are

 +1,-1,-1,+1,-1,+1,-3,+3,+1,-1,+1,-1.

Here reverse AE->CD is CD->AE with rate2CD. Thus jump magnitude<=3. Integer A gives4A-5A²<=-A; the displayed domain yields

 GW<=1-AB/2-CD.

Since A<=B, B>=1, C+D<=B/2 and E<=B/8,

 q_W<=1+15AB+3CD<=1+30[(AB/2)+CD].

Define the ACTUAL continuous compensator budget

 Q(t)=integral_0^t[(AB/2)+CD]ds.

Stop at the first domain exit, time d, or Q=Qbar. The storage Dynkin martingale M has jumps<=3 and bracket<=d+30Qbar. If the Q budget is reached before the other stops, nonnegativity of terminal W and the drift inequality force

 M>=x:=Qbar-W(X0)-d.

For x>0, bounded-jump Freedman therefore gives

 P[Q reaches Qbar by d before a domain exit]
 <=exp{-x²/[2(d+30Qbar+x)]}.

A simultaneous adverse domain exit should be assigned to the domain-failure event, not treated as successful service. The bound is on the actual stopped martingale; no conditioning on favorable histories or independence of counts is used.

On paths staying within the Q budget and B>=cN until the same stop,

 integral A ds<=2Qbar/(cN), integral CD ds<=Qbar.

Put S0=W(X0)+d. Taking Qbar=2S0 gives x=S0 and the literal bounds: A-occupation<=4S0/(cN), CD-occupation<=2S0, and budget-exit probability<=exp(-S0/124), since d<=S0. Uniform O(nu) occupation AND exp(-Omega(nu N)) failure follow when S0=Theta(nu N), with declared comparison constants and fixed c. Emax=Theta(nu N) and d=o(N) alone do not ensure that condition: initial A or proximity to the E ceiling matters. Alternatively a deterministic Qbar of order nu N may be chosen above W(X0)+d with an explicit positive gap. These are distinct from the sharper weighted O(T^-2) budgets for integrals A e^-p.

The true-death counter has compensator integral A ds at this SAME stop. A counting-process Chernoff bound can therefore charge a lower total-population exit; immigration is independently bounded in law by its known unit-rate Poisson count over the declared horizon. Neither count is replaced by a conditional independent Poisson variable. The present component does not establish the B floor, cone, A cap or a final physical removal time.
