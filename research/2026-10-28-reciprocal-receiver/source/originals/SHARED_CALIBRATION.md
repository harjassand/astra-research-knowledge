# Weak-target metrology with shared calibration and finite load tolerance

28 October 2026. A mathematical/executable extension; no hardware calibration
was performed.

## 1. Obstruction removed

Independently charging reference error against each bright return can overwhelm
a weak target. But the task uses differences: a shared background offset
cancels, a shared complex gain scales the residue, and fixed quadrature
imbalance also acts on differences. Retaining these correlations replaces a
background-sized absolute calibration floor by a relative floor. Arbitrary
drift does not have this property.

## 2. Acquired contract

For one command, h_z=h0+a z/(1-sz), |s|<=1, p=|a|<=1. Nominal loads are
z_l=0,+r,-r, 0<r<1. Actual loads satisfy |zeta_l-z_l|<=d_z and
|zeta_l|,|z_l|<=rmax<1. Reconstructed fields obey

    x_l=alpha h_zeta_l+beta conjugate(h_zeta_l)+b+e_l,
    0<gL<=|alpha|<=gU, |beta|<=bmax, |e_l|<=epsilon.

Alpha,beta,b are common across all three states. Their values may be unknown.
Local calibration provides these bounds and a warranted stability allowance;
epsilon includes readout, arithmetic and all unshared drift. No bound on the
common offset b is needed. Incident-power normalization and reciprocity remain
physical requirements; a finite fit does not prove an unrestricted stability law.

The receiver model follows from four fixed reference phasors L0,...,L3. With
physical I_k=|h+Lk|^2/2, nominal R>0, x=[I0-I2+i(I1-I3)]/(2R), and
X=L0-L2, Y=L1-L3, direct expansion gives

    alpha=(conjugate(X)+i conjugate(Y))/(4R),
    beta=(X+iY)/(4R),
    b=(|L0|^2-|L2|^2+i(|L1|^2-|L3|^2))/(4R).

Ideal quadrature has alpha=1,beta=b=0. Common detector gain multiplies these
coefficients. Static phase/amplitude imbalance need not be inferred as
independent errors on each load. Load-dependent coefficients belong in e_l.

## 3. Proof of the relative interval

For nominal fields define c=(h_r-h_-r)/(2r), d=(h_r+h_-r-2h0)/(2r).
Then c=a/(1-r^2s^2), d=rs c, so

    |c|<=p/(1-r^2), |d|<=rp/(1-r^2).

Exact subtraction shows that the load perturbation obeys

    |h_zeta-h_z|=p|zeta-z|/|(1-s zeta)(1-sz)|<=p lambda,
    lambda=d_z/(1-rmax)^2.

The background h0 is absent. Put q=|alpha|p and compare acquired contrasts
with the feasible pair (alpha c,alpha d), whose residue is alpha a. Since
nominal loads and contrast coefficients are real, beta contamination is
(beta conjugate(c), beta conjugate(d)). Noise and load perturbation contribute
per-field size <=epsilon+(|alpha|+|beta|)p lambda.

The explicit radial clip in COHERENT_THREE_LOAD_OBSERVABLE.md has residue
error <=(1+3r^2)e_c+4r e_d. Its magnitude estimate p_tilde therefore obeys

    |p_tilde-q| <= K_r epsilon
       +[K_r lambda(|alpha|+|beta|)
              +(1+7r^2)|beta|/(1-r^2)]p,
    K_r=1/r+3r+8.

Define acquired bounds

    B=K_r epsilon + certified numerical residue/magnitude error,
    Theta=K_r lambda(1+bmax/gL)
              +(1+7r^2)/(1-r^2)*bmax/gL.

Then |p_tilde-q|<=B+Theta q. For Theta<1 and gL>0, rearrange to obtain

    p in [ max(0,p_tilde-B)/((1+Theta)gU),
                  (p_tilde+B)/((1-Theta)gL) ] intersect [0,1].    (1)

Use outward rational endpoints for p_tilde and clipping error. Do not cap
the scaled magnitude at one before this inversion: q can exceed one.
An empty interval indicates inconsistency. If Theta>=1 or gL<=0, retain
[0,1] or another independently sound certificate, not a fabricated relative bound.

The common scalar-gain case sets bmax=0. Unknown common phase is harmless.

## 4. Illustrative finite calibration budget

For r=1/2, rmax=0.51, d_z=0.001, gL=0.99, gU=1.01, bmax=0,
Theta=11.5*0.001/0.49^2, approximately 0.0479. Common one-percent gain
uncertainty and 0.001 load-reflection tolerance cause finite relative interval
inflation even for weak targets. They do not automatically add order-0.01
background-power uncertainty. These are declared requirements, not measured
component specifications. Readout and unshared drift still must resolve p.

At r=1/2, fixed quadrature leakage adds (11/3)bmax/gL to Theta, plus its
load-tolerance cross term. Moderate fixed I/Q imbalance can be retained.
A tighter known real-linear calibration could instead be inverted directly;
that stronger knowledge is not assumed.

## 5. Power in an imperfect final load

The p above is the original matched-target quantity. If the final operating
load satisfies |z_op|<=d0<1, actual absorbed power is

    p_op=(1-|z_op|^2)p/|1-s z_op|^2,
    (1-d0)/(1+d0)*p <= p_op <= (1+d0)/(1-d0)*p.

Combine this factor with (1). It distinguishes ideal matched target power
from power absorbed in the actual slightly mismatched termination.

## 6. Failures and control

The load-dependent phase counterfeit in NEW_LIMITS.md violates the shared
contract, so (1) cannot repair it. Nor does (1) remove the uncalibrated-load
scale gauge: bounded loads and gL>0 are essential. Timing must use complete
certified decay blocks or include the shorter-window energy factor.

Query-specific intervals can feed the existing exact interval controller via
its actual per-step widths. Closed-form O(n) constants require a common
absolute delta. Calibration width may persist as noise tends to zero.
No optimizer, photon or device superiority follows from this improvement.

`access/shared_calibration_checks.py` records exact twelve-power software
checks with common gain and finite load tolerance, including the unchanged
IEEE-derived model. They are conditional stationary emulations, not laboratory
measurements or acquired hardware calibration. The broader I/Q theorem is
also checked algebraically in the supplementary exact tests.
