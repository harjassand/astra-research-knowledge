# The coarse-target identity also fails for two binary heat-bath sites

29 October 2026. Root's strengthening of the three-state counterexample
inside the binary unit-site heat-bath primitive. This is a supplied exact
four-state source, with no acquired or simulated unknown law.

For 0<epsilon<=1/4, give states 00,01,10,11 stationary masses

    (1-3epsilon, epsilon, epsilon, epsilon).

Refresh each of the two coordinates at rate one from its exact conditional
law. Every positive two-spin distribution is a pairwise Ising law, so this
is within that finite source type. Write

    s=epsilon/(1-2epsilon), p=2epsilon,
    beta=1/2-s, A={10,11}.

The target is the coarse event that the first spin is 1. The two centered
coordinate indicators g1,g2 satisfy

    -Q g1=g1-beta*g2, -Q g2=g2-beta*g1.

Their common variance is p(1-p), and their correlation is beta. The remaining
mean-zero interaction function is killed by either conditional expectation,
so -Q acts on it with eigenvalue 2. Hence the exact spectrum is

    0, 1-beta, 1+beta, 2.

The full gap is at least 1/2 as epsilon tends to zero. This is not a hidden
slow-clock counterexample.

## Exact actual mean

The killed generator on the non-target states 00,01 is

    -Q_Ac = [[2s, -s], [-(1-s), 3/2-s]].

Its inverse applied to 1 is

    h00=(3/2)/[s(2-s)],
    h01=(1+s)/[s(2-s)].

The true stationary law conditioned outside A is (1-s,s). Consequently

    T_A=(3/2-s/2+s^2)/[s(2-s)].                     (1)

This is a conventional exact two-by-two killed solve. It supplies the
correct answer cheaply in this example.

## The normalized-indicator substitution is still wrong

Since -Q leaves span(g1,g2) invariant,

    (-Q)^+g1=(g1+beta*g2)/(1-beta^2),
    C_A=<g1,(-Q)^+g1>_pi
        =p(1-p)(1+beta^2)/(1-beta^2).

For the normalized indicator, Z_A=C_A/p. Substituting it into the singleton
formula would predict

    T_bad=Z_A/[p(1-p)]
         =(1+beta^2)/[p(1-beta^2)]
         =(5/4-s+s^2)/[s(3/2-s)].                   (2)

Exactly,

    T_bad/T_A
      =1+beta^2/[(3/2-s)(3/2-s/2+s^2)] ->10/9
                                                    as epsilon->0. (3)

Thus target rarity and a uniform full gap do not make that identity valid.
The error persists even though the correct killed mean is explicitly known.
This strengthens the general reversible three-state failure without claiming
that every source condition in the extensive-N geometric theorem holds
along this epsilon sequence: the minimum conditional probability decreases
and the interaction strength grows as epsilon shrinks. The point-target
theorem itself is unaffected. The failed step is the purported EXACT
replacement of a singleton by a coarse indicator.

To translate the geometric construction to coarse targets, it is necessary
to retain the actual killed generator or an exact boundary/entrance
representation. Concentrating the spectral measure of the wrong normalized
indicator cannot repair (2). This connects the next scientific obligation
back to Astra's preserved Schur-memory and killed-mean constructions.

The exact executable check verifies the complete heat-bath generator,
detailed balance, all four independent eigendirections, the Poisson and
killed equations, and (1)-(3) at six rational epsilon values down to 2^-128.
It uses rational arithmetic throughout; no floating spectrum is a premise.
