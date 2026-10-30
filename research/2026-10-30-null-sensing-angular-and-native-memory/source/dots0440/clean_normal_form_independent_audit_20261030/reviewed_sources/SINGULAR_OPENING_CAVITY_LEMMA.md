# Singular opening coefficient: local gate omission lemma
2026-10-30. Clean controller-only setting. Supplements CLEAN_EFFECTIVE_NORMAL_FORM Section 5.

Let K>=0 be a fixed-support controller operator, possibly singular. For globally ordered finite-depth positive local activity circuits Y_A define G_A=Y_A^dagger Y_A. Every selected gate is exp(delta X_g), with uniformly bounded X_g (including the epsilon-squared singleton coefficients). Gate supports and incidence are fixed.

Remove from Y_A every selected gate whose support meets supp(K). The removed set is a bounded subset of ONE fixed global gate catalog, chosen independently of A. Denote the remaining circuit Yhat_A and Ghat_A=Yhat_A^dagger Yhat_A. Every remaining gate commutes K; hence Yhat_A and Ghat_A commute K. If desired remove the entire fixed circuit cone as well; this changes only the fixed constants.

The quotient Z_A=Yhat_A Y_A^{-1} has fixed support after cancelling disjoint gates through the bounded-depth layers, and

    ||Z_A-I||<=C delta,  ||Z_A||<=1+C delta.

Consequently

    Y_A^dagger K Y_A-Yhat_A^dagger K Yhat_A
      =Y_A^dagger (K-Z_A^dagger K Z_A)Y_A,

so the TWO-SIDED operator bound is

    +/-[Y_A^dagger K Y_A-K Ghat_A]
          <=C delta ||K|| G_A.                       (1)

No inverse or lower bound of K appears.

The omitted-gate rule is independent of A. Therefore bounded animal extension B=A union D changes only O(|D|) remaining gates, and the usual quotient comparison remains valid for Ghat:

    exp(-C delta |D|)Ghat_A <=Ghat_B<=exp(C delta |D|)Ghat_A.

Apply the operator-valued full-animal move-completion lemma to the positive weights Ghat_A. For the actual accepted Phi_h move,

    sum_A Ghat_A (f_A-Phi_h*f_A)>=0.

Because K commutes all these weights and DATA, multiplication by K preserves positivity. Combining with (1) and the fixed local-orbit bound |f_A-Phi_h*f_A|<=C_h f_A on affected animals gives

    -sum_A Y_A^dagger K Y_A (f_A-Phi_h*f_A)
        <= C delta ||K|| sum_(A affected by h) G_A f_A.

After summing a bounded-incidence family of opening coefficients K_h and multiplying by the outer credit strength t, the error is at most C t delta W_G. This is precisely the budget used in the clean normal form. It repairs the invalid shortcut of inferring Y_B^dagger K Y_B≈Y_A^dagger K Y_A from G_B≈G_A when K is singular.
