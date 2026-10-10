# Exponential EB approximation survives postselection

9 October 2026. Operational strengthening of the new exponential approximation candidate. It is derived after the preserved focused reviews and is not covered by them. No external certification or priority claim is made. The later EXPLICIT_EB_NOISE_REPAIR.md gives explicit constants and a positive separable-noise repair; the general normalization argument here remains useful.

## 1. Statewise theorem

Fix d>=2. Let epsilon_d(n)=min(2,C_d exp(-a_d n)), where C_d,a_d are dimension-only constants from EXPONENTIAL_APPROXIMATE_PPT_WORDS.md.

For every serial word T=A_n ... A_1 of CP and 2-copositive maps on M_d, there is one EB CP map E such that

 E*(I)=T*(I),                                           (1)

and for EVERY finite-dimensional reference R and EVERY positive joint input X on R tensor C^d,

 ||(id_R tensor (T-E))(X)||_1
   <= epsilon_d(n) tr[(id_R tensor T)(X)].               (2)

The same E works for all references and inputs. Neither T nor its factors need be trace preserving. If T is trace nonincreasing, E is trace nonincreasing as well.

For any input density matrix rho with success probability

 p=tr[(id_R tensor T)(rho)]>0,

the normalized outputs have

 || (id_R tensor T)(rho)/p - (id_R tensor E)(rho)/p ||_1
   <= epsilon_d(n).                                    (3)

The second state is separable across R : C^d. Thus the conditional output's trace distance from the separable states decays exponentially, without a factor 1/p. This is stronger than merely dividing the earlier norm-relative CP bound by a small success probability.

The theorem bounds approximation error. It does not assert that any finite output is exactly separable.

## 2. Exact backwards normalization, including singular effects

Write H=T*(I). We prove that there are CPTP and 2-copositive maps Theta_1,...,Theta_n on M_d satisfying the EXACT identity

 T=Theta_n ... Theta_1 Ad_(sqrt(H)).                    (4)

For positive-definite backwards effects, set Y_n=I and

 Y_(j-1)=A_j*(Y_j),
 Theta_j=Ad_(sqrt(Y_j)) A_j Ad_(Y_(j-1)^(-1/2)).

Then Theta_j*(I)=I. CP filtering preserves CP and 2-copositivity. Telescoping gives (4), with Y_0=H.

There is also an exact formula valid directly at singular effects. Let P_(j-1) be the support projection of Y_(j-1), and let B_(j-1) be its inverse square root on that support, extended by zero on the kernel. Choose any density matrix tau_j, and put

 Theta_j(X)=sqrt(Y_j) A_j(B_(j-1) X B_(j-1)) sqrt(Y_j)
            +tr[(I-P_(j-1))X] tau_j.                  (4a)

The first summand has input effect P_(j-1), so the added EB summand makes Theta_j TP. Both summands are CP and 2-copositive. To check the telescoping identity, take Kraus matrices K_(j,a) for A_j and write L_a=sqrt(Y_j)K_(j,a). Then

 sum_a L_a*L_a=Y_(j-1).

Every L_a annihilates ker Y_(j-1), since the corresponding sum of squared norms is zero. Therefore

 Theta_j Ad_(sqrt(Y_(j-1)))=Ad_(sqrt(Y_j)) A_j.          (4b)

This includes Y_(j-1)=0: both sides are zero. Multiplying (4b) over j proves (4) directly. Inverse square roots are used only on their supports, never on a zero eigenvalue. The completion term has no effect on the states entering that factor in the exact telescoping identity.

For completeness, an alternative proof avoids support inverses and uses compactness. For singular effects, replace A_j by A_j^(t)=A_j+tD, where t>0 and D(X)=tr(X)I. All backwards effects are now positive definite, so

 T_t=Theta_n^(t) ... Theta_1^(t) Ad_(sqrt(H_t)),
 H_t=T_t*(I).

The set of CP, 2-copositive CPTP maps on M_d is closed and compact. For this fixed finite n, extract one sequence t_k decreasing to zero along which the entire tuple of normalized factors converges:

 Theta_j^(t_k) -> Theta_j              for every j=1,...,n.

