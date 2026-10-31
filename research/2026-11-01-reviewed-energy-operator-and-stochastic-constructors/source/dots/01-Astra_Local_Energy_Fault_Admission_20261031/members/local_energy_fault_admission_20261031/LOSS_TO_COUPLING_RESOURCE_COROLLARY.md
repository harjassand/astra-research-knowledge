# Resource corollary: actual loss-to-coupling ratio

31 October 2026. Separate corollary to the reviewed occupation proof; it does not modify that frozen source or its receipt. The derivation below is initially pending separate review.

## Physical units and general-radius bound

Use the same actual model and location/control hypotheses as `QUANTUM_OCCUPATION_LOCAL_ADMISSION_CANDIDATE.md`, SHA `0b0bd7ffa77e9c90323be91d5dec929b5bbd66d0c059ad783357838bf5ba010e`. Let

- lambda be the physical source loss rate;
- c=sqrt(lambda)b be the actual per-source unwanted Hamiltonian norm bound;
- gamma=1-2 beta>0 be the acquired loss-relative coherent-transport margin;
- g>=1 be the maximum number of source indices assigned to one location;
- a be the physical incoherent injection rate bound;
- tau be the actual maximum location duration;
- epsilon_ctl be the integrated unwanted source-independent Hamiltonian bound per location, including actual finite controls where applicable.

Assume c>0; c=0 is the ordinary control-only case. For any

  1<R<=gamma lambda/(8c),

choose the backward potential r=2Rc/lambda<=gamma/4. The reviewed proof gives

  ||E(S)|| <= eta(R)^|S|,
  eta(R)=exp[R h]/(R-1),
  h=2c g(1+a tau)/(gamma lambda)+epsilon_ctl.        (1)

Indeed the weighted dilation squared-norm exponent is C|S|+2R epsilon_ctl|S| with C=2r g(1+a tau)/gamma. Taking its square root and applying the Cauchy kernel gives (1). No replacement of an amplitude norm by a probability has occurred.

## No control mismatch

Choose

  R0=gamma lambda/[8c g(1+a tau)].

Because g(1+a tau)>=1, this respects the admissible radius cap. If R0>=2, then R0 h=1/4 and R0-1>=R0/2, so

  eta <=16 exp(1/4) c g(1+a tau)/(gamma lambda).    (2)

Thus the sufficient local amplitude strength is linear in the actual unwanted-coupling/loss ratio and in the per-location activation budget. The earlier fixed-potential choice introduced an avoidable exponential in a tau. It remains a valid proof but is not the best resource reading.

## With a real acquired control-error budget

If epsilon_ctl>0 take

  R=min(R0,1/(2 epsilon_ctl)).

When R>=2, its source contribution to R h is <=1/4 and its control contribution is <=1/2. Therefore

 eta <= max{16 exp(3/4)c g(1+a tau)/(gamma lambda),
            4 exp(3/4)epsilon_ctl}.               (3)

For epsilon_ctl=0 use (2), or interpret the second cap as infinity. If the chosen R is below two, do not announce a small-noise admission from (2) or (3); the exact general bound (1) is available only when R>1. The receiver's actual threshold still has to be supplied.

For a desired sufficient amplitude eta_star, conservative admission conditions from (3) are

  lambda/c >=16 exp(3/4)g(1+a tau)/(gamma eta_star),
  epsilon_ctl <=eta_star/[4 exp(3/4)],

along with R>=2 and the actual graph/location/source hypotheses. These are sufficient mathematical conditions, not claimed hardware specifications or an optimized threshold. The maximum in (3) is not a missing additive error: it arises exactly from the reciprocal of the minimum radius and an already-combined exponent bound.

## What must be paid

This form is invariant to how the original sqrt(lambda)b parametrization is described. Rapid loss alone is not free: the actual ratio lambda/c, the transport margin gamma, injection a and gate duration tau must be physically acquired. Increasing lambda while allowing a or c to increase can negate admission. For example a proportional to lambda contributes a nonvanishing c g tau term to h; the corollary does not erase that cost.

The control parameter is the stated integrated Hamiltonian discrepancy. A reported average gate infidelity or a reduced channel calibration is not silently the same parameter; it needs its own valid receiving argument. Gate, reset, initialization, measurement, routing and classical-control implementation remain the ordinary fault-tolerance consumer's actual resources.

The result is a local noise-amplitude certificate for a supplied Markov loss/injection model with arbitrary finite-source input and coherent exterior transport. It is not a simulation gate count, a finite experimental calibration result, a numerical threshold, or a practical superiority claim.
