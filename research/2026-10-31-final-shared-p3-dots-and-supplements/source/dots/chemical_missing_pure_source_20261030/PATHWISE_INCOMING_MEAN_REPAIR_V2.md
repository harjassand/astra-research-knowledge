# V2 interface repair: incoming-dependent physical mean
Status: explicit additional lemma prompted by independent reviewer. PATHWISE_GRAPH_PROFILE_TRANSFER_V1.md remains byte-identical. V1's interface list omitted this load-bearing input and is incomplete without it.

The corrected whole-cycle proof charges a FAST IMMIGRATION by the incoming inverse-m profile, requiring

    (B)_q T(x)<=C(1+A_initial)^-m.                     (IM)

A uniform p0 bound and joint moment transport alone do not state (IM). The following proves it under the pathwise-transfer contract, without reintroducing immediate A-producing edges.

## 1. An incoming-weighted occupation estimate
Use V1 notation a0>=2, v>=2, m=a0+v, b=v-1+delta. On the underlying operational fast chain, Q_op f_(2a0)<=lambda f_(2a0), lambda=C N^(v-1), where f_s(A)=(1+A)^-s. Thus at each deterministic operational time s,

    E f_(2a0)(A_s)<=exp(lambda s) f_(2a0)(A_initial).

For sigma equal to the first actual connector event in operational time, survival is bounded by the reviewed clearing survival C exp(-cN^b s). No independence is required for Cauchy-Schwarz:

    E[f_a0(A_s)1_{sigma>s}]
       <=[E f_(2a0)(A_s)]^(1/2) P(sigma>s)^(1/2)
       <=C f_a0(A_initial) exp[-(cN^b-lambda)s/2].

Since 1/(A)_a0<=C f_a0(A) on A>=a0, integrating the physical clock gives

    (B)_q T(x)<=C N^-b f_a0(A_initial).               (O)

The underlying operational chain is allowed to continue after the connector mark for this deterministic-time estimate; sigma is a stopping mark on that same chain. Nonexplosion is automatic on its finite conserved shell.

## 2. Small incoming A
Choose a fixed R large and L=R N^((v-1)/v). If A_initial<=L, (O) gives

    (B)_q T/f_m(A_initial)
       <=C N^-b(1+A_initial)^v
       <=C_R N^-delta.

This is uniformly bounded and even tends to0.

## 3. Large incoming A and the actual boundary value
Normalize physical time by the fixed (B)_q factor. The killed generator before the first connector event is

    Kbar=(A)_a0 Q_op-k_D(A)_m-(normalized competing hazard).

V1's positive-drift estimate gives Q_op f_m<=C N^(v-1) f_m. Consequently, when A>L and N is large,

    Kbar f_m<=C N^(v-1) A^-v-c_0.

Here (A)_m f_m is bounded below by a positive constant for A>=L>>m, and competing killing only improves the inequality. Choose R so C/R^v<=c_0/2. Then Kbar f_m<=-c_0/2 throughout this upper domain.

Stop at the first connector event or the first fast entrance into A<=L. Fast A-jumps have magnitude at most v, so a boundary entrance lies in[L-v,L]. Its remaining normalized mean from (O), divided by f_m at that entrance, is O(N^-b L^v)=O(N^-delta). Thus for sufficiently large N a fixed multiple D f_m dominates the ACTUAL remaining-time boundary value and has killed drift <=-1 in A>L.

Finite-shell stopped Dynkin first proves finite expected time to this stopping boundary (the positive supersolution pays elapsed time); then strong Markov and the boundary-value comparison yield

    (B)_q T(x)<=D f_m(A_initial)

for every upper-domain start. Together with section2 this proves (IM) uniformly over all active large-N compositions and B>=q. Fixed finitely many smaller active states may be covered by enlarging constants; inactive states are handled by the separate actual seed rule, not this lemma.

## 4. Interface consequence
The first fast-immigration subkernel now has mass

    k_I T(x)<=C B^-q f_m(A_initial),

so it can be charged by the incoming inverse-m profile in the repaired full-cycle argument (E), exactly as required. Rare activation profile norms, all-event moment transport, good-region occupation gap and the p0/gamma replacement remain as in V1.

V2 of the pathwise transfer is V1 PLUS this file, with dependencies on the separately reviewed operational strict-clearing theorem and the repaired six-file whole-cycle profile theorem (including its review completions). It does not import dormant-face calculations, claim a generic WR result, or alter any previous receipt.