Also T_t->T and H_t->H. Continuity of the positive matrix square root and finite composition now gives (4). No limiting inverse of a singular H is taken. Zero maps cause no difficulty.

This compactness argument proves exact factorization; it is not a numerical procedure for finding well-conditioned factors.

## 3. Proof of the statewise bound

Apply the exponential CPTP theorem to

 S=Theta_n ... Theta_1.

Choose an EB CPTP Z with ||S-Z||_diamond<=epsilon_d(n), and define

 E=Z Ad_(sqrt(H)).

Equation (1) follows because Z is TP. For positive joint X, let

 X'=(id_R tensor Ad_(sqrt(H)))(X)>=0.

Using (4) and trace preservation of S,

 tr X'=tr[(id_R tensor T)(X)].

The diamond bound, valid with every finite reference, gives

 ||(id_R tensor (T-E))(X)||_1
 =||(id_R tensor (S-Z))(X')||_1
 <=epsilon_d(n)||X'||_1
 =epsilon_d(n)tr[(id_R tensor T)(X)].

This proves (2). Exact equality of the effects means that both outputs in (3) have the SAME success probability p, so (3) follows directly. If p=0, both positive outputs vanish and (2) remains valid.

## 4. Finite selective instruments and adaptive classical records

Consider a finite instrument {T_b}_b acting on the transmitted d-dimensional system. For each classical record b, assume the complete branch map T_b factors into at least n CP, 2-copositive maps on M_d. Arbitrary intervening CP operations may be absorbed into neighboring counted factors: the class CP intersect 2-CoPos is stable under CP pre- and postcomposition.

Apply Sections 1–3 to each branch. The resulting EB maps E_b have

 E_b*(I)=T_b*(I).

Consequently they form an instrument whenever the original maps do: positivity is retained and the sum of their effects is unchanged. For every input, ALL classical record probabilities are reproduced exactly. Every nonzero conditioned output differs from its corresponding separable output by at most epsilon_d(n).

If several records are retained together, then for every positive joint X,

 sum_b ||(id_R tensor (T_b-E_b))(X)||_1
 <=epsilon_d(n) sum_b tr[(id_R tensor T_b)(X)].          (5)

Thus any selected collection of classical outcomes has the same conditional approximation guarantee. The positive separable comparison outputs add; their probability weights are not discarded. This also controls the trace norm when the classical record is retained as an orthogonal flag.

For a protocol adaptive only through a finite classical record, fix a branch and absorb its selected operations into that branch's factors. Equation (5) then permits summing the branches. The EB replacement is a global instrument for the completed protocol. No efficient online construction or local round-by-round implementation of the replacement is asserted.

## 5. Operational meaning and essential boundaries

Within this model, conditioning on extremely rare successful records cannot retain a fixed positive trace-distance separation from the separable states after arbitrarily many counted steps. The guarantee is uniform over input states and reference systems, not limited to the maximally entangled input.

The assumptions are essential to the statement being made:

- The transmitted quantum system has fixed dimension d at every counted step. Dimension-only constants need not remain useful if d grows with n.
- Any coherent memory carried across steps must be included in that system. The argument does not allow a retained noiseless quantum memory that bypasses the counted noise.
- Each complete branch factor being counted is CP and 2-copositive. A channel that is PPT only after averaging unobserved outcomes does not automatically have PPT or 2-copositive individual branches.
- Interventions are CP maps on the same bounded system; adaptivity in this statement is carried by classical records. Introducing new coherent side channels or a general network changes the model.
- The result concerns serial composition and the stated instrument. It is not a general impossibility theorem for quantum repeaters or quantum networks, nor a tensor-power distillability claim.
- EXPLICIT_EB_NOISE_REPAIR.md now supplies a conservative explicit sufficient length of order d^2 log(d/eta). It does not claim an optimal engineering threshold or an efficient measure-and-prepare implementation.

## Relation to exact concentration barriers

INTERMEDIATE_CONCENTRATION_BARRIERS.md shows that an absorbing failure flag can hide a surviving lower-dimensional conditional branch. That mechanism defeats inference of exact separability from small absolute output weight. It is consistent with the present result: whatever conditional entanglement remains in a long serial branch must itself become exponentially weak in the stated distance, but it need not vanish exactly at a finite time.
