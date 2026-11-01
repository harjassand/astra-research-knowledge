# Exact scope witness: tiny CDF error need not control extreme tails or preparation means

This is a reviewer-derived abstract reversible Markov example, not an assertion about the detailed tail of the specific quartic diffusion. It validates the necessary limits of the reviewed spectral theorem.

## Spectral distribution with arbitrarily small defect

Choose 0<delta<1 and set

    a=(1-2delta/3)/(1-delta)>1.

Let X have mass 1-delta at a and density 2delta x on 0<x<1. Then

    EX=1,
    E(1/X)-1=delta(2-delta)/(3-2delta)<=delta.

The reviewed lemma therefore gives arbitrarily small uniform absolute error from exp(-t). Nevertheless its exponential mixture survival is exactly

    Fbar(t)=(1-delta)exp(-a t)
              +2delta[1-(1+t)exp(-t)]/t^2, t>0,
    Fbar(0)=1.

It has tail Fbar(t)~2delta/t^2. Its mean is finite, but its second moment is infinite because E(1/X^2)=infinity. Every positive exponential hitting-time moment is infinite: positive probability is assigned to rates below any positive exponential-moment parameter. Relative tail error against exp(-t) is unbounded, and sufficiently extreme quantiles are not relatively controlled.

## Actual reversible realization

Let D be the rate space with probability measure nu equal to the law of X. Add one state b, with unnormalized reference mass m({b})=1 and m|D=nu. A point x in D jumps to b at rate x. From b the jump-rate measure into D is x nu(dx), with total rate EX=1. Rates are bounded for each fixed delta, so the process is nonexplosive, and detailed balance follows from nu(dx)x=1*[x nu(dx)]. It has a finite invariant reversible reference measure.

Kill at b and set A=D, S empty. The killed generator is multiplication by x, h=1_D, M=1, C0=E X=1 and Q_A=E(1/X)<infinity. Thus rho=0 and the reviewed theorem applies exactly. The killed spectral bottom is zero, while the source inverse form is finite. This is a concrete process inside the ABSTRACT theorem, not merely a formal spectral measure.

## Initial-law contrast

For 0<eta<1 and any x0 in (0,1), let the initial law be

    nu_eta=(1-eta)nu+eta delta_(x0).

Its total-variation distance from nu is eta. Every survival probability changes by at most eta, uniformly in time, because the survival kernel lies in [0,1]. But its mean is

    E_(nu_eta) tau_b=(1-eta)E_nu tau_b+eta/x0,

which is unbounded as x0 decreases to zero. Thus a genuinely earned small-TV initialization error CAN be added to a bounded-CDF certificate, but cannot by itself certify a mean. Point-start laws, fixed rays in a nonclosed projection, and unverified finite-bit preparations cannot be substituted for the declared initial law.
