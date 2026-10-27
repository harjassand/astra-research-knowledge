# Exact singular-boundary compression and faithful lift

2026-10-25. This is an analytic reduction, not exclusion of the remaining boundary and not a proof of the unrestricted WH3 target.

Let A>=0 be nonzero and singular, B>0, Tr A=Tr B, A<=9B. Write P=supp A and Q=I-P, and A_P=A restricted to P. For 0<p<1/4 put C=pA+(1-p)B>0. Define the finite operator on P

L_p(A,B)=2 P log C P - log A_P - P log B P.

## 1. Universal logarithmic kernel expansion

Set A_e=(1-e)A+eB for e>0. Then, in operator norm,

log A_e = (log e) Q + (log A_P) direct-sum (log B_Q) + o(1),

where B_Q=QBQ restricted to Q. In particular the off-diagonal P/Q blocks tend to zero, even though A_e generally does not commute with A.

Proof: the positive spectral cluster of A is separated from zero. Its spectral projection P_e differs from P by O(e), and a unitary U_e=I+O(e) carries P to P_e. In that splitting, U_e* A_e U_e has positive block A_P+O(e) and small block e B_Q+O(e^2), with zero cross block by the spectral decomposition. Since B_Q>0, their logarithms are respectively log A_P+O(e) and log e I_Q+log B_Q+O(e). Conjugating back adds O(e |log e|), which tends to zero. This also supplies a quantitative remainder O(e |log e|) for fixed A,B.

Consequently,

F_p(A_e,B)=log(1/e) Q+K_p+o(1),

K_p=2log C-log B-[(log A_P) direct-sum (log B_Q)],

and P K_p P=L_p(A,B). No log of a singular matrix has been substituted into the faithful expression.

## 2. Exact eigenvalue survivor

The Q block diverges to positive infinity; all cross blocks remain bounded. Taking its Schur complement gives

P F_p(A_e,B) P - P F_p(A_e,B) Q [Q F_p(A_e,B) Q]^{-1} Q F_p(A_e,B) P
= L_p(A,B)+o(1).

The lowest dim(P) eigenvalues converge to those of L_p; the remaining dim(Q) eigenvalues diverge to positive infinity. In particular:

- If L_p>0, then F_p(A_e,B)>0 for all sufficiently small e>0.
- If L_p has a strictly negative eigenvalue, then F_p(A_e,B) is not positive definite for all sufficiently small e>0.
- A zero eigenvalue of L_p is not decided by this leading-order statement; the finite Schur correction and smaller terms remain relevant.

Every A_e has the same trace as B. Also

9B-A_e=(1-e)(9B-A)+8e B>0.

Therefore L_p>0 at any admissible singular boundary pair produces a genuine faithful strict-cap counterexample to the sufficient generic matrix lemma. Conversely, the radial theorem's singular alternative arrives with F_p>=delta I uniformly for a fixed delta>0, and compression/continuity therefore gives L_p>=delta I>0. The same spectral-cluster argument applies to the radial approach A_t, with the first-order positive kernel block replacing B_Q; that block affects only K's Q component and not L_p.

Thus the radial singular alternative is exactly a finite, lower-dimensional compressed-log positivity problem, not a merely formal divergence loophole.

## 3. What ordinary support induction loses

Let B_P=PBP restricted to P. Define the nonnegative compression Jensen defects

J_B=log B_P-P log B P,
J_C=log[pA_P+(1-p)B_P]-P log C P.

Then exactly

L_p(A,B)=F_p(A_P,B_P)+J_B-2J_C.

Both J_B,J_C>=0, but their difference has no sign from Jensen alone. Moreover

Tr A_P=Tr B_P+Tr B_Q > Tr B_P.

Consequently the compressed pair is not trace balanced, and simply invoking the original equal-trace lemma in lower dimension is invalid. A valid induction must retain the missing bath mass and the paid logarithmic correction J_B-2J_C.

When A and B commute, choose a common eigenvector in P with ratio r=a_i/b_i>=1; such a ratio exists because Tr A_P>Tr B_P. The cap gives r<=9. The scalar contrast is nonpositive for every r in [1,9] when p<1/4. Thus L_p cannot be positive definite in the commuting boundary case. This does not dispose of the noncommuting boundary.

## Scope

This reduction closes the analytic endpoint-definition gap in the radial path. It does not establish the sign of the finite noncommuting survivor. In particular it does not automatically transfer the previously proved commuting boundary jets, nor establish the full WH3 contraction conjecture.
