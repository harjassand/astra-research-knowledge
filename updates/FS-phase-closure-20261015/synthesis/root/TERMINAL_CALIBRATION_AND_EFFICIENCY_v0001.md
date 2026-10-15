# Terminal calibration, reciprocity and sharp efficiency ambiguity

15 October 2026, Australia/Brisbane. Root derivation. Internally derived and
same-team checked; external correctness and historical novelty UNKNOWN. These
are linear-response inference statements, not a new converter or measured
hydraulic operation. Standard two-port efficiency theory is prior art.

## Exact metrology interface

Let actual terminal forces p and fluxes Q satisfy Q=L p, with their physical
power pairing p dot Q. Assume a real steady response, positive diagonal entries
and L12,L21>0 (port signs can be reversed together). Force and flow readings
may have unknown fixed positive gains: p'=D_p p, Q'=D_Q Q. The measured matrix is

    M=D_Q L D_p^(-1).

Unknown additive offsets must first be controlled; arbitrary cross-talk,
condition-dependent gains, nonlinearities, hysteresis and unmetered driving
ports are not covered by this multiplicative model.

The bidirectional unloaded-flow ratios have invariant product

    z=(M21/M11)(M12/M22)=L12 L21/(L11 L22).

Both pressure and flow gain factors cancel. Under an INDEPENDENTLY JUSTIFIED
reciprocity premise L12=L21 and positive-definite dissipation, 0<z<1 and the
standard optimum steady forward efficiency is

    eta0(z)=(1-sqrt(1-z))/(1+sqrt(1-z)).

This is a useful screening invariant even without absolute flow-scale
calibration. It neither establishes output power/throughput nor acquires
reciprocity, passivity, isolation, a microscopic mechanism or cost advantage.
Absolute calibrated force/flux measurements and loaded work remain needed.

## Sharp ambiguity when reciprocity is not acquired

Assume only symmetric-part passivity (L+L^T)/2 positive semidefinite. Put

    a=L21/L12>0,  0<z<1,  s=sqrt(1-z).

Operate with p1>0 and an opposing force p2<0, demanding Q2>0. Let
x=-p2 L22/(p1 L21), so 0<x<1. The exact efficiency is

    eta(x)=a z x(1-x)/(1-zx).

The maximum over passive scalar loads occurs at x=1/(1+s), giving

    eta_forward,max=a eta0(z).

No source/load-control cost has been waived; this is the static model's
terminal ratio. The symmetric-part determinant condition is

    z(a+1)^2 <= 4a,

which is equivalent to

    eta0(z) <= a <= 1/eta0(z).

Consequently the SAME gain-invariant z is compatible with the sharp range

    eta0(z)^2 <= eta_forward,max <= 1.

At the endpoints dissipation is semidefinite. Strictly positive dissipation
has the open interval, with endpoints approached. Sharpness: normalize
L11=L22=1 and set L12=sqrt(z/a), L21=sqrt(za), for any a in the allowed interval.
Thus a measured invariant is a complete maximum-efficiency parameter only
within the independently justified reciprocal model class. A single gain
product cannot silently substitute for that premise. These formulas specialize
established nonreciprocal two-port algebra; no efficiency-law priority claimed.

### Fully explicit identical-readout passive countermodels

Take measured M=[[1,1/2],[1/2,1]], pressure readings exact, and unknown positive
flow gains. Three possible actual matrices, each with a positive-definite
symmetric part, are

    L0=[[1,1/2],[1/2,1]],       D_Q=diag(1,1),
    L1=[[1,1/2],[1/20,1/10]],   D_Q=diag(1,10),
    L2=[[1/10,1/20],[1/2,1]],   D_Q=diag(10,1).

They give identical M and z=1/4. Their forward optimum efficiencies are
respectively eta0(1/4), eta0(1/4)/10 and 10 eta0(1/4), approximately
0.0718, 0.00718 and 0.718. Positive symmetric determinants are respectively
3/4, 39/1600 and 39/1600. These are mathematical passive response matrices,
not fabricated hydraulic devices. The nonreciprocal realizations would need
a physically justified mechanism and all bias/control costs accounted for.

## What extra ports can and cannot test

For at least three ports, every oriented cycle has a gain-invariant ratio

    C(i1,...,ik)=product M(i_j,i_(j+1))/M(i_(j+1),i_j).

A reciprocal underlying matrix requires every nonzero-support cycle ratio1
and symmetric sign/support. Conversely, for connected support with paired
same-sign nonzero off-diagonals, these cycle equalities permit positive
weights d_i satisfying d_i Mij=d_j Mji: choose weights along a spanning tree;
cycle identities establish path independence. Thus D M is symmetric.

This is compatibility with some reciprocal calibration, not a proof of actual
reciprocity. Even complete same-device readings cannot select the true power
pairing from unknown unrelated force/flux gains by those equalities alone.
If Mii>0, the symmetrized normalized matrix

    Cii=1,
    Cij=sign(Mij)*sqrt(Mij Mji/(Mii Mjj))

is invariant to positive diagonal sensor gains. Given cycle compatibility,
its positive semidefiniteness is equivalent to the existence of a reciprocal
passive explanation. It remains an existence test, not identification of the
actual calibration, hidden active ports, material mechanism or useful output.

## Robust decision and cost boundary

With independently acquired reciprocity and a simultaneous confidence set for
the actual bidirectional readouts, minimize z over that SAME joint set, then
apply the monotone eta0 to get a conservative efficiency-screening floor.
Separate optimistic numerator/denominator choices cannot certify it. Fixed
positive multiplicative flow gains cancel; drift, additive offsets and
mechanical/plumbing cross-talk need their own acquired bounds. The equally
informed conventional pressure-transfer incumbent receives the same gains,
confidence set and experimental budget.

A positive floor still does not certify net saving at fixed source task.
That comparison needs the old loss actually displaced, the full loaded
terminal response, settling/leakage/chemistry and control-power ledger, and
retained useful work. The passive-network output/loss envelope in the separate
worker proof supplies the conditional model calculation. No such physical
qualification was acquired in this campaign.

## Primary-source inspection and scope

Takashi Ohira, *Power transfer efficiency formulation for reciprocal and
non-reciprocal linear passive two-port systems*, IEICE Electronics Express
15(3), 20171196 (2018), DOI10.1587/elex.15.20171196. Read the actual six-page
primary paper, especially sections2–6 and equations5,16,20. It establishes
existing complex two-port machinery; the real force/flux derivation above is
written explicitly rather than importing an electrical formula without unit
conversion. https://www.jstage.jst.go.jp/article/elex/15/3/15_15.20171196/_pdf

Coquinot et al., *Momentum tunnelling between nanoscale liquid flows*,
Nature Nanotechnology20,397–403 (2025), DOI10.1038/s41565-024-01842-8.
Primary abstract and author-hosted accepted paper were located; material
worker separately inspects the full mechanism. Theory/molecular simulation
and loaded experimental work are distinct evidence levels.
https://arxiv.org/abs/2501.01253

The useful new campaign deduction is a precise acquired-versus-invariant
metrology boundary and its sharp ambiguity, not a claimed new physical law.
