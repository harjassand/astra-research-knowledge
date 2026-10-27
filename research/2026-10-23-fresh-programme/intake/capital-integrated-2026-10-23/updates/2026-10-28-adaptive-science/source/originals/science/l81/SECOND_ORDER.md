# Executed second positive correction

The n^(-2) deterministic covariance remainder can be removed by another ordinary binomial term without treating an action as a matrix. This finite acquired construction still has general d^(1/3) query rate. The independent audit and full coefficient proof are retained in helper/SECOND_ORDER.md.

Compose two fresh GLOBAL four-query covariance actions to obtain J^(2)(v), with E[J^(2)(v)|v]=Sigma^2v and ||J^(2)(v)||<=L^4||v||. This costs EIGHT original g values. The two actions have independent times and centers; reusing a center does not generally give Sigma^2.

With k first actions and ell second words, use separate fresh blocks conditional on retained Z and return

    Y2=gbar_n+tau Z-Jbar(Z)/(2tau n)
         -Jbar^(2)(Z)/(8tau^3 n^2)+eta W.                    (1)

Mean is exactly mu. Query cap is n+4k+8ell on every execution; arithmetic is O((n+k+ell)d), streaming storage O(d).

For the deterministic comparison set M2=tau I-Sigma/(2tau n)-Sigma^2/(8tau^3 n^2). Direct multiplication yields

    Sigma/n+M2^2+eta^2I=sigma^2I+Q2,
    Q2=Sigma^3/(8tau^4n^3)+Sigma^4/(64tau^6n^4)>=0.           (2)

Thus the Sigma^2 term cancels exactly. Keeping Q2 fixed in the covariance interpolation of THEOREM.md is valid for every n, because C_1=M2^2+eta^2I>=eta^2I and C_t=C_1+(1-t)Sigma/n. Conditional centered shift variance is at most

    d[L^4/(4tau^2n^2k)+L^8/(64tau^6n^4ell)].                 (3)

Cross terms vanish because the two correction blocks are independent given Z. The exact implemented law therefore obeys the safe bound

    TV(Y2,N(mu,sigma^2I))
      <=L^2 sqrt(d)/(2eta^2n^(3/2))+||Q2||F/(2eta^2)
        +d[L^4/(4tau^2n^2k)+L^8/(64tau^6n^4ell)]/(2eta^2).   (4)

For tau=eta=sigma/sqrt(2), r=L/sigma, a scalar upper bound is

    r^2 sqrt(d)/n^(3/2)+r^6 sqrt(d)/(2n^3)+r^8 sqrt(d)/(8n^4)
       +r^4d/(2n^2k)+r^8d/(8n^4ell).                        (5)

Only the FINAL operator of each second word may be ell-stratified while the first remains global: individual means Sigma_j Sigma then average to Sigma^2. Stratifying both operators at the same stratum would target a different mean of conditional squares and is not used.

`second_corrected_sampler` implements (1) at actual g-value points. For affine g=Ax+b the second word equals A^4v pathwise, and the exact output covariance is sigma^2I+A^6/(8tau^4n^3)+A^8/(64tau^6n^4). This supplies a direct power/sign check.

The second correction removes a genuine deterministic term but leaves the first-action randomization and averaged Stein fluctuation. Bound (5) therefore supplies no improved general exponent, log-accuracy theorem or self-applicable quadratic law update. Equal-query first-correction and ordinary-average competitors are retained in second_checks.json. Numerical radial checks do not establish practical advantage or certify full law.
