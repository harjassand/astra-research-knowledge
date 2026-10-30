# Exact neutral collapse must retain entry-phase memory

The weakly reversible network C+2A <-> B+2A and C <-> A+B, all rates 1, with B+C=1, has neutral internal switching rate a=n(n-1) at count n. Its nonhorizontal exits are upward from C at rate 1 and downward from B at rate n.

At frozen count n>=2, the killed neutral generator is

    H=[[-a-1,a],[a,-a-n]].

The upward-exit probabilities from starting modes C and B are respectively

    (a+n)/(a(n+1)+n),  a/(a(n+1)+n).

They are not equal. Thus exact elimination cannot replace this component by a single memoryless mode. Keeping entry phase yields exact rational phase-type exit probabilities and mean holding times through (-H)^(-1). One may replace each holding-time law by an exponential with the same mean for return-probability/expected-return-time questions of the corresponding Markov-renewal skeleton, but the number of entry phases does not necessarily decrease. The resulting rates are rational, not automatically a weakly reversible mass-action diagram.

This is an obstruction to one particular elimination induction, not a recurrence counterexample. The fixed-tilt/dual-measure proof does not need this collapse.

Independent exact tilt fixture for this network, with theta=log4, eta=log2 and beta_C=beta_B=0:

    G=[[-a-1,a+8],[a+n/2,-a-n]],
    det G = n(n^2-15n+8)/2,
    v_C=(4n-1)/(n^2-15n+8),
    v_B=2(2n^2-2n+9)/(n(n^2-15n+8)).

G is Hurwitz for every integer n>=15. The actual adjoint defects for mu_j(n)=4^(-n)v_j(n), divided by 4^(-n), are

    D_C=-(4n^4-84n^3+445n^2-119n-276)
         /[2(n^2-15n+8)(n^2-13n-6)],
    D_B=-(n^4-16n^3-5n^2-20n+160)
         /[(n^2-17n+24)(n^2-15n+8)].

These exact rational identities were independently computed with SymPy. Both defects are eventually negative, but the matrix Hurwitz threshold is NOT automatically the actual-adjoint threshold: D_B is positive at n=16. The dual lift must take its separate finite shift-ratio threshold, exactly as its proof states. A coarse coefficient bound yields both numerators positive for n>232, with all denominators positive there; this is a sufficient all-size certificate, not a sharp threshold. [For the first numerator, the elementary bound is n>(84+445+119+276)/4=231; for the second, n>16+5+20+160=201.]
