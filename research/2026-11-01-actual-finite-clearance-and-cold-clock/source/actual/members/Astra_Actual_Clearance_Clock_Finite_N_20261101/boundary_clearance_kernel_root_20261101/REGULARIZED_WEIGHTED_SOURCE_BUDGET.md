# Regularized weighted source storage through the zero-E startup

Status: root full-generator construction, pending independent review. This is a conditional budget, not admission or clearance. It regularizes a test function; it does NOT change the actual reaction rates or prepare a reference process.

Let N=T^5, T>=10. Put e=E/T³, w=E+T³, k=8/5, and

 phi=(1+e)^-2, W=A phi+k T³/(1+e).

Admit actual pre-stop states with

 B>=(9/10)N, L<=N/5000, E<=N/100,
 A/(E+T³)<=2.

A<=L holds identically; no A/L or imbalance cap is used by this storage drift. The source starts at the raw corner A=E=0, where W0=kT³, and the declared ORIGINAL horizon is4T. The ratio/other-domain exit probabilities remain separate obligations.

## Literal finite-jump identity

Let d_+phi=phi(E+1)-phi(E), d_-phi=phi(E-1)-phi(E), and
alpha_+=T³[(1+e)^-1-(1+e+T^-3)^-1],
alpha_-=T³[(1+e-T^-3)^-1-(1+e)^-1].
Only active rows are used; E-consuming rows have E>=1. All physical target weights remain positive. With a2=A(A-1),

 GW=phi[1-A-3a2+A(C+D)-AB+3CD]
    +d_+phi[(A-1)a2+2(A+1)CD]+2A²E d_-phi
    -k a2 alpha_+-2k CD alpha_++2k AE alpha_-.

All twelve actual channels are included, and the coefficient E remains the ACTUAL count, not w.

Exact ratios are

 alpha_+/phi=w/(w+1), alpha_-/phi=w/(w-1),
 (d_-phi)/phi=(2w-1)/(w-1)².

For w>=T³>=1000, w(2w-1)/(w-1)²<=5/2. Since E<=w, the positive derivative term is at most5A²phi. Rewriting A(C+D)=2AL-2A² cancels this against the actual -5A². The d_+ rows and the remaining negative a2 term are favorable. Thus, with b=100/99, sigma=17/101,

 GW<=phi{1+A[2+2L+2kbE]-AB-sigma CD}.

Here alpha_+/phi>=100/101 and alpha_-/phi<=100/99. The admitted caps imply

 2+2L+2kbE<=(1/20)B,

because N>=10^5. Therefore

 GW<=phi-(19/20)AB phi-(17/101)CD phi.                 (1)

## Jumps and bracket

For Delta E=0, Delta W=+/-phi. For E-changing rows, the exact formulas are the same product differences displayed above. The bounds

 |d_+phi|/phi<=2/w, (d_-phi)/phi<=(5/2)/w,
 alpha_+/phi<=1, alpha_-/phi<=100/99,
 (A+1)/w<=2+1/1000

give |Delta W|<=8phi<=8 for EVERY actual enabled row.

The full rate is q_A=1+A+3a2+A(C+D)+2AE+AB+3CD. Using A<=L,

 q_A<=1+[1+(3L+2E)/B]AB+3CD
     <=1+(21/20)AB+3CD.

Let

 Q=integral[(19/20)AB+(17/101)CD]phi dt.

Since phi<=1, the actual storage bracket obeys

 <M_W> <=64[4T+(303/17)Q]

through the same stop. No conditional independent Poisson law is used.

## Paid deterministic budget

Stop also at Qbar=4T³. If this budget is hit before the physical/gate stops, positive terminal W and (1) force

 M_W>=Qbar-W0-4T>=2T³.

The predictable bracket is then below4600T³, and jumps are bounded by8. Bounded-jump Freedman gives

 P(Q hits4T³ before original4T and the other gates)<=exp(-T³/2500).

On the same budget event, with the same stop,

 integral A/(1+e)² dt <=800/(171T²),
 integral CD/(1+e)² dt <=(404/17)T³.

These are literal finite-T bounds, not just big-O claims. Initial-storage and horizon costs have been included explicitly. A later entry may instead use its actual initial W and remaining original horizon; it cannot inherit W0=kT³ without proof.

The additional gate A/(E+T³)<=2 can be received from a separately paid lower barrier for U0=E-A/2, namely U0>=-T³. Its initial/startup and first-exit accounting are not supplied here. The key achieved change is that the storage and its source-time integrals are well defined at E=0 and across all later returns; no positive-E restart or lower-ratio assumption is needed by this budget.
