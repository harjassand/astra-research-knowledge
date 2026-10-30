# Exposure-moment threshold for polynomial collective forcing

30 October 2026. New abstract local candidate, conditional on CUMULATIVE_ADVERSE_BUDGET_PRODUCT.md. No fixed raw-rate necessity or global recurrence claim.

Let H_i(T)=integral_0^T b_i(t)dt be the actual adverse participation compensator of persistent label i. Keep the exact progress allocation, fixed batch size k and safe-event contract. Suppose for some eta>1 and constant M,

    E exp(eta H_i(T))<=M

uniformly in every initial label i, population and admitted horizon. No independence across labels is assumed.

Choose a in(0,1) so C=(1-a)^(-(k-1))<eta. Exhaust virtual labels at budget B as in the preceding note. Markov gives E J_T<=n M exp(-eta B). The product witness gives virtual threshold proportional to n exp(-CB)g_L(T) and exponential lower-tail bound. Paying exhaustion by Markov yields, for0<T<=1,

    P(A_T<=c n exp(-CB)T^L)
      <=exp[-c n exp(-CB)T^L]
        +C' M T^(-L) exp[-(eta-C)B].                (M)

Here constants depend on q,L,k,a, not n,T,B. Specifically use target threshold half the virtual lower-tail threshold and exhaustion threshold the other half. This is a priced failure statement, not independent-law factorization.

Set T=n^-delta and B=gamma log n. If

    L delta/(eta-C) < gamma < (1-L delta)/C,

then zeta=1-C gamma-L delta>0 and beta=(eta-C)gamma-L delta>0, and (M) becomes

    P(A_T<=c n^zeta)<=exp(-c n^zeta)+C'M n^-beta.

Such gamma exists whenever0<delta<(eta-C)/(L eta). Thus exposure exponential moments of order strictly greater than1 suffice for a nontrivial polynomial forcing scale even without a pointwise adverse-rate bound. This is weaker than the bounded-budget/pointwise theorem and does not automatically yield its sharp Green powers.

## Order one alone does not guarantee any polynomial small-time forcing

Use independent rank1 labels, with progress1->0 at rate q, no safe extras and adverse batches of size1. For each small horizon T, set B=1/T and epsilon=exp(-2/T), taking T small enough that epsilon<T. At t0=T-epsilon, mark exactly those labels currently at rank0. For each marked label, turn on an adverse0->1 clock of rate K=B/epsilon until its first such jump or time T, whichever occurs first. After that first adverse jump, turn its adverse clock off. Unmarked labels never have an adverse clock. This is a finite-rate adapted rule, not an anticipatory decision.

For a marked label the accumulated adverse hazard is min(E,B), E~Exp(1). Thus

    E exp(min(E,B))=1+B.

The probability a label is marked is p=1-exp(-q t0)<=qT. Therefore for EVERY label,

    E exp(H_i(T))=1+pB<=1+q,

uniformly as T tends to zero. Yet a marked label remains target only if it avoids the entire adverse pulse, or progresses back after its reset. The former probability is exp(-B), and any progress in the final epsilon interval has probability<=q epsilon. Unmarked labels also can reach target only by such a late progress. Consequently

    P(label target at T)<=qT exp(-1/T)+q exp(-2/T).

Taking T=n^-delta for any fixed delta>0 gives E A_T tending to zero faster than any inverse power of n. In particular P(A_T>=1)->0, despite the uniform order-one exponential exposure moment. All label processes are nonexplosive and every adverse event touches only one label.

This counterexample proves that the strict eta>1 condition cannot in general be relaxed to eta=1 when seeking a UNIFORM POLYNOMIAL small-time forcing conclusion over this adversarial class. It does not rule out weaker non-polynomial bounds at order1, and it is not a necessity statement for any fixed physical network. The pulse rate K depends on the tested horizon; that is allowed in the stated adversarial uniformity test and must not be mistaken for one fixed chemical rate law.
